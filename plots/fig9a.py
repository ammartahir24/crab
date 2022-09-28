from functions import *

# data from videosdata.py
clu_avg = [21.10833595097048, 19.282633245945988, 20.339869087212843]
clu_std = [1.3637703854812768, 1.458275183774017, 0.8817220006767149]
cpe_avg = [6.373678621791352, 6.983106560114181, 7.348989828122168]
cpe_std = [0.4233366930234317, 0.32174597131766486, 0.3080509068631689]

wlu_avg = [26.66835912637443, 26.9873464518258, 27.33176283515716]
wlu_std = [1.0432094449979692, 0.15728919941556535, 0.223444607401027]
wpe_avg = [6.882514593709952, 7.295294925618867, 7.9218387669830905]
wpe_std = [0.44347871549068696, 0.418687498000105, 0.08193993184824784]

lu_avg = [wlu_avg, 26.87523265573631, clu_avg]
lu_std = [wlu_std, 0.1714782415790002, clu_std]
pe_avg = [wpe_avg, 4.92765087566839, cpe_avg]
pe_std = [wpe_std, 0.6428837861145027, cpe_std]

fig,(ax1)=plt.subplots(figsize=(5,4))
labels = ["WFQ@bottleneck", "Status Quo", "CRAB@end-host"]
marks = ["s", "v", "o"]#, "^"]
colors = ["black", "navy", "darkslategray", "gray", "skyblue"]
for i in range(len(lu_avg)):
  ax1.errorbar(lu_avg[i],pe_avg[i],yerr=pe_std[i],xerr=lu_std[i],label=labels[i].split("/")[0],marker=marks[i],ls='', color=colors[i])

colors = ["deepskyblue", "darkorange", "red", "teal", "skyblue"]
ax2 = ax1.twinx()
ls = ["video 1:5 bulk", "video 1:1 bulk", "video 5:1 bulk"]
for i in range(len(clu_avg)):
  ax2.plot([clu_avg[i], wlu_avg[i]], [cpe_avg[i], wpe_avg[i]],":" , color=colors[i], label=ls[i])

x1,x2,y1,y2 = plt.axis()
plt.axis([0,32,1,8.5])
ax1.set_xlabel("Link Utilization (Mbps)")
ax1.set_ylabel("Video Quality")
ax1.set_yticks([2,3,4,5,6, 7, 8])
ax1.set_yticklabels(['240p', '360p', '480p', '720p', '1080p', '1440p', '2160p'])
# ax2.grid(b=True, color='white', linestyle='-')
ax2.get_yaxis().set_visible(False)
ax1.legend(loc=3)
ax2.legend(loc=4, title="Link Sharing Ratio")
plt.savefig("viderrplot.pdf", bbox_inches="tight")