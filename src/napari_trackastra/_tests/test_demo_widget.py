import napari
from trackastra.data import example_data_bacteria

from napari_trackastra._widget import Tracker


def test_demo_widget():
    viewer = napari.Viewer()
    img, mask = example_data_bacteria()
    viewer.add_image(img)
    viewer.add_labels(mask)

    viewer.window.add_dock_widget(Tracker(viewer))


def test_save():
    viewer = napari.Viewer()
    img, mask = example_data_bacteria()
    viewer.add_image(img)
    viewer.add_labels(mask)

    tracker = Tracker(viewer)
    viewer.window.add_dock_widget(tracker)
    tracker._run()
    tracker._save()
    # import ipdb

    # ipdb.set_trace()


if __name__ == "__main__":
    # test_demo_widget()
    test_save()
