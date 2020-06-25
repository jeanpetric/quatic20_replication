import pandas as pd
import archive as arh
import os, os.path

projects = ["hadoop-common", "camel", "derby", "hive"]
commits_analysed = {"hadoop-common": 10509, "camel": 44609, "derby": 8269, "hive": 14377}
demographics = []

for project in projects:
    df = pd.read_csv(f"../input/{project}_ff2.csv", names=["dev", "file", "sha", "nb"], delimiter=",", encoding="latin1")
    nb_def_sha = len(set(df[df["file"].str.contains(".java")]["sha"]))
    nb_processed_sha = commits_analysed[project]
    df = arh.instances_from_archive(project)
    df["total_classes"] = df["pckg:concreteClassCount"] + df["pckg:abstractClassCount"]
    sums = df.groupby(by=["name"]).mean()
    nb_avg_classes = int(sums["total_classes"].sum())
    nb_avg_pckg = int(len(sums))
    demographics.append([project, nb_def_sha, nb_processed_sha, nb_avg_pckg, nb_avg_classes])

print(pd.DataFrame(demographics, columns=["Project", "# defects", "# analysed commits", "avg. package #", "avg. class #"]).to_latex(index=False))
