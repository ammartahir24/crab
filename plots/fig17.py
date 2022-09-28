from functions import *

lu_avg, lu_std, pe_avg, pe_std = [21.637466838051103, 17.58622340878471, 21.957070109092, 21.187817120585996, 20.74680834836482], [0.8817220006767149, 1.3463267938922356, 1.7968965093715348, 2.640252719829904, 0.8664606066062825],[7.498429907056038, 7.626486451302989, 7.251066112504456, 7.626348644760972, 7.371623210015373], [0.3080509068631689, 0.1418423677922692, 0.2358089436483745, 0.20412570243134616, 0.1717214736129997]
fig,(ax1)=plt.subplots(figsize=(5,4))
labels = ["headroom=0.25Mbps (Default)", "nxt=3s", "nxt=0.5s", "headroom=0.5mbps", "headroom=0.05mbps"]
marks = ["H", "s", "D", "s", "D"]
# marks = ["o", "v", "^", "s"]
colors = ["black","royalblue", "royalblue", "navy", "navy"]
for i in range(len(lu_avg)):
  if i in [0,3,4]:
    eb1 = ax1.errorbar(lu_avg[i],pe_avg[i],yerr=pe_std[i],xerr=lu_std[i],label=labels[i].split("/")[0],marker=marks[i],ls='',color=colors[i])
    eb1[-1][0].set_linestyle(':')
x1,x2,y1,y2 = plt.axis()
plt.axis([0,32,1,8.5])
plt.xlabel("Link Utilization (Mbps)")
plt.ylabel("Video Quality")
ax1.set_yticks([2,3,4,5,6, 7, 8])
ax1.set_yticklabels(['240p', '360p', '480p', '720p', '1080p', '1440p', '2160p'])
# plt.grid(b=True, which='major', color='white', linestyle='-')
plt.legend(loc=3)
plt.savefig("sens_analysis2.pdf", bbox_inches="tight")