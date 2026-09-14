# Tobii image semantic demo

Expanded native image smoke/demo using the original `tobii-pytracker` runtime without modifying upstream source.

The experiment presents 12 committed local images in three balanced semantic classes:

- `BIOLOGICAL` — 4 images,
- `OBJECT` — 4 images,
- `SCENE` — 4 images.

The participant explores each image with MouseGaze and selects the best category. Upstream also shows `NONE`; it may be used when no category fits.

## Run

From the parent `tobii-pytracker` directory:

```bash
conda run --no-capture-output -n pytracker-env \
  bash tobii-pytracker-demo/examples/tobii_image_semantic_demo/run_native.sh
```

Successful collection ends with:

```text
NATIVE_IMAGE_SEMANTIC_COLLECTION_PASS
NATIVE_IMAGE_SEMANTIC_COLLECTION_COMPLETE
```

## Analyze

```bash
conda run --no-capture-output -n pytracker-env \
  python tobii-pytracker-demo/examples/tobii_image_semantic_demo/analysis/analyze_results.py
```

Successful analysis ends with:

```text
NATIVE_IMAGE_SEMANTIC_ANALYSIS_PASS
```

This is a functional demonstration of the image dataset + gaze-analysis pipeline, not a validated scientific stimulus set.
