from functions import *

clu_avg = [24.47250692643283]
clu_std = [0.6953668911814308]
cpe_avg = [7.417872476354858]
cpe_std = [0.4556852245366699]

wlu_avg = [22.202798957946115]
wlu_std = [0.35503032125067674]
wpe_avg = [7.736308121628493]
wpe_std = [0.19552620345916824]

lu_avg = [clu_avg, 26.87523265573631, wlu_avg, 26.580258771766935]#, 18.71598230176343]
lu_std = [clu_std, 0.1714782415790002, wlu_std, 0.1918863741764211]#, 1.2878151688773454]
pe_avg = [cpe_avg, 4.92765087566839, wpe_avg, 6.125022230448635]#, 7.596559186397141]
pe_std = [cpe_std, 0.6428837861145027, wpe_std, 0.9646957208036163]#, 0.1578065990477277]

# lu_avg = [clu_avg, 26.87523265573631, wlu_avg, 26.485729083770696]#, 18.71598230176343]
# lu_std = [clu_std, 0.1714782415790002, wlu_std, 0.08730578112496112]#, 1.2878151688773454]
# pe_avg = [cpe_avg, 4.92765087566839, wpe_avg, 6.51822607283226]#, 7.596559186397141]
# pe_std = [cpe_std, 0.6428837861145027, wpe_std, 0.479182710665807]#, 0.1578065990477277]

fig,(ax1)=plt.subplots(figsize=(5,4))
labels = ["Original CRAB", "Status Quo", "PQ after throttling to 25 Mbps", "PQ without throttling"]#, "CRAB-Noisy"]
marks = ["s", "v", "o", "^"]#, "^"]
colors = ["black", "navy", "darkslategray", "gray", "skyblue"]
order = [3, 2, 1, 0]
for i in order:
  ax1.errorbar(lu_avg[i],pe_avg[i],yerr=pe_std[i],xerr=lu_std[i],label=labels[i].split("/")[0],marker=marks[i],ls='', color=colors[i])

# colors = ["deepskyblue", "darkorange", "red", "teal", "skyblue"]
# ax2 = ax1.twinx()
# ls = ["video 1:5 bulk", "video 1:1 bulk", "video 5:1 bulk"]
# for i in range(len(clu_avg)):
#   ax2.plot([clu_avg[i], wlu_avg[i]], [cpe_avg[i], wpe_avg[i]],":" , color=colors[i], label=ls[i])

x1,x2,y1,y2 = plt.axis()
plt.axis([0,32,1,8.5])
ax1.set_xlabel("Link Utilization (Mbps)")
ax1.set_ylabel("Video Quality")
ax1.set_yticks([2,3,4,5,6, 7, 8])
ax1.set_yticklabels(['240p', '360p', '480p', '720p', '1080p', '1440p', '2160p'])
# ax2.grid(b=True, color='white', linestyle='-')
# ax2.get_yaxis().set_visible(False)
ax1.legend(loc=3)
# ax2.legend(loc=4, title="Link Sharing Ratio")
plt.savefig("pqvidplot.pdf", bbox_inches="tight")