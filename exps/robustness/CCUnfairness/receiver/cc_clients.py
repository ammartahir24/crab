import os
import sys
import threading

def run_client(port, cc):
	os.system("iperf3 -c 192.168.1.239 -p %d -t 100 -R -C %s" %(port, cc))

cc1 = sys.argv[1]
cc2 = sys.argv[2]
start_port = 3000



threading.Thread(target=run_client, args=(3001,cc1,)).start()
threading.Thread(target=run_client, args=(3002,cc2,)).start()

os.system("iperf3 -c 192.168.1.239 -p %d -t 30 -R -C cubic" %(3003))
