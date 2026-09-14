# Stimulus sources

The demo bundles three local photographs so the test does not depend on network access at runtime. They were exported from the `skimage.data` sample-image collection and normalized to 800x600 RGB PNG for this repository.

| Demo class | File | Source fixture |
| --- | --- | --- |
| human | `data/human/astronaut.png` | `skimage.data.astronaut()` |
| animal | `data/animal/cat.png` | `skimage.data.chelsea()` |
| object | `data/object/coffee.png` | `skimage.data.coffee()` |

These are test stimuli, not a scientific stimulus set. Before any real study, replace them with stimuli whose provenance, licensing, balancing and experimental selection criteria are appropriate for that study.
