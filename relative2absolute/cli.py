import argparse
import sys
from relative2absolute.core import convert_imports

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert relative imports to absolute imports in Python files."
    )
    parser.add_argument(
        "--root", "-r",
        required=True,
        help="Path to the root package where absolute imports should begin"
    )

    args = parser.parse_args()

    try:
        convert_imports(root=args.root)
        print(f"Successfully converted imports in '{args.root}'")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
