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
    CATEGORY = "Stalkervr/Text"

    def concatenate_inputs(self, any_1="", any_2="", separator="", newline=False):
        # Преобразуем входы в строки для конкатенации
        str_input1 = str(any_1)
        str_input2 = str(any_2)

        if newline:
            concatenated_output = f"{str_input1}{separator}\n{str_input2}"
        else:
            concatenated_output = f"{str_input1}{separator}{str_input2}"

        return (concatenated_output,)

class TextBlockProcessor:
    """Node to split text by newline, wrap each block with prefix/suffix, and return final string + block count."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {"multiline": False, "default": "Line 1\nLine 2\nLine 3"}),
                "prefix": ("STRING", {"multiline": False, "default": "[PREFIX] "}),
                "suffix": ("STRING", {"multiline": False, "default": " [SUFFIX]"}),
            }
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("FINAL_PROMPT", "COUNT")
    FUNCTION = "process_text"
    CATEGORY = "Stalkervr/Text"

    def process_text(self, input_text, prefix, suffix):
        separator = "\n"
        lines = [line.strip() for line in input_text.splitlines() if line.strip()]
        processed_lines = [f"{prefix}{line}{suffix}{'|'}" for line in lines]
        final_text = separator.join(processed_lines)
        if final_text:
            final_text = final_text[:-1]
        count = len(processed_lines)
        return (final_text, count)

class TextWrapper:
    """
    Node to wrap input text with a prefix and suffix.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prefix": ("STRING", {"multiline": False, "default": ""}),
                "input_text": ("STRING", {"multiline": False, "default": ""}),
                "suffix": ("STRING", {"multiline": False, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "wrap_text"
    CATEGORY = "Stalkervr/Text"

    def wrap_text(self, prefix, input_text, suffix):
        prefix = prefix.strip()
        input_text = input_text.strip()
        suffix = suffix.strip()
        parts = [prefix, input_text, suffix]
        combined = " ".join([p for p in parts if p])

        return (combined,)

class ListToString:
    """
    Node to join a list of strings into a single string using a specified separator.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string_list": ("LIST", {"default": []}),
                "separator": ("STRING", {"default": ", "}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("OUTPUT",)
    FUNCTION = "join_list"
    CATEGORY = "Stalkervr/Text"

    def join_list(self, string_list, separator):
        safe_list = [str(item) for item in string_list]
        combined = separator.join(safe_list)
        return (combined,)


class StringCollector:
    """
    Accumulates STRING inputs into a single list.
    Uses INPUT_IS_LIST=True so it can collect multiple inputs over time.
    """

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "text_input": ("STRING", {}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    RETURN_TYPES = ("LIST",)
    RETURN_NAMES = ("collected_texts",)
    INPUT_IS_LIST = True
    OUTPUT_NODE = True
    FUNCTION = "collect_texts"
    CATEGORY = "Stalkervr/Text"

    def collect_texts(self, unique_id=None, extra_pnginfo=None, **kwargs):
        values = []
        if "text_input" in kwargs:
            for val in kwargs["text_input"]:
                try:
                    if isinstance(val, str):
                        values.append(val.strip())
                    elif isinstance(val, list):
                        values.extend([str(v).strip() for v in val])
                    else:
                        values.append(str(val).strip())
                except Exception:
                    values.append(str(val).strip())
                    pass

        if extra_pnginfo and isinstance(extra_pnginfo, list) and extra_pnginfo:
            if isinstance(extra_pnginfo[0], dict) and "workflow" in extra_pnginfo[0]:
                workflow = extra_pnginfo[0]["workflow"]
                node = next((x for x in workflow["nodes"] if str(x["id"]) == unique_id[0]), None)
                if node:
                    node["widgets_values"] = [values]

        return {"ui": {"text": values}, "result": (values,)}
