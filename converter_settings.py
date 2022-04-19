import json
import re


class ConverterSettings:
    def __init__(self):
        with open('./settings.json', 'r+') as settings_file:
            content = str.join('', settings_file.readlines())
            if not len(content):
                self.settings = ConverterSettings.create_default_settings()
                json.dump(self.settings, settings_file)
            self.settings = json.loads(content)

    def save_settings(self):
        with open('./settings.json', 'w') as settings_file:
            json.dump(self.settings, settings_file)

    def reset_settings(self):
        self.settings = ConverterSettings.create_default_settings()
        self.save_settings()
        print("Настройки сброшены")

    def set_size(self, size: str):
        if not re.match('^\d{1,10}:\d{1,10}', size):
            print(f"{size} в неподдерживаемом формате, используйте формат [width]:[height]")
        else:
            size = size.split(':')
            self.settings['picture size'] = [int(size[0]), int(size[1])]
            self.save_settings()
            print("Размер установлен!")

    @staticmethod
    def create_default_settings() -> dict:
        return {"font": "arial",
                "font size": 12,
                "space": 8,
                "color level": 6,
                "picture size": [],
                "ascii table": "' `.itfxzahao*#MW&8%B@$'"}
