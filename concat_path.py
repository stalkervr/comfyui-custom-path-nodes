import os
from aiohttp import web
from server import PromptServer

class ConcatPath:
    """
    A node that builds various folder paths and file names for a given character model,
    and outputs a pipeline tuple for connecting downstream pipe nodes.

    INPUT TYPES (strings):
        path_delimeter               - delimiter for filesystem paths
        file_name_delimeter          - delimiter for file names
        base_work_path               - base working directory
        model_character_name         - name of the character model
        model_grid_folder            - grid folder name (relative)
        model_grid_up_folder         - grid up folder name (relative)
        model_crop_folder            - crop folder name (relative)
        model_dataset_folder         - dataset folder name (relative)
        postfix_file_pattern         - pattern appended to file names
        grid_prefix                  - prefix for grid file names
        grid_up_prefix               - prefix for grid-up file names
        crop_prefix                  - prefix for crop file names
        dataset_prefix               - prefix for dataset file names

    RETURN TYPES (tuple):
        PATH_PIPE                   - pipeline tuple for ConcatPath outputs
        character_folder
        character_grid_folder
        character_grid_up_folder
        character_grid_crop_folder
        character_dataset_folder
        character_model_file_name
        grid_model_file_name
        grid_model_file_up_name
        grid_model_file_crop_name
        dataset_file_name

    RETURN NAMES:
        path_pipe
        character_folder
        character_grid_folder
        character_grid_up_folder
        character_grid_crop_folder
        character_dataset_folder
        character_model_file_name
        grid_model_file_name
        grid_model_file_up_name
        grid_model_file_crop_name
        dataset_file_name

    FUNCTION:
        concat

    CATEGORY:
        Custom/Path
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path_delimeter": ("STRING", {"default": os.sep}),
                "file_name_delimeter": ("STRING", {"default": "_"}),
                "base_work_path": ("STRING", {"default": "/work"}),
                "model_character_name": ("STRING", {"default": "charA"}),
                "model_grid_folder": ("STRING", {"default": "grid"}),
                "model_grid_up_folder": ("STRING", {"default": "grid_up"}),
                "model_crop_folder": ("STRING", {"default": "crop"}),
                "model_dataset_folder": ("STRING", {"default": "dataset"}),
                "postfix_file_pattern": ("STRING", {"default": "%time_%seed"}),
                "grid_prefix": ("STRING", {"default": "GRID"}),
                "grid_up_prefix": ("STRING", {"default": "GRID_UP"}),
                "crop_prefix": ("STRING", {"default": "CROP"}),
                "dataset_prefix": ("STRING", {"default": "DATASET"}),
            }
        }

    RETURN_TYPES = (
        "PATH_PIPE",
        "ANY","ANY","ANY","ANY","ANY",
        "ANY","ANY","ANY","ANY","ANY",
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
    FUNCTION = "concat"
    CATEGORY = "Stalkervr/Path"

    def concat(
        self,
        path_delimeter,
        file_name_delimeter,
        base_work_path,
        model_character_name,
        model_grid_folder,
        model_grid_up_folder,
        model_crop_folder,
        model_dataset_folder,
        postfix_file_pattern,
        grid_prefix,
        grid_up_prefix,
        crop_prefix,
        dataset_prefix,
    ):
        # Helper to clean paths
        def clean_folder(name):
            return name.strip(path_delimeter)

        # Normalize base path
        bwp = base_work_path.rstrip(path_delimeter)
        name = clean_folder(model_character_name)

        # Clean subfolder names
        grid_f = clean_folder(model_grid_folder)
        grid_up_f = clean_folder(model_grid_up_folder)
        crop_f = clean_folder(model_crop_folder)
        dataset_f = clean_folder(model_dataset_folder)

        # Build folders
        character_folder = bwp + path_delimeter + name
        character_grid_folder = character_folder + path_delimeter + grid_f
        character_grid_up_folder = character_grid_folder + path_delimeter + grid_up_f
        character_grid_crop_folder = character_folder + path_delimeter + crop_f
        character_dataset_folder = (
            character_folder
            + path_delimeter + crop_f
            + path_delimeter + dataset_f
        ).lower()

        # Helper for file names: [prefix][delimiter][name][delimiter][postfix]
        def build_name(prefix):
            parts = [prefix, name, postfix_file_pattern]
            parts = [p for p in parts if p]
            return file_name_delimeter.join(parts)

        character_model_file_name = build_name("")
        grid_model_file_name = build_name(grid_prefix)
        grid_model_file_up_name = build_name(grid_up_prefix)
        grid_model_file_crop_name = build_name(crop_prefix)
        dataset_file_name = build_name(dataset_prefix)

        # Prepare pipeline tuple
        pipe_tuple = [
            character_folder,
            character_grid_folder,
            character_grid_up_folder,
            character_grid_crop_folder,
            character_dataset_folder,
            character_model_file_name,
            grid_model_file_name,
            grid_model_file_up_name,
            grid_model_file_crop_name,
            dataset_file_name,
        ]

        # Return pipeline tuple + individual outputs
        return (
            pipe_tuple,
            character_folder,
            character_grid_folder,
            character_grid_up_folder,
            character_grid_crop_folder,
            character_dataset_folder,
            character_model_file_name,
            grid_model_file_name,
            grid_model_file_up_name,
            grid_model_file_crop_name,
            dataset_file_name,
        )

# Optional API endpoint
@PromptServer.instance.routes.get("/concat_path")
async def _concat_api(request):
    params = request.rel_url.query
    node = ConcatPath()
    inputs = node.INPUT_TYPES()["required"]
    values = [params.get(k) or cfg.get("default") for k, (_, cfg) in inputs.items()]
    result = node.concat(*values)
    return web.json_response(dict(zip(node.RETURN_NAMES, result)))

# Export mappings
NODE_CLASS_MAPPINGS = {"ConcatPath": ConcatPath}
NODE_DISPLAY_NAME_MAPPINGS = {"ConcatPath": "Concat Path"}
