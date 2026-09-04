# EEG preprocessing

This directory contains the reproducible preprocessing workflow for the AVMoments-EEG recordings.

## Planned workflow

1. Load each recording session and standardize channel metadata.
2. Detect or import bad-channel annotations.
3. Fit independent component analysis (ICA).
4. Review and apply component-exclusion decisions.
5. Filter, epoch, and align trials to the released event grid.
6. Export cleaned epochs and stimulus-level ERP products used in validation.

## Planned contents

- `preprocess_sessions.py`: session-level preprocessing entry point.
- `fit_ica.py`: ICA fitting and diagnostic export.
- `apply_ica.py`: application of reviewed ICA exclusions.
- `align_trial_grid.py`: alignment of cleaned epochs to the common trial grid.
- `build_stimulus_level_erp.py`: construction of stimulus-level ERP products.
- `preprocessing_config.yaml`: preprocessing parameters and paths.
- `bad_channels.tsv`: reviewed bad-channel decisions.
- `ica_exclusions.tsv`: reviewed ICA-component exclusions.

## Reproducibility notes

Record all thresholds, filters, reference choices, epoch windows, random seeds, and manual-review decisions. Generated EEG data should be written outside the Git repository.

The scripts and configuration templates will be added after the study code has been cleaned, parameterized, and checked against the released dataset structure.
