import json
from pathlib import Path
from aiohttp import web

class DataFileLoader:
    @classmethod
    def INPUT_TYPES(cls):
        sources = cls._get_sources()

        # Соберём список всех имен из всех source-файлов
        all_names = set()
        for source in sources:
            all_names.update(cls._get_names_for_source(source))

        all_names = sorted(all_names)
        print(f"[DataFileLoader] INPUT_TYPES -> sources: {sources}")
        print(f"[DataFileLoader] INPUT_TYPES -> all names: {all_names}")

        return {
            "required": {
                "source": (sources, {"default": sources[0]}),
                "name": (all_names, {"default": all_names[0] if all_names else ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "get_description"
    CATEGORY = "Stalkervr/List"

    def get_description(self, source, name):
        print(f"[DataFileLoader] get_description called with source='{source}', name='{name}'")
        file_path = Path(__file__).parent / "data" / f"{source}.json"
        try:
            with open(file_path, encoding="utf-8") as f:
                content = json.load(f)
                for item in content:
                    if item.get("name") == name:
                        description = item.get("description", "")
                        print(f"[DataFileLoader] Description found: {description}")
                        return (description,)
        except Exception as e:
            print(f"[DataFileLoader] Ошибка при поиске description: {e}")
        return ("",)

    @staticmethod
    def _get_sources():
        data_dir = Path(__file__).parent / "data"
        sources = [f.stem for f in data_dir.glob("*.json")]
        print(f"[DataFileLoader] _get_sources -> {sources}")
        return sources

    @staticmethod
    def _get_names_for_source(source):
        file_path = Path(__file__).parent / "data" / f"{source}.json"
        if not file_path.exists():
            print(f"[DataFileLoader] _get_names_for_source -> файл не найден: {file_path}")
            return []
        try:
            with open(file_path, encoding="utf-8") as f:
                content = json.load(f)
                names = [item["name"] for item in content if "name" in item]
                return names
        except Exception as e:
            print(f"[DataFileLoader] Ошибка чтения файла '{file_path}': {e}")
            return []

# === HTTP API ===

DATA_DIR = Path(__file__).parent / "data"

async def handle_names_for_source(request):
    data = await request.post()
    source = data.get("source")
    print(f"[DataFileLoader] Запрошен список имён для source: '{source}'")

    file_path = DATA_DIR / f"{source}.json"
    if not file_path.exists():
        print(f"[DataFileLoader] Файл не найден: {file_path}")
        return web.json_response({"names": []})

    try:
        with open(file_path, encoding="utf-8") as f:
            content = json.load(f)
            names = [item["name"] for item in content if "name" in item]
            print(f"[DataFileLoader] Найдено имён: {len(names)} -> {names}")
            return web.json_response({"names": names})
    except Exception as e:
        print(f"[DataFileLoader] Ошибка при чтении файла '{file_path}': {e}")
        return web.json_response({"names": []})

def setup_routes(app):
    app.router.add_post("/datafile/names_for_source", handle_names_for_source)

try:
    import server
    setup_routes(server.PromptServer.instance.app)
    print("[DataFileLoader] Эндпоинт /datafile/names_for_source зарегистрирован")
except Exception as e:
    print(f"[DataFileLoader] Ошибка регистрации эндпоинта: {e}")
