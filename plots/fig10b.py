from functions import *

paths = ['data/web/wfq/1/', 'data/web/sq/1/', 'data/web/crab/1/']
names = ["WFQ@bottleneck", "Status Quo", "CRAB@end-host"]
link_util = []
td = 50
for p in paths:
  flows = parse_log(p+'ifb0.txt', [], bg=True)
  cum_flows, tm, mbps,_ = cummulate(flows)
  link_util.append(cum_flows[0])

l_utils = [np.mean(l) for l in link_util]
print(l_utils)
names = ["WFQ\n@bottleneck", "S.Q.", "CRAB\n@end-host"]

plt.figure(figsize=(2,4))
plt.bar(names, l_utils, width=0.4,  color="royalblue")
plt.ylabel("Average Link Utilization (Mbps)")
plt.grid(b=True, which='major', color='white', linestyle='-')
x1,x2,y1,y2 = plt.axis()
print(x1,x2,y1,y2)
plt.axis([x1,x2,0,10])
# plt.xticks(rotation = 90)
plt.savefig("plt_link_util.pdf", bbox_inches="tight")
