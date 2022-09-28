import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import matplotlib.pyplot as plt
sns.set()
sns.palplot(sns.color_palette("cubehelix", 5))
from scipy.interpolate import make_interp_spline, BSpline
import numpy as np
import os
# sns.set(rc={'axes.facecolor':'white', 'figure.facecolor':'white'})
sns.set_style("whitegrid")


td = 100

def bw_cap(time_s, file="", ud = (1,10)):
  if file == "":
    if ud == 1:
      return [1500*1000*8/(1024*1024)]*time_s
    else:
      _, down = ud
      bytes_s = (1000 / down) * 2 * 8 * 1500
      return [bytes_s/(1024*1024)]*time_s
  else:
    f = open(file, 'r')
    data = f.read().split("\n")[:-1]
    times = [int(d) for d in data]
    ret_times = [d for d in times]
    last_s = ret_times[-1]
    while (last_s/1000) < time_s:
      new_times = [d+last_s for d in times]
      ret_times += new_times
      last_s = ret_times[-1]
    MTU = 1500
    bw_s = [0]*(int(last_s/1000) + 1)
    for t in ret_times:
      t_s = int(t/1000)
      bw_s[t_s] += MTU
    mbps = [(d*8)/(1024*1024) for d in bw_s]
    return mbps
# print(bw_cap(100, ud = 1))
# print(bw_cap(15, ud = (1,11)))
# bw_cap(330, file="Verizon-LTE-short.down")

def parse_downlink_log(file):
  f = open(file, 'r')
  data = f.read()
  data = data.split('\n')
  timestamp = int(data[3].split(' ')[-1])
  # print(timestamp)
  data = [d.split(' ') for d in data][:-1]
  downlink_bytes = [0] * int(int(data[-1][0]) / td)
  for row in data:
    if row[1] == '-':
      sec = int(int(row[0])/td)
      # if sec < len(downlink_bytes):
      downlink_bytes[sec] += int(row[2])
      # else:
      #   downlink_bytes.append(int(row[2]))
  down_mbps = [float(d*8)*(1000/td) / (1024*1024) for d in downlink_bytes]
  # print(len(down_mbps))
  return down_mbps, timestamp

def convert_to_ms(ts):
  hr, min, sec = ts.split(':')
  try:
    time_s = float(hr)*60*60 + float(min)*60 + float(sec)
  except:
    print(ts)
    sec = sec.replace("IP","")
    time_s = float(hr)*60*60 + float(min)*60 + float(sec[:9])
  return time_s*1000

def parse_log(file, flows, bg=False):
  f = open(file, 'r')
  data = f.read()
  data = data.split('\n')
  print(len(data))
  data = [d for d in data if "> crab" in d or "> cs-ammart2" in d or "> 192.168.1.174" in d]
  # data = [d for d in data if "> crab" in d]
  print(len(data))
  flow_bws = []
  for fl in flows:
    flow_log = [d for d in data if fl in d]
    flow_log = [d for d in flow_log if 'length' in d]
    print(len(flow_log))
    # print(flow_log[:2])
    abs_times = [convert_to_ms(e.split(' ')[0]) for e in flow_log]
    byte = [e.split('length ')[1] for e in flow_log]
    byte = [int(e.split(' ')[0].replace(':','')) for e in byte]
    time = [t-abs_times[0] for t in abs_times]
    # print(len(time))
    # print(time[-1])
    bytes_recv = [0]* (int(int(time[-1])/td)+1)
    for t,b in zip(time, byte):
      t = int(int(t)/td)
      try:
        bytes_recv[t] += b
      except:
        print(t, time[-1])
    mbps = [float(d*8)*(1000/td)/(1024*1024) for d in bytes_recv]
    flow_bws.append((mbps, abs_times[0], abs_times[-1]))
    # print(mbps[:10])
    # print(byte[:10])
  if bg:
    sent_data2 = [d for d in data if 'length' not in d]
    print(sent_data2)
    sent_data = [d for d in data if 'length' in d]
    for fl in flows:
      sent_data = [d for d in sent_data if fl not in d]
    print(sent_data[:5])
    abs_times = [convert_to_ms(e.split(' ')[0]) for e in sent_data]
    byte = [int(e.split('length ')[1].split(' ')[0].replace(':','')) for e in sent_data]
    time = [t-abs_times[0] for t in abs_times]
    bytes_recv = [0]* (int(int(time[-1])/td)+1)
    for t,b in zip(time, byte):
      t = int(int(t)/td)
      try:
        bytes_recv[t] += b
      except:
        print(t, time[-1])
    mbps = [float(d*8)*(1000/td)/(1000*1000) for d in bytes_recv]
    flow_bws = [(mbps, abs_times[0], abs_times[-1])] + flow_bws
    # print(mbps[:10])
    
  return flow_bws
  # print(data[0])

