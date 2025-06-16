from .path_pipe_nodes import (
    PipePathReroute,
    PipeFromConcatPath,
    PipeToConcatPath
)

from .concat_path import ConcatPath

from .image_grid_cropper import (
    ImageGridCropper,
    BatchImageCrop
)

NODE_CLASS_MAPPINGS = {
    "PipePathReroute": PipePathReroute,
    "PipeFromConcatPath": PipeFromConcatPath,
    "PipeToConcatPath": PipeToConcatPath,
    "ConcatPath": ConcatPath,
    "ImageGridCropper": ImageGridCropper,
    "BatchImageCrop": BatchImageCrop,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PipePathReroute": "Pipe Path Reroute",
    "PipeFromConcatPath": "Pipe From Path Pipe",
    "PipeToConcatPath": "Pipe To Path Pipe",
    "ConcatPath": "Concat Path",
    "ImageGridCropper": "Image Grid Cropper",
    "BatchImageCrop": "Batch Image Crop",
}
