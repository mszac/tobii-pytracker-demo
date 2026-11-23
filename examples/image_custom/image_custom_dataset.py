"""Flat stimulus folder for the image_custom demo.

The upstream ImageDataset reads images from one subfolder per class and shuffles
them. This demo instead takes every image of a single folder, without
subfolders, and shows them in alphabetical order of the file name, so numbered
files such as 1_start.png, 2_task.png are presented in that order.

A flat folder carries no category, so the class of a sample is the file name
without its extension. That value lands in the `classification` column of the
recorded data.csv and identifies the stimulus of the trial. The response buttons
stay the ones of the image_semantic_demo and are listed in RESPONSE_BUTTONS.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from tobii_pytracker.datasets.custom_dataset import ImageDataset as UpstreamImageDataset

RESPONSE_BUTTONS = ["biological", "object", "scene"]
IMAGE_TYPES = (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".tif")


def list_stimuli(folder: Path) -> List[Path]:
    """Images of one folder in alphabetical order, case is ignored while sorting.

    Plain alphabetical order puts 10_ before 2_, so number your files 01_, 02_
    when a session has more than nine stimuli.
    """
    files = [p for p in Path(folder).iterdir()
             if p.is_file() and p.suffix.lower() in IMAGE_TYPES]
    return sorted(files, key=lambda p: p.name.lower())


class FlatImageDataset(UpstreamImageDataset):
    """Upstream image dataset reading one flat folder instead of class folders."""

    def _load_data(self) -> None:
        folder = Path(self.dataset_path)
        if not folder.is_dir():
            raise FileNotFoundError(f"Stimulus folder not found: {folder}")

        files = list_stimuli(folder)
        if not files:
            raise FileNotFoundError(
                f"No images in {folder}. Put your stimulus images in that folder, "
                f"supported types are {', '.join(IMAGE_TYPES)}")

        self.classes = list(RESPONSE_BUTTONS)
        samples: List[Dict[str, Any]] = []
        for path in files:
            sample = {"class": path.stem, "data": str(path), "id": path.name}
            if self.calculate_bboxes:
                sample["bboxes"] = self._compute_image_bboxes(str(path))
            samples.append(sample)
        self.data = samples


def install_image_custom_demo(main_module: Any) -> None:
    """Make the demo read one flat stimulus folder in alphabetical order."""
    main_module.ImageDataset = FlatImageDataset
