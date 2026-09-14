# Native text smoke demo

> Iteration tests must start from fresh sibling repository clones. The authoritative Windows command sequence is `docs/windows/NATIVE_TESTING.md`; Linux is documented separately in `docs/linux/NATIVE_TESTING.md`.

This bundle is owned by the examples layer. It does not modify or vendor `src/tobii_pytracker`.

## Reference directory layout

Clone the original package, then clone the demo repository inside it:

```text
workspace/
├── tobii-pytracker/          # original sbobek runtime authority
└── tobii-pytracker-demo/ # demo config/data/analysis authority
```

Install `tobii-pytracker` only from the original clone. Run the commands below from the **demo repository root**.

## N3-A — collection without eyetracker

Even when eyetracking is disabled, current upstream inspects the eyetracker YAML during GUI startup. Supply the original upstream MouseGaze config explicitly:

```bash
tobii-pytracker \
  --config_file examples/smoke_text/config.native.yaml \
  --eyetracker_config_file ../tobii-pytracker/configs/mouse_eyetracker_config.yaml \
  --loop_count 4
```

Expected result: a new `output/<timestamp>/data.csv` with four trial rows after completing all four stimuli.

## N4-A — collection with original upstream MouseGaze

```bash
tobii-pytracker \
  --config_file examples/smoke_text/config.native.yaml \
  --eyetracker_config_file ../tobii-pytracker/configs/mouse_eyetracker_config.yaml \
  --enable_eyetracker \
  --loop_count 4
```

Native MouseGaze uses the original upstream control contract: hold the **RIGHT mouse button** while moving the pointer to produce gaze samples. Release RIGHT before using LEFT CLICK for the response; upstream MouseGaze also assigns a simultaneous LEFT+RIGHT press to its blink control.

## Output smoke analysis

```bash
python examples/smoke_text/analysis/smoke_analysis.py --output-root output
```

The script selects the lexicographically newest timestamped session, checks the current upstream GUI output columns, requires exactly four completed trial rows by default and reports row/response/gaze counts.

## Docker reuse contract

The CSV dataset and experiment intent are canonical shared assets. A future Docker wrapper may use a Docker-specific main/tracker config to change input instructions and use the direct-mouse CTRL overlay, but it must keep the same stimuli, response labels, output schema and analysis script/notebook compatibility.
