from functions import *

paths = ['data/web/wfq/1/', 'data/web/sq/1/', 'data/web/crab/1/']
names = ["WFQ@bottleneck", "Status Quo", "CRAB@end-host"]
datas = [str_to_list(f) for f in paths]
print(datas)
print([sorted(x)[10] for x in datas])
datas = [sorted(x)[:-1] for x in datas]
lines = ["-", "--", "-.", ":"]
plot_cdf(datas, names, "Page Load Time (s)", "CDF", "CDF of Page Load Time", save="plt_pdf.pdf", lines=lines)