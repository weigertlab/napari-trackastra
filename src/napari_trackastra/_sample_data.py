"""
This module is an example of a barebones sample data provider for napari.

It implements the "sample data" specification.
see: https://napari.org/stable/plugins/guides.html?#sample-data

Replace code below according to your needs.
"""
from __future__ import annotations

from pathlib import Path
import numpy
import tifffile
from trackastra import data


def test_data_bacteria() -> list[tuple[numpy.ndarray, dict, str]]:
    imgs, masks = data.example_data_bacteria() 
    return [(imgs, dict(name='img'), 'image'), (masks, dict(name='mask'), 'labels')]


def test_data_hela() -> list[tuple[numpy.ndarray, dict, str]]:
    imgs, masks = data.example_data_hela() 
    return [(imgs, dict(name='img'), 'image'), (masks, dict(name='mask'), 'labels')]
