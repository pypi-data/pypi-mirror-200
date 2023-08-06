#!/usr/bin/env python3
# Copyright (c) 2023 Robin Jarry
# SPDX-License-Identifier: MIT

"""
Convert a bit list into a hex mask or the other way around.
"""

import argparse
import re
import typing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "args",
        type=mask_or_list,
        metavar="MASK_OR_LIST",
        nargs="+",
        help="""
        A set of bits specified as a hexadecimal mask value (e.g. 0xeec2) or as
        a comma-separated list of bit IDs. Consecutive ids can be compressed as
        ranges (e.g. 5,6,7,8,9,10 --> 5-10).
        """,
    )
    g = parser.add_argument_group("mode").add_mutually_exclusive_group()
    g.add_argument(
        "-m",
        "--mask",
        action="store_const",
        dest="mode",
        const=hex_mask,
        help="""
        Print the combined args as a hexadecimal mask value (default).
        """,
    )
    g.add_argument(
        "-b",
        "--bit",
        action="store_const",
        dest="mode",
        const=bit_mask,
        help="""
        Print the combined args as a bit mask value.
        """,
    )
    g.add_argument(
        "-l",
        "--list",
        action="store_const",
        dest="mode",
        const=bit_list,
        help="""
        Print the combined args as a list of bit IDs. Consecutive IDs are
        compressed as ranges.
        """,
    )
    parser.set_defaults(mode=bit_mask)
    args = parser.parse_args()
    bit_ids = set()
    for a in args.args:
        bit_ids.update(a)
    print(args.mode(bit_ids))


HEX_RE = re.compile(r"0x[0-9a-fA-F]+")
RANGE_RE = re.compile(r"\d+-\d+")
INT_RE = re.compile(r"\d+")


def mask_or_list(arg: str) -> typing.Set[int]:
    bit_ids = set()
    for item in arg.strip().split(","):
        if not item:
            continue
        if HEX_RE.match(item):
            item = int(item, 16)
            bit = 0
            while item != 0:
                if item & 1:
                    bit_ids.add(bit)
                bit += 1
                item >>= 1
        elif RANGE_RE.match(item):
            start, end = item.split("-")
            bit_ids.update(range(int(start, 10), int(end, 10) + 1))
        elif INT_RE.match(item):
            bit_ids.add(int(item, 10))
        else:
            raise argparse.ArgumentTypeError(f"invalid argument: {item}")
    return bit_ids


def hex_mask(bit_ids: typing.Set[int]) -> str:
    mask = 0
    for bit in bit_ids:
        mask |= 1 << bit
    return hex(mask)


def bit_mask(bit_ids: typing.Set[int]) -> str:
    mask = 0
    for bit in bit_ids:
        mask |= 1 << bit
    return f"0b{mask:_b}"


def bit_list(bit_ids: typing.Set[int]) -> str:
    groups = []
    bit_ids = sorted(bit_ids)
    i = 0
    while i < len(bit_ids):
        low = bit_ids[i]
        while i < len(bit_ids) - 1 and bit_ids[i] + 1 == bit_ids[i + 1]:
            i += 1
        high = bit_ids[i]
        if low == high:
            groups.append(str(low))
        elif low + 1 == high:
            groups.append(f"{low},{high}")
        else:
            groups.append(f"{low}-{high}")
        i += 1
    return ",".join(groups)


if __name__ == "__main__":
    main()
