tc qdisc del dev lan1 root
tc qdisc add dev lan1 root handle 2: htb default 2

tc class add dev lan1 parent 2: classid 2:2 htb rate 30mbit

tc qdisc add dev lan1 parent 2:2 handle 1: htb default 10

tc class add dev lan1 parent 1: classid 1:10 htb rate 100mbit
#tc class add dev lan1 parent 1: classid 1:11 htb rate 2mbit
tc class add dev lan1 parent 1: classid 1:11 htb rate 100mbit quantum 1500
tc class add dev lan1 parent 1: classid 1:12 htb rate 100mbit quantum 3000
tc class add dev lan1 parent 1: classid 1:13 htb rate 100mbit quantum 4500
tc class add dev lan1 parent 1: classid 1:14 htb rate 100mbit quantum 6000

tc qdisc add dev lan1 parent 1:11 bfifo limit 584000
tc qdisc add dev lan1 parent 1:12 bfifo limit 584000
tc qdisc add dev lan1 parent 1:13 bfifo limit 584000
tc qdisc add dev lan1 parent 1:14 bfifo limit 584000

tc filter add dev lan1 parent 2: protocol ip prio 1 u32 match ip src 185.125.190.37 flowid 2:2
tc filter add dev lan1 parent 2: protocol ip prio 1 u32 match ip src 185.125.190.40 flowid 2:2
tc filter add dev lan1 parent 2: protocol ip prio 1 u32 match ip src 91.189.91.123 flowid 2:2
tc filter add dev lan1 parent 2: protocol ip prio 1 u32 match ip src 91.189.91.124 flowid 2:2
tc filter add dev lan1 parent 2: protocol ip prio 1 u32 match ip src 91.189.88.247 flowid 2:2
tc filter add dev lan1 parent 2: protocol ip prio 1 u32 match ip src 91.189.88.248 flowid 2:2

tc filter add dev lan1 parent 2: protocol ip prio 1 u32 match ip src 104.18.102.100 flowid 2:2
tc filter add dev lan1 parent 2: protocol ip prio 1 u32 match ip src 104.18.103.100 flowid 2:2

tc filter add dev lan1 parent 2: protocol ip prio 1 u32 match ip src 130.215.31.13 flowid 2:2
tc filter add dev lan1 parent 2: protocol ip prio 1 u32 match ip src 147.75.197.195 flowid 2:2

tc filter add dev lan1 parent 2: protocol ip prio 1 u32 match ip src 18.7.29.125 flowid 2:2

tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 185.125.190.37 flowid 1:11
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 185.125.190.40 flowid 1:11
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 91.189.91.123 flowid 1:11
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 91.189.91.124 flowid 1:11
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 91.189.88.247 flowid 1:11
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 91.189.88.248 flowid 1:11

tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 104.18.102.100 flowid 1:12
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 104.18.103.100 flowid 1:12

tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 130.215.31.13 flowid 1:13
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 147.75.197.195 flowid 1:13

tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 18.7.29.125 flowid 1:14