def cummulate(flows, tdiff=0):
  times = [[s,e] for _,s,e in flows]
  min_t, max_t = min([min(t) for t in times]), max([max(t) for t in times])
  # print(times, min_t, max_t)
  mbps = [0] * (int((max_t - min_t) / td) + 1)
  cum_flows = []
  for f,s,e in flows:
    start_buf = int((s-min_t) / td)
    # end_buf = int((max_t-e) / td)
    buf_mbps = [0]* start_buf + f + [0]* ((len(mbps)) - (len(f) + start_buf))
    mbps = np.add(mbps, buf_mbps)
    # print(mbps[:10])
    cum_flows.append(buf_mbps)
  return cum_flows, range(len(mbps)), mbps, min_t

def bw_cap2(time_s, pkts):
  bps = (pkts*1000) * 1500 * 8
  mbps = bps / (1024*1024)
  return [mbps] * time_s


def plot(mm_bw, mm_ts, flows, tm, mbps, bw_tup, labels, file=""):
  cap_bw = bw_cap2(len(mm_bw), bw_tup)
  mm_time = range(len(mm_bw))
  cap_time = range(len(cap_bw))
  max_bw = max(max(cap_bw), max(mm_bw))
  plt.figure(figsize=(10,10))
  plt.plot(cap_time, cap_bw, "b--", label="Capped Bandwidth")
  plt.plot(mm_time, mm_bw, "g", label = "MahiMahi observed Bandwidth")
  plt.plot(tm, mbps, "y", label = "Goodput")
  i = 0
  for f in flows:
    l = labels[i]
    i += 1
    plt.plot(tm, f, label=l)
  x1,x2,y1,y2 = plt.axis()
  plt.axis((x1,x2,0,max_bw + (max_bw / 2)))
  plt.ylabel("Mbps")
  plt.xlabel("Time (%d-th of s)" %(1000/td))
  plt.legend()
  # plt.title(title)
  plt.show()

