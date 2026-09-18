from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .normalized import load_normalized
from .prep import build_brief


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a local ReAion interview brief")
    parser.add_argument("export", help="normalized Calendar/Gmail JSON export")
    args = parser.parse_args()
    event, messages = load_normalized(args.export)
    print(json.dumps(asdict(build_brief(event, messages)), default=str, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
