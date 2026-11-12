import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, json
plt.rcParams.update({"font.size":9, "axes.edgecolor":"#888888"})
PINK="#E4007C"; NAVY="#12263F"; GREY="#8A94A6"; LIGHT="#F2C6DA"
d=json.load(open("finalists.json"))
# 1 batters: pressure SR vs baseline SR (baseline = pr_sr - uplift)
names=[x["name"].replace(" ","\n") for x in d["batters"][:10]]
pr=[x["pr_sr"] for x in d["batters"][:10]]
base=[round(x["pr_sr"]-x["uplift"],1) for x in d["batters"][:10]]
fig,ax=plt.subplots(figsize=(8.2,3.6))
x=np.arange(10); w=0.38
ax.bar(x-w/2, pr, w, color=PINK, label="Pressure SR")
ax.bar(x+w/2, base, w, color=NAVY, label="Non-pressure SR")
ax.set_xticks(x); ax.set_xticklabels(names, fontsize=7.5)
ax.set_ylabel("Strike rate"); ax.set_title("Top 10 batters — strike rate under pressure vs their own non-pressure baseline", fontsize=10, color=NAVY, loc="left")
ax.legend(frameon=False, fontsize=8); ax.spines[["top","right"]].set_visible(False); ax.set_ylim(0,250)
for i,v in enumerate(pr): ax.text(i-w/2, v+6, f"{v:.0f}", ha="center", fontsize=7.5, color=PINK, weight="bold")
plt.tight_layout(); plt.savefig("chart_bat.png", dpi=200); plt.close()
# 2 bowlers: pressure econ vs expected econ (par given mix = pr_econ - adj)
names=[x["name"].replace(" ","\n") for x in d["bowlers"][:10]]
pr=[x["pr_econ"] for x in d["bowlers"][:10]]
exp=[round(x["pr_econ"]-x["adj"],2) for x in d["bowlers"][:10]]
fig,ax=plt.subplots(figsize=(8.2,3.6))
x=np.arange(10); w=0.38
ax.bar(x-w/2, pr, w, color=PINK, label="Pressure economy")
ax.bar(x+w/2, exp, w, color=NAVY, label="Expected economy (par for same situations)")
ax.set_xticks(x); ax.set_xticklabels(names, fontsize=7.5)
ax.set_ylabel("Runs per over"); ax.set_title("Top 10 bowlers — economy under pressure vs par for the same situations (lower is better)", fontsize=10, color=NAVY, loc="left")
ax.legend(frameon=False, fontsize=8); ax.spines[["top","right"]].set_visible(False); ax.set_ylim(0,12)
for i,v in enumerate(pr): ax.text(i-w/2, v+0.3, f"{v:.2f}", ha="center", fontsize=7.5, color=PINK, weight="bold")
plt.tight_layout(); plt.savefig("chart_bowl.png", dpi=200); plt.close()
# 3 par SR by subtype
subs=["Collapse","Death","Knockout\ndeath*","Late high\nRRR","Tight\nfinish"]
ipl=[112.9,177.9,173.5,150.9,173.7]; t20=[104.9,163.0,140.3,136.6,148.7]
fig,ax=plt.subplots(figsize=(8.2,3.2))
x=np.arange(5); w=0.38
ax.bar(x-w/2, ipl, w, color=PINK, label="IPL par SR")
ax.bar(x+w/2, t20, w, color=NAVY, label="T20I par SR")
ax.set_xticks(x); ax.set_xticklabels(subs, fontsize=8)
ax.set_ylabel("Par strike rate"); ax.set_title("What 'par' means in each pressure situation — league strike rate on pressure balls", fontsize=10, color=NAVY, loc="left")
ax.legend(frameon=False, fontsize=8); ax.spines[["top","right"]].set_visible(False); ax.set_ylim(0,200)
plt.tight_layout(); plt.savefig("chart_par.png", dpi=200); plt.close()
print("charts done")
