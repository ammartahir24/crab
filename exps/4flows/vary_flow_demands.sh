ip link add name ifb0 type ifb
ip link set ifb0 up
tc qdisc del dev wan ingress
tc qdisc add dev wan handle ffff: ingress
tc filter add dev wan parent ffff: protocol ip u32 match u32 0 0 action mirred egress redirect dev ifb0

tc qdisc del dev ifb0 root
tc qdisc add dev ifb0 root handle 3: htb default 10
tc class add dev ifb0 parent 3: classid 3:10 htb rate 100mbit
tc class add dev ifb0 parent 3: classid 3:11 htb rate 100mbit
tc class add dev ifb0 parent 3: classid 3:12 htb rate 100mbit
tc class add dev ifb0 parent 3: classid 3:13 htb rate 100mbit
tc class add dev ifb0 parent 3: classid 3:14 htb rate 100mbit

tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 91.189.91.123 flowid 3:11
tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 91.189.91.124 flowid 3:11
tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 91.189.88.247 flowid 3:11
tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 91.189.88.248 flowid 3:11
tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 185.125.190.37 flowid 3:11
tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 185.125.190.40 flowid 3:11

tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 104.18.102.100 flowid 3:12
tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 104.18.103.100 flowid 3:12

tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 147.75.197.195 flowid 3:13
tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 130.215.31.13 flowid 3:13
tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 213.174.147.249 flowid 3:13

tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 18.7.29.125 flowid 3:14
tc filter add dev ifb0 parent 3: protocol ip prio 1 u32 match ip src 128.163.159.62 flowid 3:14

sleep 125s
tc class change dev ifb0 parent 3: classid 3:14 htb rate 1kbit
echo "f1 1kbit"
sleep 30s
tc class change dev ifb0 parent 3: classid 3:13 htb rate 10.5mbit
echo "f2 10.5mbit"
sleep 30s
tc class change dev ifb0 parent 3: classid 3:12 htb rate 10.5mbit
echo "f3 10.5mbit"