def plot3(flows, tm, mbps, bws, bwt, bw_e, tm_e, fname="", trange=-1, yheight=-1, smooth=10, labels=[], lines=[], texts=[], lutil=[]):
  # cap_bw = bw_cap2(len(mm_bw), bw_tup)
  # mm_time = range(len(mm_bw))
  # cap_time = range(len(cap_bw))
  # max_bw = max(max(cap_bw), max(mm_bw))
  plt.figure(figsize=(8,3))
  # plt.figure(figsize=(10,7))
  font = {'family' : 'Helvetica',
        'weight' : 'normal',
        'size'   : 16}
  plt.rc('font', **font)
  # plt.plot(cap_time, cap_bw, "b--", label="Capped Bandwidth")
  # plt.plot(mm_time, mm_bw, "g", label = "MahiMahi observed Bandwidth")
  # plt.plot(tm, smoothen(mbps, 10), "y", label = "Goodput")
  lines = ['--', ':', '-.', '--', '--', '--', '--']
  colors = ["black", "royalblue", "navy", "rebeccapurple"]
  tm = [t/(1000/td) for t in tm]
  i = 0
  rets = []
  for f in flows:
    # l = labels[i]
    i += 1
    label = "f%d" %(i)
    line = "-"
    if labels != []:
      label = labels[i-1]
    if lines != []:
      line = lines[i-1]
    rets += [smoothen(f,smooth)]
    plt.plot(tm, smoothen(f, smooth), lines[i-1], label=label, color=colors[i-1])
  link_util = [sum(item) for item in zip(*flows)]
  if lutil != []:
    link_util = lutil
  plt.fill_between(tm, smoothen(link_util, smooth), 0, label="Link Utilization",
                 facecolor="darkslategray", # The fill color
                 color='darkslategray',       # The outline color
                 alpha=0.2)
  if len(bwt):
    plt.plot(bwt, bws, "-", label="Link Bandwidth", color="k")
  if len(tm_e):
    plt.plot(tm_e, bw_e, label="Max_BW")
  x1,x2,y1,y2 = plt.axis()
  if trange!=-1:
    x1, x2 = trange[0], trange[1]
  if yheight != -1:
    y1, y2 = yheight[0], yheight[1]
  plt.axis([x1,x2,y1,y2])
  plt.grid(b=True, which='major', color='white', linestyle='-')

  
  if texts != []:
    txs = [t[0] for t in texts]
    plt.plot(txs,[0]*len(txs),"k*", label = "Demand Changes")
    for i,j,t in texts:
      plt.text(i,j,t, size=10)
  # plt.axis((x1,x2,0,max_bw + (max_bw / 2)))
  plt.ylabel("Throughput (Mbps)")
  plt.xlabel("Time (s)")
  # plt.grid()
  plt.legend(loc=2, ncol=4)
  # plt.title(title)
  if fname != "":
    plt.savefig(fname, bbox_inches="tight")
    return rets
  plt.show()

def cummulative_increasing(x):
  ret = []
  for i in range(len(x)):
    ret.append((sum(x[:i])/8))
  return ret

def plot4(flows, tm, mbps, bw_tup, fname=""):
  plt.figure(figsize=(10,5))
  i = 0
  for f in flows:
    i += 1
    plt.plot(tm, cummulative_increasing(f), label="flow %d" %(i))
  x1,x2,y1,y2 = plt.axis()
  plt.ylabel("MB")
  plt.xlabel("Time (%d-th of s)" %(1000/td))
  plt.grid()
  plt.legend()
  if fname != "":
    plt.savefig(fname, bbox_inches="tight")
    return
  plt.show()


def smoothen(f, avg_over):
  return [np.mean(f[i - min(i,avg_over):i]) for i in range(len(f))]

def flow_download(flows, trange=-1):
  if trange == -1:
    return [sum(f)/8/(1000/td) for f in flows]
  else:
    return [sum(f[trange[0]:trange[1]])/8/(1000/td) for f in flows]


