from pathlib import Path

project_root = Path(__file__).parent.parent
assets_dir = project_root / 'assets'
assets_dir.mkdir(exist_ok=True)


def output_file(file, ext):
    return str(assets_dir / (Path(file).stem + ext))


if __name__ == '__main__':
    print("project root:", project_root)
