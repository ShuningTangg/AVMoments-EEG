# Experiment

This directory is reserved for the code used to run the AVMoments-EEG audiovisual event-perception experiment.

## Planned contents

- `run_experiment.py`: main experiment entry point.
- `experiment_config.yaml`: paths, timing parameters, display settings, and run-level options.

## Expected inputs

- Stimulus files and their metadata.
- A configuration file defining the experimental run.

## Expected outputs

- Trial-level event logs.
- Trigger and timing records needed to align the experiment with the EEG acquisition.

## Reproducibility notes

The public version should avoid machine-specific absolute paths. Keep participant identifiers, data locations, and run parameters in the configuration file rather than hard-coding them in the program.

The executable experiment files and usage command will be added after the original study code has been cleaned and checked for public release.
