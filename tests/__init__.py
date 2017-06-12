"kount"

from __future__ import absolute_import, unicode_literals, division, print_function
import sys
from pathlib import Path

root = str(Path(__file__).resolve().parents[1])
tests = str(Path(__file__).resolve().parents[0])
sys.path.append(root)
sys.path.append(tests)
