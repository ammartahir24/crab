tc qdisc del dev ifb0 root
tc qdisc add dev ifb0 root handle 1: htb default 11
tc class add dev ifb0 parent 1: classid 1:10 htb rate 30mbit
tc class add dev ifb0 parent 1:10 classid 1:11 htb rate 25mbit ceil 30mbit
tc class add dev ifb0 parent 1:10 classid 1:12 htb rate 5mbit ceil 30mbit
tc qdisc add dev ifb0 parent 1:11 bfifo limit 384000
tc qdisc add dev ifb0 parent 1:12 bfifo limit 384000

tc filter add dev ifb0 parent 1: protocol ip prio 1 u32 match ip src 185.125.190.37 flowid 1:10
tc filter add dev ifb0 parent 1: protocol ip prio 1 u32 match ip src 185.125.190.40 flowid 1:10
tc filter add dev ifb0 parent 1: protocol ip prio 1 u32 match ip src 91.189.88.248 flowid 1:10
tc filter add dev ifb0 parent 1: protocol ip prio 1 u32 match ip src 91.189.88.247 flowid 1:10
tc filter add dev ifb0 parent 1: protocol ip prio 1 u32 match ip src 91.189.91.123 flowid 1:10
tc filter add dev ifb0 parent 1: protocol ip prio 1 u32 match ip src 91.189.91.124 flowid 1:10

tc filter add dev ifb0 parent 1:10 protocol ip prio 1 u32 match ip src 185.125.190.37 flowid 1:12
tc filter add dev ifb0 parent 1:10 protocol ip prio 1 u32 match ip src 185.125.190.40 flowid 1:12
tc filter add dev ifb0 parent 1:10 protocol ip prio 1 u32 match ip src 91.189.88.248 flowid 1:12
tc filter add dev ifb0 parent 1:10 protocol ip prio 1 u32 match ip src 91.189.88.247 flowid 1:12
tc filter add dev ifb0 parent 1:10 protocol ip prio 1 u32 match ip src 91.189.91.123 flowid 1:12
tc filter add dev ifb0 parent 1:10 protocol ip prio 1 u32 match ip src 91.189.91.124 flowid 1:12
