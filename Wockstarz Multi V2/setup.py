#!/usr/bin/env python3
"""Wock-Multi — v2.0"""
import os
import sys

# Fix imports when launched via start.bat (cwd = Wock-Tools root)
_WOCK = os.path.dirname(os.path.abspath(__file__))
if _WOCK not in sys.path:
    sys.path.insert(0, _WOCK)

from lib.entry import run_wock

if __name__ == "__main__":
    run_wock()
