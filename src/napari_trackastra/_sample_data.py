"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/stable/plugins/guides.html?#sample-data

Replace code below according to your needs.
"""

from __future__ import annotations

import numpy
from trackastra import data


def example_data_bacteria() -> list[tuple[numpy.ndarray, dict, str]]:
    imgs, masks = data.example_data_bacteria()
    return [
        (imgs, {"name": "img"}, "image"),
        (masks, {"name": "mask"}, "labels"),
    ]


def example_data_hela() -> list[tuple[numpy.ndarray, dict, str]]:
    imgs, masks = data.example_data_hela()
    return [
        (imgs, {"name": "img"}, "image"),
        (masks, {"name": "mask"}, "labels"),
    ]