def plot2(flows, tm, mbps, quality, rebuf, rebuf_pt, bws=[], bwt=[], smooth=10, fair_share=-1, num_bulk=-1, fname="", trange=-1, yheight=-1, lutil=[]):
  plt.figure(figsize=(5,3))
  font = {'family' : 'Helvetica',
        'weight' : 'normal',
        'size'   : 25}
  plt.rc('font', **font)
  plt.rcParams.update({'font.size': 25})
  fig, ax1 = plt.subplots(figsize=(6,4))
  ax2 = ax1.twinx()
  # ax1.plot(tm, mbps, "y", label = "Goodput")
  i = 0
  line = ['--', ':', '--', '--', '--', '--', '--']
  # colors = []
  tm = [t/(1000/td) for t in tm]
  for f in flows:
    if i==0:
      print("Video flow cummulative:", sum(f)/8/(1000/td))
      ax1.plot(tm, smoothen(f, smooth), line[i], label="Video Flow", color="navy")
    else:
      print("Bulk flow %d cummulative:" %(i), sum(f)/8/(1000/td))
      ax1.plot(tm, smoothen(f, smooth), line[i], label="Bulk Flows", color="royalblue")
    i += 1
  
  link_util = [sum(item) for item in zip(*flows)]
  if lutil != []:
    link_util = lutil
  ax1.fill_between(tm, smoothen(link_util, smooth), 0, #label="Link Utilization",
                 facecolor="darkslategray", # The fill color
                 color='darkslategray',       # The outline color
                 alpha=0.2)
  # ax1.plot(tm, smoothen(link_util, smooth), "*-", label="Link Utilization", color="gray")
  if fair_share!=-1:
    ax1.plot([tm[0], tm[-1]], [fair_share, fair_share], '--', label="fair share")
  for r in rebuf:
    xs, ys = [r[0]], [rebuf_pt]
    if r[1] != 0:
      xs += [r[0]+r[1]]
      ys += [rebuf_pt]
    ax1.plot([x/(1000/td) for x in xs], ys, 'g-*')
  tmq = [t/(1000/td) for t in quality[1]]
  ax2.plot(tmq, [q-1 for q in quality[0]], "k-", label="Video Quality", linewidth=3)
  if len(bwt):
    ax1.plot(bwt, bws, label="Link BW")
  x1,x2,y1,y2 = ax1.axis()
  if trange!=-1:
    x1, x2 = trange[0], trange[1]
  if yheight != -1:
    y2 = yheight
  else:
    y2 += 0.25*y2
  ax2.axis([x1,x2,0,9])
  ax1.axis([x1,x2,0,y2])    
  ax1.set_ylabel("Throughput (Mbps)")
  ax1.grid()
  ax2.set_ylabel("Quality")
  ax2.set_yticks([1,2,3,4,5,6,7])
  ax2.set_yticklabels(['240p', '360p', '480p', '720p', '1080p', "1440p", "2160p"])
  ax1.set_xlabel("Time (s)")
  ax1.legend(loc=2)
  ax2.legend(loc=1)
  # plt.title(title)
  if fname != "":
    plt.savefig(fname, bbox_inches="tight")
    return
  plt.show()


def intify(xs):
  vlevels = ['tiny','small', 'medium', 'large', 'hd720', 'hd1080', "hd1440", "hd2160"]
  return [(t,vlevels.index(q.replace("'",""))+1) for t,q in xs]

def linearize(xy, end):
  xs = []
  ys = []
  prev = xy[0][1]
  for x,y in xy:
    x = int(x/td)
    xs += [x, x]
    ys += [prev,y]
    prev = y
  xs += [int(end/td)]
  ys += [ys[-1]]
  return ys, xs

def vlog2(file, diff= 0):
  f = open(file, 'r')
  data = f.read()
  data = data.split('\n')
  print(data[0:5])
  # for x in data:
  #   print(x)
  data = [x for x in data if 'video.html' in x or '\u200b' in x]
  data = [x for x in data if 'Failed' not in x]
  data = [x for x in data if 'Intervention' not in x]
  # for x in data:
  #   print(x)
  start_ts = int(data[0].split(' ')[1]) - diff*1000
  start_qu = [x for x in data if 'Starting quality' in x][0].split(' ')[-1].replace('"', '')
  q_change = [x for x in data if 'Playback quality changed ' in x]
  q_t_series = [(int(x.split(' ')[1])-start_ts, x.split(' ')[-1].replace('"','')) for x in q_change]
  rebuf = [x for x in data if 'Rebuffering' in x]
  vplay = [x for x in data if 'Video playing' in x]
  print(rebuf, vplay)
  if len(vplay) == len(rebuf)+1:
    vplay = vplay[1:]
  if len(vplay)+1 == len(rebuf):
    rebuf = rebuf[1:]
  print(len(rebuf), len(vplay))
  assert(len(rebuf) == len(vplay))
  rebuf_t_series = [(int(rebuf[i].split(' ')[1]) -start_ts, int(vplay[i].split(' ')[1]) -start_ts) for i in range(len(rebuf))]
  end_ts = int([x for x in data if 'Ended' in x][0].split(' ')[1]) - start_ts
  quality_series = linearize(intify(q_t_series),end_ts)
  rebuffers = [(int(x/td), int((y-x)/td)) for x,y in rebuf_t_series]
  return quality_series, rebuffers, end_ts

