# napari-trackastra

A napari plugin for cell tracking with [`trackastra`](https://github.com/weigertlab/trackastra).

https://github.com/weigertlab/napari-trackastra/assets/11042162/2751e81a-3992-4c60-bceb-c3f340732435


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

`trackastra` expects a timeseries of raw images and corresponding segmentations masks as input. We provide some demo data at
```
File > Open Sample > trackastra
```

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
