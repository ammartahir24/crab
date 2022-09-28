tc qdisc del dev eth0 root
tc qdisc add dev eth0 root handle 1: htb default 10
tc class add dev eth0 parent 1: classid 1:10 htb rate 60mbit
tc qdisc add dev eth0 parent 1:10 netem delay 30ms
#tc qdisc add dev eth0 parent 1:10  bfifo limit 384000