def vlog(file, diff= 0):
  f = open(file, 'r')
  data = f.read()
  data = data.split('\n')
  print(data[-2])
  # data = [x for x in data if 'video.html' in x]
  start_ts = int(data[0].split(': ')[1].split(', ')[0]) - diff*1000
  start_qu = data[0].split(': ')[1].split(', ')[1]
  q_change = [x for x in data if 'quality-changed' in x]
  q_t_series = [(0, start_qu)]+[(int(x.split(': ')[1].split(', ')[0])-start_ts, x.split(': ')[1].split(', ')[1]) for x in q_change]
  # rebuf = [x for x in data if 'Rebuffering' in x]
  # vplay = [x for x in data if 'Video playing' in x]
  # assert(len(rebuf) == len(vplay))
  # rebuf_t_series = [(int(rebuf[i].split(' ')[1]) -start_ts, int(vplay[i].split(' ')[1]) -start_ts) for i in range(len(rebuf))]
  end_ts = [x for x in data if 'end' in x]
  if end_ts == []:
    end_ts = 296000
  else:
    end_ts = end_ts[0]
    end_ts = int(end_ts.split(': ')[1].split(', ')[0]) - start_ts
  print(q_t_series)
  quality_series = linearize(intify(q_t_series),end_ts)
  print(quality_series)
  rebuffers = []
  return quality_series, rebuffers, end_ts

def parse_crab_log(fname, string="assigned_bw", fnames=[]):
  f = open(fname, 'r')
  data = f.read()
  data = data.split('*\n')
  start_ts = float(data[0])
  log = data[1:]
  if fnames == []:
    flow_names = [d.split(": ")[1].split(", ")[0] for d in data[1].split("\n") if "flow_name" in d]
  else:
    flow_names = fnames
  print(flow_names)
  ret = []
  string1 = "assigned_bw"
  string2 = "lended_bw"
  for e in log:
    e = e.split("\n")
    ts = float(e[0].split(": ")[0]) - start_ts
    obs_bw = float(e[0].split(": ")[1])
    bws = [float(x.split(string1)[1].split(", ")[0].replace(":","").replace(" ","")) - float(x.split(string2)[1].split(", ")[0].replace(":","").replace(" ","")) for x in e[1:-1]]
    ret += [(ts, obs_bw, bws)]
  return ret, start_ts, flow_names

def parse_crab_log_get_max_bw(fname, td):
  f = open(fname, 'r')
  data = f.read()
  data = data.split('*\n')
  start_ts = float(data[0])
  log = data[1:]

  ret = []
  tss = []
  for e in log:
    e = e.split("\n")
    ts = float(e[0].split(": ")[0]) - start_ts
    obs_bw = float(e[0].split(": ")[1])
    # print(e[1:])
    bws = sum([float(x.split("actual_share")[1].split(", ")[0].replace(":","").replace(" ","")) for x in e[1:-1]])
    if ts > td:
      ret += [bws]
      tss += [ts - td]
  return ret, tss, start_ts


def parse_crab_log2(fname, string="actual_share", fnames=[]):
  f = open(fname, 'r')
  data = f.read()
  data = data.split('*\n')
  start_ts = float(data[0])
  log = data[1:]
  if fnames == []:
    flow_names = [d.split(": ")[1].split(", ")[0] for d in data[1].split("\n") if "flow_name" in d]
  else:
    flow_names = fnames
  print(flow_names)
  ret = []
  for e in log:
    e = e.split("\n")
    ts = float(e[0].split(": ")[0]) - start_ts
    obs_bw = float(e[0].split(": ")[1])
    # print(e[1:])
    # print([x for x in e[1].split("flow_id")])
    bws = [float(x.split(string)[1].split(", ")[0].replace(":","").replace(" ","")) for x in e[1].split("flow id")[1:]]
    ret += [(ts, obs_bw, bws)]
  print(data[1])
  print(ret[0])
  print(data[2])
  print(ret[1])
  return ret, start_ts, flow_names

