from functions import *

path = 'data/4flows/crab/1/'
flow_idfrs = ['canonical.com.https > crab-VirtualBox', '.100.https > crab', 'edge.kernel.org.http > crab', 'mirrors.mit.edu.http > crab']
# flow_idfrs = ['mirrors.mit.edu.http > crab', 'edge.kernel.org.http > crab', '.100.https > crab', 'canonical.com.https > crab-VirtualBox']
td = 50
pts = [(0,-3, "f1:0 to $\infty$"), (30,-6, "f2:0 to $\infty$"), (60,-3, "f3:0 to $\infty$"), (90,-6, "f4:0 to $\infty$"), (125,-3, "f4:$\infty$ to 0"), (155,-6, "f3:$\infty$ to 10.5"), (185,-3, "f2:$\infty$ to 10.5")]
for i in range(1):
  p = path#+str(i+1)+"/"
  flows = parse_log(p+'ifb0.txt', flow_idfrs, bg=False)
  # quality, rebuf, end_ts = vlog2(path+'vlog.txt')
  cum_flows, tm, mbps,_ = cummulate(flows)
  # texts = [(30,20,"* flow 3 starts"), (60,15,"* flow 2 starts"), (90,12,"* flow 1 starts"), (125,14,"* flow 1 drops to 0 Mbps"), (155,12,"* flow 2 drops to 10.5 Mbps"), (185,14,"*flow 3 drops to 0 Mbps")]
  plot3(cum_flows, tm, mbps, [30,30], [0,220], [], [], fname="4f_crab.pdf", yheight=(-7,43), texts=pts, trange=(0,220))