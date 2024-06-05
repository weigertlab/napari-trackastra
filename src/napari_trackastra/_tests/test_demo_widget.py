import napari
from trackastra.data import example_data_bacteria

from napari_trackastra._widget import Tracker


def test_demo_widget():
    viewer = napari.Viewer()
    img, mask = example_data_bacteria()
    viewer.add_image(img)
    viewer.add_labels(mask)

    tracker = Tracker(viewer)
    viewer.window.add_dock_widget(tracker)
    tracker._run()
    tracker._save()


if __name__ == "__main__":
    test_demo_widget()
