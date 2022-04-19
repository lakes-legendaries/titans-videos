####################
Render Titans Videos
####################

This package provides a command-line interface (cli) to batch-render Titans Of
Eden videos that were created in blender.

**********
Quickstart
**********

#. Requirements:

   #. python3.7+
   #. ffmpeg

#. Get blender:

   .. code-block:: bash

      ./install-blender

#. Install python requirements

   .. code-block:: bash

      python -m venv .venv
      source .venv/bin/activate
      python -m pip install --upgrade pip
      python -m pip install -r requirements.txt

#. Render videos:

   .. code-block:: bash

      ./render

#. Make gifs

   .. code-block:: bash

      python make_gifs.py
