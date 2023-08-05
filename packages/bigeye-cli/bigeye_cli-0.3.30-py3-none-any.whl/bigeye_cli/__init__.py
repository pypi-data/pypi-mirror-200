import os
from pathlib import Path

HOME_DIR = str(Path.home())
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CRED_FILE = os.path.join(HOME_DIR, '.bigeye', 'default_cred.json')
CLI_DOCS_MD = os.path.join(PROJECT_ROOT, 'CLI_DOCS.md')
