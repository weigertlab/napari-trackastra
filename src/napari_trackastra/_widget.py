import napari
import numpy as np
import torch
import trackastra
from magicgui.widgets import (
    ComboBox,
    Container,
    FileEdit,
    PushButton,
    RadioButtons,
    create_widget,
)
from pathlib import Path
from napari.utils import progress
from trackastra.model import Trackastra
from trackastra.tracking import graph_to_ctc, graph_to_napari_tracks
from trackastra.utils import normalize

device = "cuda" if torch.cuda.is_available() else "cpu"


logo_path = Path(__file__).parent/"resources"/"trackastra_logo_small.png"

def _track_function(model, imgs, masks, mode="greedy", **kwargs):
    print("Normalizing...")
    imgs = np.stack([normalize(x) for x in imgs])
    print(f"Tracking with mode {mode}...")
    track_graph = model.track(
        imgs,
        masks,
        mode=mode,
        max_distance=128,
        progbar_class=progress,
        **kwargs,
    )  # or mode="ilp"
    # Visualise in napari
    df, masks_tracked = graph_to_ctc(track_graph, masks, outdir=None)
    napari_tracks, napari_tracks_graph, _ = graph_to_napari_tracks(track_graph)
    return track_graph, masks_tracked, napari_tracks


class Tracker(Container):
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self._viewer = viewer
        self._label = create_widget(widget_type="Label", 
                                    label=f'<img src="{logo_path}"></img>')
        self._image_layer = create_widget(label="Images", annotation="napari.layers.Image")

        self._mask_layer = create_widget(
            label="Masks", annotation="napari.layers.Labels"
        )
        self._model_type = RadioButtons(
            label="Model Type",
            choices=["Pretrained", "Custom"],
            orientation="horizontal",
            value="Pretrained",
        )
        self._model_pretrained = ComboBox(
            label="Pretrained Model",
            choices=tuple(trackastra.model.pretrained._MODELS.keys()),
            value="general_2d",
        )
        self._model_path = FileEdit(label="Model Path", mode="d")
        self._model_path.hide()
        self._run_button = PushButton(label="Track")

        self._linking_mode = ComboBox(
            label="Linking",
            choices=("greedy_nodiv", "greedy", "ilp"),
            value="greedy",
        )

        self._out_mask, self._out_tracks = None, None

        self._model_type.changed.connect(self._model_type_changed)
        self._model_pretrained.changed.connect(self._update_model)
        self._model_path.changed.connect(self._update_model)
        self._run_button.changed.connect(self._run)

        # append into/extend the container with your widgets
        self.extend(
            [
                self._label,
                self._image_layer,
                self._mask_layer,
                self._model_type,
                self._model_pretrained,
                self._model_path,
                self._linking_mode,
                self._run_button,
            ]
        )

    def _model_type_changed(self, event):
        if event == "Pretrained":
            self._model_pretrained.show()
            self._model_path.hide()
        else:
            self._model_pretrained.hide()
            self._model_path.show()

    def _update_model(self, event=None):
        if self._model_type.value == "Pretrained":
            self.model = Trackastra.from_pretrained(
                self._model_pretrained.value, device=device
            )
        else:
            self.model = Trackastra.from_folder(
                self._model_path.value, device=device
            )

    def _show_activity_dock(self, state=True):
        # show/hide activity dock if there is actual progress to see
        self._viewer.window._status_bar._toggle_activity_dock(state)

    def _run(self, event=None):
        self._update_model()

        if self.model is None:
            raise ValueError("Model not loaded")

        imgs = np.asarray(self._image_layer.value.data)
        masks = np.asarray(self._mask_layer.value.data)

        self._show_activity_dock(True)
        track_graph, masks_tracked, napari_tracks = _track_function(
            self.model, imgs, masks, mode=self._linking_mode.value
        )

        self._mask_layer.value.visible = False
        self._show_activity_dock(False)

        lays = tuple(
            lay for lay in self._viewer.layers if lay.name == "masks_tracked"
        )
        if len(lays) > 0:
            lays[0].data = masks_tracked
        else:
            self._viewer.add_labels(masks_tracked, name="masks_tracked")

        lays = tuple(
            lay for lay in self._viewer.layers if lay.name == "tracks"
        )
        if len(lays) > 0:
            lays[0].data = napari_tracks
        else:
            self._viewer.add_tracks(napari_tracks, name="tracks", tail_length=5)
        
