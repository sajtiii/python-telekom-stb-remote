"""
Shared shim so the examples run straight from a checkout without installing.
If you `pip install -e .` the package instead, you can delete the
`import _bootstrap` line from each example.
"""

import os
import sys

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_REPO_ROOT, "src"))
