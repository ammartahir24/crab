from functions import *

path = 'data/robustness_analysis/'
flow_idfrs = ['.3001 > crab', '.3002 > crab', '.3003 > crab', '.3004 > crab', '.3005 > crab', '.3006 > crab', '.3007 > crab', '.3008 > crab', '.3009 > crab', '.3010 > crab', '.3011 > crab', '.3012 > crab', '.3013 > crab', '.3014 > crab', '.3015 > crab', '.3016 > crab', '.3017 > crab', '.3018 > crab', '.3019 > crab', '.3020 > crab', '.3021 > crab', '.3022 > crab', '.3023 > crab', '.3024 > crab']
exps = ["3flows/", "6flows/", "12flows/", "24flows/"]
exp_names = ["3 flows", "6 flows", "12 flows", "24 flows"]
fid = [3, 6, 12, 24]
# flow_idfrs = ['mirrors.mit.edu.http > crab', 'edge.kernel.org.http > crab', '.100.https > crab', 'canonical.com.https > crab-VirtualBox']
td = 50
flows_2 = []

for i in range(len(exps)):
  p = path+exps[i]
  flows = parse_log(p+'ifb0.txt', flow_idfrs[0:fid[i]], bg=False)
  # quality, rebuf, end_ts = vlog2(path+'vlog.txt')
  cum_flows, tm, mbps,_ = cummulate(flows)
  fd = flow_download(cum_flows)
  fd2 = []
  fd2 += [fd[j]/sum(fd) for j in range(len(fd)) if j%3==0]
  fd2 += [fd[j]/sum(fd) for j in range(len(fd)) if j%3==1]
  fd2 += [fd[j]/sum(fd) for j in range(len(fd)) if j%3==2]
  flows_2.append(fd2)
  # texts = [(30,20,"* flow 3 starts"), (60,15,"* flow 2 starts"), (90,12,"* flow 1 starts"), (125,14,"* flow 1 drops to 0 Mbps"), (155,12,"* flow 2 drops to 10.5 Mbps"), (185,14,"*flow 3 drops to 0 Mbps")]
  # plot3(cum_flows, tm, mbps, [30,30], [0,220], [], [], fname="4f_non_sat_bwprobe.pdf", yheight=(-7,43), texts=[], trange=(0,95))}
print(flows_2)
# video, bulks = [2071.4478809999796, 218.57516199999915, 2626.7805910000334], [2394.8471479415894, 5176.89426612854, 2751.7163410186768]
plt.figure(figsize=(5,4))
width = 0.3
pos = 0.45
for fl in flows_2:
  sum_fl = 0
  print(fl)
  for i in range(len(fl)):
    if i>=(len(fl)/3) and i<2*(len(fl)/3):
      plt.bar(pos, fl[i], bottom=sum_fl, width=0.3, label="flow 2", color="navy")
    elif i>= 2*(len(fl)/3):
      plt.bar(pos, fl[i], bottom=sum_fl, width=0.3, label="flow 2", color="royalblue")
    else:
      plt.bar(pos, fl[i], bottom=sum_fl, width=0.3, label="flow 2", color="gray")
    sum_fl+=fl[i]
  pos+=0.6
# x1,x2,y1,y2 = plt.axis()
# plt.axis([x1,x2,y1,y2])
plt.ylabel("%age of downloaded data")
plt.xlabel("Number of CRAB flow groups")
plt.xticks([0.45, 1.05, 1.65, 2.25], ["3 flows", "6 flows", "12 flows", "24 flows"])
# plt.legend()
plt.savefig("multipleflows.pdf", bbox_inches="tight")