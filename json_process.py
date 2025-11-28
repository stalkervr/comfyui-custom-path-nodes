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
    CATEGORY = "Stalkervr/JSON"
    DESCRIPTION = "Node to extract a field value from a JSON string and convert it to multiple output formats"

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

class JsonFieldRemover:
    """
    Removes fields from JSON by paths separated with '|'
    Example: "action.props | action.sequence"
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_text": ("STRING", {"multiline": False}),
                "remove_fields": ("STRING", {
                    "default": "action.props | action.sequence",
                    "multiline": False
                }),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("json_cleaned",)
    FUNCTION = "clean_json"
    CATEGORY = "Stalkervr/JSON"
    DESCRIPTION = "Removes fields from JSON by paths separated with '|' Example: action.props | action.sequence"

    #
    # Helper: removes nested field by dot-path
    #
    def _remove_path(self, obj, path: str):
        parts = path.split(".")
        current = obj

        for i, part in enumerate(parts):
            if not isinstance(current, dict):
                return  # can't go deeper → skip
            if part not in current:
                return  # no such field → skip

            if i == len(parts) - 1:
                # last element → delete
                del current[part]
                return
            else:
                current = current[part]

    #
    # Main function
    #
    def clean_json(self, json_text, remove_fields):
        try:
            data = json.loads(json_text)
        except Exception:
            return (json_text,)  # return original if JSON invalid

        # parse list of fields
        field_paths = [
            f.strip()
            for f in remove_fields.split("|")
            if f.strip()
        ]

        for path in field_paths:
            self._remove_path(data, path)

        return (json.dumps(data, ensure_ascii=False, indent=2),)

class JsonFieldReplaceAdvanced:
    """
    JSON FIELD REPLACE (ADVANCED)
    ------------------------------------------------------------
    Примеры использования ноды:

    1) Замена простого поля
       ---------------------
       JSON:
       {
           "action": { "value": 10 }
       }

       field_path: action.value
       new_value: 999

       Результат:
       {
           "action": { "value": 999 }
       }


    2) Замена вложенного поля
       ------------------------
       JSON:
       {
           "action": { "params": { "value": 123 } }
       }

       field_path: action.params.value
       new_value: 42

       Результат:
       {
           "action": { "params": { "value": 42 } }
       }


    3) Замена в массиве по индексу
       ----------------------------
       JSON:
       {
           "items": [
               { "name": "A" },
               { "name": "B" }
           ]
       }

       field_path: items.1.name
       new_value: Updated

       Результат:
       {
           "items": [
               { "name": "A" },
               { "name": "Updated" }
           ]
       }


    4) Автоматическое создание отсутствующих объектов
       ------------------------------------------------
       JSON:
       {}

       field_path: a.b.c.d
       new_value: test

       Результат:
       {
           "a": {
               "b": {
                   "c": {
                       "d": "test"
                   }
               }
           }
       }


    5) Автоматическое определение типов
       ---------------------------------
       new_value: 123     -> число (int)
       new_value: 3.14    -> число (float)
       new_value: true    -> bool True
       new_value: false   -> bool False
       new_value: null    -> None
       new_value: hello   -> строка "hello"
    ------------------------------------------------------------
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_string": ("STRING", {"multiline": False}),
                "field_path": ("STRING", {"default": ""}),   # путь: a.b.c или arr.1.name
                "new_value": ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "replace_field"
    CATEGORY = "Stalkervr/JSON"
    DESCRIPTION = "Add new field in JSON or replace exists field value"

    # --- попытка привести новое значение к bool/int/float/null ---
    def cast_value(self, value: str):
        v = value.strip()
        v_low = v.lower()

        if v_low == "true":
            return True
        if v_low == "false":
            return False
        if v_low == "null":
            return None

        # integer?
        if (v.startswith("-") and v[1:].isdigit()) or v.isdigit():
            try:
                return int(v)
            except:
                pass

        # float?
        try:
            return float(v)
        except:
            pass

        return value  # оставить строкой

    # --- установка значения по пути ---
    def set_by_path(self, data, path_parts, value):
        obj = data

        for i, part in enumerate(path_parts):
            is_last = i == len(path_parts) - 1

            # индекс массива?
            if part.isdigit():
                idx = int(part)

                if not isinstance(obj, list):
                    raise Exception("Path error: trying to index non-array object")

                # расширяем массив если нужно
                while len(obj) <= idx:
                    obj.append({})

                if is_last:
                    obj[idx] = value
                else:
                    if not isinstance(obj[idx], (dict, list)):
                        obj[idx] = {}
                    obj = obj[idx]

            else:
                # ключ объекта
                if is_last:
                    obj[part] = value
                else:
                    if part not in obj or not isinstance(obj[part], (dict, list)):
                        obj[part] = {}
                    obj = obj[part]

    def replace_field(self, json_string, field_path, new_value):
        # парсим JSON
        try:
            data = json.loads(json_string)
        except Exception as e:
            return (f"JSON parse error: {str(e)}",)

        if not field_path:
            # просто вернуть форматированный JSON
            return (json.dumps(data, ensure_ascii=False, indent=4),)

        # преобразуем новое значение
        casted = self.cast_value(new_value)

        # путь: a.b.c → ["a","b","c"]
        path_parts = field_path.split(".")

        # установка
        try:
            self.set_by_path(data, path_parts, casted)
        except Exception as e:
            return (f"Path set error: {str(e)}",)

        # ✔ Возвращаем форматированный JSON
        formatted = json.dumps(data, ensure_ascii=False, indent=4)

        return (formatted,)
