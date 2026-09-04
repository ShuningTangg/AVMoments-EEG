# Technical validation

This directory is reserved for analyses used to validate the quality and scientific utility of the AVMoments-EEG dataset. It does not contain a separate behavioral-analysis workflow.

## Planned organization

```text
validation/
├── figure3_erp/
│   └── plot_erp_gfp_topography.py
├── figure4_decoding/
│   ├── time_resolved_decoding.py
│   ├── cross_temporal_decoding.py
│   ├── cluster_permutation.py
│   └── plot_decoding_results.py
└── README.md
```

## ERP, GFP, and topography validation

The `figure3_erp/` workflow will reproduce the event-related potential, global field power, and scalp-topography results used for technical validation.

## Decoding validation

The `figure4_decoding/` workflow will contain time-resolved decoding, cross-temporal generalization, statistical testing, and result-plotting code.

## Reproducibility notes

Each analysis should document its input files, channel selection, time window, preprocessing assumptions, cross-validation scheme, scoring metric, statistical test, correction procedure, random seed, and output locations.

The executable validation scripts and example commands will be added after they have been checked against the public data products.
