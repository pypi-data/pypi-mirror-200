#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2023 Robin Jarry

"""
Display linux interrupts information.

CPU and IRQ IDs can be specified as a hexadecimal mask values (e.g. 0xeec2) or
as a comma-separated list of IDs. Consecutive IDs can be compressed as ranges
(e.g. 5,6,7,8,9,10 --> 5-10).
"""

import argparse
import os
import re
import sys


# ------------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-r",
        "--root",
        default="/",
        help="""
        Root dir used to determine paths to /proc/interrupts and
        /proc/irq/$NUM (default /).
        """,
    )
    parser.add_argument(
        "-c",
        "--cpu",
        type=mask_or_list,
        metavar="CPU_RANGE_OR_MASK",
        action="append",
        default=[],
        help="""
        Only show these CPUs. Can be used multiple times.
        """,
    )
    parser.add_argument(
        "-i",
        "--irq",
        action="append",
        default=[],
        help="""
        Only show this IRQ. Can be used multiple times.
        """,
    )
    parser.add_argument(
        "-n",
        "--num-per-cpu",
        action="store_true",
        help="""
        Display the number of bound IRQs per CPU.
        """,
    )
    parser.add_argument(
        "-s",
        "--stats",
        action="store_true",
        help="""
        Display interrupt counts.
        """,
    )
    parser.add_argument(
        "-z",
        "--display-zeroes",
        action="store_true",
        help="""
        Also show -s/--stats with 0 values.
        """,
    )
    parser.add_argument(
        "-e",
        "--exact",
        action="store_true",
        help="""
        Display exact stats values.
        """,
    )
    args = parser.parse_args()
    cpu_ids = set()
    for m in args.cpu:
        cpu_ids.update(m)
    irq_ids = set(args.irq)

    if args.stats and args.num_per_cpu:
        parser.error("-s is not supported with -n")

    try:
        os.chdir(args.root)
        irqs = parse_proc_interrupts()
        cpus = {}
        for irq, i in irqs.items():
            for c in range(len(i["counters"])):
                cpus.setdefault(c, {"affinity": 0, "effective": 0})
            if args.stats or (irq_ids and irq not in irq_ids):
                continue
            try:
                with open(f"proc/irq/{irq}/smp_affinity_list", "r") as f:
                    affinity = mask_or_list(f.read().strip())
                i["affinity"] = affinity
                for c in affinity:
                    cpus[c]["affinity"] += 1
                with open(f"proc/irq/{irq}/effective_affinity_list", "r") as f:
                    effective = mask_or_list(f.read().strip())
                i["effective"] = effective
                for c in effective:
                    cpus[c]["effective"] += 1
            except FileNotFoundError as e:
                pass  # not all irqs are listed here

        if cpu_ids - cpus.keys():
            raise ValueError(f"no such CPUs: {id_list(cpu_ids - cpus.keys())}")
        if irq_ids - irqs.keys():
            raise ValueError(f"no such IRQs: {irq_ids - irqs.keys()}")

    except Exception as e:
        sys.stderr.write(f"error: {e}\n")
        sys.stderr.flush()
        return 1

    if args.exact:
        num_format = str
    else:
        num_format = human_readable

    for i in irqs.values():
        if not i.get("affinity"):
            i["affinity"] = set(cpus.keys())
        if not i.get("effective"):
            i["effective"] = set(cpus.keys())

    if irq_ids:
        irq_ids = list(irq_ids)
        per_cpu = True
    else:
        irq_ids = list(irqs.keys())
        per_cpu = False
    if cpu_ids:
        per_irq = True
        cpu_ids = sorted(cpu_ids)
    else:
        per_irq = False
        cpu_ids = sorted(cpus.keys())
    irq_ids.sort(key=lambda i: f"{int(i):04d}" if i.isdigit() else i)

    if args.stats:
        if per_cpu:
            header = ["CPU"] + [f"IRQ-{i}" if i.isdigit() else i for i in irq_ids]
            align = [1] * len(header)
            align[0] = -1
            rows = [tuple(header)]
            for cpu in sorted(cpus.keys()):
                if cpu_ids and cpu not in cpu_ids:
                    continue
                nums = [irqs[i]["counters"][cpu] for i in irq_ids]
                if not any(nums) and not args.display_zeroes:
                    continue
                nums = [num_format(n) for n in nums]
                rows.append(tuple([str(cpu)] + nums))

        elif per_irq:
            header = ["IRQ"] + [f"CPU-{c}" for c in cpu_ids] + ["DESCRIPTION"]
            align = [1] * len(header)
            align[0] = -1
            align[-1] = -1
            rows = [tuple(header)]
            for irq in irq_ids:
                i = irqs[irq]
                nums = [i["counters"][c] for c in cpu_ids]
                if not any(nums) and not args.display_zeroes:
                    continue
                nums = [num_format(n) for n in nums]
                rows.append(tuple([irq] + nums + [i["desc"]]))

        else:
            rows = [("IRQ", "TOTAL", "DESCRIPTION")]
            align = [-1, 1, -1]
            for irq in irq_ids:
                i = irqs[irq]
                total = sum(i["counters"][c] for c in sorted(cpus.keys()))
                if total == 0 and not args.display_zeroes:
                    continue
                rows.append((irq, num_format(total), i["desc"]))

    elif args.num_per_cpu:
        rows = [("CPU", "AFFINITY-IRQs", "EFFECTIVE-IRQs")]
        align = [-1, 1, 1]
        for cpu in cpu_ids:
            c = cpus[cpu]
            rows.append((str(cpu), str(c["affinity"]), str(c["effective"])))

    else:
        rows = [("IRQ", "AFFINITY", "EFFECTIVE-CPU", "DESCRIPTION")]
        align = [-1, 1, 1, -1]
        for irq in irq_ids:
            i = irqs[irq]
            if cpu_ids and not i["effective"].intersection(cpu_ids):
                continue
            rows.append(
                (
                    irq,
                    id_list(i["affinity"]),
                    id_list(i["effective"]),
                    i["desc"],
                )
            )

    widths = [len(c) for c in rows[0]]
    for row in rows:
        for c in range(len(widths)):
            if len(row[c]) > widths[c]:
                widths[c] = len(row[c])
    for w in range(len(widths)):
        widths[w] = align[w] * widths[w]
    if widths[-1] < 0:
        widths[-1] = ""
    fmt = "  ".join(f"%{w}s" for w in widths)
    for row in rows:
        print(fmt % row)

    return 0


