import napari
import pytest
from trackastra.data import example_data_bacteria

from napari_trackastra._widget import Tracker


@pytest.mark.parametrize("output_format", ["CTC", "GEFF"])
def test_demo_widget(output_format):
    viewer = napari.Viewer()
    img, mask = example_data_bacteria()
    scale = (1, 1.2, 1.2)
    viewer.add_image(img, scale=scale)
    viewer.add_labels(mask, scale=scale)

    # Test widget only on CPU
    tracker = Tracker(viewer, device="cpu")
    viewer.window.add_dock_widget(tracker)
    tracker._run()

    tracker._save_format.value = output_format
    tracker._save()


if __name__ == "__main__":
    test_demo_widget("GEFF")
    napari.run()
