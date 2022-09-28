import subprocess
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import sys
import os
import json
import signal
import psutil

videos = [
	'xcJtL7QggTI',
    'fLJUx1XrGFI',
    '7ePaVk7TKGM',
    '8xzJjqpa-RQ',
    '1J5swK2FGB0',
    'vOQVBbGStGQ',
    'tJVHr8HsejQ'
]
    # 'Hx5_P1MIwJk'

video_res_h = 2160
video_res_w = 3544


def play_video(video):
	process = subprocess.Popen(["google-chrome", "--incognito", "--disable-web-security", "file:///home/crab/crab/exps/video.html#%s" %(video)])
	return process

def run_tcpdump():
	global logfile
	logfile = open("ifb0.txt", "w")
	process = subprocess.Popen(["sudo", "tcpdump", "-i", "ifb0"], shell=False, stdout=logfile, preexec_fn=os.setsid)
	return process

def start_bulk():
	process = subprocess.Popen(["wget", "https://releases.ubuntu.com/20.04/ubuntu-20.04.5-desktop-amd64.iso"], shell=False, stdout=subprocess.DEVNULL)
	return process

def copy_results(i):
	os.mkdir("4k/%d" %(i))
	os.system("mv ifb0.txt 4k/%d/ifb0.txt" %(i))
	os.system("mv vlog.txt 4k/%d/vlog.txt" %(i))
	os.system("rm ubuntu-20.04.3-desktop-amd64.iso*")


def get_pid(name):
	try:
		output = subprocess.check_output(["pidof", name])
		return list(map(int, output.split()))
	except:
		return []

def kill_tcpdump():
	tcpdump_pids = get_pid("tcpdump")
	for pid in tcpdump_pids:
		os.system("sudo kill -9 %s" %(pid))


def handle_data(data):
	# data = data.split("\n")
	print(data)
	global tcpdump, bulk1, bulk2, video, i, sem, logfile
	file = open("vlog.txt", "w")
	file.write(data)
	file.close()
	logfile.close()
	print("Files saved.")
	video.terminate()
	print("video killed.")
	bulk1.terminate()
	print("bulk1 killed.")
	bulk2.terminate()
	print("bulk2 killed.")
	# tcpdump.terminate()
	print(tcpdump.pid)
	os.system("sudo kill -9 %s" %(tcpdump.pid))
	# os.killpg(os.getpgid(tcpdump.pid), signal.SIGKILL)
	kill_tcpdump()
	print("tcpdump killed.")
	copy_results(i)
	print("Files copied.")
	sem.release()

class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def _html(self, message):
		"""This just generates an HTML document that includes `message`
		in the body. Override, or re-write this do do more interesting stuff.
		"""
		content = f"<html><body><h1>{message}</h1></body></html>"
		return content.encode("utf8")  # NOTE: must return a bytes object!

	def do_GET(self):
		self._set_headers()
		self.wfile.write(self._html("hi!"))

	def do_HEAD(self):
		self._set_headers()

	def do_POST(self):
		# Doesn't do anything with posted data
		content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
		post_data = self.rfile.read(content_length).decode('utf8').replace("'", '"') # <--- Gets the data itself
		try:
			post_data = json.loads(post_data)
			handle_data(post_data)
			self._set_headers()
		except:
			self._set_headers()

def run_server(server_class=HTTPServer, handler_class=S, addr="127.0.0.1", port=8888):
	server_address = (addr, port)
	httpd = server_class(server_address, handler_class)

	print(f"Starting httpd server on {addr}:{port}")
	httpd.serve_forever()


tcpdump, bulk1, bulk2, video = None, None, None, None
i = 0
sem = threading.Semaphore()
logfile = None

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
# run_server()

sem.acquire()
os.mkdir("4k")
for video in videos:
	tcpdump = run_tcpdump()
	bulk1 = start_bulk()
	time.sleep(2)
	bulk2 = start_bulk()
	time.sleep(5)
	video = play_video(video)
	i += 1
	sem.release()
	sem.acquire()
	sem.acquire()

sem.release()
sys.exit()