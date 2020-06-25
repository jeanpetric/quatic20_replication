from __future__ import division
import pandas as pd
import sys
import re
from os import listdir
from os.path import join


def to_package(x, col, prefix=[r"src/main/java/", r"src/java/"], postfix=[]):
    result = None
    name = x[col].split(r"/")[:-1]
    pre = next((pre for pre in prefix if re.match(pre, x[r"file"])), None)
    if len(name) > 0 and pre is not None:
        pre = r"^.*" + re.sub(r"/", r".", pre)
        name = ".".join(name)
        result = re.sub(pre, "", name)
    return result


def match(x, df):
    index = df.index[(df["hash"] == x["hash"]) & (df["name"] == x["package"])]
    if len(index.tolist()) == 0:
        index = []
    return index


def main():
    project_name = sys.argv[1]
    prefix_patterns = {"hadoop-common": [r"src/main/java/", r"src/java/"],
                       "derby": [r"java/engine/", r"java/build/", r"java/client/",
                                 r"java/drda/", r"java/optional/", r"java/org.apache.derby",
                                 r"java/shared/"],
                        "camel": [r"camel-api/src/main/java/", r"camel-core/src/main/java/",
                                  r"components-starter/camel-core-starter/src/main/java/",
                                  r"components/camel-.*/src/main/java/",
                                  r"core/camel-.*/src/main/java/",
                                  r"platforms/string-boot/.*/src/main/java/"],
                        "hive": [r".*/src/java/", r".*/src/main/java/",
                                 r".*/src/.*/gen-javabean/"]}
    prefix_pattern = prefix_patterns[project_name]
    process_file = join("../output", project_name + "_preprocess_.csv")
    process_csv = pd.read_csv(process_file, delimiter=",")

    ff_csv = pd.read_csv(join("../input", project_name + "_ff2.csv"), delimiter=",", encoding='latin-1', names=["developer", "file", "hash", "size"])
    ff_csv["package"] = ff_csv.apply(to_package, axis=1, col="file", prefix=prefix_pattern)
    ff_csv = ff_csv.dropna()

    merged = process_csv.merge(ff_csv, on="hash", how="left")

    indexes = merged.index[(merged["name"] == merged["package"])]
    merged["defective"] = 0
    merged.loc[indexes, "defective"] = 1

    merged.to_csv(project_name + ".csv", index=False)


main()
