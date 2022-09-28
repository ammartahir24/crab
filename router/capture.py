from scapy.all import sniff, TCP, UDP
import threading
import time
import datetime
import subprocess as sub


class Packet:
	def __init__(self, pkt):
		self.pkt = str(pkt)[2:-1]
		try:
			self.src = self.pkt.split("IP ")[1].split(" >")[0].split(".")
			self.src, self.sport = ".".join(self.src[:-1]), self.src[-1] 
			self.dst = self.pkt.split("> ")[1].split(":")[0].split(".")
			self.dst, self.dport = ".".join(self.dst[:-1]), self.dst[-1]
			self.len = int(self.pkt.split('length ')[-1]) + 20
			time = self.pkt.split(".")[0]
			msec = float(self.pkt.split(".")[1].split(" ")[0])/1000000
			date = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")	 
			self.time = datetime.datetime.timestamp(date) + msec
		except:
			self.src = None	

class TrafficAnalyzer:
	def __init__(self, td=1, new_flow_handle = None):
		self.flows = {}
		self.td = td
		self.new_flow_callback = new_flow_handle
		threading.Thread(target=self.run_sniffer).start()
		

	def recv_pkt(self, packet):
		if packet.src == None:
			return
		src, dst, sport, dport, length, time = packet.dst, packet.src, packet.sport, packet.dport, packet.len, packet.time
		if "192.168.1" not in src:
			return
		if src not in self.flows:
			print("New flow", src, sport, dport)
			self.flows[src] = [{}, length]
			self.flows[src][0][int(time/self.td)] = length
			self.new_flow_callback(src, dport)
		else:
			self.flows[src][1] += length
			if int(time/self.td) in self.flows[src][0]:
				self.flows[src][0][int(time/self.td)] += length
			else:
				self.flows[src][0][int(time/self.td)] = length

	def last_readings(self, flow_src, flows, n=5):
		now = time.time()
		last_n = []
		if flow_src != "default":
			if flow_src not in self.flows:
				return [0]*n
			for i in range(n):
				if int((now - i*self.td)/self.td) in self.flows[flow_src][0]:
					last_n += [self.flows[flow_src][0][int((now - i*self.td)/self.td)]]
				else:
					last_n += [0]
			return last_n
		else:
			last_n = [0]*n
			for f in self.flows.keys():
				if f not in flows:
					for i in range(n):
						if int((now - i*self.td)/self.td) in self.flows[f][0]:
							last_n[i] += self.flows[f][0][int((now - i*self.td)/self.td)]
			return last_n

	def last_readings_flow(self, ip_list, main_traffic=[], n=5):
		traffic_for_flow = [0]*n
		if ip_list == '*':
			traffic_for_flow = self.last_readings("default", main_traffic, n)
			return traffic_for_flow
		else:
			for ip in ip_list:
				this_flow = self.last_readings(ip, main_traffic, n)
				traffic_for_flow = [traffic_for_flow[i]+this_flow[i] for i in range(n)]
			return traffic_for_flow


	def print_flows(self):

		print("\nSource IP\t Total Data \t Last 5 rates\n")
		for k in self.flows.keys():
			last_n = "\t".join([str(x/(10**6)) for x in self.last_readings(k)])
			print(k, self.flows[k][1]/(10**6), last_n)

	def run_sniffer(self):
		#sniff(iface="lan1", filter="ip", prn=self.recv_pkt, count=-1, store=0)
		p = sub.Popen(('tcpdump', '--direction=out', '-tttt', '-ni', 'lan1', '-l'), stdout=sub.PIPE)
		for row in iter(p.stdout.readline, b''):
			self.recv_pkt(Packet(row.rstrip()))

# t = TrafficAnalyzer()