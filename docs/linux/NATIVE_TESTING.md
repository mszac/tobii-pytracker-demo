# Linux native testing

Linux/WSL physical validation is deferred. Bash-only reference layout. After cloning, keep the shell in the original `tobii-pytracker` root:

```bash
mkdir -p ~/pytracker-test
cd ~/pytracker-test
rm -rf tobii-pytracker
git clone https://github.com/sbobek/tobii-pytracker.git
cd tobii-pytracker
git clone https://github.com/mszac/tobii-pytracker-demo.git
```

Reference invariants: Python 3.10; install the package only from the current original clone (`pip install .`); never install the demo repo; invoke demo scripts through `tobii-pytracker-demo/...`; launchers may internally switch to the demo root because config/data/output paths are demo-root-relative. Linux/WSL dependency closure remains pending physical validation.
