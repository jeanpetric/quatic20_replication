from __future__ import division
import pandas as pd
import sys
import re
from os import listdir
from os.path import join


def remove_df_columns_inplace(df, cols=[], first=False, last=False):
    if first is True:
        df.drop(df.columns[0], axis=1, inplace=True)
    if last is True:
        df.drop(df.columns[-1:], axis=1, inplace=True)
    if len(cols) > 0:
        df.drop(df.columns[cols], axis=1, inplace=True)


def try_or_none(f):
    def f_or_none(x):
        try:
            return f(x)
        except:
            return None
    return f_or_none


def clean_data(x, cols, parsers):
    result = {}
    for col, parser in zip(cols, parsers):
        if parser is not None:
            result[col] = try_or_none(parser)(x[col])
        else:
            result[col] = x[col]
    return pd.Series(result, index=cols)


def nonempty_str(str):
    return str if len(str) > 0 else None


def abstractness(x):
    try:
        return x["pckg:abstractClassCount"] / (x["pckg:abstractClassCount"] + x["pckg:concreteClassCount"])
    except:
        return 0


def instability(x):
    try:
        return x["pckg:fanOut"] / (x["pckg:fanIn"] + x["pckg:fanOut"])
    except:
        return 0


def distance(x):
    return abs(x["abstractness"] + x["instability"] - 1)


def get_hashes(root_dir):
    hashes = []
    for csv_path in listdir(root_dir):
        splits = csv_path.split("_")
        if len(splits) == 4:
            hashes.append(splits[2])
    return hashes


def process_csv(csv, hash, prev):
    df = pd.DataFrame(csv)
    remove_df_columns_inplace(df, last=True)
    df = df.apply(clean_data,
                  axis=1,
                  cols=["name", "pckg:fanIn", "pckg:abstractClassCount",
                        "pckg:concreteClassCount", "pckg:fanOut"],
                  parsers=[nonempty_str, int, int, int, int])
    df = df.dropna()
    df["abstractness"] = df.apply(abstractness, axis=1)
    df["instability"] = df.apply(instability, axis=1)
    df["distance"] = df.apply(distance, axis=1)
    df["hash"] = hash
    df["prev"] = prev
    return df


def main():
    project_name = sys.argv[1]
    hashes = get_hashes(join("../output", project_name))

    for hash in hashes:
        basename = "javametrics_" + project_name + "_" + hash
        ff_filename = join("../output", project_name, basename + ".csv")
        ffprev_filename = join("../output", project_name,
                               basename + "_ffprev.csv")
        ff_csv = []
        ffprev_csv = []
        try:
            ff_csv = pd.read_csv(ff_filename, delimiter=",")
            ffprev_csv = pd.read_csv(ffprev_filename, delimiter=",")
        except FileNotFoundError:
            print(ffprev_csv)
            continue
        ff_df = process_csv(ff_csv, hash, 0)
        ffprev_df = process_csv(ffprev_csv, hash, 1)

        out = join("../output", project_name + "_preprocess_.csv")
        pd.concat([ff_df, ffprev_df]).to_csv(out, mode="a", index=False)


main()
