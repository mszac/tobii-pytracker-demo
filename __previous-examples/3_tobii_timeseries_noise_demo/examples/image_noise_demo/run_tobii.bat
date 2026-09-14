@echo off
cd /d "%~dp0\..\.."
python examples\image_noise_demo\check_dataset.py || exit /b 1
tobii-pytracker --config_file configs/config_image_noise_demo.yaml --eyetracker_config_file configs/eyetracker_config.yaml --enable_eyetracker --loop_count 18
pause
