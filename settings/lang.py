import os
import yaml
import datetime

from utils.globals import cache

class Language():
    _modules: dict[str,dict[str,str]]

    def __init__ (self, language: str):
        self._last_use = datetime.datetime.now()
        self.language = language
        self._load_text()

    def _load_text(self):
        self._update_last_use()
        for module_name in LANG_MODULES:
            path = os.path.join("settings", "languages", self.language, f"{module_name}.yaml")
            try: 
                with open(path, 'r') as yaml_file:
                    self._modules[module_name] = yaml.safe_load(yaml_file)
            except Exception as e:
                print(f"Error loading language file:\n{e}")
    
    def get_text(self, module: str, key: str):
        return self._modules[module][key]

    def get_language(self):
        self._update_last_use()
        return self.language

    def get_last_use(self):
        return self._last_use

    def _update_last_use(self):
        self._last_use = datetime.datetime.now()

LANG_CODES: list[str] = []
LANG_MODULES: list[str] = []

def load_lang_codes():
    path = os.path.join("settings", "languages")
    for file in os.listdir(path):
        LANG_CODES.append(file.title())

def load_lang_modules():
    path = os.path.join("settings", "languages", LANG_CODES[0])
    for file in os.listdir(path):
        LANG_MODULES.append(file.split(".")[0].upper())

def load_lang(lang: str, module: str, key: str) -> str:
    if lang in LANG_CODES:
        language = cache.get_language(lang)
        if language == None:
            language = cache.add_language(lang)

        return language.get_text(module, key)

    else: 
        raise Exception("Language not found")
