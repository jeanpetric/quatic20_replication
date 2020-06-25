import zipfile
import pandas as pd
from pathlib import Path


def uncompress(what, where):
    with zipfile.ZipFile(what, "r") as f:
        f.extractall(where)


def compress(what, where):
    with zipfile.ZipFile(where, "w", zipfile.ZIP_DEFLATED) as f:
        f.write(what)


def get_csv(name):
    path = Path(f"/tmp/{name}.csv")
    if not path.is_file():
        uncompress(f"../output/{name}.zip", "/tmp")
    return pd.read_csv(path, delimiter=",",
                       dtype={"abstractness": "float64", "instability": "float64"})


def instances_from_archive(project, extension="defects"):
    extension = f"_{extension}_"
    return get_csv(f"{project}{extension}")


def instances_to_archive(instances, project, extension):
    instances.to_csv(f"/tmp/{project}_{extension}_.csv", sep=",", index=False)
    compress(f"/tmp/{project}_{extension}_.csv", f"../output/{project}_{extension}_.zip")
