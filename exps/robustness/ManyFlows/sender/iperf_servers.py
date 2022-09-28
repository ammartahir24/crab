import os
import sys
import threading

num_servers = int(sys.argv[1])

base_port = 3000

def run_server(port):
	os.system("iperf3 -s -p %d" %(port))

for i in range(num_servers):
	base_port+=1
	threading.Thread(target=run_server, args=(base_port,)).start()
