from .path import (
    SavePath,
    PathPipeReroute,
    PathPipeIn,
    PathPipeOut
)

from .image_process import (
    ImageGridCropper,
    BatchImageCrop
)

from .context import (
    ContextPipeIn,
    ContextPipeOut,
    ContextPipeReroute
)

from .sting_process import (
    PromptPartJoin,
    PromptPartConcatenation,
    StringConcatenation
)

NODE_CLASS_MAPPINGS = {
    "PathPipeReroute": PathPipeReroute,
    "PathPipeOut": PathPipeOut,
    "PathPipeIn": PathPipeIn,
    "SavePath": SavePath,
    "ImageGridCropper": ImageGridCropper,
    "BatchImageCrop": BatchImageCrop,
    "ContextPipeIn": ContextPipeIn,
    "ContextPipeOut": ContextPipeOut,
    "ContextPipeReroute": ContextPipeReroute,
    "PromptPartJoin": PromptPartJoin,
    "PromptPartConcatenation": PromptPartConcatenation,
    "StringConcatenation": StringConcatenation,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PathPipeReroute": "Path Pipe Reroute",
    "PathPipeOut": "Path Pipe Out",
    "PathPipeIn": "Path Pipe In",
    "SavePath": "Save Path",
    "ImageGridCropper": "Image Grid Cropper",
    "BatchImageCrop": "Batch Image Crop",
    "ContextPipeIn": "Context Pipe In",
    "ContextPipeOut": "Context Pipe Out",
    "ContextPipeReroute": "Context Pipe Reroute",
    "PromptPartJoin": "Prompt Part Join",
    "PromptPartConcatenation": "Prompt Part Concatenation",
    "StringConcatenation": "String Concatenation",
}
