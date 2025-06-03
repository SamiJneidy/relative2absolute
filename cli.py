import argparse
from .core import convert_imports

def main() -> None:
    parser = argparse.ArgumentParser(description='Convert relative imports to absolute')
    parser.add_argument('root', help='Root directory to process')
    args = parser.parse_args()
    convert_imports(args.root)
    