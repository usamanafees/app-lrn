import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / 'data'
DEFAULT_EVENTS_FILE = DATA_DIR / 'sample_events.jsonl'


# __file__ = "events/services.py"   # relative — possible in some cases
# Path(__file__)
# # still relative → events/services.py
# Path(__file__).resolve()
# # forced full → /Users/.../django-learning/events/services.py
# Short answer
# Path(__file__) = wrap string in path object (often already full path)
# .resolve() = "make sure it's the real full path"

def read_events(file_path: str = DEFAULT_EVENTS_FILE):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield (json.loads(line))