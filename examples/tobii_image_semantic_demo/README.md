# Tobii image semantic demo

12 committed images in three balanced categories: BIOLOGICAL, OBJECT and SCENE.

## Run

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/tobii_image_semantic_demo/run_native.sh
```

Expected collection markers: `NATIVE_IMAGE_SEMANTIC_COLLECTION_PASS`, `NATIVE_IMAGE_SEMANTIC_COLLECTION_COMPLETE`. Missing gaze no longer aborts a completed classification session.

## Analyze in Jupyter

```bash
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/tobii_image_semantic_demo/analysis/image_semantic_analysis.ipynb
```

The notebook resolves the demo output path independently of the shell working directory and analyzes only real collected data.
