#!/usr/bin/env python
from __future__ import annotations

import argparse
import sys
from pathlib import Path

DEMO_ROOT = Path(__file__).resolve().parents[2]
if str(DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(DEMO_ROOT))

from tobii_pytracker import main as main_module
from tobii_pytracker.configs.custom_config import CustomConfig
from tobii_pytracker.utils.custom_logger import CustomLogger
from tools.demo_runtime_adapters import install_image_semantic_demo


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--config-file", default="examples/image_semantic_demo/config.native.yaml")
    p.add_argument("--eyetracker-config-file", default="../configs/mouse_eyetracker_config.yaml")
    p.add_argument("--loop-count", type=int, default=12)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    install_image_semantic_demo(main_module)
    main_module.LOGGER = CustomLogger("info", main_module.__name__).logger
    main_module.main(
        config=CustomConfig(args.config_file),
        loop_count=args.loop_count,
        eyetracker_config_file=args.eyetracker_config_file,
        enable_eyetracker=True,
        enable_voice=False,
        raw_data=False,
        enable_psychopy=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