def cdf(x):
  x, y = sorted(x), np.arange(len(x)) / len(x)
  return (x, y)

def plot_cdf(xs, names, xlabel, ylabel, title, save="", lines = []):
  cdfs = [cdf(x) for x in xs]
  plt.figure(figsize=(5,4))
  line = ['--', ':', '-.', '--', '--', '--', '--']
  colors = ["royalblue", "navy", "slategray", "black"]
  for i in range(len(xs)):
    x,y = cdfs[i]
    print("median for", names[i], x[int(len(x)/2)])
    print("Mean for", names[i], np.nanmean(xs[i]))
    if lines != []:
      plt.plot(x,y,lines[i], label= names[i], color=colors[i])
    else:
      plt.plot(x,y, line[i],label= names[i], color=colors[i])
  font = {'family' : 'Helvetica',
    'weight' : 'normal',
    'size'   : 22}
  plt.rc('font', **font)
  plt.xlabel(xlabel)
  plt.xticks(np.arange(5, 60, 5.0))
  plt.ylabel(ylabel)
  x1,x2,y1,y2 = plt.axis()
  plt.axis([0,x2,0,y2])
  # plt.title(title)
  plt.legend(loc="lower right")
  if save!="":
    plt.savefig(save, bbox_inches="tight")
  return cdfs

def plot_tail(tail, xs, names, xlabel, ylabel, title, save="", lines = []):
  cdfs = [cdf(x) for x in xs]
  plt.figure(figsize=(20,10))
  for i in range(len(xs)):
    x,y = cdfs[i]
    print("median for", names[i], x[int(len(x)/2)])
    print("Mean for", names[i], np.mean(xs[i]))
    olen = len(x)
    x = x[int(tail*len(x)):]
    y = y[int(tail*olen):]
    print(len(x), len(y))
    if lines != []:
      plt.plot(x,y,lines[i], label= names[i])
    else:
      plt.plot(x,y,label= names[i])
  font = {'family' : 'Helvetica',
    'weight' : 'normal',
    'size'   : 16}
  plt.rc('font', **font)
  plt.xlabel(xlabel)
  plt.xticks(np.arange(1, 80, 5.0))
  plt.ylabel(ylabel)
  # plt.title(title)
  plt.legend(loc="bottom right")
  if save!="":
    plt.savefig(save, bbox_inches="tight")

def str_to_list(fname, pg_sizes = False):
  f = open(fname+'plt.txt', 'r')
  x = f.read()
  f.close()
  x = x.split('])')
  # print(x)
  all_plts = []
  sizes = []
  for e in x:
    if e == "]":
      continue
    # print(e)
    try:
      plts = e.replace('[(','(').split(".com', [")[1].split(", ")
      plts = [int(p) for p in plts]
      all_plts += plts
    except:
      plts = e.replace('[(','(').split(".com', ")[1].split("), (")
      plts = [p.replace('(','').replace(')','').split(', ') for p in plts]
      plts_ = [int(p[0]) for p in plts]
      sizes.append([int(p[1]) for p in plts])
      all_plts += plts_
  # x = x.replace('[','').replace(']','')
  # x = x.split(', ')
  if pg_sizes:
    return sizes
  all_plts = [int(i)/1000 for i in all_plts]
  return all_plts

