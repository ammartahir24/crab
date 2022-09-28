import numpy as np
from selenium import webdriver
import time
from dataset import browsing_data
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import json
import threading
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import re

hyperlink = "https://bbc.com"

options = webdriver.ChromeOptions()
options.add_argument("--incognito")


INTERVAL_TIME = 60
INTERSESSION_TIME = 5

# should we make INTERSESSION_TIME a function of pagesize?
def read_dataset(browsing_data):
	return browsing_data.keys(), browsing_data

def write_results(results):
	file = open('plt.txt', 'w')
	file.write(str(results))
	file.close()

def random_time(mean):
	return np.random.poisson(mean)


def browse(driver, webpage):
	try:
		driver.get(webpage)
		loadEnd = driver.execute_script("return window.performance.timing.loadEventEnd")
		while loadEnd <=0:
			time.sleep(1)
			loadEnd = driver.execute_script("return window.performance.timing.loadEventEnd")

		navStart = driver.execute_script("return window.performance.timing.navigationStart")
		resStart = driver.execute_script("return window.performance.timing.responseStart")
		total_bytes = []
		# logs = driver.execute('getLog', {'type': 'performance'})['values']
		# print(logs)
		for entry in driver.get_log('performance'):
			if "Network.dataReceived" in str(entry):
				r = re.search(r'encodedDataLength\":(.*?),', str(entry))
				total_bytes.append(int(r.group(1)))
				size = sum(total_bytes)
		# print("Page size:", size)

		return loadEnd - navStart, size
	except:
		return browse(driver, webpage)

def run_session(webpage_list):
	options = webdriver.ChromeOptions()
	# options.add_argument("--incognito")
	logging_prefs = {'performance': 'INFO'}
	caps = DesiredCapabilities.CHROME.copy()
	caps.update({'goog:loggingPrefs': {'performance': 'INFO'}, 'detach': False})
	options.add_argument("load-extension=../chrome_extension")
	driver = webdriver.Chrome(desired_capabilities=caps, chrome_options=options,executable_path="../chromedriver")
	plts = []
	for web in webpage_list:
		plt = browse(driver, web)
		plts.append(plt)
		time.sleep(random_time(INTERSESSION_TIME))
	driver.quit()
	return plts

def run_experiment():
	data, webpages = read_dataset(browsing_data)
	rslts = []
	for w in data:
		for i in range(5):
			plts = run_session(webpages[w])
			print(w, plts)
			rslts.append((w,plts))
		if list(data)[-1] != w:
			time.sleep(random_time(INTERVAL_TIME))
	write_results(rslts)
	print("Experiment completed.")

run_experiment()

