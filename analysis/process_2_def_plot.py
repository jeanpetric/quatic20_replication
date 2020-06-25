import plotnine as plt
import pandas as pd


# title="Distance from the Main Sequence defective (True) vs non-defective (False) components"
def get_scatterplot(instances, group=False):
    instances["hash"] = instances["hash"].apply(lambda x: x[:6])
    p = plt.ggplot(instances, plt.aes(x="instability", y="abstractness")) + \
        plt.geom_point(plt.aes(color="defective", shape="defective"), alpha=0.6) + \
        plt.geom_abline(slope=-1, intercept=1) + \
        plt.scale_x_continuous(limits=[0, 1]) + \
        plt.scale_y_continuous(limits=[0, 1]) + \
        plt.scale_color_manual(["gray", "red"]) + \
        plt.theme(axis_text_x=plt.element_text(rotation=90))
    if group is True:
        p += plt.facet_wrap("hash")
    return p


def get_boxplot(instances, group=False):
    p = plt.ggplot(instances, plt.aes(x="defective", y="distance")) + \
        plt.geom_boxplot() + \
        plt.labs(title="Boxplot Distance with various interests (e.g. Zone of Pain and Useless Zone)")
    if group is True:
        p += plt.facet_wrap("hash")
    return p


def distance_boxplot(instances, group=None, title="Title"):
    p = plt.ggplot(instances, plt.aes(x="defective", y="distance")) + \
        plt.geom_boxplot() + \
        plt.scale_y_continuous(limits=[0, 1]) + \
        plt.labs(title=title)
    if group is not None:
        p += plt.facet_wrap(group)
    return p


def avg_distance_boxplot(instances, deviation="0.3", title=None):
    instances["defective"] = instances["defective"].astype(bool)
    return distance_boxplot(instances, group="project", title=title)
