# Linux native testing

Linux/WSL physical validation is deferred. Bash-only reference layout:

```bash
mkdir -p ~/pytracker-test
cd ~/pytracker-test
rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone -b psychopy https://github.com/mszac/tobii-pytracker-examples.git
cd tobii-pytracker-examples
```

Reference invariants: Python 3.10; install package only from parent original clone (`pip install ..`); never install the examples repo; run examples from examples-root; upstream MouseGaze config is `../configs/mouse_eyetracker_config.yaml`. Linux/WSL dependency details will be finalized after Windows native validation.