def plot_bws(flows, flow_names, trange=-1):
  bw_lists = [[] for i in range(len(flow_names))]
  time = []
  for t,_,b_list in flows:
    if (trange!=-1 and t>trange[0] and t<trange[1]) or trange==-1:
      time.append(t)
      for i in range(len(b_list)):
        bw_lists[i].append(b_list[i])
  plt.figure(figsize=(10,5))
  line = ['-', '-', '-', '-', '--', '--', '--']
  for i in list(range(len(bw_lists))):
    plt.plot(time,bw_lists[i],line[i],label= flow_names[i])
  font = {'family' : 'Helvetica',
    'weight' : 'normal',
    'size'   : 16}
  plt.rc('font', **font)
  plt.xlabel("Time(s)")
  plt.ylabel("Actual Share of Bandwidth")
  # plt.title(title)
  plt.legend()
  plt.grid()
  plt.savefig("bws.png", bbox_inches="tight")


def plot_video(xs, names, xlabel, ylabel, title):
  plt.figure(figsize=(10,5))
  for i in range(len(xs)):
    print(xs[i][0], xs[i][1])
    tmq = [t/(1000/td) for t in xs[i][1]]
    plt.plot(tmq, [q+1 for q in xs[i][0]], "*-", label=names[i])
  font = {'family' : 'Helvetica',
    'weight' : 'normal',
    'size'   : 16}
  plt.rc('font', **font)
  plt.ylabel("Quality")
  plt.yticks([2,3,4,5,6])
  # plt.set_yticklabels(['240p', '360p', '480p', '720p', '1080p'])
  plt.xlabel(xlabel)
  # plt.ylabel(ylabel)
  # plt.title(title)
  plt.legend(loc="bottom right")
  plt.savefig("vid.pdf", bbox_inches="tight")
def avg_video_quality(vq):
  quality, times = vq[0], vq[1]
  prev_time = 0
  vq_sum = 0
  for i in range(len(quality)):
    vq_sum += quality[i] * (times[i] - prev_time)
    prev_time = times[i]
  return vq_sum / times[-1]


def count_bytes(file, id, trange=-1):
  f = open(file, 'r')
  data = f.read()
  data = data.split('\n')
  data = [d for d in data if "> crab" in d or "> cs-ammart2" in d]
  data = [d for d in data if id in d]
  print(data[1000:1010])
  # data = [d for d in data if "> crab" in d]
  sent_data = [d for d in data if 'length' in d]
  abs_times = [convert_to_ms(e.split(' ')[0]) for e in sent_data]
  byte = [int(e.split('length ')[1].split(' ')[0].replace(':','')) for e in sent_data]
  time = [t-abs_times[0] for t in abs_times]
  num_bytes = 0
  if trange == -1:
    trange = (time[0], time[-1])
  else:
    trange = (trange[0]*1000, trange[1]*1000)
  for i in range(len(byte)):
    if time[i] >= trange[0] and time[i] <= trange[1]:
      num_bytes += byte[i]  
  return num_bytes

def packet_inter(file, id, trange=-1):
  f = open(file, 'r')
  data = f.read()
  data = data.split('\n')
  # data = [d for d in data if "> crab" in d or "> cs-ammart2" in d]
  data = [d for d in data if id in d]
  print(data[0], data[-1])
  # data = [d for d in data if "> crab" in d]
  # sent_data = [d for d in data if 'length' in d]
  sent_data = data
  for i in range(25):
    print(i, sent_data[i])
  abs_times = [convert_to_ms(e.split(' ')[0]) for e in sent_data]
  # byte = [int(e.split('length ')[1].split(' ')[0].replace(':','')) for e in sent_data]
  time = [t-abs_times[0] for t in abs_times]
  if trange == -1:
    trange = (time[0], time[-1])
  intertimes = []
  for i in range(len(time)):
    if time[i] >= trange[0]:
      for j in range(i, len(time)):
        if time[j] <= trange[1]:
          intertimes.append(time[j] - time[i])
      break
  plt.figure(figsize=(10,5))
  print(len(intertimes))
  # plt.figure(figsize=(10,7))
  font = {'family' : 'Helvetica',
        'weight' : 'normal',
        'size'   : 16}
  plt.rc('font', **font)
  plt.plot(intertimes, "*-")
  plt.xlabel("Packet #")
  plt.ylabel("Time (ms)")
  plt.title("Interarrival time from first packet")
  plt.show()

