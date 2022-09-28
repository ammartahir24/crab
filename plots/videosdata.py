from functions import *

path_ = 'data/4kvideo/'
# 9 plot data
# labels = ["crab/4k/", "4kweights/1_1/crab/4k/", "4kweights/1_5/crab/4k/", "wfq/4k/", "4kweights/1_1/wfq/4k/", "4kweights/1_5/wfq/4k/", "sq/4k/"]
# 11 plot data
# labels = ["crab_nobwprobe/4k/", "sq/4k/", "prio/unthrottled/4k/", "prio/25mbps/4k/"]
# 13 plot data
# labels = ["crab/4k/", "sens_analysis/0_5nt/4k/", "sens_analysis/3nt/4k/", "htb/4k/"]
# 17 plot data
labels = ["crab/4k/", "sens_analysis/0_5thresh/4k/", "sens_analysis/0_05thresh/4k/"]

flow_idfrs = ['canonical.com.https > crab-VirtualBox']
pe_avg = []
pe_std = []
lu_avg = []
lu_std = []
dls = []
for label in labels:
  path = path_+label
  if label == "paper/4kvideo/crab/4/4k/":
    flow_idfrs = ['.100.https > crab']
  else:
    flow_idfrs = ['canonical.com.https > crab-VirtualBox']
  print(label)
  vq = []
  util = []
  dl = []
  for i in range(1,7):
    try:
      p = path+str(i+1)+"/"
      flows = parse_log(p+'ifb0.txt', flow_idfrs, bg=True)
      quality, rebuf, end_ts = vlog2(p+'vlog.txt')
      cum_flows, tm, mbps,_ = cummulate(flows)
      vq.append(avg_video_quality(quality))
      util.append(sum(flow_download(cum_flows, trange=-1))/((tm[-1])/(1000/td)))
      dl.append(flow_download(cum_flows))
    except:
      continue
  avg = np.mean(vq)
  dls.append(dl)
  pe_avg.append(avg)
  std_dev = np.std(vq)
  pe_std.append(std_dev)
  print("Average Difference", avg)
  print("Standard dev", std_dev)
  avg_util = np.mean(util)
  lu_avg.append(avg_util*8)
  std_dev_util = np.std(util)
  lu_std.append(std_dev_util*8)
  print("Average Utilization", avg_util*8)
  print("Standard dev", std_dev_util*8)

print(lu_avg, lu_std)
print(pe_avg, pe_std)
