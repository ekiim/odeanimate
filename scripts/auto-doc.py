#!/usr/bin/env python
from pathlib import Path
from sys import argv


def file_to_module(p):
    is_init = p.name == "__init__.py"
    if is_init:
        value = str(p.parent)
    else:
        value = str(p)[:-3]
    return value.replace("/", "."), is_init


def module_to_doc_file(module_name, path):
    return path / (module_name + ".md")


if __name__ == "__main__":
    try:
        prog, path, module = argv
    except:
        print("Error")
        exit(1)
    target = Path(path)
    for file in Path(module).glob(f"**/*.py"):
        module_name, is_init = file_to_module(file)
        doc_file = module_to_doc_file(module_name, target)
        doc_file.parent.mkdir(parents=True, exist_ok=True)
        doc_file.write_text(f"::: {module_name}\n")
