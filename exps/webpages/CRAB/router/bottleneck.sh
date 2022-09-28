tc qdisc del dev lan1 root
tc qdisc add dev lan1 root handle 1: htb default 10
tc class add dev lan1 parent 1: classid 1:10 htb rate 10mbit
tc qdisc add dev lan1 parent 1:10 bfifo limit 128000
