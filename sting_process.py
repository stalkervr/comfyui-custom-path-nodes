class PromptPartJoin:
    """Node to combine 6 multiline text fields into a single STRING output."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "camera_shot": ("STRING", {"multiline": True, "default": "CAMERA_SHOT", "label": "CAMERA_SHOT"}),
                "main_character": ("STRING", {"multiline": True, "default": "MAIN_CHARACTER", "label": "MAIN_CHARACTER"}),
                "pose_action": ("STRING", {"multiline": True, "default": "POSE_ACTION", "label": "POSE_ACTION"}),
                "clovers_style": ("STRING", {"multiline": True, "default": "CLOVERS_STYLE", "label": "CLOVERS_STYLE"}),
                "advance_character": ("STRING", {"multiline": True, "default": "ADVANCE_CHARACTER", "label": "ADVANCE_CHARACTER"}),
                "env_photo_style": ("STRING", {"multiline": True, "default": "ENV_PHOTO_STYLE", "label": "ENV_PHOTO_STYLE"}),
            },
            "optional": {
                "separator": ("STRING", {"default": ", "}),
                "newline": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("POSITIVE",)
    FUNCTION = "combine_texts"
    CATEGORY = "Stalkervr/Text"

    def combine_texts(
        self,
        camera_shot,
        main_character,
        pose_action,
        clovers_style,
        advance_character,
        env_photo_style,
        separator=", ",
        newline=False
    ):
        parts = [
            camera_shot,
            main_character,
            pose_action,
            clovers_style,
            advance_character,
            env_photo_style,
        ]

        if newline:
            separator += "\n\n"

        combined = separator.join(parts)
        return (combined,)


class PromptPartConcatenation:
    """Node to concatenate two strings with an optional separator and newline."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "cam_view": ("STRING", {"default": "top view, pov, from above, dutch angle"}),
                "model_sys_teg": ("STRING", {"default": "score_9, score_8_up, score_7_up"}),
                "separator": ("STRING", {"default": ",,"}),
                "newline": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "concatenate_strings"
    CATEGORY = "Stalkervr/Text"

    def concatenate_strings(self, cam_view, model_sys_teg, separator="", newline=False):
        if newline:
            concatenated_string = f"{cam_view}{separator}\n\n{model_sys_teg}{separator}"
        else:
            concatenated_string = f"{cam_view}{separator}{model_sys_teg}{separator}"
        return (concatenated_string,)

class StringConcatenation:
    """Node to concatenate two inputs of type ANY with an optional separator and newline."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                "any_1": ("STRING", {"default": ""}),
                "any_2": ("STRING", {"default": ""}),
                "separator": ("STRING", {"default": ",,"}),
                "newline": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "concatenate_inputs"
    CATEGORY = "Stalkervr/Utility"

    def concatenate_inputs(self, any_1="", any_2="", separator="", newline=False):
        # Преобразуем входы в строки для конкатенации
        str_input1 = str(any_1)
        str_input2 = str(any_2)

        if newline:
            concatenated_output = f"{str_input1}{separator}\n{str_input2}"
        else:
            concatenated_output = f"{str_input1}{separator}{str_input2}"

        return (concatenated_output,)