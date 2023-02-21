import json
import os

import mrvi
import scanpy as sc
from redun import File, task


@task()
def fit_mrvi(adata_in: File, config_in: File) -> File:
    adata = sc.read(adata_in.path)
    with open(config_in.path) as f:
        config = json.load(f)

    name = config.get("name", "example")
    sample_key = config.get("sample_key", None)
    batch_key = config.get("batch_key", None)
    model_kwargs = config.get("model_kwargs", {})
    train_kwargs = config.get("train_kwargs", {})

    mrvi.MrVI.setup_anndata(adata, sample_key=sample_key, categorical_nuisance_keys=[batch_key])
    model = mrvi.MrVI(adata, **model_kwargs)
    model.train(**train_kwargs)

    model_out = os.path.join("models", f"{name}.mrvi")
    model.save(dir_path=model_out, overwrite=True)
    return File(model_out)


@task()
def get_latent_mrvi(adata_in: File, model_in: File, config_in: File) -> File:
    adata = sc.read(adata_in.path)
    model = mrvi.MrVI.load(model_in.path, adata=adata)
    with open(config_in.path) as f:
        config = json.load(f)

    name = config.get("name", "example")

    adata.obsm["X_mrvi"] = model.get_latent_representation(adata)

    adata_out = os.path.join("data", f"{name}.mrvi.h5ad")
    adata.write(adata_out)
    return File(adata_out)
