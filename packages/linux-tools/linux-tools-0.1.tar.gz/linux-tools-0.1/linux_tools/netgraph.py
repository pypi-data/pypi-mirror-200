#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2023 Robin Jarry

"""
Convert linux networking configuration to a DOT graph. The output can be piped
to dot to convert it to SVG or other formats. Example:

    %(prog)s | dot -Tsvg > net.svg
"""

import argparse
import json
import subprocess
import sys
import re


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-2",
        "--l2-addresses",
        action="store_true",
        help="""
        Display mac addresses.
        """,
    )
    parser.add_argument(
        "-4",
        "--ipv4-addresses",
        action="store_true",
        help="""
        Display IPv4 addresses.
        """,
    )
    parser.add_argument(
        "-6",
        "--ipv6-addresses",
        action="store_true",
        help="""
        Display IPv6 addresses.
        """,
    )
    parser.add_argument(
        "-l",
        "--local-addresses",
        action="store_true",
        help="""
        Display link local addresses.
        """,
    )
    args = parser.parse_args()

    namespaces = preprocess(get_running(), args)

    print("// generated using net2dot")
    print("graph {")
    print('  node [fontsize=11 fontname=monospace margin=0];')
    print('  graph [compound=true style=dotted];')

    for ns, links in namespaces.items():
        print()
        if ns:
            print(f"  subgraph {safe(ns)} {{")
            print(f'    label="netns {ns}";')
            print("    cluster=true;")
            print()
            indent = "  "
        else:
            indent = ""
        for link in links:
            print(f"{indent}  {link['id']} [{node_attrs(link)}];")
        if ns:
            print("  }")

    print()
    for links in namespaces.values():
        for link in links:
            if "master" in link:
                print(f"  {link['id']} -- {link['master']};")
            if "link" in link:
                print(f"  {link['id']} -- {link['link']} [style=dashed];")

    print()
    print("  {")
    print("    rank=sink cluster=false;")
    for link in namespaces[""]:
        if "master" not in link and "link" not in link:
            print(f"    {link['id']};")
    print("  }")

    print("}")


def safe(n):
    return re.sub(r"\W", "_", n)


COLORS = {
    "bond": "deeppink",
    "loopback": "peru",
    "veth": "red",
    "vlan": "green",
    "vxlan": "blue",
}
SHAPES = {
    "bond": "house",
    "bridge": "diamond",
    "loopback": "invtriangle",
    "veth": "hexagon",
}

def node_attrs(link):
    attrs = {}
    color = COLORS.get(link["kind"], "gray")
    attrs["color"] = color
    attrs["shape"] = SHAPES.get(link["kind"], "oval")
    labels = [
        f"<b>{link['name']}</b>",
        f'<font color="{color}">{link["kind"]}</font>',
    ] + [
        f'<font color="{color}">{key} {value}</font>'
        for key, value in link["attributes"].items()
    ] + [
        f'<font color="orange">{mac}</font>' for mac in link["l2"]
    ] + [
        f'<font color="navy">{v4}</font>' for v4 in link["ipv4"]
    ] + [
        f'<font color="magenta">{v6}</font>' for v6 in link["ipv6"]
    ]
    attrs["label"] = f"<{'<br/>'.join(labels)}>"
    return " ".join(f"{k}={v}" for k, v in attrs.items())


def ip(*cmd):
    args = ["ip", "-d", "-j"] + list(cmd)
    out = subprocess.check_output(args).decode("utf-8")
    if not out.strip():
        return []
    return json.loads(out)


def get_running():
    addrs = ip("addr", "show")
    nsids = ip("netns", "list-id")
    running = {
        "": {
            "addr_names": {a["ifname"]: a for a in addrs},
            "addr_ids": {a["ifindex"]: a for a in addrs},
            "nsids": {n["nsid"]: n.get("name", "") for n in nsids},
        },
    }
    for ns in running[""]["nsids"].values():
        addrs = ip("-n", ns, "addr", "show")
        nsids = ip("-n", ns, "netns", "list-id")
        running[ns] = {
            "addr_names": {a["ifname"]: a for a in addrs},
            "addr_ids": {a["ifindex"]: a for a in addrs},
            "nsids": {n["nsid"]: n.get("name", "") for n in nsids},
        }

    return running


def preprocess(conf, args):
    out = {}
    for ns, nsconfig in conf.items():
        for addr in nsconfig["addr_names"].values():
            ethtool = {}
            try:
                cmd = ["ethtool", "-i", addr["ifname"]]
                if ns != "":
                    cmd = ["ip", "netns", "exec", ns] + cmd
                stdout = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
                for line in stdout.decode("utf-8").splitlines():
                    if ":" not in line:
                        continue
                    k, v = line.split(": ", 1)
                    ethtool[k] = v.strip()
            except subprocess.CalledProcessError:
                pass

            attributes = {}

            if "linkinfo" in addr and "info_kind" in addr["linkinfo"]:
                kind = addr["linkinfo"]["info_kind"]
            elif ethtool.get("driver", "") not in ("", "N/A"):
                kind = ethtool["driver"]
                if ethtool.get("bus-info", "") not in ("", "N/A"):
                    attributes["bus"] = ethtool["bus-info"]
            elif "link_type" in addr:
                kind = addr["link_type"]
            else:
                kind = "???"

            data = addr.get("linkinfo", {}).get("info_data", {})
            if "link_netnsid" in addr and "link_index" in addr:
                link_ns = nsconfig["nsids"][addr["link_netnsid"]]
                link_dev = conf[link_ns]["addr_ids"][addr["link_index"]]["ifname"]
            elif "link" in addr:
                link_ns = ns
                link_dev = addr["link"]
            else:
                link_ns = ns
                link_dev = addr.get("linkinfo", {}).get("info_data", {}).get("link")

            if kind == "vxlan":
                attributes["id"] = data["id"]
                if "local" in data:
                    attributes["local"] = data["local"]
                if "remote" in data:
                    attributes["remote"] = data["remote"]
                elif "group" in data:
                    attributes["group"] = data["group"]
            elif kind == "bond":
                attributes["mode"] = data["mode"]
                if data["ad_lacp_active"] == "on":
                    attributes["lacp"] = data["ad_lacp_rate"]
            elif kind == "vlan":
                attributes["id"] = data["id"]

            l2 = []
            if args.l2_addresses:
                l2.append(addr["address"])

            ipv4 = []
            ipv6 = []
            for a in addr["addr_info"]:
                if a["family"] == "inet" and args.ipv4_addresses:
                    if a["scope"] == "global" or args.local_addresses:
                        ipv4.append(f"{a['local']}/{a['prefixlen']}")
                elif a["family"] == "inet6" and args.ipv6_addresses:
                    if a["scope"] == "global" or args.local_addresses:
                        ipv6.append(f"{a['local']}/{a['prefixlen']}")

            a = {
                "id": safe(f"{ns}_{addr['ifname']}"),
                "name": addr["ifname"],
                "kind": kind,
                "attributes": attributes,
                "l2": l2,
                "ipv4": ipv4,
                "ipv6": ipv6,
            }
            if "master" in addr:
                a["master"] = safe(f"{ns}_{addr['master']}")
            if link_dev is not None:
                a["link"] = safe(f"{link_ns}_{link_dev}")

            out.setdefault(ns, []).append(a)

    return out

if __name__ == "__main__":
    sys.exit(main())
