from functions import *

flow_idfrs = ['canonical.com.https > crab-VirtualBox']
path = 'data/router/nocrab/'
td = 50
bwt = [0,114]
bws = [30,30]
tdif = 3
# bwt = [0,30+tdif,30+tdif,60+tdif,60+tdif,90+tdif,90+tdif,120+tdif,120+tdif,155]
flows = parse_log(path+'ifb0.txt', flow_idfrs, bg=True)
flows2 = parse_log(path+'ifb1.txt', [], bg=True)
# quality, rebuf, end_ts = vlog2(path+'vlog.txt', diff=5)
cum_flows, tm, mbps,_ = cummulate(flows+flows2)
# tm_e, bw_e, _ = parse_crab_log_get_max_bw(path+"log.txt", td = 8)
labels = ["flow 1", "flow 2", "Traffic from other device"]
lines = ["-", "-", "--"]
plot3(cum_flows, tm, mbps, bws, bwt, [], [], fname="woroutercrab.pdf", labels=labels, lines=lines, yheight=(0,43), trange=(0,114))
