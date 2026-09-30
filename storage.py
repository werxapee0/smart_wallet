import json
from pathlib import Path


class FileStorage:
    """ Класс для безопасного сохранения и загрузки данных из JSON-файла. """

    def __init__(self, file_path: str = "data/wallet.json"):
        self.file_path = Path(file_path)
        # Если нет папки data, автоматически создаем ее
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_data(self) -> list[dict]:
        """ Загружает список транзакций из файла. """
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    def save_data(self, data: list[dict]) -> None:
        """ Сохраняет список транзакций в JSON-файл. """
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)