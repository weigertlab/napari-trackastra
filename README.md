# napari-trackastra

[![PyPI](https://img.shields.io/pypi/v/napari-trackastra.svg?color=green)](https://pypi.org/project/napari-trackastra)
[![tests](https://github.com/weigertlab/napari-trackastra/workflows/tests/badge.svg)](https://github.com/weigertlab/napari-trackastra/actions)
[![codecov](https://codecov.io/gh/weigertlab/napari-trackastra/branch/main/graph/badge.svg)](https://codecov.io/gh/weigertlab/napari-trackastra)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-trackastra)](https://napari-hub.org/plugins/napari-trackastra)

A napari plugin for cell tracking with [`trackastra`](https://github.com/weigertlab/trackastra).

![demo](https://github.com/weigertlab/napari-trackastra/assets/8866751/097eb82d-0fef-423e-9275-3fb528c20f7d)


## Installation

First install napari (and PyQt), e.g.
```
conda install -y -c conda-forge pyqt
pip install napari
```

Then install the latest version from PyPI with:
```
pip install napari-trackastra
```

Notes:
- On Windows currently only supported for Python 3.10.

## Usage

- `trackastra` expects a timeseries of raw images and corresponding segmentations masks as input.
- We provide some demo data at `File > Open Sample > trackastra`.
- Tracked cells can be directly saved to [Cell Tracking Challenge format](https://celltrackingchallenge.net/datasets/).
- Results can be drag-and-dropped back into napari for inspection. 

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
