# linux-tools

Various command line utilities for Linux written in python.

## License

BSD 3 Clause

## Installation

```console
$ pip install --user linux-tools
```

## bits

```
usage: bits [-h] [-m | -b | -l] MASK_OR_LIST [MASK_OR_LIST ...]

Convert a bit list into a hex mask or the other way around.

positional arguments:
  MASK_OR_LIST  A set of bits specified as a hexadecimal mask value (e.g.
                0xeec2) or as a comma-separated list of bit IDs. Consecutive
                ids can be compressed as ranges (e.g. 5,6,7,8,9,10 --> 5-10).

options:
  -h, --help    show this help message and exit

mode:
  -m, --mask    Print the combined args as a hexadecimal mask value (default).
  -b, --bit     Print the combined args as a bit mask value.
  -l, --list    Print the combined args as a list of bit IDs. Consecutive IDs
                are compressed as ranges.
```

Examples:

```console
$ bits -m 4,5-8 16,30
0x400101f0
```

```console
$ bits -l 0xeec2
1,6,7,9-11,13-15
```

```console
$ bits -b 4,5-8 16,30
0b100_0000_0000_0001_0000_0001_1111_0000
```

## irqstat

```
usage: irqstat [-h] [-r ROOT] [-c CPU_RANGE_OR_MASK] [-i IRQ] [-n] [-s] [-z]
               [-e]

Display linux interrupts information.

options:
  -h, --help            show this help message and exit
  -r ROOT, --root ROOT  Root dir used to determine path to /proc (default /).
  -c CPU_RANGE_OR_MASK, --cpu CPU_RANGE_OR_MASK
                        CPUs specified as an hexadecimal mask values (e.g.
                        0xeec2) or as a comma-separated list of IDs.
                        Consecutive IDs can be compressed as ranges (e.g.
                        5,6,7,8,9,10 --> 5-10). Can be used multiple times.
  -i IRQ, --irq IRQ     Only show this IRQ. Can be used multiple times.
  -n, --num-per-cpu     Display the number of bound IRQs per CPU.
  -s, --stats           Display interrupt counts.
  -z, --display-zeroes  Also show -s/--stats with 0 values.
  -e, --exact           Display exact stats values.
```

Examples:

```console
$ irqstat -sc 0x3
IRQ      CPU-0  CPU-1  DESCRIPTION
12           0    144  IO-APIC 12-edge i8042
21         129     28  IO-APIC 21-fasteoi qxl
38          36      0  PCI-MSI 1048576-edge xhci_hcd
44           0     10  PCI-MSI 1572865-edge virtio1-virtqueues
46           0   3.7K  PCI-MSI 524289-edge virtio0-input.0
47          44      9  PCI-MSI 524290-edge virtio0-output.0
49        1.0K      0  PCI-MSI 2097153-edge virtio2-req.0
50           0    803  PCI-MSI 2097154-edge virtio2-req.1
54           0    212  PCI-MSI 442368-edge snd_hda_intel:card0
CAL      18.4K  26.8K  Function call interrupts
HI           6      1  high priority tasklet softirq
HYP          1      1  Hypervisor callback interrupts
LOC      73.1K  43.5K  Local timer interrupts
MCP         13     12  Machine check polls
NET_RX      44   3.8K  network receive softirq
NET_TX       0      1  network transmit softirq
RCU      21.2K  12.9K  RCU softirq
RES       2.3K   3.5K  Rescheduling interrupts
SCHED    34.4K  31.8K  schedule softirq
TASKLET     35     10  normal priority tasklet softirq
TIMER    30.6K  27.0K  timer softirq
TLB         51     29  TLB shootdowns
```

