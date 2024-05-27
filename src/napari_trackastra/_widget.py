
import torch 
import numpy as np


import napari
from magicgui import magic_factory, magicgui
from magicgui.widgets import CheckBox, Container, create_widget, PushButton, FileEdit, ComboBox, RadioButtons
from pathlib import Path
from typing import List
from napari.utils import progress
import trackastra
from trackastra.utils import normalize
from trackastra.model import Trackastra
from trackastra.tracking import graph_to_ctc, graph_to_napari_tracks
 
device = "cuda" if torch.cuda.is_available() else "cpu"


def _track_function(model, imgs, masks, **kwargs):    
    print("Normalizing...")
    imgs = np.stack([normalize(x) for x in imgs])
    print("Tracking...")
    track_graph = model.track(imgs, masks, mode="greedy", 
                                max_distance=128,
                                progbar_class=progress,
                                **kwargs)  # or mode="ilp"
    # Visualise in napari
    df, masks_tracked = graph_to_ctc(track_graph,masks,outdir=None)
    napari_tracks, napari_tracks_graph, _ = graph_to_napari_tracks(track_graph)
    return track_graph, masks_tracked, napari_tracks


# logo = Path(__file__).parent/"resources"/"trackastra_logo_small.png"

# @magicgui(call_button="track", 
#           label_head=dict(widget_type="Label", label=f'<h1>Trackastra</h1>'),
#           model_path={"label": "Model Path", "mode": "d"},
#           persist=True)
# def track(label_head, img_layer: napari.layers.Image, mask_layer:napari.layers.Labels, model_path:Path, distance_costs:bool=False) -> List[napari.types.LayerDataTuple]:
#     if model_path.exists():
#         model = Trackastra.from_folder(model_path, device=device)
#     else: 
#         model = Trackastra.from_pretrained(model_path.name, device=device)
#     imgs = np.asarray(img_layer.data)
#     masks = np.asarray(mask_layer.data)
#     track_graph, masks_tracked, napari_tracks = _track_function(model, imgs, masks, use_distance=distance_costs)
#     mask_layer.visible = False
#     return [(napari_tracks, dict(name='tracks',tail_length=5), "tracks"), (masks_tracked, dict(name='masks_tracked', opacity=0.3), "labels")]



# if we want even more control over our widget, we can use
# magicgui `Container`
class Tracker(Container):
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self._viewer = viewer
        self._label = create_widget(widget_type="Label", label=f'<h1>Trackastra</h1>')
        self._image_layer = create_widget(label="Images", annotation="napari.layers.Image")

        self._out_mask, self._out_tracks = None, None

        self._mask_layer = create_widget(label="Masks", annotation="napari.layers.Labels")
        self._model_type = RadioButtons(label="Model Type", choices=["Pretrained", "Custom"], orientation="horizontal", value="Pretrained")
        self._model_pretrained = ComboBox(label="Pretrained Model", 
                                          choices=tuple(trackastra.model.pretrained._MODELS.keys()), value="general_2d")
        self._model_path = FileEdit(label="Model Path", mode="d")
        self._model_path.hide()
        self._run_button = PushButton(label="Track")


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

    def _run(self, event=None):
        self._update_model()

        if self.model is None:
            raise ValueError("Model not loaded")
        
        imgs = np.asarray(self._image_layer.value.data)
        masks = np.asarray(self._mask_layer.value.data)
        track_graph, masks_tracked, napari_tracks = _track_function(self.model, imgs, masks)
        self._mask_layer.value.visible = False

        
        lays = tuple(lay for lay in self._viewer.layers if lay.name=="masks_tracked")
        if len(lays) > 0:
            lays[0].data = masks_tracked
        else:
            self._viewer.add_labels(masks_tracked, name="masks_tracked")
        
        lays = tuple(lay for lay in self._viewer.layers if lay.name=="tracks")
        if len(lays) > 0:
            lays[0].data = napari_tracks
        else:
            self._viewer.add_tracks(napari_tracks, name="tracks")
        
    def _update_model(self, event=None):
        if self._model_type.value == "Pretrained":
            self.model = Trackastra.from_pretrained(self._model_pretrained.value, device=device)
        else:
            self.model = Trackastra.from_folder(self._model_path.value, device=device)