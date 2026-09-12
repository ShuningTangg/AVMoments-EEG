# EEG preprocessing

`preprocess_eeg.ipynb` processes continuous BrainVision EEG into session epochs and participant-level post-ICA NoReject FIF/NumPy files.

## Setup

Use Python 3.12 and install the dependencies in `requirements.txt` in a dedicated environment. The pinned versions were read from the local EEG_MNE environment on 2026-09-12; they are not a recovered historical environment lock. Open the notebook in a Jupyter-compatible editor and use a desktop plotting backend for interactive figures.

```bash
python -m pip install -r requirements.txt
```

## Run

1. Work from this directory. Set `DATA_ROOT` to the downloaded `BIDS_Data` folder and `OUTPUT_ROOT` to a separate results folder. The default relative input path matches the local Code_uploaded/Data layout and may need changing after download.
2. Set `subid` (default: `sub-003zgf`), `SESSION_IDS`, and any `MANUAL_BADS_BY_SESSION` entries.
3. Run the numbered cells in order through ICA inspection. After reviewing components, assign your list to `ICA_EXCLUDE` in a new code cell, then continue with ICA application. Do not rerun the initialization cell just to update this variable. `None` stops ICA application; use `[]` only after deciding that no components should be removed.
4. Continue through referencing, plotting, and export. Existing FIF outputs are protected by `OVERWRITE=False`; enable overwriting only for an intended rerun. Figures and logs may be overwritten or appended during repeated execution.

Events are read from BrainVision annotations. Corrections stored only in `_events.tsv` are not read, so this version does not cover the harmonized-event workflow for the first two participants. Input montage filenames must match the notebook's `_space-CapTrak_electrodes.tsv` convention.

## Outputs

`OUTPUT_ROOT/Epoched_Data/<subject>/` contains session epochs and figures. `OUTPUT_ROOT/ICA/<subject>/` contains post-ICA FIF/NumPy data and figures. A participant processing log is saved under `OUTPUT_ROOT`.

The workflow retains the source settings: 0.03-50 Hz filtering, a 50 Hz notch with 4 Hz width, 100 Hz sampling, -1.5 to 5 s epochs, a -0.1 to 0 s baseline, ICA fitted on a 1 Hz high-pass-filtered 0-3 s copy, and M1/M2 referencing.

Fixed trial alignment, trial rejection, and stimulus-level ERP averaging are not included. A limited input and epoch-export check was performed; the complete eight-session filtering/PyPREP/ICA pipeline has not been rerun for this packaging update.
