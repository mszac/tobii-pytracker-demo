#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../.."
tobii-pytracker --config_file configs/config_text_search_demo.yaml --eyetracker_config_file configs/eyetracker_config.yaml --enable_eyetracker --loop_count 12
