Upstream Basic Examples RST integration
=======================================

This directory contains reStructuredText source prepared for inclusion in the
upstream ``sbobek/tobii-pytracker`` Sphinx documentation.

The target upstream directory is ``docs/``.  Copy the five ``basic_*.rst``
files from this directory into that upstream directory.  The supplied
``basic_examples.rst`` is intended to replace the current placeholder page.
No change to ``docs/index.rst`` is required because the upstream index already
includes ``basic_examples`` in its data-collection toctree.

Prepared pages
--------------

* ``basic_examples.rst`` -- category landing page and replacement for the
  current upstream placeholder;
* ``basic_example_image_semantic_demo.rst`` -- image-data example;
* ``basic_example_ux_ab_text_demo.rst`` -- controlled text-placement example;
* ``basic_example_text_search_demo.rst`` -- applied text-search example;
* ``basic_example_timeseries_noise_demo.rst`` -- time-series example.

The technical three-image Test Demo is intentionally not included because its
purpose is installation and interaction verification rather than demonstration
of a research design.

The experiment implementations, fixed stimuli, collection validators, Docker
bridge, and Jupyter notebooks remain in the companion
`tobii-pytracker-demo <https://github.com/mszac/tobii-pytracker-demo>`_
repository.  These RST pages link to that repository rather than duplicating
experiment code in the upstream documentation tree.
