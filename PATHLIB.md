# Understanding paths in `events/services.py`

This explains the code in `events/services.py` — step by step, with real examples.

---

## The problem we're solving

Your code needs to open this file:

```
events/data/sample_events.jsonl
```

That file lives **next to** `services.py`:

```
django-learning/
  events/
    services.py              ← your Python code is here
    data/
      sample_events.jsonl    ← you want to open this
```

### Wrong way — hardcoded absolute path

```python
open("/Users/muhammadusama/Desktop/23p/python practice/django-learning/events/data/sample_events.jsonl")
```

Works on your Mac only. Breaks on another machine, in Docker, on CI.

### Wrong way — relative to where you ran the command

```python
open("events/data/sample_events.jsonl")
```

This depends on your **current working directory** (where you ran the terminal command).

| You run from | Does it work? |
|--------------|---------------|
| `django-learning/` (project root) | Yes |
| `events/` folder | No — looks for `events/events/data/...` |
| `/tmp/` or anywhere else | No |

**Problem:** Django, pytest, and shell commands can start from different folders. You can't rely on that.

### Right way — relative to the Python file itself

```python
DATA_DIR = Path(__file__).resolve().parent / 'data'
DEFAULT_EVENTS_FILE = DATA_DIR / 'sample_events.jsonl'
```

This always means: *"starting from where `services.py` lives, go into `data/`"*

Works whether you run `python manage.py shell`, `pytest`, or anything else.

---

## The full code

```python
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / 'data'
DEFAULT_EVENTS_FILE = DATA_DIR / 'sample_events.jsonl'

def read_events(file_path=DEFAULT_EVENTS_FILE):
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)
```

Now let's break down **only these two lines**:

```python
DATA_DIR = Path(__file__).resolve().parent / 'data'
DEFAULT_EVENTS_FILE = DATA_DIR / 'sample_events.jsonl'
```

Read them **inside out** — start from the middle, work outward.

---

## Step 1: `__file__`

**What is it?**  
A variable Python creates automatically when it loads your file. You never write it yourself.

**What does it contain?**  
The path to **this exact `.py` file** — as a plain string.

**Try it yourself:**

Add to `events/services.py`:
```python
print(__file__)
```

Run:
```bash
cd django-learning
python manage.py shell
```

In the shell:
```python
from events import services
```

You'll see something like:
```
/Users/muhammadusama/Desktop/23p/python practice/django-learning/events/services.py
```

That printed value **is** `__file__`.

**One sentence:** `__file__` answers *"where is this Python file on my disk?"*

**NestJS equivalent:** `__filename` in Node.js

---

## Step 2: `Path(__file__)`

`__file__` is just a **string**. Strings can't do `.parent` or clean path joining nicely.

`Path()` wraps that string in a **path object** — a special type from Python's `pathlib` module that knows how to work with file paths.

```python
__file__
# '/Users/.../django-learning/events/services.py'   ← plain string

Path(__file__)
# Path('/Users/.../django-learning/events/services.py')   ← path object
```

**Why bother?** Because now you can use:
- `.parent` — go up a folder
- `/ 'data'` — go into a subfolder
- `.resolve()` — get full absolute path
- `.read_text()` — read file contents directly

**Analogy:** A string is like writing an address on paper. A `Path` object is like having GPS that can navigate from that address.

**NestJS equivalent:** `path.parse(__filename)` or using the `path` module

---

## Step 3: `.resolve()`

**What does it do?**  
Turns the path into a **guaranteed full absolute path** — starting from the root of your disk.

**Why do we need it?**

Sometimes `__file__` is already a full path. Sometimes it's relative:

```python
__file__ = "events/services.py"           # relative (no /Users/...)
Path(__file__)                            # still relative
Path(__file__).resolve()                  # /Users/.../django-learning/events/services.py
```

In Django it usually works without `.resolve()`. We add it to be safe — handles `..`, symlinks, and weird edge cases.

**Analogy:** Someone says *"room 5, one floor up"* (relative). `.resolve()` is GPS giving the full street address (absolute).

**You asked in prep:** *"I thought Path(__file__) already gives the whole path?"*

**Answer:** Usually yes in Django. But `.resolve()` means *"I am 100% sure this is the real full path."* That's why we use it — best practice, not always strictly required.

**After this step, our path looks like:**
```
/Users/muhammadusama/Desktop/23p/python practice/django-learning/events/services.py
```

