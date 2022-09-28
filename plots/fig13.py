from scipy.interpolate import make_interp_spline
from functions import *


lu_avg, lu_std, pe_avg, pe_std = [20.637466838051103, 16.58622340878471, 20.957070109092, 21.187817120585996, 20.74680834836482, 26.69444701460731], [0.8817220006767149, 1.3463267938922356, 1.7968965093715348, 2.640252719829904, 0.8664606066062825, 0.19540985155831742],[7.498429907056038, 7.626486451302989, 7.251066112504456, 7.626348644760972, 7.371623210015373, 5.162360333484794], [0.3080509068631689, 0.1418423677922692, 0.2358089436483745, 0.20412570243134616, 0.1717214736129997, 0.7255990784114073]
fig,(ax1)=plt.subplots(figsize=(5,4))
labels = [r"$n \times t= 5 \times 0.2s = 1s$ (Default)", r"$n \times t= 10 \times 0.3s=3s$", r"$n \times t= 5 \times 0.1= 0.5s$", "","","Instantaneous Reallocation"]
marks = ["H", "s", "D", "o", "D", "o"]
# marks = ["o", "v", "^", "s"]
colors = ["black","royalblue", "royalblue", "navy", "navy", "gray"]
for i in range(len(lu_avg)):
  if i in [0,1,2,5]:
    eb1 = ax1.errorbar(lu_avg[i],pe_avg[i],yerr=pe_std[i],xerr=lu_std[i],label=labels[i].split("/")[0],marker=marks[i],ls='',color=colors[i])
    eb1[-1][0].set_linestyle(':')
# print(x,y)
# X_Y_Spline = make_interp_spline(x, y)

x,y = [16.58622340878471, 20.637466838051104, 20.957070109092, 26.69444701460731], [7.626486451302989, 7.498429907056038, 7.251066112504456, 5.162360333484794]

# Returns evenly spaced numbers
# over a specified interval.
# X_ = np.linspace(x[0], x[3], 3)
# Y_ = X_Y_Spline(X_)

plt.plot(x, y, ":", color="gray")
x1,x2,y1,y2 = plt.axis()
plt.axis([0,32,1,8.5])
plt.xlabel("Link Utilization (Mbps)")
plt.ylabel("Video Quality")
ax1.set_yticks([2,3,4,5,6, 7, 8])
ax1.set_yticklabels(['240p', '360p', '480p', '720p', '1080p', '1440p', '2160p'])
# plt.grid(b=True, which='major', color='white', linestyle='-')
plt.legend(loc=3)
plt.savefig("sens_analysis1.pdf", bbox_inches="tight")