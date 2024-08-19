from pathlib import Path
import sys


app_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(app_path))