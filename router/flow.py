import os 


class IpProps:
	def __init__(self, ip, ip_num, f_id):
		self.ip = ip
		self.ip_num = ip_num
		self.ip_handle = self.ip_num.get_num()
		self.flow_id = f_id

class Flow:
	def __init__(self, flow_id, ip_list, weight, ip_num_handle, bw = 0, min_=1, name="", apps=[], time_to_realloc_thresh=10):
		self.id = flow_id
		self.name = name
		self.apps = apps
		self.ip_addrs = ip_list
		self.ip_props_list = {}
		self.weight = weight
		self.assigned_bw = bw 
		self.true_share = bw 
		self.borrowed_bw = 0
		self.lended_bw = 0 
		self.observed_bw = 0
		self.min = min_
		self.active = False
		self.exhaustive = False
		self.non_exhaustive = False
		self.growing = False
		self.satisfying_bw = 0
		self.previous_committed_assigned_bw = self.assigned_bw
		self.ip_num = ip_num_handle
		self.time_to_realloc_thresh = time_to_realloc_thresh
		self.time_to_realloc = 0
		self.counter = 0

	def setup(self):
		os.system("tc class add dev lan1 parent 1:1 classid 1:%d htb rate %fmbit ceil %fmbit" %(self.id, self.true_share, self.true_share))

	def get_time_to_realloc(self):
		# return self.time_to_realloc_thresh
		self.counter += 1
		if self.counter <= 1:
			return self.time_to_realloc_thresh
		else:
			return 0

			
	def filters_for_ips(self):
		for ip in self.ip_addrs:
			# self.ip_addrs.append(ip)
			ip_props = IpProps(ip, self.ip_num, self.id)
			self.ip_props_list[ip] = ip_props
			print("IP %s added with handle %d" %(ip, ip_props.ip_handle))
			os.system("tc filter add dev lan1 parent 1: handle 800::%d protocol ip prio 10 u32 match ip dst %s flowid 1:%d" %(ip_props.ip_handle, ip, self.id))


	def set_bandwidth(self, bw):
		assert(bw+0.01 >= self.true_share)
		self.assigned_bw = bw
		print("Resetting flow %d's bandwidth to %f" %(self.id, bw))
		os.system("tc class change dev lan1 parent 1:1 classid 1:%d htb rate %fmbit ceil %fmbit" %(self.id, self.assigned_bw, self.assigned_bw))

	def add_ip_to_flow(self, ip):
		print("Adding to flow %d the IP %s" %(self.id, ip))
		if ip not in self.ip_addrs:
			self.ip_addrs.append(ip)
			ip_props = IpProps(ip, self.ip_num, self.id)
			self.ip_props_list[ip] = ip_props
			print("IP %s added with handle %d" %(ip, ip_props.ip_handle))
			os.system("tc filter add dev lan1 parent 1: handle 800::%d protocol ip prio 10 u32 match ip dst %s flowid 1:%d" %(ip_props.ip_handle, ip, self.id))

	def remove_ip_from_flow(self, ip):
		print("Removing from flow %d the IP %s" %(self.id, ip))
		if ip in self.ip_addrs:
			self.ip_addrs.remove(ip)
			os.system("tc filter del dev lan1 parent 1: handle 800::%d prio 10 protocol ip u32" %(self.ip_props_list[ip].ip_handle))
			self.ip_num.return_num(self.ip_props_list[ip].ip_handle)
			del self.ip_props_list[ip]

	def add_port_to_flow(self, port):
		print("Adding to flow %d the port %d" %(self.id, port))
		if port not in self.ip_addrs:
			self.ip_addrs.append(port)
			ip_props = IpProps(port, self.ip_num, self.id)
			self.ip_props_list[port] = ip_props
			print("Port %d added with handle %d" %(port, ip_props.ip_handle))
			os.system("tc filter add dev lan1 parent 1: handle 801::%d protocol ip prio 9 u32 match ip dport %d 0xffff flowid 1:%d" %(ip_props.ip_handle, port, self.id))

	def remove_port_from_flow(self, port):
		print("Removing from flow %d the port %d" %(self.id, port))
		if port in self.ip_addrs:
			self.ip_addrs.remove(port)
			os.system("tc filter del dev lan1 parent 1: handle 801::%d prio 9 protocol ip u32" %(self.ip_props_list[port].ip_handle))
			self.ip_num.return_num(self.ip_props_list[port].ip_handle)
			del self.ip_props_list[port]
