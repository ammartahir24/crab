tc qdisc del dev ifb0 root
tc qdisc add dev ifb0 root handle 1: htb default 11
tc class add dev ifb0 parent 1: classid 1:10 htb rate 25mbit
tc class add dev ifb0 parent 1:10 classid 1:11 htb rate 25mbit ceil 25mbit prio 1
tc class add dev ifb0 parent 1:10 classid 1:12 htb rate 1kbit ceil 25mbit prio 2
tc qdisc add dev ifb0 parent 1:11 bfifo limit 300000
tc qdisc add dev ifb0 parent 1:12 bfifo limit 300000

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

# tc filter add dev ifb0 parent 1: protocol ip prio 10 u32 match u32 0 0 flowid 1:11
