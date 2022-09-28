import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json
from config import configurations
from capture import TrafficAnalyzer
from flow import Flow
from controlloop import TrafficShapper
from portMapper import PortMapper
import time



'''
This class is to assign and keep track of IDs assigned to tc filters.

'''
class IpHandleNum:
	def __init__(self, seed = 1):
		self.num = seed
		self.num_used = {}
		self.num_in_use = 0
		for i in range(1000):
			self.num_used[i] = 0

	def get_num(self):
		if self.num_in_use >= 999:
			return -1
		while self.num_used[self.num] == 1 or self.num == 0:
			self.num = (self.num + 1) % 1000
		self.num_used[self.num] = 1
		self.num_in_use += 1
		return self.num

	def return_num(self, num_):
		if self.num_used[num_] != 0:
			self.num_in_use -= 1
			self.num_used[num_] = 0


'''
Crab class spins up all Crab threads and handles coordination between them.

Particularly, it reads and translates the config file, spins up traffic analyzer for throughput measurements, starts traffic shapper thread, spins up a thread to listen to browser messages. This thread is responsible for installing appropriate tc filters.

Input: configurations object defined in config file

'''
class Crab:
	def __init__(self, configurations):
		self.web_pages = {}
		self.active_tab_id = -1
		self.configurations = configurations
		self.td = 0.1
		self.ip_handle_num = IpHandleNum(seed = 800)
		self.max_bw = configurations["bw_estimate"]
		self.fname = "requests_log.txt"
		file = open(self.fname, "w")
		file.write("\n")
		file.close()
		self.default_rule = None
		self.flows = self.translate_configs()
		self.hp_browser_flow = self.flows[0]
		self.traffic_analyzer = TrafficAnalyzer(td = self.td, new_flow_handle=self.new_flow_handle)
		self.port_mapper = PortMapper()
		threading.Thread(target=TrafficShapper, args=(self.flows, self.traffic_analyzer, self.max_bw)).start()


	def translate_configs(self):
		rates = []
		for k,fg in self.configurations["flow_groups"].items():
			if (self.configurations["browser_active_window_prioritization"] and k == "active_window") or k!="active_window":
				srcs = fg["apps"]
				ip_srcs = [f for f in srcs if "ip>>" in f]
				ip_srcs = [f.split(">>")[1] for f in ip_srcs]
				weight = fg["weight"]
				rates.append([ip_srcs, weight, k, srcs])
		sorted(rates, key=lambda x:x[1])
		weight_sum = sum([x[1] for x in rates])
		flows = []
		mark = 10
		for f in rates:
			if f[2] == 'default':
				fl = Flow(10, f[0], f[1], self.ip_handle_num, bw=self.max_bw*f[1]/weight_sum, name=f[2], apps=f[3])
				flows.append(fl)
				self.default_rule = fl
				continue
			mark += 1
			fl = Flow(mark, f[0], f[1], self.ip_handle_num, bw=self.max_bw*f[1]/weight_sum, name=f[2], apps=f[3])
			flows.append(fl)
		return flows
	
	'''
	callback from traffic analyzer when a packet from unknown flow is encountered
	'''
	def new_flow_handle(self, ip, port):
		# if ip already part of a flow, rule already installed
		for flow in self.flows:
			if ip in flow.ip_addrs:
				print("PORTMAPPER: Flow installed already.")
				return
		# check flow's application from port and classify if not chrome
		app = self.port_mapper.get_pname_from_dest_port(port)
		if app == None:
			print("PORTMAPPER: None")
			self.default_rule.add_ip_to_flow(ip)
			return
		if app != "chrome":
			for flow in self.flows:
				if "app>>"+app in flow.apps:
					print("PORTMAPPER: New app flow %s for flow %s" %(app, flow.name))
					flow.add_ip_to_flow(ip)
					return
			self.default_rule.add_ip_to_flow(ip)
			return
		# if chrome flow, wait until chrome sends message
		print("PORTMAPPER: Browser flow")

	def log_request(self, to_write):
		file = open(self.fname, "a")
		file.write(to_write)
		file.write("\n")
		file.close()

	def curate_url(self, url):
		return url.replace("https://","").replace("www.","").replace("http://","").split("/")[0]

	'''
	callback for when a message from browser is received.
	data is a dictionary containing contents of message.
	'''
	def browser_message(self, data):
		if data['type'] == 'new_request':
			if data["tab"] > 0:
				if data["tab"] in self.web_pages:
					try:
						domain = self.curate_url(data["initiator"])
						self.log_request("Initiator: %s" %(domain))
						if data["ip"] not in self.web_pages[data["tab"]]["ip_list"]:
							self.web_pages[data["tab"]]["ip_list"].append(data["ip"])
							self.web_pages[data["tab"]]["flow"].add_ip_to_flow(data["ip"])
							self.log_request("New-IP, %s, %s, %d, %d" %(domain, data["ip"], data["tab"], data["size"]))
							# install rule for data["ip"]
						else:
							self.log_request("Hit, %s, %s, %d, %d" %(domain, data["ip"], data["tab"], data["size"]))
					except:
						domain = self.curate_url(data['url'])
						# URL of page changed
						self.log_request("URL: %s" %(domain))
						if self.web_pages[data["tab"]]["domain"] != domain:
							print("New Request at tab", data["tab"], ":", domain, data["ip"])
							self.log_request("URL-Changed, %s, %s, %d, %d" %(domain, data["ip"], data["tab"], data["size"]))
							self.print_webpages()
							this_flow = None
							for fl in self.flows:
								if "gc>>"+domain in fl.apps:
									this_flow = fl
									break
							if this_flow == None:
								# put in explicit default queue
								this_flow = self.default_rule
								# return
							# flush previous rules (FIX: not all rules though?)
							for ip in self.web_pages[data["tab"]]["ip_list"]:
								self.web_pages[data["tab"]]["flow"].remove_ip_from_flow(ip)
							self.web_pages[data["tab"]] = {
								"domain": domain,
								"ip_list": [data["ip"]],
								"flow": this_flow
							}
							this_flow.add_ip_to_flow(data["ip"])
							self.print_webpages()
							# install rule for data["ip"]
					# else:
				else:
					this_flow = None
					try:
						domain = self.curate_url(data["initiator"])
					except:
						domain = self.curate_url(data['url'])
					for fl in self.flows:
						if "gc>>"+domain in fl.apps:
							this_flow = fl
							break
					if this_flow == None:
						this_flow = self.default_rule
					self.web_pages[data["tab"]] = {
						"domain": domain,
						"ip_list": [data["ip"]],
						"flow": this_flow
					}
					this_flow.add_ip_to_flow(data["ip"])
					self.log_request("New-IP, %s, %s, %d, %d" %(domain, data["ip"], data["tab"], data["size"]))
					# install rule for data["ip"]
				if self.active_tab_id == -1:
					self.handle_active_tab_change(data["tab"])
			else:
				print("Missed me", data)
		if data['type'] == 'active_view_change':
			# print("Active View Changed", data["tab"], ":", data['url'])
			self.handle_active_tab_change(data["tab"])
			self.print_webpages()
		if data['type'] == 'url_change':
			self.log_request(" Actual URL Changed %d: %s" %(data["tab"], data['url']))
			return
		if data['type'] == 'tab_closed':
			self.print_webpages()
			# print("Tab Closed", data["tab"])
			self.handle_tab_close(data["tab"])
			self.print_webpages()
	
	def handle_active_tab_change(self, tab):
		prev_active_tab = self.active_tab_id
		self.active_tab_id = tab
		# propagate changes to rule installer

	def handle_tab_close(self, tab):
		# find the list of IP addresses to remove from rules
		if tab not in self.web_pages:
			return
		for ip in self.web_pages[tab]["ip_list"]:
			self.web_pages[tab]["flow"].remove_ip_from_flow(ip)
		del self.web_pages[tab]

	def print_webpages(self):
		# for k,v in self.web_pages.items():
		# 	print("------", k, "------")
		# 	if self.active_tab_id == k:
		# 		print("*****Active Tab******")
		# 	print("Domain:", v["domain"])
		# 	for ip in v["ip_list"]:
		# 		print(ip)
		# 	print("---------------------")
		return

