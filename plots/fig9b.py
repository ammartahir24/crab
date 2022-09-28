from functions import *

# data from fig9adata.py
video, bulks = [2626.7805910000334, 218.57516199999915, 2071.4478809999796], [2751.7163410186768, 5176.89426612854, 2394.8471479415894]
plt.figure(figsize=(5,4))
labels = ["WFQ\n@bottleneck", "Status Quo", "CRAB\n@end-host"]
plt.bar(labels, video, width=0.3, label="Video flow", color="navy")
plt.bar(labels, bulks, bottom=video, width=0.3, label="Bulk download flow", color="royalblue")
x1,x2,y1,y2 = plt.axis()
plt.axis([x1,x2,y1,7000])
plt.ylabel("Data Downloaded (MB)")
plt.legend()
plt.savefig("videodownload.pdf", bbox_inches="tight")