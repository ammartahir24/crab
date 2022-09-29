from functions import *

path = 'data/robustness_analysis/'
flow_idfrs = ['.3001 > crab-VirtualBox', '.3002 > crab', '.3003 > crab']
exps = ["cubic_cubic/", "bbr_bbr/", "cubic_bbr/", "bbr_cubic/"]
exp_names = ["Cubic \&\nCubic", "BBR \&\nBBR", "Cubic \&\nBBR", "BBR \&\nCubic"]
td = 50
flow1 = []
flow2 = []
for i in range(len(exps)):
  p = path+exps[i]
  flows = parse_log(p+'ifb1.txt', flow_idfrs, bg=False)
  cum_flows, tm, mbps,_ = cummulate(flows)
  fd = flow_download(cum_flows)
  flow1.append(fd[0]/(fd[0]+fd[1]))
  flow2.append(fd[1]/(fd[0]+fd[1]))
  
plt.figure(figsize=(5,4))
plt.bar(exp_names, flow1, width=0.3, label="flow 1", color="navy")
plt.bar(exp_names, flow2, bottom=flow1, width=0.3, label="flow 2", color="royalblue")
x1,x2,y1,y2 = plt.axis()
plt.axis([x1,x2,y1,y2])
plt.ylabel("%age of downloaded data")
plt.legend()
plt.savefig("ccunfairness.pdf", bbox_inches="tight")