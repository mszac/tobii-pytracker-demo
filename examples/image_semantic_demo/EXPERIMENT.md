# Image Semantic Demo

## Design

The demo presents 12 distinct images from three semantic classes:

- 4 x BIOLOGICAL;
- 4 x OBJECT;
- 4 x SCENE.

The experiment uses response-gated trials: a stimulus remains visible until the participant selects one of the three semantic classes.

## Presentation order

There are no category blocks. At the start of every session the local demo adapter independently shuffles images within each class and creates a balanced interleaved sequence. Each consecutive group of three trials contains one image from every category, and adjacent trials cannot share a category.

This constrained randomization reduces obvious run-length/category-order effects while keeping the 4/4/4 balance intact.

## Response classes

Only **BIOLOGICAL**, **OBJECT**, and **SCENE** are displayed. Upstream `ImageDataset` normally appends `none`; this demo removes it locally before button creation without modifying the parent upstream repository.
