import json

# class JsonFieldValueExtractor:
#     """
#     Node to extract a field value from a JSON string and convert it to multiple output formats:
#     STRING, INT, FLOAT, JSON, STRINGS, BATCH_ANY
#     """
#
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "required": {
#                 "json_input": ("STRING", {
#                     "multiline": True,
#                     "default": "{\n"
#                                "  \"name\": \"Harley\",\n"
#                                "  \"age\": 25,\n"
#                                "  \"power\": 9.5,\n"
#                                "  \"info\": {\"city\": \"Gotham\", \"zip\": \"10001\"},\n"
#                                "  \"tags\": [\"psycho\", \"funny\", \"dangerous\"],\n"
#                                "  \"scores\": [1, 2.5, 3, 4]\n"
#                                "}"
#                 }),
#                 "field_name": ("STRING", {"default": "tags", "multiline": False}),
#             }
#         }
#
#     RETURN_TYPES = ("STRING", "INT", "FLOAT", "STRING", "LIST", "BATCH_ANY")
#     RETURN_NAMES = ("STRING", "INT", "FLOAT", "JSON", "STRINGS", "BATCH_ANY")
#     OUTPUT_IS_LIST = (False, False, False, False, False, True)  # BATCH_ANY — batch-выход
#     FUNCTION = "extract_value"
#     CATEGORY = "Stalkervr/Json"
#
#     def extract_value(self, json_input, field_name):
#         try:
#             data = json.loads(json_input)
#
#             # Поддержка вложенных ключей, например: "info.city"
#             keys = field_name.split(".")
#             value = data
#             for key in keys:
#                 if isinstance(value, dict) and key in value:
#                     value = value[key]
#                 else:
#                     return (f"[ERROR] Field '{field_name}' not found", 0, 0.0, "{}", [], [])
#
#             # --- Приведение типов ---
#             str_value = str(value)
#
#             try:
#                 int_value = int(float(value))
#             except (ValueError, TypeError):
#                 int_value = 0
#
#             try:
#                 float_value = float(value)
#             except (ValueError, TypeError):
#                 float_value = 0.0
#
#             # --- JSON-представление значения ---
#             try:
#                 json_value = json.dumps(value, ensure_ascii=False, indent=2)
#             except Exception:
#                 json_value = "{}"
#
#             # --- Если значение — массив ---
#             str_list = []
#             batch_any = []
#             if isinstance(value, list):
#                 str_list = [str(v) for v in value]
#                 batch_any = value
#
#             return (str_value, int_value, float_value, json_value, str_list, batch_any)
#
#         except json.JSONDecodeError as e:
#             return (f"[ERROR] Invalid JSON: {e}", 0, 0.0, "{}", [], [])
#         except Exception as e:
#             return (f"[ERROR] {e}", 0, 0.0, "{}", [], [])

# import json
#
# class JsonFieldValueExtractor:
#     """
#     Node to extract a field value from a JSON string and convert it to multiple output formats:
#     STRING, INT, FLOAT, JSON, BATCH_ANY
#     """
#
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "required": {
#                 "json_input": ("STRING", {
#                     "multiline": False,
#                     "default": "{\n"
#                                "  \"name\": \"Harley\",\n"
#                                "  \"age\": 25,\n"
#                                "  \"power\": 9.5,\n"
#                                "  \"info\": {\"city\": \"Gotham\", \"zip\": \"10001\"},\n"
#                                "  \"tags\": [\"psycho\", \"funny\", \"dangerous\"],\n"
#                                "  \"scores\": [1, 2.5, 3, 4]\n"
#                                "}"
#                 }),
#                 "field_name": ("STRING", {"default": "tags", "multiline": False}),
#             }
#         }
#
#     RETURN_TYPES = ("STRING", "INT", "FLOAT", "STRING", "BATCH_ANY")
#     RETURN_NAMES = ("STRING", "INT", "FLOAT", "JSON", "BATCH_ANY")
#     OUTPUT_IS_LIST = (False, False, False, False, True)  # BATCH_ANY — batch-выход
#     FUNCTION = "extract_value"
#     CATEGORY = "Stalkervr/Json"
#
#     def extract_value(self, json_input, field_name):
#         try:
#             data = json.loads(json_input)
#
#             # Поддержка вложенных ключей, например: "info.city"
#             keys = field_name.split(".")
#             value = data
#             for key in keys:
#                 if isinstance(value, dict) and key in value:
#                     value = value[key]
#                 else:
#                     return (f"[ERROR] Field '{field_name}' not found", 0, 0.0, "{}", [])
#
#             # --- Приведение типов ---
#             str_value = str(value)
#
#             try:
#                 int_value = int(float(value))
#             except (ValueError, TypeError):
#                 int_value = 0
#
#             try:
#                 float_value = float(value)
#             except (ValueError, TypeError):
#                 float_value = 0.0
#
#             # --- JSON-представление значения ---
#             try:
#                 json_value = json.dumps(value, ensure_ascii=False, indent=2)
#             except Exception:
#                 json_value = "{}"
#
#             # --- Если значение — массив ---
#             batch_any = []
#             if isinstance(value, list):
#                 batch_any = value
#
#             return (str_value, int_value, float_value, json_value, batch_any)
#
#         except json.JSONDecodeError as e:
#             return (f"[ERROR] Invalid JSON: {e}", 0, 0.0, "{}", [])
#         except Exception as e:
#             return (f"[ERROR] {e}", 0, 0.0, "{}", [])

import json

class JsonFieldValueExtractor:
    """
    Node to extract a field value from a JSON string and convert it to multiple output formats:
    STRING, INT, FLOAT, JSON, VALUE_LIST, BATCH_ANY
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_input": ("STRING", {
                    "multiline": False,
                    "default": "{\n"
                               "  \"name\": \"Harley\",\n"
                               "  \"age\": 25,\n"
                               "  \"power\": 9.5,\n"
                               "  \"info\": {\"city\": \"Gotham\", \"zip\": \"10001\"},\n"
                               "  \"tags\": [\"psycho\", \"funny\", \"dangerous\"],\n"
                               "  \"scores\": [1, 2.5, 3, 4]\n"
                               "}"
                }),
                "field_name": ("STRING", {"default": "tags", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING", "INT", "FLOAT", "STRING", "LIST", "BATCH_ANY")
    RETURN_NAMES = ("STRING", "INT", "FLOAT", "JSON", "LIST", "BATCH")
    OUTPUT_IS_LIST = (False, False, False, False, False, True)  # BATCH_ANY — batch-выход
    FUNCTION = "extract_value"
    CATEGORY = "Stalkervr/Json"

    def extract_value(self, json_input, field_name):
        try:
            data = json.loads(json_input)

            # Поддержка вложенных ключей, например: "info.city"
            keys = field_name.split(".")
            value = data
            for key in keys:
                if isinstance(value, dict) and key in value:
                    value = value[key]
                else:
                    return (f"[ERROR] Field '{field_name}' not found", 0, 0.0, "{}", [], [])

            # --- Приведение типов ---
            str_value = str(value)

            try:
                int_value = int(float(value))
            except (ValueError, TypeError):
                int_value = 0

            try:
                float_value = float(value)
            except (ValueError, TypeError):
                float_value = 0.0

            # --- JSON-представление значения ---
            try:
                json_value = json.dumps(value, ensure_ascii=False, indent=2)
            except Exception:
                json_value = "{}"

            # --- Если значение — массив ---
            value_list = []
            batch_any = []
            if isinstance(value, list):
                value_list = value  # теперь список любых типов
                batch_any = value

            return (str_value, int_value, float_value, json_value, value_list, batch_any)

        except json.JSONDecodeError as e:
            return (f"[ERROR] Invalid JSON: {e}", 0, 0.0, "{}", [], [])
        except Exception as e:
            return (f"[ERROR] {e}", 0, 0.0, "{}", [], [])

