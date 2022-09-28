tc qdisc del dev lan1 root
tc qdisc add dev lan1 root handle 1: htb default 11

tc class add dev lan1 parent 1: classid 1:10 htb rate 10mbit
tc class add dev lan1 parent 1:10 classid 1:11 htb rate 7mbit ceil 30mbit quantum 7000
tc class add dev lan1 parent 1:10 classid 1:12 htb rate 3mbit ceil 30mbit quantum 3000

tc qdisc add dev lan1 parent 1:11 bfifo limit 128000
tc qdisc add dev lan1 parent 1:12 bfifo limit 128000

tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 185.125.190.37 flowid 1:10
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 185.125.190.40 flowid 1:10
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 91.189.91.123 flowid 1:10
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 91.189.91.124 flowid 1:10
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 91.189.88.247 flowid 1:10
tc filter add dev lan1 parent 1: protocol ip prio 1 u32 match ip src 91.189.88.248 flowid 1:10

tc filter add dev lan1 parent 1:10 protocol ip prio 1 u32 match ip src 185.125.190.37 flowid 1:12
tc filter add dev lan1 parent 1:10 protocol ip prio 1 u32 match ip src 185.125.190.40 flowid 1:12
tc filter add dev lan1 parent 1:10 protocol ip prio 1 u32 match ip src 91.189.91.123 flowid 1:12
tc filter add dev lan1 parent 1:10 protocol ip prio 1 u32 match ip src 91.189.91.124 flowid 1:12
tc filter add dev lan1 parent 1:10 protocol ip prio 1 u32 match ip src 91.189.88.247 flowid 1:12
tc filter add dev lan1 parent 1:10 protocol ip prio 1 u32 match ip src 91.189.88.248 flowid 1:12

