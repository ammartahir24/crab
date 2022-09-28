import os

'''
Run this file after booting. It sets up ifb interface at the ingress where CRAB sets up and updates HTB queues.
'''

os.system("sudo modprobe ifb numifbs=1")
os.system("sudo ip link set dev ifb0 up")
os.system("sudo tc qdisc add dev enp0s3 handle ffff: ingress")
os.system("sudo tc filter add dev enp0s3 parent ffff: protocol ip u32 match u32 0 0 action mirred egress redirect dev ifb0")
