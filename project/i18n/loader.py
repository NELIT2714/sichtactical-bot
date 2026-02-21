import yaml
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[2]
LOCALES_PATH = BASE_PATH / "resources" / "locales"


class LocaleStorage:
    def __init__(self):
        self._locales = {}

    def load(self):
        for file in LOCALES_PATH.glob("*.yml"):
            with open(file, "r", encoding="utf-8") as f:
                self._locales[file.stem] = yaml.safe_load(f)

    def get(self, lang: str) -> dict:
        return self._locales.get(lang) or self._locales["ru"]
