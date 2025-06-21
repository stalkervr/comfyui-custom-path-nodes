import os
from aiohttp import web
from server import PromptServer

class SavePath:
    """
    A node that builds various folder paths and file names for a given character model,
    and outputs a pipeline tuple for connecting downstream pipe nodes.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "path_delimeter": ("STRING", {"default": os.sep}),
                "file_name_delimeter": ("STRING", {"default": "_"}),
                "base_work_path": ("STRING", {"default": "/home/stalkervr/Pictures/PhotoModel"}),
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
        "STRING","STRING","STRING","STRING","STRING",
        "STRING","STRING","STRING","STRING","STRING",
    )
    RETURN_NAMES = (
        "path_pipe",
        "CHARACTER_FOLDER",
        "CHARACTER_GRID_FOLDER",
        "CHARACTER_GRID_UP_FOLDER",
        "CHARACTER_GRID_CROP_FOLDER",
        "CHARACTER_DATASET_FOLDER",
        "CHARACTER_MODEL_FILE_NAME",
        "GRID_MODEL_FILE_NAME",
        "GRID_MODEL_FILE_UP_NAME",
        "GRID_MODEL_FILE_CROP_NAME",
        "DATASET_FILE_NAME",
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
    node = SavePath()
    inputs = node.INPUT_TYPES()["required"]
    values = [params.get(k) or cfg.get("default") for k, (_, cfg) in inputs.items()]
    result = node.concat(*values)
    return web.json_response(dict(zip(node.RETURN_NAMES, result)))

class PathPipeReroute:
    """
    Pipe node: pass through the ConcatPath pipeline data without any manual inputs.
    """
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"path_pipe": ("PATH_PIPE",)}}

    RETURN_TYPES = ("PATH_PIPE",)
    RETURN_NAMES = ("path_pipe",)
    FUNCTION = "execute"
    CATEGORY = "Stalkervr/Path"

    def execute(self, path_pipe):
        # Simply forward the pipeline tuple
        return (path_pipe,)

class PathPipeOut:
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

class PathPipeIn:
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
                "character_folder": ("STRING",),
                "character_grid_folder": ("STRING",),
                "character_grid_up_folder": ("STRING",),
                "character_grid_crop_folder": ("STRING",),
                "character_dataset_folder": ("STRING",),
                "character_model_file_name": ("STRING",),
                "grid_model_file_name": ("STRING",),
                "grid_model_file_up_name": ("STRING",),
                "grid_model_file_crop_name": ("STRING",),
                "dataset_file_name": ("STRING",),
            }
        }

    RETURN_TYPES = ("PATH_PIPE",)
    RETURN_NAMES = ("path_pipe",)
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
