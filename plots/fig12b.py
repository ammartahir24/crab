from functions import *

flow_idfrs = ['canonical.com.https > crab-VirtualBox']
# flow_idfrs = ['kazooie.canonical.com.https > crab.', 'https-services.banjo.canonical.com.https > crab']
path = 'data/router/crab/'
td = 50
bwt = [0,114]
bws = [30,30]
flows = parse_log(path+'ifb0.txt', flow_idfrs, bg=True)
flows2 = parse_log(path+'ifb1.txt', [], bg=True)
# quality, rebuf, end_ts = vlog2(path+'vlog.txt', diff=5)
cum_flows, tm, mbps,_ = cummulate(flows+flows2)
# tm_e, bw_e, _ = parse_crab_log_get_max_bw(path+"log.txt", td = 8)
labels = ["flow 1", "flow 2", "Traffic from other device"]
lines = ["-", "-", "--"]
plot3(cum_flows, tm, mbps, bws, bwt, [], [], fname="routercrab.pdf", labels=labels, lines=lines, yheight=(0,43), trange=(0,114))
