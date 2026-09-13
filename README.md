<div align="center">

# AVMoments-EEG

**A Large-Scale EEG Dataset of Naturalistic Audiovisual Event Perception**

Shuning Tang · Zitong Lu · Leiting Li · Dongwei Li

**10 participants · 64 channels · 960 video identities · 16 event categories**

Experiment and preprocessing code available · Baidu Netdisk data access available · Zenodo release in preparation

[Overview](#overview) · [Experimental design](#experimental-design) · [Code](#code) · [Getting started](#getting-started) · [Data access](#data-access) · [Citation](#citation)

</div>

## Overview

AVMoments-EEG records human scalp EEG during free viewing of 3-second naturalistic event videos derived from the Audiovisual Moments in Time dataset. The design combines a broad training stimulus set with densely repeated test videos under three audiovisual conditions.

The dataset supports research on dynamic event perception, audiovisual processing, neural encoding and decoding, and comparisons between brain responses and computational models. This repository provides the experiment program and an interactive EEG preprocessing notebook.

## Experimental design

Each participant completed eight sessions, with **10,368 planned trials per participant**.

- **Training set:** 896 distinct videos, comprising 56 videos per category, each presented three times with intact audiovisual content.
- **Test set:** 64 held-out video identities, comprising four videos per category. Each test video was presented 40 times in each of three conditions:

1. **Intact audiovisual:** original visual and auditory streams.
2. **Intact visual, scrambled audio:** original visual stream paired with temporally scrambled audio.
3. **Scrambled visual, intact audio:** spatially and temporally scrambled visual stream paired with the original audio.

Training and test sets contain distinct video identities. The same 64 test identities are shared across the three test conditions.

## Code

```text
AVMoments-EEG/
├── README.md
├── .gitignore
├── experiment/
│   ├── README.md
│   ├── run_experiment.py
│   └── trigger_codes.txt
└── preprocessing/
    ├── README.md
    ├── requirements.txt
    └── preprocess_eeg.ipynb
```

**[Experiment](experiment/README.md)** — PsychoPy video presentation, attention checks, parallel-port EEG triggers, and behavioral recording. See [trigger definitions](experiment/trigger_codes.txt) for the acquisition codes.

**[Preprocessing](preprocessing/README.md)** — MNE-Python filtering, bad-channel interpolation, epoching, ICA, mastoid referencing, and export of session-level and participant-level NoReject epochs.

## Getting started

Clone the repository:

```bash
git clone https://github.com/ShuningTangg/AVMoments-EEG.git
cd AVMoments-EEG
```

### Run the experiment

Use the experiment environment described in [experiment/README.md](experiment/README.md): Python 3.10 and PsychoPy 2024.2.4, with the additional dependencies listed there. Prepare the matching video files and configure a compatible parallel port before running:

```bash
cd experiment
python run_experiment.py
```

Videos are distributed separately; the program is configured for acquisition hardware and has no hardware-free demo mode.

### Preprocess EEG

Use a separate Python 3.12 analysis environment. From the repository root:

```bash
cd preprocessing
python -m pip install -r requirements.txt
```

Open [preprocess_eeg.ipynb](preprocessing/preprocess_eeg.ipynb) in a Jupyter-compatible editor, with `preprocessing/` as the working directory. Set `DATA_ROOT`, `OUTPUT_ROOT`, and the participant settings, then follow the numbered cells.

The default participant is `sub-003zgf`. ICA exclusions require manual review. This notebook reads BrainVision annotations and does not apply label corrections stored only in `_events.tsv`; see the preprocessing README before using recordings from the first two participants.

## Data access

The Zenodo dataset has not yet been published. The formal data link will be added here once it is available.

**Reserved dataset DOI:** `10.5281/zenodo.22227356`.

For the Chinese community, we also provide a [Baidu Netdisk link](https://pan.baidu.com/s/1JV4HvoSmkXrRnId3lX5pDA?pwd=sxx3) (access code: `sxx3`).

The dataset includes the following components, distributed separately from this code repository:

- `Video stimuli`: Due to licensing restrictions, access to the video stimuli used in this study can be obtained by contacting the corresponding authors (zitonglu@mit.edu or DongweiLi@bnu.edu.cn).
- `BIDS_Data/`: continuous BrainVision EEG, behavioral records, available ECG recordings, and metadata.
- `Epochs/`: session-level and post-ICA epoch derivatives in FIF and NumPy formats.
- `Re-arranged_Stimulus-Level_ERPs/`: responses averaged by video identity, with labels and channel names.

For data reuse, consult the archive's README and LICENSE. Trial-grid placeholders labeled `s9999` are not recorded EEG and must be excluded from analyses.

## Citation

When using the data or code, cite the dataset record and the accompanying manuscript:

> Tang, S., Lu, Z., Li, L., & Li, D. *AVMoments-EEG: A Large-Scale EEG Dataset of Naturalistic Audiovisual Event Perception.*

The manuscript citation will be updated with its publication details when available. After the data release, use the citation exported by Zenodo for the dataset version you use. For code reproducibility, also record the Git commit used in your analysis.

## Contact

For code questions and reproducibility issues, please [open a GitHub issue](https://github.com/ShuningTangg/AVMoments-EEG/issues).

For dataset or stimulus access, contact the corresponding authors:

- **Zitong Lu:** [zitonglu@mit.edu](mailto:zitonglu@mit.edu)
- **Dongwei Li:** [DongweiLi@bnu.edu.cn](mailto:DongweiLi@bnu.edu.cn)
