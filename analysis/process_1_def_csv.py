import pandas as pd
import plotnine as plt
from pathlib import Path
from archive import get_csv, instances_from_archive, instances_to_archive


def to_instances_with_defects(csv):
    csv["ones"] = 1
    sums = csv.groupby(by="hash", sort=False, as_index=False).agg({
        "defective": "sum",
        "ones": "count"
        }).sort_values(by=["defective", "ones"], ascending=[False, True])
    sums = sums[(sums["defective"] > 0)]
    shas = sums["hash"] #.iloc[0:12]
    result = pd.DataFrame(columns=csv.columns)
    for sha in shas:
        result = result.append(csv[(csv["hash"] == sha)])
    result = result.dropna()
    return result


# deviation is percentage
def normalise_instances_for_size(instances, deviation=0.1):
    result = pd.DataFrame(columns=instances.columns)
    instances["classTotal"] = instances["pckg:abstractClassCount"] + instances["pckg:concreteClassCount"]
    shas = set(instances["hash"])
    for sha in shas:
        tmp = instances[(instances["hash"] == sha)]
        defective_avg = tmp[(tmp["defective"] == 1)]["classTotal"].mean()
        deviation = float(deviation)
        tmp = tmp[(tmp["classTotal"] > (defective_avg*(1-deviation))) & (tmp["classTotal"] < (defective_avg*(1+deviation)))]
        result = result.append(tmp)
    return result


def group_by_defectiveness(instances):
    return instances.groupby(by=["hash", "defective"], as_index=False).mean()


def avg_distance_aggregated(projects, deviation="0.3"):
    instances = instances_from_archive(projects[0], extension=f"defects_normalised_{deviation}")
    instances["project"] = projects[0]
    for i in range(1, len(projects)):
        tmp = instances_from_archive(projects[i], extension=f"defects_normalised_{deviation}")
        tmp["project"] = projects[i]
        instances = instances.append(tmp)
    return instances


def defective_individual(project, deviation=[0.3], top: int = None):
    """
    This method removes all rows for hashes where for a hash no defective components exist.
    In other words, keep metrics for all hashes where at least one component has been defective.
    Runs for an individual project.
    """
    csv = get_csv(project)

    instances = to_instances_with_defects(csv)
    instances_to_archive(instances, project, "defects")

    for dev in deviation:
        normalised = normalise_instances_for_size(instances, deviation=dev)
        instances_to_archive(normalised, project, f"defects_normalised_{dev}")
        if top is not None:
            top_normalised = normalised.groupby(by="hash", as_index=False, sort=False) \
                                       .count() \
                                       .sort_values(by=["defective"], ascending=False)
            top_normalised = top_normalised["hash"][:top]
            top = normalised.loc[normalised["hash"].isin(top_normalised)]
            instances_to_archive(top, project, f"top_defects_normalised_{dev}")


def defective_aggregated(projects, deviation):
    """
    This method does the same like defective_individual but for multiple projects to produce one, aggregated file.
    """
    aggregated = avg_distance_aggregated(projects)
    instances_to_archive(aggregated, "aggregated", f"defects_normalised_{deviation}")
