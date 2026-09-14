#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/../.."
python examples/image_noise_demo/analyze_results.py
