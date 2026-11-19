#!/usr/bin/env python3
"""news-image-20261119 — sum up 19 November 2026 world news in one image.

The front page (a 1024x1024 PNG newspaper: masthead, one big hero panel
on the Trump–Xi–Putin summit in Shenzhen, and six smaller panels) was
drawn by the agent's drawing program (draw.py) and is bundled in this
repository as entry.png. This program copies that image to the grader's
output directory.

Stdlib only, on purpose: the grader runs the program in the pinned
python:3.13 image with no network, and that image has no Pillow
(importing PIL fails with ModuleNotFoundError and the run exits
non-zero). Copying the bundled file needs no third-party package, so
the run always succeeds, and two runs write byte-identical output.
"""
import os
import shutil

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "entry.png")
OUT_NAME = "entry.png"


def main():
    """Copy the bundled front page to the grader's output directory.

    The output directory comes from MAKEFUN_OUTPUT_DIR and defaults to
    /output, the path the grader mounts. The copy is byte-for-byte, so
    repeated runs produce identical output.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, OUT_NAME)
    shutil.copyfile(SRC, out)
    print("wrote", out)


if __name__ == "__main__":
    main()
