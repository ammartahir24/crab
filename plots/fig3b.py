from functions import *

path = 'data/4kvideo/sq/4k/'
flow_idfrs = ['canonical.com.https > crab-VirtualBox']
td = 50
for i in range(6,7):
  p = path+str(i+1)+"/"
  flows = parse_log(p+'ifb0.txt', flow_idfrs, bg=True)
  quality, rebuf, end_ts = vlog2(p+'vlog.txt')
  cum_flows, tm, mbps,_ = cummulate(flows)
  plot2(cum_flows, tm, mbps, quality, rebuf, -0.1, smooth=10, fname="viddef.pdf", yheight=40, trange=(0,141))
  print(i)
  # plot3(cum_flows, tm, mbps, [], [], [], [], fname="vid_base_%d.png" %(i+1), trange=-1)