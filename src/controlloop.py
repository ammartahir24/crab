import os
import numpy as np
import time
import random
import math
# from config import rates
from capture import TrafficAnalyzer
from flow import Flow


'''
Responsible for configuring rates of the flows
Keeps track of throughput/demand changes, calculates weighted fair shares and enforces them.
Also responsible for probing bandwidth
'''
class TrafficShapper:
	def __init__(self, flows, traffic_analyzer, max_bw=30):
		# optimise for utilisation
		self.THRESH_FOR_EXHAUST = 0.1 # multiplier to cushion decision of labeling a flow as exhaustive
		self.THRESH_FOR_BW_FLUCT_DOWN = 1.1  # multiplier to cushion decision of scaling down self.max_bw
		self.THRESH_FOR_BW_FLUCT_UP = 1.1  # multiplier to cushion decision of scaling up self.max_bw
		self.td = 0.2 # observation period t
		self.n_obsv = 5 # number of observations n
		self.excess = 0
		self.min_bw = 0.25
		self.obsv_period = self.td*(self.n_obsv + 0)
		self.skip_low = True
		self.state_cache = []
		self.flows = flows
		self.default_rule = None
		self.max_bw = max_bw
		self.observed_bw = 0
		self.observed_bws = [0, 0, 0]
		self.min = 1
		self.rounds_since_bw_probe = 0
		self.bw_probe_freq = 0
		self.increment = 0.125
		self.traffic_analyzer = traffic_analyzer
		self.traffic_analyzer.td = self.td
		self.fast_queue_observed_bw = 0
		self.did_reallocation = True
		self.log_file = "log.txt"
		self.inc_flow_i = 0
		file = open(self.log_file, "w")
		file.write('%f' %(time.time()),)
		file.close()
		for f in self.flows:
			if f.name == "default":
				self.default_rule = f
		self.install_base_rules()
		while True:
			self.get_observations()
			self.bw_probe()
			self.reallocate()


	def install_base_rules(self):
		os.system("sudo tc qdisc del dev ifb0 root")
		os.system("sudo tc qdisc add dev ifb0 root handle 1: htb default 1 r2q 83")
		os.system("sudo tc class add dev ifb0 parent 1: classid 1:1 htb rate %dmbit ceil %dmbit quantum 1500 burst 0" %(self.max_bw, self.max_bw))
		# self.default_rule.setup()
		for f in self.flows:
			# if f.ip_addrs!="*":
			f.setup()
			f.filters_for_ips()
				

	def print_flows(self):
		file = open(self.log_file, "a")
		print("#######################################")
		print("Estimated BW: %f, max_bw: %f\n" %(self.observed_bw, self.max_bw))
		file.write("*\n")
		file.write("%f: %f: %f\n" %(time.time(), self.observed_bw, self.max_bw))
		print("fast_queue_observed_bw: %f" %(self.fast_queue_observed_bw))
		for f in self.flows:
			print("flow_name: %s, assigned_bw: %f, true_bw: %f, lended_bw: %f,  borrowed_bw: %f, observed_bw:%f, active:%d, exhaustive: %d, non_exhaustive: %d, growing:%d" %(f.name, f.assigned_bw, f.true_share, f.lended_bw, f.borrowed_bw, f.observed_bw, f.active, f.exhaustive, f.non_exhaustive, f.growing))
			file.write("flow_name: %s, flow id: %d, assigned_bw: %f, true_share: %f, lended_bw: %f,  borrowed_bw: %f, observed_bw:%f, active:%d, exhaustive: %d, non_exhaustive: %d, growing:%d\n" %(f.name, f.id, f.assigned_bw, f.true_share, f.lended_bw, f.borrowed_bw, f.observed_bw, f.active, f.exhaustive, f.non_exhaustive, f.growing))
		file.close()

	def get_observations(self, n=-1):
		if n == -1:
			n = self.n_obsv
		for flow in self.flows:
			flow.observed_bws = []
		fast_queue_observed_bws = []
		for i in range(n):
			time.sleep(self.td)
			main_traffic = []
			for flow in self.flows:
				last_n_readings = self.traffic_analyzer.last_readings_flow(flow.ip_addrs, n=i+1)
				flow.observed_bws = [(8*ni/(10**6))/self.td for ni in last_n_readings]
				flow.observed_bw = max(flow.observed_bws)
				flow.active = flow.observed_bw > 0
				flow.delta = max(self.THRESH_FOR_EXHAUST * flow.observed_bw, self.min_bw)
				flow.growing = (flow.lended_bw > 0) and (flow.observed_bw >= (flow.assigned_bw - flow.lended_bw))
				flow.exhaustive =  flow.growing or (flow.observed_bw + flow.delta >= flow.assigned_bw)
				flow.non_exhaustive = flow.observed_bw + flow.delta < flow.assigned_bw - flow.lended_bw
				if flow.exhaustive and flow.time_to_realloc <= 0:
					flow.time_to_realloc = flow.get_time_to_realloc()
				main_traffic += flow.ip_addrs
			# for default/background traffic
			last_n_readings = self.traffic_analyzer.last_readings_flow("*", main_traffic=main_traffic, n=1+i)
			fast_queue_observed_bws = [(8*ni/(10**6))/self.td for ni in last_n_readings]
			self.fast_queue_observed_bw = max(fast_queue_observed_bws)
			any_growing = sum([f.growing for f in self.flows])
			if any_growing:
				break
		observed_bws = fast_queue_observed_bws
		observed_bw = self.fast_queue_observed_bw
		for f in self.flows:
			observed_bw += f.observed_bw
			observed_bws = [observed_bws[i]+f.observed_bws[i] for i in range(len(f.observed_bws))]
		# self.observed_bw = observed_bw
		try:
			self.observed_bw = sorted(observed_bws)[4]
		except:
			self.observed_bw = max(observed_bws)
		# self.observed_bw = max(observed_bws)
		self.observed_bws = observed_bws
		# self.observed_bw = observed_bw
		return observed_bw

	def pick_flow_to_increment(self):
		for i in range(len(self.flows)):
			if self.flows[self.inc_flow_i].exhaustive:
				return self.flows[self.inc_flow_i]
			else:
				self.inc_flow_i = (self.inc_flow_i + 1) % len(self.flows)

	def bw_probe(self):
		print("bw_probe")
		self.print_flows()
		any_growing = sum([f.growing for f in self.flows])
		any_exhaustive = sum([f.exhaustive for f in self.flows])
		any_non_exhaustive = sum([f.non_exhaustive for f in self.flows])
		any_active = sum([f.active for f in self.flows])
		if any_growing:
			self.skip_low = 0
			return
		if self.observed_bw * self.THRESH_FOR_BW_FLUCT_DOWN < self.max_bw and any_active > 1:
			if self.skip_low <= 0:
				self.skip_low += 1
				# self.get_observations()
				return
			elif self.skip_low > 0 and not self.did_reallocation:
				print("Bandwidth Decreased.")
				self.max_bw = self.observed_bw
				self.excess = 0
				weight_sum = sum([f.weight for f in self.flows])
				for flow in self.flows:
					prev_assigned_bw = flow.assigned_bw
					flow.assigned_bw = self.max_bw * flow.weight / weight_sum
					flow.true_share = flow.assigned_bw
					flow.lended_bw = 0
					flow.borrowed_bw = 0
				self.redivide_excess()
				self.commit_assigned_bws()
				self.get_observations(n=5)
				self.skip_low = 0
				self.increment = 0.125
				return
		self.skip_low = 0
		if any_exhaustive:
			self.rounds_since_bw_probe = 0
			while True:
				flow_to_increment = self.pick_flow_to_increment()
				if flow_to_increment == None:
					break
				bw_increment = max(self.increment*self.max_bw, 1)
				flow_to_increment.set_bandwidth(flow_to_increment.assigned_bw + bw_increment)
				self.get_observations(n=5)
				self.print_flows()
				any_non_exhaustive = sum([f.non_exhaustive for f in self.flows])
				any_growing = sum([f.growing for f in self.flows])
				if any_growing:
					flow_to_increment.set_bandwidth(flow_to_increment.assigned_bw - bw_increment)
					return
				observed_bw = self.observed_bw
				print(self.observed_bws, observed_bw)
				if (observed_bw > self.THRESH_FOR_BW_FLUCT_UP * self.max_bw) or (observed_bw - self.max_bw) > 1:
					print("Bandwidth Increased.")
					self.max_bw = observed_bw
					self.excess = 0
					flow_to_increment.assigned_bw -= bw_increment
					weight_sum = sum([f.weight for f in self.flows])
					for flow in self.flows:
						prev_assigned_bw = flow.assigned_bw
						flow.assigned_bw = self.max_bw * flow.weight / weight_sum
						flow.true_share = flow.assigned_bw
						if flow.lended_bw > 0.01:
							flow.lended_bw += (flow.assigned_bw - prev_assigned_bw)
							self.excess += flow.lended_bw
						else:
							flow.lended_bw = 0
						flow.borrowed_bw = 0
					self.redivide_excess()
					self.commit_assigned_bws()
					self.increment *= 4
				else:
					flow_to_increment.set_bandwidth(flow_to_increment.assigned_bw - bw_increment)
					self.increment = 0.125
					self.inc_flow_i = (self.inc_flow_i + 1) % len(self.flows)
					break
			self.get_observations()

	def reallocate(self):
		print("reallocate")
		self.print_flows()
		self.did_reallocation = False
		any_active = sum([f.active for f in self.flows])
		any_growing = sum([f.growing for f in self.flows])
		any_exhaustive = sum([f.exhaustive for f in self.flows])
		any_non_exhaustive = sum([f.non_exhaustive for f in self.flows])
		if self.observed_bw * self.THRESH_FOR_BW_FLUCT_DOWN > self.max_bw or any_active < 1:
			self.skip_low = 0
		if any_growing:
			print("Reclaiming!")
			for flow in self.flows:
				if flow.growing:
					if flow.lended_bw - flow.borrowed_bw > 0:
						self.excess -= (flow.lended_bw - flow.borrowed_bw)
					flow.lended_bw = 0
			self.redivide_excess()
		elif any_exhaustive and any_non_exhaustive:
			print("Reallocating")
			for flow in self.flows:
				if flow.non_exhaustive:
					prev_lended = flow.lended_bw
					flow.lended_bw = flow.assigned_bw - flow.observed_bw - self.min_bw
					if flow.lended_bw > flow.borrowed_bw:
						self.excess += (flow.lended_bw - max(0, prev_lended - flow.borrowed_bw) - flow.borrowed_bw)
						flow.lended_bw -= flow.borrowed_bw
						flow.borrowed_bw = 0
			self.redivide_excess()
			self.did_reallocation = True
		self.commit_assigned_bws()

	def redivide_excess(self):
		for flow in self.flows:
			if flow.lended_bw > 0:
				flow.satisfying_bw = flow.true_share + flow.borrowed_bw - flow.lended_bw
			else:
				flow.satisfying_bw = math.inf
			flow.assigned_bw = flow.true_share
			if flow.satisfying_bw > flow.assigned_bw:
				flow.lended_bw = 0
				flow.borrowed_bw = 0
		excess = self.excess
		print(excess)
		while excess >= 0.01:
			residual_excess = 0
			weight_sum = sum([flow.weight for flow in self.flows if flow.satisfying_bw > flow.assigned_bw])
			for flow in self.flows:
				if flow.satisfying_bw > flow.assigned_bw:
					flow.assigned_bw += excess * (flow.weight / weight_sum)
					flow.borrowed_bw += excess * (flow.weight / weight_sum)
					if flow.assigned_bw > flow.satisfying_bw:
						residual_excess += (flow.assigned_bw - flow.satisfying_bw)
						flow.lended_bw += (flow.assigned_bw - flow.satisfying_bw)
			excess = residual_excess

	def commit_assigned_bws(self):
		for flow in self.flows:
			if flow.previous_committed_assigned_bw != flow.assigned_bw:
				flow.set_bandwidth(flow.assigned_bw)
				flow.previous_committed_assigned_bw = flow.assigned_bw
		