**NestJS equivalent:** `path.resolve(__filename)`

---

## Step 4: `.parent`

**What does it do?**  
Goes **up one level** — from a file to the folder that contains it.

```python
Path(".../events/services.py").parent
# → .../events/
```

You're on `services.py` → `.parent` gives you the `events/` folder.

```
django-learning/
  events/           ← .parent lands here
    services.py     ← we start here (__file__)
    data/
      sample_events.jsonl
```

**You asked in prep:** *"If I keep doing .parent.parent, does it keep going up?"*

**Answer:** Yes.

```python
Path(__file__).parent              # events/
Path(__file__).parent.parent       # django-learning/
Path(__file__).parent.parent.parent  # python practice/
```

Each `.parent` = one folder up.

**After this step:**
```
/Users/muhammadusama/Desktop/23p/python practice/django-learning/events/
```

**NestJS equivalent:** `path.dirname(__filename)` — gives you the folder containing the current file

---

## Step 5: `/ 'data'`

The `/` operator on a `Path` object **joins** path parts.

```python
Path(".../events/") / 'data'
# → .../events/data/
```

It's like clicking into the `data` folder in Finder.

```
events/
  services.py
  data/              ← / 'data' takes you here
    sample_events.jsonl
```

**After this step — this is `DATA_DIR`:**
```
/Users/muhammadusama/Desktop/23p/python practice/django-learning/events/data/
```

**NestJS equivalent:** `path.join(__dirname, 'data')`

---

## Step 6: `DEFAULT_EVENTS_FILE`

Same idea — join the filename onto the folder:

```python
DEFAULT_EVENTS_FILE = DATA_DIR / 'sample_events.jsonl'
```

```python
Path(".../events/data/") / 'sample_events.jsonl'
# → .../events/data/sample_events.jsonl
```

**Final result:**
```
/Users/muhammadusama/Desktop/23p/python practice/django-learning/events/data/sample_events.jsonl
```

Now `read_events()` uses this as the default file to open.

---

## Full walkthrough — every step with values

Starting from `events/services.py`:

```python
Path(__file__).resolve().parent / 'data'
```

| Step | Code | What you get |
|------|------|--------------|
| 1 | `__file__` | `".../events/services.py"` (string) |
| 2 | `Path(__file__)` | Path object for `services.py` |
| 3 | `.resolve()` | `"/Users/.../django-learning/events/services.py"` |
| 4 | `.parent` | `"/Users/.../django-learning/events/"` |
| 5 | `/ 'data'` | `"/Users/.../django-learning/events/data/"` |

Then:

```python
DEFAULT_EVENTS_FILE = DATA_DIR / 'sample_events.jsonl'
# → "/Users/.../django-learning/events/data/sample_events.jsonl"
```

---

## How `read_events` uses it

```python
def read_events(file_path=DEFAULT_EVENTS_FILE):
```

- If you call `read_events()` with no argument → uses `DEFAULT_EVENTS_FILE` (the path we built)
- If you call `read_events("/some/other/file.jsonl")` → uses that instead

The path we built is **stable** — it always points to the right file regardless of where you run Django from.

---

## Why not just use a string?

You could write:

```python
import os
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
```

That works too — it's the old way. `pathlib.Path` is the modern Python way (cleaner, same idea):

| Old (`os.path`) | New (`pathlib`) |
|-----------------|-----------------|
| `os.path.dirname(__file__)` | `Path(__file__).parent` |
| `os.path.join(a, b)` | `a / b` |
| `os.path.abspath(x)` | `Path(x).resolve()` |

---


**Finding test data from a test file:**
```python
DATA = Path(__file__).parent.parent / "data" / "rates.json"
```
From the test file → up one folder → up again → into `data/rates.json`

**Fixing imports when a folder isn't a Python package:**
```python
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "prep"))
```
Adds `prep/` to Python's import search path so `from hourly import ...` works.

---

## Summary — remember these 5 things

1. **`__file__`** — Python tells you where this `.py` file lives
2. **`Path(...)`** — turn that string into a path object you can manipulate
3. **`.resolve()`** — make sure it's a full absolute path
4. **`.parent`** — go up one folder (from file to its folder)
5. **`/ 'name'`** — go down into a subfolder or file

**The goal:** never hardcode `/Users/...` — always build paths starting from `__file__`.
