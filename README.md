# AVMoments-EEG

Experiment, EEG preprocessing, and technical validation code for the AVMoments-EEG dataset.

## Overview

This repository accompanies the AVMoments-EEG dataset and organizes the code used to run the experiment, preprocess the EEG recordings, and validate the released data. Behavioral-analysis code is not included in the current release.

## Repository structure

```text
AVMoments-EEG/
├── experiment/       # Experiment program and configuration
├── preprocessing/    # EEG preprocessing workflow
├── validation/       # ERP, GFP, topography, and decoding analyses
├── .gitignore
└── README.md
```

## Code organization

- [`experiment/`](experiment/) contains the stimulus-presentation program and experiment settings.
- [`preprocessing/`](preprocessing/) contains the EEG cleaning, ICA, epoch alignment, and ERP-construction workflow.
- [`validation/`](validation/) contains the analyses used for technical validation, including ERP/GFP/topography and decoding.

Each directory has its own README describing the intended inputs, outputs, and script organization.

## Getting started

The executable scripts, configuration files, software environment, and example commands will be added as the code is prepared for public release. Large raw and derived data files should not be committed to this repository.

## Data availability

The EEG dataset is maintained separately from this code repository. The public dataset link and access instructions will be added here when the data release is available.

## Citation

If you use this code or dataset, please cite the associated AVMoments-EEG article. Full citation details will be added after publication.

## Contact

Please use the repository's issue tracker for questions about the code or reproducibility.