```console
$ irqstat -c 4
IRQ       AFFINITY  EFFECTIVE-CPU  DESCRIPTION
134              4              4  IR-PCI-MSIX-0000:2e:00.0 5-edge nvme0q5
142              4              4  IR-PCI-MSI-0000:00:02.0 0-edge i915
154            0-7            0-7  dummy 21 elan_i2c
BLOCK          0-7            0-7  block device softirq
CAL            0-7            0-7  Function call interrupts
DFR            0-7            0-7  Deferred Error APIC interrupts
HI             0-7            0-7  high priority tasklet softirq
HRTIMER        0-7            0-7  high resolution timer softirq
IRQ_POLL       0-7            0-7  IO poll softirq
IWI            0-7            0-7  IRQ work interrupts
LOC            0-7            0-7  Local timer interrupts
MCE            0-7            0-7  Machine check exceptions
MCP            0-7            0-7  Machine check polls
NET_RX         0-7            0-7  network receive softirq
NET_TX         0-7            0-7  network transmit softirq
NMI            0-7            0-7  Non-maskable interrupts
NPI            0-7            0-7  Nested posted-interrupt event
PIN            0-7            0-7  Posted-interrupt notification event
PIW            0-7            0-7  Posted-interrupt wakeup event
PMI            0-7            0-7  Performance monitoring interrupts
RCU            0-7            0-7  RCU softirq
RES            0-7            0-7  Rescheduling interrupts
RTR            0-7            0-7  APIC ICR read retries
SCHED          0-7            0-7  schedule softirq
SPU            0-7            0-7  Spurious interrupts
TASKLET        0-7            0-7  normal priority tasklet softirq
THR            0-7            0-7  Threshold APIC interrupts
TIMER          0-7            0-7  timer softirq
TLB            0-7            0-7  TLB shootdowns
TRM            0-7            0-7  Thermal event interrupts
```

```console
$ irqstat -n
CPU  AFFINITY-IRQs  EFFECTIVE-IRQs
0               14              11
1               14               3
2               16               4
3               14               2
4               14               2
5               16               3
6               17               6
7               14               2
```

## netgraph

```
usage: netgraph [-h] [-2] [-4] [-6] [-l]

Convert linux networking configuration to a DOT graph. The output can be piped
to dot to convert it to SVG or other formats. Example:

    netgraph | dot -Tsvg > net.svg

System dependencies: iproute2, ethtool

options:
  -h, --help            show this help message and exit
  -2, --l2-addresses    Display mac addresses.
  -4, --ipv4-addresses  Display IPv4 addresses.
  -6, --ipv6-addresses  Display IPv6 addresses.
  -l, --local-addresses
                        Display link local addresses.
```

Example:

