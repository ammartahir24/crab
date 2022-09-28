import time
import subprocess
import os

logfile = open("ifb0.txt", "w")
tcpdump = subprocess.Popen(["sudo", "tcpdump", "-i", "ifb0"], shell=False, stdout=logfile, preexec_fn=os.setsid)
bulk1 = subprocess.Popen(["wget", "https://releases.ubuntu.com/20.04/ubuntu-20.04.4-desktop-amd64.iso"], shell=False, stdout=subprocess.DEVNULL)
time.sleep(30)
bulk2 = subprocess.Popen(["wget", "https://cdimage.kali.org/kali-2021.3/kali-linux-2021.3a-installer-amd64.iso"], shell=False, stdout=subprocess.DEVNULL)
time.sleep(30)
bulk3 = subprocess.Popen(["wget", "http://mirrors.advancedhosters.com/archlinux/iso/2022.04.05/archlinux-2022.04.05-x86_64.iso"], shell=False, stdout=subprocess.DEVNULL)
time.sleep(30)
bulk4 = subprocess.Popen(["wget", "http://mirrors.aggregate.org/archlinux/iso/2022.04.05/archlinux-2022.04.05-x86_64.iso"], shell=False, stdout=subprocess.DEVNULL)
time.sleep(65)


bulk1.terminate()
bulk2.terminate()
bulk3.terminate()
bulk4.terminate()
print("Bulks flows terminated")
logfile.close()
print("Files saved.")
os.system("sudo kill -9 %s" %(tcpdump.pid))

def get_pid(name):
	try:
		output = subprocess.check_output(["pidof", name])
		return list(map(int, output.split()))
	except:
		return []
tcpdump_pids = get_pid("tcpdump")
for pid in tcpdump_pids:
	os.system("sudo kill -9 %s" %(pid))