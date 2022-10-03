"""
Summarise data for visualisation
"""
from pathlib import Path
import pandas as pd
from fmriprep_denoise.features.derivatives import get_qc_criteria
from fmriprep_denoise.visualization import utils


atlas_name = None
dimension = None
qc = 'stringent'
datasets = ['ds000228', 'ds000030']
fmriprep_version = 'fmriprep-20.2.1lts'
input_root = None
output_root = None


if __name__ == "__main__":
    input_root = utils.get_data_root() / "denoise-metrics" if input_root is None else Path(input_root)
    output_root = utils.get_data_root() / "denoise-metrics" if output_root is None else Path(output_root)
    qc = get_qc_criteria(qc)

    for dataset in datasets:
        print(f"Processing {dataset}...")
        ds_modularity = utils.prepare_modularity_plotting(dataset, fmriprep_version, atlas_name, dimension, input_root, qc)
        ds_qcfc = utils.prepare_qcfc_plotting(dataset, fmriprep_version, atlas_name, dimension, input_root)
        data = pd.concat([ds_qcfc, ds_modularity], axis=1)
        data.to_csv(output_root / f"{dataset}_{fmriprep_version.replace('.', '-')}_summary.tsv", sep="\t")
