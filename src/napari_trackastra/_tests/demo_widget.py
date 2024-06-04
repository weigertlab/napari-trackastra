import napari
from trackastra.data import example_data_bacteria

from napari_trackastra._widget import Tracker
from trackastra.data import example_data_bacteria


def demo_widget():
    viewer = napari.Viewer()
    img, mask = example_data_bacteria()
    viewer.add_image(img)
    viewer.add_labels(mask)

    viewer.window.add_dock_widget(Tracker(viewer))


if __name__ == "__main__":
    demo_widget()

    napari.run()