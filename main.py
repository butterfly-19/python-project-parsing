import json
from dataclasses import asdict
from project_parser import ProjectParser
import sys

path = sys.argv[1] if len(sys.argv) > 1 else "."
parser = ProjectParser(path)

data = [asdict(x) for x in parser.parse()]

with open("parsed_project.json","w",encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Готово: parsed_project.json")
