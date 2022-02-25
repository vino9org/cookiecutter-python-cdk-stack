import os
import sys

cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(f"{cwd}/../runtime"))
sys.path.insert(0, os.path.abspath(f"{cwd}/../infrastructure"))
