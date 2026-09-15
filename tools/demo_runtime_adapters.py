"""Local native-demo adapters layered over the unmodified upstream runtime.

The adapters are intentionally narrow:
- paragraph-aware TextDataset geometry for explicit blank lines;
- visual relabeling of the upstream text `none` response;
- balanced mixed ImageDataset ordering with the `none` response removed.
"""
from __future__ import annotations

import random
from collections import defaultdict
from typing import Any, Dict, List, Tuple

from psychopy import visual
from tobii_pytracker.datasets.custom_dataset import ImageDataset as UpstreamImageDataset
from tobii_pytracker.datasets.custom_dataset import TextDataset as UpstreamTextDataset


def _centered_bbox(x_min: float, y_min: float, x_max: float, y_max: float,
                   area_x: int, area_y: int) -> Dict[str, float]:
    width = max(1.0, x_max - x_min)
    height = max(1.0, y_max - y_min)
    return {
        "cx": float(x_min + width / 2.0 - area_x / 2.0),
        "cy": float(area_y / 2.0 - (y_min + height / 2.0)),
        "w": float(width),
        "h": float(height),
    }


class ParagraphTextDataset(UpstreamTextDataset):
    """Upstream-compatible text dataset that preserves explicit newlines in AOI geometry."""

    def draw_stimulus(self, window: visual.Window, sample: Dict[str, Any]) -> Dict[str, Any]:
        text = str(sample["data"])
        area_x, area_y = self.config.get_area_of_interest_size()
        wrap_width = int(area_x * self.wrap_frac)

        paragraph = visual.TextStim(
            win=window,
            text=text,
            pos=(0, 0),
            height=self.font_height,
            wrapWidth=wrap_width,
            alignText="left",
            color="white",
        )
        paragraph.draw()
        window.flip()

        space_stim = visual.TextStim(win=window, text=" ", height=self.font_height)
        space_width = float(space_stim.boundingBox[0] or (self.font_height * 0.3))

        # Preserve every explicit line, including intentionally blank separator lines.
        visual_lines: List[List[Tuple[str, float, float]]] = []
        line_heights: List[float] = []
        for explicit_line in text.split("\n"):
            words = explicit_line.split()
            if not words:
                visual_lines.append([])
                line_heights.append(float(self.font_height))
                continue

            measured: List[Tuple[str, float, float]] = []
            for word in words:
                stim = visual.TextStim(win=window, text=word, height=self.font_height, wrapWidth=None)
                width, height = stim.boundingBox
                measured.append((word, float(width), float(height)))

            current: List[Tuple[str, float, float]] = []
            current_width = 0.0
            for word, width, height in measured:
                added = width if not current else space_width + width
                if current and current_width + added > wrap_width:
                    visual_lines.append(current)
                    line_heights.append(max(h for _, _, h in current))
                    current = [(word, width, height)]
                    current_width = width
                else:
                    current.append((word, width, height))
                    current_width = width if len(current) == 1 else current_width + added
            if current:
                visual_lines.append(current)
                line_heights.append(max(h for _, _, h in current))

        total_height = sum(line_heights)
        y_cursor = (area_y - total_height) / 2.0
        words_out: List[Dict[str, Any]] = []
        lines_out: List[Dict[str, Any]] = []

        for line, line_height in zip(visual_lines, line_heights):
            if not line:
                y_cursor += line_height
                continue
            line_width = sum(width for _, width, _ in line) + space_width * max(0, len(line) - 1)
            left_x = (area_x - line_width) / 2.0
            lines_out.append({
                "text": " ".join(word for word, _, _ in line),
                "conf": 1.0,
                "bbox": _centered_bbox(left_x, y_cursor, left_x + line_width,
                                         y_cursor + line_height, area_x, area_y),
            })
            x_cursor = left_x
            for word, width, height in line:
                y_min = y_cursor + (line_height - height) / 2.0
                words_out.append({
                    "word": word,
                    "conf": 1.0,
                    "bbox": _centered_bbox(x_cursor, y_min, x_cursor + width,
                                             y_min + height, area_x, area_y),
                })
                x_cursor += width + space_width
            y_cursor += line_height

        return {"words": words_out, "lines": lines_out}


class MixedNoNoneImageDataset(UpstreamImageDataset):
    """Image dataset with three response classes and balanced session-level mixing."""

    def _load_data(self) -> None:
        super()._load_data()
        self.classes = [str(c) for c in self.classes if str(c).casefold() != "none"]

        by_class: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for sample in self.data:
            cls = str(sample["class"])
            if cls.casefold() != "none":
                by_class[cls].append(sample)

        rng = random.SystemRandom()
        for samples in by_class.values():
            rng.shuffle(samples)

        ordered: List[Dict[str, Any]] = []
        previous: str | None = None
        while any(by_class.values()):
            cycle = [cls for cls, samples in by_class.items() if samples]
            rng.shuffle(cycle)
            if previous is not None and len(cycle) > 1 and cycle[0] == previous:
                swap = next(i for i, cls in enumerate(cycle[1:], start=1) if cls != previous)
                cycle[0], cycle[swap] = cycle[swap], cycle[0]
            for cls in cycle:
                ordered.append(by_class[cls].pop())
                previous = cls
        self.data = ordered


def install_text_demo(main_module: Any, unknown_label: str = "I DON'T KNOW") -> None:
    """Install paragraph-aware text geometry and relabel the upstream `none` button."""
    main_module.TextDataset = ParagraphTextDataset
    original_prepare_buttons = main_module.gui.prepare_buttons

    def prepare_buttons(config: Any, window: Any, dataset: Any):
        buttons = original_prepare_buttons(config, window, dataset)
        for _rect, text, label in buttons:
            if str(label).casefold() == "none":
                text.text = unknown_label
        return buttons

    main_module.gui.prepare_buttons = prepare_buttons


def install_image_semantic_demo(main_module: Any) -> None:
    """Remove the upstream `none` class and guarantee balanced category interleaving."""
    main_module.ImageDataset = MixedNoNoneImageDataset
