from redun import File, task

from tasks import fit_mrvi, get_latent_mrvi

redun_namespace = "mrvi.workflow"


@task()
def fit_and_get_latent_mrvi(adata_in: File, config_in: File) -> File:
    model_out = fit_mrvi(adata_in, config_in)
    adata_out = get_latent_mrvi(adata_in, model_out, config_in)
    return adata_out
