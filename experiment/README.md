# AVMoments-EEG experiment

PsychoPy code for video presentation, attention checks, EEG triggers, and behavioral recording in AVMoments-EEG.

## Files

- `run_experiment.py`: main experiment script.
- `trigger_codes.txt`: acquisition trigger definitions.

## Requirements

- Python 3.10 and PsychoPy 2024.2.4 (reported acquisition environment).
- NumPy, OpenCV, and psutil.
- A compatible parallel port and driver; check the configured address `0x3EFC` before running.

## Video files

Videos are provided separately. Place them under `Videos/` in this directory:

```text
Videos/Exp1/type{1-16}/video_{1-56}.mp4
Videos/Exp2/Cond{1-3}/type{1-16}/video_{1-4}.mp4
```

Braces indicate numeric ranges, not literal folder names. Cond1: intact audiovisual; Cond2: intact visual with scrambled audio; Cond3: scrambled visual with intact audio.

## Run

Run from this directory:

```bash
python run_experiment.py
```

Enter the requested participant information, run, and part. Use run `0` and part `0` for practice; formal runs are `1-8`, each with parts `1-3`.

Space starts or resumes the experiment; during a video it requests a rest after the trial. Enter submits an attention response. Escape exits during video playback.

## Outputs

Behavioral CSV files and the participant-specific trial-list JSON are saved in `WatchVideo_csv_data/`. Keep the JSON across sessions to preserve the trial schedule. Reusing a participant/run/part filename appends to the existing CSV. Do not upload identifiable participant outputs to the code repository.
