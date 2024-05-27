import numpy as np
import napari
from napari_trackastra._widget import Tracker
from trackastra.data import test_data_bacteria


def test_widget():
    viewer = napari.Viewer()
    img, mask = test_data_bacteria()
    viewer.add_image(img)
    viewer.add_labels(mask)

    viewer.window.add_dock_widget(Tracker(viewer))

    

if __name__ == "__main__":
    test_widget()

    napari.run()
    