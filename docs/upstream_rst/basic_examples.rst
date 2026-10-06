===============
Basic Examples
===============

This section presents small experiment designs that demonstrate the built-in
image, text, and time-series dataset workflows in Tobii-Pytracker.  The
research-oriented examples are maintained in the companion
`tobii-pytracker-demo <https://github.com/mszac/tobii-pytracker-demo>`_
repository so that the documentation can describe the experimental logic while
the executable stimuli, launchers, validators, and Jupyter notebooks remain in
one reproducible example package.

For command-line options and output fields, see :doc:`commandline_usage`.  For
mouse-based gaze emulation, see :doc:`mouse_emulation`.  Saved-session loading
and visualization are described in :doc:`data_loading_visualization`.  The
notebooks linked from the example pages use the public analysis helpers
described in :doc:`data_analyzers` together with experiment-specific AOI logic
where required.

The technical three-image Test Demo from the companion repository is not listed
here because it verifies installation and interaction mechanics rather than a
scientific example design.

Raw signal recording
--------------------

Tobii-Pytracker can also be used without the PsychoPy stimulus interface to
record the continuous raw eye-tracker stream.  A typical command is::

   tobii-pytracker --enable_eyetracker --raw_data --disable_psychopy

The resulting ``raw_stream.csv`` contains timestamped raw eye-tracker samples.
See :doc:`commandline_usage` for the available recording options and output
format.

Image Data Examples
-------------------

.. toctree::
   :maxdepth: 1

   Image Semantic Demo <basic_example_image_semantic_demo>

Text Data Examples
------------------

.. toctree::
   :maxdepth: 1

   UX A/B Text Demo <basic_example_ux_ab_text_demo>
   Text Search Demo <basic_example_text_search_demo>

Time Series Data Examples
-------------------------

.. toctree::
   :maxdepth: 1

   Time-Series Noise Demo <basic_example_timeseries_noise_demo>
