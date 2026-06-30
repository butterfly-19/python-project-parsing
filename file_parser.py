import ast
from models import FunctionInfo, ClassInfo, FileInfo

class FileParser:
    def __init__(self, path):
        self.path = path
        self.source = open(path, encoding="utf-8").read()
        self.tree = ast.parse(self.source)

    def parse(self):
        imports, functions, classes, calls = [], [], [], []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                imports.extend([a.name for a in node.names])

            elif isinstance(node, ast.ImportFrom):
                for a in node.names:
                    imports.append(f"{node.module}.{a.name}")

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(self._parse_function(node))

            elif isinstance(node, ast.ClassDef):
                classes.append(self._parse_class(node))

            elif isinstance(node, ast.Call):
                name = self._call_name(node.func)
                if name:
                    calls.append(name)

        return FileInfo(
            path=self.path,
            imports=sorted(set(imports)),
            functions=functions,
            classes=classes,
            calls=sorted(set(calls))
        )

    def _parse_function(self, node):
        args = []
        for a in node.args.args:
            ann = ast.unparse(a.annotation) if a.annotation else None
            args.append({"name": a.arg, "type": ann})

        ret = ast.unparse(node.returns) if node.returns else None
        decs = [ast.unparse(d) for d in node.decorator_list]

        return FunctionInfo(
            node.name, args, ret, decs,
            ast.get_docstring(node),
            node.lineno, getattr(node, "end_lineno", node.lineno)
        )

    def _parse_class(self, node):
        methods = [self._parse_function(n) for n in node.body
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        return ClassInfo(
            node.name,
            [ast.unparse(b) for b in node.bases],
            [ast.unparse(d) for d in node.decorator_list],
            ast.get_docstring(node),
            methods
        )

    def _call_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            left = self._call_name(node.value)
            return f"{left}.{node.attr}" if left else node.attr
        return None
