#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../.."
python examples/image_noise_demo/check_dataset.py
tobii-pytracker --config_file configs/config_image_noise_demo.yaml --eyetracker_config_file configs/eyetracker_config.yaml --enable_eyetracker --loop_count 18
