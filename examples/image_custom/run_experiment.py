#!/usr/bin/env python
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

DEMO_ROOT = Path(__file__).resolve().parents[2]
DEMO_DIR = Path(__file__).resolve().parent
for entry in (str(DEMO_ROOT), str(DEMO_DIR)):
    if entry not in sys.path:
        sys.path.insert(0, entry)
os.chdir(DEMO_ROOT)  # config and dataset paths in the YAML are relative to the demo root

from tobii_pytracker import main as main_module
from tobii_pytracker.configs.custom_config import CustomConfig
from tobii_pytracker.utils.custom_logger import CustomLogger

from image_custom_dataset import install_image_custom_demo, list_stimuli


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--config-file", default="examples/image_custom/config.native.yaml")
    p.add_argument("--eyetracker-config-file", default="../configs/mouse_eyetracker_config.yaml")
    p.add_argument("--loop-count", type=int, default=0,
                   help="number of stimuli to show, 0 shows every image of the stimulus folder")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    config = CustomConfig(args.config_file)

    folder = Path(config.get_dataset_path())
    stimuli = list_stimuli(folder) if folder.is_dir() else []
    if not stimuli:
        print(f"No images found in {folder}")
        print("Put your stimulus images in that folder, one flat folder without subfolders")
        return 2

    loop_count = args.loop_count if args.loop_count > 0 else len(stimuli)
    loop_count = min(loop_count, len(stimuli))
    print(f"Stimulus folder: {folder}")
    print(f"Images found: {len(stimuli)}, shown in this run: {loop_count}")
    for number, path in enumerate(stimuli[:loop_count], start=1):
        print(f"  {number:>3}. {path.name}")

    install_image_custom_demo(main_module)
    main_module.LOGGER = CustomLogger("info", main_module.__name__).logger
    main_module.main(
        config=config,
        loop_count=loop_count,
        eyetracker_config_file=args.eyetracker_config_file,
        enable_eyetracker=True,
        enable_voice=False,
        raw_data=False,
        enable_psychopy=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
