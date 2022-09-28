from functions import *

path = 'data/4kvideo/vidalone/4k/'
flow_idfrs = []
td = 50
for i in range(1):
  p = path+str(i+1)+"/"
  flows = parse_log(p+'ifb0.txt', flow_idfrs, bg=True)
  quality, rebuf, end_ts = vlog2(p+'vlog.txt')
  cum_flows, tm, mbps,_ = cummulate(flows)
  plot2(cum_flows, tm, mbps, quality, rebuf, -0.1, smooth=10, fname="vidalone.pdf", yheight=40, trange=(0,141))
  print(i)
  # plot3(cum_flows, tm, mbps, [], [], [], [], fname="vid_base_%d.png" %(i+1), trange=-1)