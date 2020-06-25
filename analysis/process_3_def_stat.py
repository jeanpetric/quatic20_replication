from archive import instances_from_archive, instances_to_archive
import pandas as pd
from scipy.stats import mannwhitneyu
import plotnine as plt
import numpy as np


project = "aggregated"
deviation = "0.3"
instances = instances_from_archive(project, extension=f"defects_normalised_{deviation}")
projects = set(instances["project"])

df = pd.DataFrame(columns=["defective", "distance", "project", "category"])
st = pd.DataFrame(columns=["project", "pval"])
for pr in projects:
    d = instances[(instances["defective"] == 1) & (instances["project"] == pr)][["defective", "distance", "project"]]
    nd = instances[(instances["defective"] == 0) & (instances["project"] == pr)][["defective", "distance", "project"]]
    _df = d.append(nd)
    _df["category"] = np.where(_df["defective"] == 1, "def", "nondef")
    df = df.append(_df)

    xd  = _df.loc[_df["defective"] == 1, "distance"]
    ynd = _df.loc[_df["defective"] == 0, "distance"]
    # dp = pd.DataFrame({"dist": xd, "defective": "def"})
    # dp = dp.append(pd.DataFrame({"distance": ynd, "defective": "nondef"}))
    # print(plt.ggplot(dp, plt.aes(x="distance", color="defective")) + plt.geom_density())
    # exit(1)
    t = mannwhitneyu(xd, ynd, alternative="greater")
    _st = pd.DataFrame({"project": [pr], "pval": [t.pvalue]})
    st = st.append(_st)

print(st.to_latex(bold_rows=True, index=False, caption="Open source project used in this paper", label="projects"))

p = plt.ggplot(df, plt.aes(x="category", y="distance")) + \
    plt.geom_boxplot() + \
    plt.labs(x="defective") + \
    plt.facet_wrap("project", ncol=4)
p.save("distance_boxplot.pdf", width=12, height=6, units="cm")

# p2 = plt.ggplot(df, plt.aes(x="distance", fill="defective")) + \
#     plt.geom_density(alpha=0.4) + \
#     plt.scale_color_grey() + \
#     plt.theme_classic() + \
#     plt.facet_wrap("project")
# p2.save("distance_density.pdf")
