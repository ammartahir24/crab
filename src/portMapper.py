import psutil
from subprocess import check_output
import time

'''
Finds the mapping between destination port of a packet and application using that port
'''
class PortMapper():
	def __init__(self):
		self.chrome_ports = []

	def get_pid(self, name):
		try:
			output = check_output(["pidof", name])
			return list(map(int, output.split()))
		except:
			return []

	def get_pname_from_dest_port(self, dest_port):
		all_conns = psutil.net_connections()
		for conn in all_conns:
			if conn.laddr.port == dest_port:
				process = psutil.Process(conn.pid)
				return process.name()
		return None

	def new_chrome_ports(self):
		chrome_pids = self.get_pid("chrome")
		# print(chrome_pids)
		all_conns = psutil.net_connections()
		# print(all_conns[0:5])
		new_ports = []
		for conn in all_conns:
			if conn.pid in chrome_pids:
				print(conn.pid, conn.laddr)
				if conn.laddr.port not in self.chrome_ports:
					new_ports.append(conn.laddr.port)
					self.chrome_ports.append(conn.laddr.port)
		return new_ports

	def inactive_ports(self):
		chrome_pids = self.get_pid("chrome")
		# print(chrome_pids)
		all_conns = psutil.net_connections()
		# print(all_conns[0:5])
		inactives = []
		chrome_ports = []
		for conn in all_conns:
			if conn.pid in chrome_pids:
				chrome_ports.append(conn.laddr.port)
				# self.chrome_ports.append(port)
		for p in self.chrome_ports:
			if p not in chrome_ports:
				inactives.append(p)
		return inactives

	def delete_ports(self, to_delete):
		for p in to_delete:
			self.chrome_ports.remove(p)

