from functions import *

path = 'data/4flows/non_sat/'
flow_idfrs = ['canonical.com.https > crab-VirtualBox', '.100.https > crab', 'aggregate.org.http > crab', '147.249.http > crab']
td = 50
pts = [(0,-4, "f1: 0 to 10"), (30,-4, "f2, f3, f4: 0 to 10"), (63,-4, "f2, f3, f4: 0 to 10")]#, (90,-6, "f4:0 to $\infty$"), (125,-3, "f4:$\infty$ to 0"), (155,-6, "f3:$\infty$ to 10.5"), (185,-3, "f2:$\infty$ to 10.5")]
for i in range(1):
  p = path#+str(i+1)+"/"
  flows = parse_log(p+'ifb0.txt', flow_idfrs, bg=False)
  cum_flows, tm, mbps,_ = cummulate(flows)
  plot3(cum_flows, tm, mbps, [30,30], [0,220], [], [], fname="4f_non_sat_bwprobe.pdf", yheight=(-7,43), texts=pts, trange=(0,95))