```console
$ netgraph -4
// generated using netgraph
// SPDX-License-Identifier: BSD-3-Clause
// Copyright (c) 2023 Robin Jarry
graph {
  node [fontsize=11 fontname=monospace margin=0];
  edge [fontsize=11 fontname=monospace margin=0];
  graph [fontsize=11 fontname=monospace compound=true style=dotted];

  _enp1s0 [tooltip="lladdr 52:54:00:71:c4:d3\ninet6 fe80::5054:ff:fe71:c4d3/64" color=gray shape=oval label=<<b>enp1s0</b><br/><font color="gray">virtio_net</font><br/><font color="gray">bus 0000:01:00.0</font><br/><font color="purple">192.168.122.233/24</font>>];
  _br_phy [tooltip="forward_delay 1500\nhello_time 200\nmax_age 2000\nageing_time 30000\nstp_state 0\npriority 32768\nvlan_filtering 1\nvlan_protocol 802.1Q\nbridge_id 8000.76:eb:ec:34:f1:b\nroot_id 8000.76:eb:ec:34:f1:b\nroot_port 0\nroot_path_cost 0\ntopology_change 0\ntopology_change_detected 0\nhello_timer 0.0\ntcn_timer 0.0\ntopology_change_timer 0.0\ngc_timer 297.74\nvlan_default_pvid 1\nvlan_stats_enabled 0\nvlan_stats_per_port 0\ngroup_fwd_mask 0\ngroup_addr 01:80:c2:00:00:00\nmcast_snooping 1\nmcast_vlan_snooping 0\nmcast_router 1\nmcast_query_use_ifaddr 0\nmcast_querier 0\nmcast_hash_elasticity 16\nmcast_hash_max 4096\nmcast_last_member_cnt 2\nmcast_startup_query_cnt 2\nmcast_last_member_intvl 100\nmcast_membership_intvl 26000\nmcast_querier_intvl 25500\nmcast_query_intvl 12500\nmcast_query_response_intvl 1000\nmcast_startup_query_intvl 3125\nmcast_stats_enabled 0\nmcast_igmp_version 2\nmcast_mld_version 1\nnf_call_iptables 0\nnf_call_ip6tables 0\nnf_call_arptables 0\nlladdr 76:eb:ec:34:f1:0b\ninet6 fe80::84f6:42ff:fe8a:5475/64" color=red shape=octagon label=<<b>br-phy</b><br/><font color="red">bridge</font>>];
  _p0 [tooltip="lladdr da:79:60:12:ef:fd\ninet6 fe80::d879:60ff:fe12:effd/64" color=blue shape=oval label=<<b>p0</b><br/><font color="blue">veth</font>>];
  _p1 [tooltip="lladdr 76:eb:ec:34:f1:0b\ninet6 fe80::74eb:ecff:fe34:f10b/64" color=blue shape=oval label=<<b>p1</b><br/><font color="blue">veth</font>>];

  subgraph compute1 {
    label="netns compute1";
    cluster=true;

    compute1_tenants [tooltip="protocol 802.1Q\nid 404\nflags ['REORDER_HDR']\nlladdr 72:83:c0:3f:a4:c0\ninet6 fe80::7083:c0ff:fe3f:a4c0/64" color=green shape=rectangle margin=0.05 label=<<b>tenants</b><br/><font color="green">vlan</font><br/><font color="green">id 404</font><br/><font color="purple">172.16.13.1/24</font>>];
    compute1_br_internal [tooltip="forward_delay 1500\nhello_time 200\nmax_age 2000\nageing_time 30000\nstp_state 0\npriority 32768\nvlan_filtering 1\nvlan_protocol 802.1Q\nbridge_id 8000.2:91:de:e7:ba:a4\nroot_id 8000.2:91:de:e7:ba:a4\nroot_port 0\nroot_path_cost 0\ntopology_change 0\ntopology_change_detected 0\nhello_timer 0.0\ntcn_timer 0.0\ntopology_change_timer 0.0\ngc_timer 297.74\nvlan_default_pvid 1\nvlan_stats_enabled 0\nvlan_stats_per_port 0\ngroup_fwd_mask 0\ngroup_addr 01:80:c2:00:00:00\nmcast_snooping 1\nmcast_vlan_snooping 0\nmcast_router 1\nmcast_query_use_ifaddr 0\nmcast_querier 0\nmcast_hash_elasticity 16\nmcast_hash_max 4096\nmcast_last_member_cnt 2\nmcast_startup_query_cnt 2\nmcast_last_member_intvl 100\nmcast_membership_intvl 26000\nmcast_querier_intvl 25500\nmcast_query_intvl 12500\nmcast_query_response_intvl 1000\nmcast_startup_query_intvl 3125\nmcast_stats_enabled 0\nmcast_igmp_version 2\nmcast_mld_version 1\nnf_call_iptables 0\nnf_call_ip6tables 0\nnf_call_arptables 0\nlladdr 02:91:de:e7:ba:a4\ninet6 fe80::2040:9bff:feb1:efbd/64" color=red shape=octagon label=<<b>br-internal</b><br/><font color="red">bridge</font>>];
    compute1_vx_internal [tooltip="id 1337\ngroup 239.0.13.37\nlink tenants\nport_range {'low': 0, 'high': 0}\nport 4789\nlearning True\nttl 5\ndf unset\nageing 300\nudp_csum True\nudp_zero_csum6_tx False\nudp_zero_csum6_rx False\nlladdr 02:91:de:e7:ba:a4\ninet6 fe80::91:deff:fee7:baa4/64" color=darkgreen shape=rectangle margin=0.05 label=<<b>vx-internal</b><br/><font color="darkgreen">vxlan</font><br/><font color="darkgreen">id 1337</font><br/><font color="darkgreen">group 239.0.13.37</font>>];
    compute1_br_external [tooltip="forward_delay 1500\nhello_time 200\nmax_age 2000\nageing_time 30000\nstp_state 0\npriority 32768\nvlan_filtering 1\nvlan_protocol 802.1Q\nbridge_id 8000.22:19:24:60:46:42\nroot_id 8000.22:19:24:60:46:42\nroot_port 0\nroot_path_cost 0\ntopology_change 0\ntopology_change_detected 0\nhello_timer 0.0\ntcn_timer 0.0\ntopology_change_timer 0.0\ngc_timer 68.36\nvlan_default_pvid 1\nvlan_stats_enabled 0\nvlan_stats_per_port 0\ngroup_fwd_mask 0\ngroup_addr 01:80:c2:00:00:00\nmcast_snooping 1\nmcast_vlan_snooping 0\nmcast_router 1\nmcast_query_use_ifaddr 0\nmcast_querier 0\nmcast_hash_elasticity 16\nmcast_hash_max 4096\nmcast_last_member_cnt 2\nmcast_startup_query_cnt 2\nmcast_last_member_intvl 100\nmcast_membership_intvl 26000\nmcast_querier_intvl 25500\nmcast_query_intvl 12500\nmcast_query_response_intvl 1000\nmcast_startup_query_intvl 3125\nmcast_stats_enabled 0\nmcast_igmp_version 2\nmcast_mld_version 1\nnf_call_iptables 0\nnf_call_ip6tables 0\nnf_call_arptables 0\nlladdr 22:19:24:60:46:42\ninet6 fe80::843a:6eff:fe60:7450/64" color=red shape=octagon label=<<b>br-external</b><br/><font color="red">bridge</font>>];
    compute1_external [tooltip="protocol 802.1Q\nid 407\nflags ['REORDER_HDR']\nlladdr 72:83:c0:3f:a4:c0\ninet6 fe80::7083:c0ff:fe3f:a4c0/64" color=green shape=rectangle margin=0.05 label=<<b>external</b><br/><font color="green">vlan</font><br/><font color="green">id 407</font>>];
    compute1_phy0 [tooltip="lladdr 72:83:c0:3f:a4:c0\ninet6 fe80::7083:c0ff:fe3f:a4c0/64" color=blue shape=oval label=<<b>phy0</b><br/><font color="blue">veth</font>>];
    compute1_vm1 [tooltip="lladdr 66:33:b0:e4:1f:ee\ninet6 fe80::6433:b0ff:fee4:1fee/64" color=blue shape=oval label=<<b>vm1</b><br/><font color="blue">veth</font>>];
    compute1_vm2 [tooltip="lladdr ea:52:34:41:78:a1\ninet6 fe80::e852:34ff:fe41:78a1/64" color=blue shape=oval label=<<b>vm2</b><br/><font color="blue">veth</font>>];
    compute1_vm6 [tooltip="lladdr 22:19:24:60:46:42\ninet6 fe80::2019:24ff:fe60:4642/64" color=blue shape=oval label=<<b>vm6</b><br/><font color="blue">veth</font>>];
  }

  subgraph guest1 {
    label="netns guest1";
    cluster=true;

    guest1_guest1 [tooltip="lladdr 9a:2e:e8:af:41:29\ninet6 fe80::982e:e8ff:feaf:4129/64" color=blue shape=oval label=<<b>guest1</b><br/><font color="blue">veth</font><br/><font color="purple">10.16.0.1/24</font>>];
  }

  subgraph guest2 {
    label="netns guest2";
    cluster=true;

    guest2_guest2 [tooltip="lladdr ce:68:e5:98:e3:e9\ninet6 fe80::cc68:e5ff:fe98:e3e9/64" color=blue shape=oval label=<<b>guest2</b><br/><font color="blue">veth</font><br/><font color="purple">10.16.0.2/24</font>>];
  }

  subgraph guest6 {
    label="netns guest6";
    cluster=true;

    guest6_guest6 [tooltip="lladdr d6:e9:38:49:be:72\ninet6 fe80::d4e9:38ff:fe49:be72/64" color=blue shape=oval label=<<b>guest6</b><br/><font color="blue">veth</font><br/><font color="purple">10.99.0.6/24</font>>];
  }

  subgraph compute2 {
    label="netns compute2";
    cluster=true;

    compute2_tenants [tooltip="protocol 802.1Q\nid 404\nflags ['REORDER_HDR']\nlladdr 6e:63:91:74:1d:33\ninet6 fe80::6c63:91ff:fe74:1d33/64" color=green shape=rectangle margin=0.05 label=<<b>tenants</b><br/><font color="green">vlan</font><br/><font color="green">id 404</font><br/><font color="purple">172.16.13.2/24</font>>];
    compute2_br_internal [tooltip="forward_delay 1500\nhello_time 200\nmax_age 2000\nageing_time 30000\nstp_state 0\npriority 32768\nvlan_filtering 1\nvlan_protocol 802.1Q\nbridge_id 8000.52:31:2a:dc:63:fc\nroot_id 8000.52:31:2a:dc:63:fc\nroot_port 0\nroot_path_cost 0\ntopology_change 0\ntopology_change_detected 0\nhello_timer 0.0\ntcn_timer 0.0\ntopology_change_timer 0.0\ngc_timer 297.72\nvlan_default_pvid 1\nvlan_stats_enabled 0\nvlan_stats_per_port 0\ngroup_fwd_mask 0\ngroup_addr 01:80:c2:00:00:00\nmcast_snooping 1\nmcast_vlan_snooping 0\nmcast_router 1\nmcast_query_use_ifaddr 0\nmcast_querier 0\nmcast_hash_elasticity 16\nmcast_hash_max 4096\nmcast_last_member_cnt 2\nmcast_startup_query_cnt 2\nmcast_last_member_intvl 100\nmcast_membership_intvl 26000\nmcast_querier_intvl 25500\nmcast_query_intvl 12500\nmcast_query_response_intvl 1000\nmcast_startup_query_intvl 3125\nmcast_stats_enabled 0\nmcast_igmp_version 2\nmcast_mld_version 1\nnf_call_iptables 0\nnf_call_ip6tables 0\nnf_call_arptables 0\nlladdr 52:31:2a:dc:63:fc\ninet6 fe80::d0ef:d6ff:fe39:a863/64" color=red shape=octagon label=<<b>br-internal</b><br/><font color="red">bridge</font>>];
    compute2_vx_internal [tooltip="id 1337\ngroup 239.0.13.37\nlink tenants\nport_range {'low': 0, 'high': 0}\nport 4789\nlearning True\nttl 5\ndf unset\nageing 300\nudp_csum True\nudp_zero_csum6_tx False\nudp_zero_csum6_rx False\nlladdr aa:67:73:6c:36:51\ninet6 fe80::a867:73ff:fe6c:3651/64" color=darkgreen shape=rectangle margin=0.05 label=<<b>vx-internal</b><br/><font color="darkgreen">vxlan</font><br/><font color="darkgreen">id 1337</font><br/><font color="darkgreen">group 239.0.13.37</font>>];
    compute2_br_external [tooltip="forward_delay 1500\nhello_time 200\nmax_age 2000\nageing_time 30000\nstp_state 0\npriority 32768\nvlan_filtering 1\nvlan_protocol 802.1Q\nbridge_id 8000.6e:63:91:74:1d:33\nroot_id 8000.6e:63:91:74:1d:33\nroot_port 0\nroot_path_cost 0\ntopology_change 0\ntopology_change_detected 0\nhello_timer 0.0\ntcn_timer 0.0\ntopology_change_timer 0.0\ngc_timer 68.34\nvlan_default_pvid 1\nvlan_stats_enabled 0\nvlan_stats_per_port 0\ngroup_fwd_mask 0\ngroup_addr 01:80:c2:00:00:00\nmcast_snooping 1\nmcast_vlan_snooping 0\nmcast_router 1\nmcast_query_use_ifaddr 0\nmcast_querier 0\nmcast_hash_elasticity 16\nmcast_hash_max 4096\nmcast_last_member_cnt 2\nmcast_startup_query_cnt 2\nmcast_last_member_intvl 100\nmcast_membership_intvl 26000\nmcast_querier_intvl 25500\nmcast_query_intvl 12500\nmcast_query_response_intvl 1000\nmcast_startup_query_intvl 3125\nmcast_stats_enabled 0\nmcast_igmp_version 2\nmcast_mld_version 1\nnf_call_iptables 0\nnf_call_ip6tables 0\nnf_call_arptables 0\nlladdr 6e:63:91:74:1d:33\ninet6 fe80::fc92:fbff:feaf:cca/64" color=red shape=octagon label=<<b>br-external</b><br/><font color="red">bridge</font>>];
    compute2_external [tooltip="protocol 802.1Q\nid 407\nflags ['REORDER_HDR']\nlladdr 6e:63:91:74:1d:33\ninet6 fe80::6c63:91ff:fe74:1d33/64" color=green shape=rectangle margin=0.05 label=<<b>external</b><br/><font color="green">vlan</font><br/><font color="green">id 407</font>>];
    compute2_phy1 [tooltip="lladdr 6e:63:91:74:1d:33\ninet6 fe80::6c63:91ff:fe74:1d33/64" color=blue shape=oval label=<<b>phy1</b><br/><font color="blue">veth</font>>];
    compute2_vm3 [tooltip="lladdr c2:bb:13:b5:bd:13\ninet6 fe80::c0bb:13ff:feb5:bd13/64" color=blue shape=oval label=<<b>vm3</b><br/><font color="blue">veth</font>>];
    compute2_vm4 [tooltip="lladdr 52:31:2a:dc:63:fc\ninet6 fe80::5031:2aff:fedc:63fc/64" color=blue shape=oval label=<<b>vm4</b><br/><font color="blue">veth</font>>];
    compute2_vm5 [tooltip="lladdr ca:96:fe:af:60:15\ninet6 fe80::c896:feff:feaf:6015/64" color=blue shape=oval label=<<b>vm5</b><br/><font color="blue">veth</font>>];
  }

  subgraph guest3 {
    label="netns guest3";
    cluster=true;

    guest3_guest3 [tooltip="lladdr aa:81:ae:0a:39:ae\ninet6 fe80::a881:aeff:fe0a:39ae/64" color=blue shape=oval label=<<b>guest3</b><br/><font color="blue">veth</font><br/><font color="purple">10.16.0.3/24</font>>];
  }

  subgraph guest4 {
    label="netns guest4";
    cluster=true;

    guest4_guest4 [tooltip="lladdr 52:cb:9e:13:35:08\ninet6 fe80::50cb:9eff:fe13:3508/64" color=blue shape=oval label=<<b>guest4</b><br/><font color="blue">veth</font><br/><font color="purple">10.16.0.4/24</font>>];
  }

  subgraph guest5 {
    label="netns guest5";
    cluster=true;

    guest5_guest5 [tooltip="lladdr 92:41:c2:96:15:99\ninet6 fe80::9041:c2ff:fe96:1599/64" color=blue shape=oval label=<<b>guest5</b><br/><font color="blue">veth</font><br/><font color="purple">10.99.0.5/24</font>>];
  }

  _p0 -- _br_phy [label="VLAN\n400-409"];
  _p1 -- _br_phy [label="VLAN\n400-409"];
  compute1_vx_internal -- compute1_br_internal;
  compute1_external -- compute1_br_external;
  compute1_vm1 -- compute1_br_internal;
  compute1_vm2 -- compute1_br_internal;
  compute1_vm6 -- compute1_br_external;
  compute2_vx_internal -- compute2_br_internal;
  compute2_external -- compute2_br_external;
  compute2_vm3 -- compute2_br_internal;
  compute2_vm4 -- compute2_br_internal;
  compute2_vm5 -- compute2_br_external;
  compute1_tenants -- compute1_phy0 [style=dashed];
  compute1_vx_internal -- compute1_tenants [style=dashed];
  compute1_external -- compute1_phy0 [style=dashed];
  compute1_phy0 -- _p0 [style=dashed];
  guest1_guest1 -- compute1_vm1 [style=dashed];
  guest2_guest2 -- compute1_vm2 [style=dashed];
  guest6_guest6 -- compute1_vm6 [style=dashed];
  compute2_tenants -- compute2_phy1 [style=dashed];
  compute2_vx_internal -- compute2_tenants [style=dashed];
  compute2_external -- compute2_phy1 [style=dashed];
  compute2_phy1 -- _p1 [style=dashed];
  guest3_guest3 -- compute2_vm3 [style=dashed];
  guest4_guest4 -- compute2_vm4 [style=dashed];
  guest5_guest5 -- compute2_vm5 [style=dashed];

  {
    rank=sink cluster=false;
    _enp1s0;
    _br_phy;
  }
}
```

Here is the result after piping this output to
[dot](https://graphviz.org/doc/info/command.html):

![netgraph](https://git.sr.ht/~rjarry/linux-tools/blob/main/netgraph-example.png)

## Development

Send questions, bug reports and patches to
[~rjarry/public-inbox@lists.sr.ht](https://lists.sr.ht/~rjarry/public-inbox).

```sh
git clone https://git.sr.ht/~rjarry/linux-tools
cd linux-tools
git config format.subjectPrefix "PATCH linux-tools"
git config sendemail.to "~rjarry/public-inbox@lists.sr.ht"
```
