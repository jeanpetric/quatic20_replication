from archive import *
from scipy.stats import wilcoxon


def ex_ratio(x, ex_zone):
    far = x[x["distance"] >= ex_zone]
    close = x[x["distance"] < ex_zone]
    ratio_ex = None
    ratio_nonex = None
    try:
        df = len(far[far["defective"] == 1])
        ndf = len(far[far["defective"] == 0])
        dc = len(close[close["defective"] == 1])
        ndc = len(close[close["defective"] == 0])
        ratio_ex = df / (df + ndf)
        ratio_nonex = dc / (dc + ndc)
    except:
        pass
    return ratio_ex, ratio_nonex


def ratio(instances, ex_zone=0.25):
    r_ex, r_nonex = zip(*instances.groupby(by="hash", sort=False, as_index=False) \
                           .apply(ex_ratio, ex_zone))
    df = pd.DataFrame({"exzone": r_ex, "nonexzone": r_nonex}).dropna()
    w = wilcoxon(df["exzone"], df["nonexzone"], alternative="greater")
    return [str(ex_zone),
            str(round(df["exzone"].mean(), 3)) + " (+/-" + str(round(df["exzone"].std(), 3)) + ")",
            str(round(df["nonexzone"].mean(), 3)) + " (+/-" + str(round(df["nonexzone"].std(), 3)) + ")",
            str(round(df["exzone"].mean() / df["nonexzone"].mean(), 3)),
            round(w.pvalue, 3)]


def ratios_for_project(instances):
    _df = []
    for shift in [0.2, 0.4, 0.6]:
        res = ratio(instances, shift)
        _df.append(res)
    df = pd.DataFrame(_df, columns=["shift", "rdef", "rnondef", "scale", "p"])
    return df


def ratios_for_projects(instances):
    projects = set(instances["project"])
    df = pd.DataFrame(columns=["project", "shift", "rdef", "rnondef", "scale", "p"])
    for project in projects:
        inst = instances[instances["project"] == project]
        _df = ratios_for_project(inst)
        _df["project"] = project
        df = df.append(_df)
    return df


instances = instances_from_archive("aggregated", "defects_normalised_0.3")
df = ratios_for_projects(instances)
print(df.to_latex(index=False, multirow=True))
