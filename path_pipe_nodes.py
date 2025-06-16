
import os
from aiohttp import web
from server import PromptServer


class PipePathReroute:
    """
    Pipe node: pass through the ConcatPath pipeline data without any manual inputs.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"path_pipe": ("PATH_PIPE",)}}

    RETURN_TYPES = ("PATH_PIPE",)
    FUNCTION = "execute"
    CATEGORY = "Stalkervr/Path"

    def execute(self, path_pipe):
        # Simply forward the pipeline tuple
        return (path_pipe,)


class PipeFromConcatPath:
    """
    Pipe node: expand ConcatPath tuple into individual outputs.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"path_pipe": ("PATH_PIPE",)}}

    RETURN_TYPES = (
        "PATH_PIPE",
        "STRING","STRING","STRING","STRING","STRING",
        "STRING","STRING","STRING","STRING","STRING",
    )
    RETURN_NAMES = (
        "path_pipe",
        "character_folder",
        "character_grid_folder",
        "character_grid_up_folder",
        "character_grid_crop_folder",
        "character_dataset_folder",
        "character_model_file_name",
        "grid_model_file_name",
        "grid_model_file_up_name",
        "grid_model_file_crop_name",
        "dataset_file_name",
    )
    FUNCTION = "execute"
    CATEGORY = "Stalkervr/Path"

    def execute(self, path_pipe):
        (char_folder,
         char_grid_folder,
         char_grid_up_folder,
         char_grid_crop_folder,
         char_dataset_folder,
         char_model_file_name,
         grid_model_file_name,
         grid_model_file_up_name,
         grid_model_file_crop_name,
         dataset_file_name,
        ) = path_pipe

        return (
            path_pipe,
            char_folder,
            char_grid_folder,
            char_grid_up_folder,
            char_grid_crop_folder,
            char_dataset_folder,
            char_model_file_name,
            grid_model_file_name,
            grid_model_file_up_name,
            grid_model_file_crop_name,
            dataset_file_name,
        )


class PipeToConcatPath:
    """
    Connector-only node: aggregate individual ConcatPath outputs without text fields.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path_pipe": ("PATH_PIPE",),
            },
            "optional": {
                "character_folder": ("ANY",),
                "character_grid_folder": ("ANY",),
                "character_grid_up_folder": ("ANY",),
                "character_grid_crop_folder": ("ANY",),
                "character_dataset_folder": ("ANY",),
                "character_model_file_name": ("ANY",),
                "grid_model_file_name": ("ANY",),
                "grid_model_file_up_name": ("ANY",),
                "grid_model_file_crop_name": ("ANY",),
                "dataset_file_name": ("ANY",),
            }
        }

    RETURN_TYPES = ("PATH_PIPE",)
    FUNCTION = "execute"
    CATEGORY = "Stalkervr/Path"

    def execute(
        self,
        path_pipe,
        character_folder=None,
        character_grid_folder=None,
        character_grid_up_folder=None,
        character_grid_crop_folder=None,
        character_dataset_folder=None,
        character_model_file_name=None,
        grid_model_file_name=None,
        grid_model_file_up_name=None,
        grid_model_file_crop_name=None,
        dataset_file_name=None,
    ):
        orig = path_pipe or [None]*10
        out = [
            character_folder or orig[0],
            character_grid_folder or orig[1],
            character_grid_up_folder or orig[2],
            character_grid_crop_folder or orig[3],
            character_dataset_folder or orig[4],
            character_model_file_name or orig[5],
            grid_model_file_name or orig[6],
            grid_model_file_up_name or orig[7],
            grid_model_file_crop_name or orig[8],
            dataset_file_name or orig[9],
        ]
        return (out,)


NODE_CLASS_MAPPINGS = {
    "PipePathReroute": PipePathReroute,
    "PipeFromConcatPath": PipeFromConcatPath,
    "PipeToConcatPath": PipeToConcatPath,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PipePathReroute": "Pipe Path Reroute",
    "PipeFromConcatPath": "Pipe From Path Pipe",
    "PipeToConcatPath": "Pipe To Path Pipe",
}
