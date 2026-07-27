import sys
from pathlib import Path

# The modules under test live at the repository root, which is only on
# sys.path when pytest is invoked as `python -m pytest` from that directory.
# Adding it here keeps the suite runnable via a plain `pytest` call too.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
