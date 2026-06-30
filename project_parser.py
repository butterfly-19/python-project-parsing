from pathlib import Path
from file_parser import FileParser

EXCLUDED = {".git",".venv","venv","__pycache__","build","dist"}

class ProjectParser:
    def __init__(self, root):
        self.root = Path(root)

    def parse(self):
        result = []
        for p in self.root.rglob("*.py"):
            if any(part in EXCLUDED for part in p.parts):
                continue
            try:
                result.append(FileParser(str(p)).parse())
            except Exception as e:
                print(f"Ошибка в {p}: {e}")
        return result
