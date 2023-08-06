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
  graph [compound=true style=dotted];

  _lo [color=peru shape=invtriangle label=<<b>lo</b><br/><font color="peru">loopback</font>>];
  _enp1s0 [color=gray shape=oval label=<<b>enp1s0</b><br/><font color="gray">virtio_net</font><br/><font color="gray">bus 0000:01:00.0</font><br/><font color="navy">192.168.122.233/24</font>>];
  _br_phy [color=gray shape=diamond label=<<b>br-phy</b><br/><font color="gray">bridge</font>>];
  _p1 [color=red shape=hexagon label=<<b>p1</b><br/><font color="red">veth</font>>];
  _p2 [color=red shape=hexagon label=<<b>p2</b><br/><font color="red">veth</font>>];

  subgraph compute1 {
    label="netns compute1";
    cluster=true;

    compute1_lo [color=peru shape=invtriangle label=<<b>lo</b><br/><font color="peru">loopback</font>>];
    compute1_tenant [color=green shape=oval label=<<b>tenant</b><br/><font color="green">vlan</font><br/><font color="green">id 200</font>>];
    compute1_phy [color=red shape=hexagon label=<<b>phy</b><br/><font color="red">veth</font>>];
    compute1_br_tenant [color=gray shape=diamond label=<<b>br-tenant</b><br/><font color="gray">bridge</font>>];
    compute1_vm3 [color=gray shape=oval label=<<b>vm3</b><br/><font color="gray">dummy</font><br/><font color="navy">192.168.1.3/24</font>>];
    compute1_vm4 [color=gray shape=oval label=<<b>vm4</b><br/><font color="gray">dummy</font><br/><font color="navy">192.168.1.4/24</font>>];
    compute1_vxlan0 [color=blue shape=oval label=<<b>vxlan0</b><br/><font color="blue">vxlan</font><br/><font color="blue">id 1234</font><br/><font color="blue">local 172.16.2.1</font><br/><font color="blue">group 239.0.0.1</font>>];
  }

  subgraph compute2 {
    label="netns compute2";
    cluster=true;

    compute2_lo [color=peru shape=invtriangle label=<<b>lo</b><br/><font color="peru">loopback</font>>];
    compute2_tenant [color=green shape=oval label=<<b>tenant</b><br/><font color="green">vlan</font><br/><font color="green">id 200</font>>];
    compute2_vxlan0 [color=blue shape=oval label=<<b>vxlan0</b><br/><font color="blue">vxlan</font><br/><font color="blue">id 1234</font><br/><font color="blue">local 172.16.2.2</font><br/><font color="blue">group 239.0.0.1</font>>];
    compute2_br_tenant [color=gray shape=diamond label=<<b>br-tenant</b><br/><font color="gray">bridge</font>>];
    compute2_phy [color=red shape=hexagon label=<<b>phy</b><br/><font color="red">veth</font>>];
    compute2_vm1 [color=gray shape=oval label=<<b>vm1</b><br/><font color="gray">dummy</font><br/><font color="navy">192.168.1.1/24</font>>];
    compute2_vm2 [color=gray shape=oval label=<<b>vm2</b><br/><font color="gray">dummy</font><br/><font color="navy">192.168.1.2/24</font>>];
  }

  _p1 -- _br_phy;
  _p1 -- compute1_phy [style=dashed];
  _p2 -- _br_phy;
  _p2 -- compute2_phy [style=dashed];
  compute1_tenant -- compute1_phy [style=dashed];
  compute1_phy -- _p1 [style=dashed];
  compute1_vm3 -- compute1_br_tenant;
  compute1_vm4 -- compute1_br_tenant;
  compute1_vxlan0 -- compute1_br_tenant;
  compute1_vxlan0 -- compute1_tenant [style=dashed];
  compute2_tenant -- compute2_phy [style=dashed];
  compute2_vxlan0 -- compute2_br_tenant;
  compute2_vxlan0 -- compute2_tenant [style=dashed];
  compute2_phy -- _p2 [style=dashed];
  compute2_vm1 -- compute2_br_tenant;
  compute2_vm2 -- compute2_br_tenant;

  {
    rank=sink cluster=false;
    _lo;
    _enp1s0;
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
