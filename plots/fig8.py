from functions import *

path = 'data/2flows/bwprobe/'
flow_idfrs = ['.100.https > crab']
td = 50
bws = [30,30,10,10,30,30]
tdif = -1
bwt = [0,95+tdif,95+tdif,125+tdif,125+tdif, 180]
flows = parse_log(path+'ifb0.txt', flow_idfrs, bg=True)
cum_flows, tm, mbps,_ = cummulate(flows)
pts = [(0,-3, "f1:0 to $10$"), (30,-6, "f2:0 to $\infty$"), (60,-3, "f1:10 to $\infty$"), (150,-6, "f1:$\infty$ to 0")]

labels = ["f1", "f2", "Throughput"]
lines = ["-", "-", "--"]
plot3(cum_flows, tm, mbps, bws, bwt, [], [], fname="2f_all.pdf", texts=pts, labels=labels, lines=lines, yheight=(-7,43), trange=(0,170))