crab = Crab(configurations)

'''
A simple HTTP server to listen to browser messages
'''
class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def _html(self, message):
		content = f"<html><body><h1>{message}</h1></body></html>"
		return content.encode("utf8")  # NOTE: must return a bytes object!

	def do_GET(self):
		self._set_headers()
		self.wfile.write(self._html("hi!"))

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		global crab
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length).decode('utf8').replace("'", '"') # <--- Gets the data itself
		try:
			post_data = json.loads(post_data)
			crab.browser_message(post_data)
			self._set_headers()
		except:
			self._set_headers()
		# print(post_data)
		# self.wfile.write("<html><body><h1>POST!</h1></body></html>")


def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8333):
	server_address = (addr, port)
	httpd = server_class(server_address, handler_class)

	print(f"Starting httpd server on {addr}:{port}")
	httpd.serve_forever()


if __name__ == "__main__":

	parser = argparse.ArgumentParser(description="Run a simple HTTP server")
	parser.add_argument(
		"-l",
		"--listen",
		default="127.0.0.1",
		help="Specify the IP address on which the server listens",
	)
	parser.add_argument(
		"-p",
		"--port",
		type=int,
		default=8000,
		help="Specify the port on which the server listens",
	)
	args = parser.parse_args()
	print("listening started")
	run(addr=args.listen, port=args.port)