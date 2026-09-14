# Linux native testing

Linux/WSL physical validation is deferred. Bash-only reference layout:

```bash
mkdir -p ~/pytracker-test
cd ~/pytracker-test
rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
cd tobii-pytracker-demo
```

Reference invariants: Python 3.10; install package only from parent original clone (`pip install ..`); never install the demo repo; run examples from the demo-repository root; upstream MouseGaze config is `../configs/mouse_eyetracker_config.yaml`. Linux/WSL dependency details will be finalized after Windows native validation.
