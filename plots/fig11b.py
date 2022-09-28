from functions import *

path = 'data/robustness_analysis/'
flow_idfrs = ['.3001 > crab-VirtualBox', '.3002 > crab', '.3003 > crab']
exps = ["crab/", "statusquo/", "throttle/", "unthrottled/"]
exp_names = ["Original CRAB", "Status Quo", "Throttled to \n25 Mbps &\n WFQ", "Unthrottled &\n WFQ"]
# flow_idfrs = ['mirrors.mit.edu.http > crab', 'edge.kernel.org.http > crab', '.100.https > crab', 'canonical.com.https > crab-VirtualBox']
td = 50
flow1 = []
flow2 = []
flow3 = []
order = [3,2,1,0]
exp_names = [exp_names[i] for i in order]
for i in order:
  p = path+exps[i]
  flows = parse_log(p+'ifb1.txt', flow_idfrs, bg=False)
  # quality, rebuf, end_ts = vlog2(path+'vlog.txt')
  cum_flows, tm, mbps,_ = cummulate(flows)
  fd = flow_download(cum_flows)
  flow1.append(fd[0])
  flow2.append(fd[1])
  flow3.append(fd[2])
  # texts = [(30,20,"* flow 3 starts"), (60,15,"* flow 2 starts"), (90,12,"* flow 1 starts"), (125,14,"* flow 1 drops to 0 Mbps"), (155,12,"* flow 2 drops to 10.5 Mbps"), (185,14,"*flow 3 drops to 0 Mbps")]
  # plot3(cum_flows, tm, mbps, [30,30], [0,220], [], [], fname="4f_non_sat_bwprobe.pdf", yheight=(-7,43), texts=[], trange=(0,95))}

plt.figure(figsize=(5,4))
plt.bar(exp_names, flow1, width=0.3, label="flow 1", color="navy")
plt.bar(exp_names, flow2, bottom=flow1, width=0.3, label="flow 2", color="royalblue")
plt.bar(exp_names, flow3, bottom=[flow1[i]+flow2[i] for i in range(len(flow1))], width=0.3, label="flow 3", color="gray")
x1,x2,y1,y2 = plt.axis()
plt.axis([x1,x2,y1,y2])
plt.ylabel("Downloaded data (MBs)")
plt.legend(loc=3)
plt.savefig("throttle_n_shape.pdf", bbox_inches="tight")