# ------------------------------------------------------------------------------
HEX_RE = re.compile(r"0x[0-9a-fA-F]+")
RANGE_RE = re.compile(r"\d+-\d+")
INT_RE = re.compile(r"\d+")


def mask_or_list(arg: str) -> "set[int]":
    cpu_ids = set()
    for item in arg.strip().split(","):
        if not item:
            continue
        if HEX_RE.match(item):
            item = int(item, 16)
            cpu = 0
            while item != 0:
                if item & 1:
                    cpu_ids.add(cpu)
                cpu += 1
                item >>= 1
        elif RANGE_RE.match(item):
            start, end = item.split("-")
            cpu_ids.update(range(int(start, 10), int(end, 10) + 1))
        elif INT_RE.match(item):
            cpu_ids.add(int(item, 10))
        else:
            raise argparse.ArgumentTypeError(f"invalid argument: {item}")
    return cpu_ids


# ------------------------------------------------------------------------------
def id_list(ids: "list[int]") -> str:
    groups = []
    ids = sorted(ids)
    i = 0
    while i < len(ids):
        low = ids[i]
        while i < len(ids) - 1 and ids[i] + 1 == ids[i + 1]:
            i += 1
        high = ids[i]
        if low == high:
            groups.append(str(low))
        elif low + 1 == high:
            groups.append(f"{low},{high}")
        else:
            groups.append(f"{low}-{high}")
        i += 1
    return ",".join(groups)


# ------------------------------------------------------------------------------
INTERRUPT_RE = re.compile(r"^\s*(\w+):\s+([\s\d]+)\s+([A-Za-z].+)$")
SOFTIRQS_RE = re.compile(r"^\s*(\w+):\s+([\s\d]+)\s*$")
SOFTIRQS_DESC = {
    "HI": "high priority tasklet softirq",
	"TIMER": "timer softirq",
	"NET_TX": "network transmit softirq",
	"NET_RX": "network receive softirq",
	"BLOCK": "block device softirq",
	"IRQ_POLL": "IO poll softirq",
	"TASKLET": "normal priority tasklet softirq",
	"SCHED": "schedule softirq",
	"HRTIMER": "high resolution timer softirq",
	"RCU": "RCU softirq",
}


def parse_proc_interrupts() -> (dict, dict):
    with open("proc/interrupts", "r", encoding="ascii") as f:
        buf = f.read()
    irqs = {}
    for line in buf.splitlines():
        m = INTERRUPT_RE.match(line)
        if m is None:
            continue
        irqs[m.group(1)] = {
            "desc": re.sub(r"\s+", " ", m.group(3).strip()),
            "counters": [int(c) for c in m.group(2).split()],
        }

    with open("proc/softirqs", "r", encoding="ascii") as f:
        buf = f.read()
    for line in buf.splitlines():
        m = SOFTIRQS_RE.match(line)
        if m is None:
            continue
        irq = m.group(1)
        irqs[irq] = {
            "desc": SOFTIRQS_DESC.get(irq, "-"),
            "counters": [int(c) for c in m.group(2).split()],
        }

    return irqs


# ------------------------------------------------------------------------------
def human_readable(value: float) -> str:
    units = ("K", "M", "G")
    i = 0
    unit = ""
    while value >= 1000 and i < len(units):
        unit = units[i]
        value /= 1000
        i += 1
    if unit == "":
        return str(value)
    if value < 100:
        return f"{value:.1f}{unit}"
    return f"{value:.0f}{unit}"


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())
