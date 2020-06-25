import plotnine as plt
import pandas as pd
import random

random.seed(42)
df = pd.DataFrame()
df = df.append([[0 + random.uniform(0, 0.25), 0 + random.uniform(0, 0.25), "ZoP"] for i in range(10)])
df = df.append([[1 - random.uniform(0, 0.25), 1 - random.uniform(0, 0.25), "ZoU"] for i in range(10)])

step = 0.1
for i in range(9):
    x = 0 + step
    y = 1 - step
    step += 0.1
    df = df.append([[x + random.uniform(0, 0.1), y - random.uniform(0, 0.1), "MS"] for i in range(3)])
df.columns = ["abstractness", "instability", "zone"]

p = plt.ggplot(df, plt.aes(x="instability", y="abstractness", color="zone")) + \
    plt.geom_abline(slope=-1, intercept=1) + \
    plt.geom_label(plt.aes(label=df["zone"])) + \
    plt.scale_color_manual(["green", "red", "firebrick"]) + \
    plt.lims(x=(0,1), y=(0,1))

# plt.geom_segment(plt.aes(x=0.2, xend=0.1, y=0.3, yend=0.2), arrow=plt.geoms.arrow()) + \
# print(p)
p.save("ai_scatter.pdf")

