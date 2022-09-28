tc qdisc del dev eth0 root

# bottleneck
tc qdisc add dev eth0 root handle 1: htb default 10
tc class add dev eth0 parent 1: classid 1:10 htb rate 30mbit

# htb just to classify traffic
tc qdisc add dev eth0 parent 1:10 handle 2: htb default 20
tc class add dev eth0 parent 2: classid 2:20 htb rate 100mbit
tc class add dev eth0 parent 2: classid 2:21 htb rate 100mbit
tc class add dev eth0 parent 2: classid 2:22 htb rate 100mbit

# different delay for each class
tc qdisc add dev eth0 parent 2:20 netem delay 10ms
tc qdisc add dev eth0 parent 2:21 netem delay 510ms
tc qdisc add dev eth0 parent 2:22 netem delay 50ms


# classify traffic into filters

#tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip dst 192.168.1.124 flowid 1:10
#tc filter add dev eth0 parent 2: protocol ip prio 1 u32 match ip dst 192.168.1.124 flowid 2:20

tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip sport 3001 0xffff flowid 1:10
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip sport 3002 0xffff flowid 1:10
tc filter add dev eth0 parent 1: protocol ip prio 1 u32 match ip sport 3003 0xffff flowid 1:10

tc filter add dev eth0 parent 2: protocol ip prio 1 u32 match ip sport 3001 0xffff flowid 2:20
tc filter add dev eth0 parent 2: protocol ip prio 1 u32 match ip sport 3002 0xffff flowid 2:21
tc filter add dev eth0 parent 2: protocol ip prio 1 u32 match ip sport 3003 0xffff flowid 2:22
