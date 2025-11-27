#!/usr/bin/env python3
import sys
from pathlib import Path

# Add src/ to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from lisp.repl import repl

if __name__ == "__main__":
    repl()
