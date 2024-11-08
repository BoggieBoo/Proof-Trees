from pathlib import Path
import re

BASE_DIR = Path(__file__).parent.parent.resolve()
DATA_DIR = Path("/data/FormL4")

print("DATA_DIR:", DATA_DIR)  # This should print the path
print("Exists:", DATA_DIR.exists())