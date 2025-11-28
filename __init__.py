import os

WEB_DIRECTORY = os.path.join(os.path.dirname(__file__), "web")

from .path import (
    SavePath,
    PathPipeReroute,
    PathPipeIn,
    PathPipeOut
)

from .image_process import (
    ImageGridCropper,
    BatchImageCrop,
    ImageAspectFixer,
    AutoAspectRatioAdjustFixer
)

from .context import (
    ContextPipeIn,
    ContextPipeOut,
    ContextPipeReroute
)

from .sting_process import (
    PromptPartJoin,
    PromptPartConcatenation,
    StringConcatenation,
    TextBlockProcessor,
    TextWrapper,
    ListToString,
    StringCollector
)

from .data_file_loader import (
    DataFileLoader
)

from .json_process import (
    JsonFieldValueExtractor,
    JsonFieldRemover,
    JsonFieldReplaceAdvanced
)

from .batch_process import (
    LoopAny,
    ListItemExtractor,
    AnyCollector
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
    "DataFileLoader": DataFileLoader,
    "TextBlockProcessor": TextBlockProcessor,
    "JsonFieldValueExtractor": JsonFieldValueExtractor,
    "JsonFieldRemover": JsonFieldRemover,
    "JsonFieldReplaceAdvanced": JsonFieldReplaceAdvanced,
    "LoopAny": LoopAny,
    "ListItemExtractor": ListItemExtractor,
    "TextWrapper": TextWrapper,
    "ListToString": ListToString,
    "StringCollector": StringCollector,
    "AnyCollector": AnyCollector,
    "ImageAspectFixer": ImageAspectFixer,
    "AutoAspectRatioAdjustFixer": AutoAspectRatioAdjustFixer,
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
    "DataFileSelector": "Data File Selector",
    "DataFileLoader": "Data File Loader",
    "TextBlockProcessor": "Text Block Processor",
    "JsonFieldValueExtractor": "JSON Field Value Extractor",
    "JsonFieldRemover": "JSON Field Remover",
    "JsonFieldReplaceAdvanced": "JSON Field Add & Replace",
    "LoopAny": "Loop Any",
    "ListItemExtractor": "List Item Extractor",
    "TextWrapper": "Text Wrapper",
    "ListToString": "List To String",
    "StringCollector": "String Collector",
    "AnyCollector": "Any Collector",
    "ImageAspectFixer": "Aspect Ratio Fixer (16:9 / 9:16)",
    "AutoAspectRatioAdjustFixer": "Aspect Ratio Fixer",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
