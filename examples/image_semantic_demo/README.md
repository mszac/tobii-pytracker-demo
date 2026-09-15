# Image Semantic Demo

12-image native classification experiment with three balanced categories: **BIOLOGICAL**, **OBJECT**, and **SCENE**.

Run from the parent `tobii-pytracker` root:

```bash
conda run --no-capture-output -n pytracker-env bash tobii-pytracker-demo/examples/image_semantic_demo/run_native.sh
```

This demo deliberately exposes only three response buttons. The upstream `NONE` class is removed locally for this demo only.

The 12 images are mixed at session start with constrained randomization: every consecutive set of three trials contains one image from each category, image order within each category is randomized, and the same category is never presented on two adjacent trials. There are no visible category blocks.

The current image remains visible until the participant clicks BIOLOGICAL, OBJECT, or SCENE.

Analysis is notebook-only:

```bash
conda run --no-capture-output -n pytracker-env jupyter lab tobii-pytracker-demo/examples/image_semantic_demo/analysis/image_semantic_analysis.ipynb
```
