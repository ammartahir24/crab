import os
import sys
import threading

def run_client(port):
	os.system("iperf3 -c 192.168.1.239 -p %d -t 100 -R" %(port))

num_clients = int(sys.argv[1])
start_port = 3000


for i in range(num_clients-1):
	start_port+=1
	threading.Thread(target=run_client, args=(start_port,)).start()

start_port+=1
os.system("iperf3 -c 192.168.1.239 -p %d -t 30 -R" %(start_port))
