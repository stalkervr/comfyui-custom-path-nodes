class PromptPartJoin:
    """Node to combine 4 multiline text fields into a single STRING output."""
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "cam_view": ("STRING", {
                    "multiline": True,
                    "default": "top view, pov, from above, dutch angle",
                }),
                "model_sys_teg": ("STRING", {
                    "multiline": True,
                    "default": "score_9, score_8_up, score_7_up",
                }),
                "style_description": ("STRING", {
                    "multiline": True,
                    "default": "",
                }),
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                }),
            },
            "optional": {
                "separator": ("STRING", {"default": ",,"}),
                "newline": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "combine_texts"
    CATEGORY = "Stalkervr/Text"

    def combine_texts(self, cam_view, model_sys_teg, style_description, prompt, separator="\n\n", newline=False):
        if newline:
            combined = "\n\n".join([cam_view, model_sys_teg, style_description, prompt])
        else:
            combined = separator.join([cam_view, model_sys_teg, style_description, prompt])
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