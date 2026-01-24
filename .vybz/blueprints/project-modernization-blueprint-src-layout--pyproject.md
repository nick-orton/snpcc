---
status: "Draft"
type: "Blueprint"
author: "Senior Python Architect"
last_updated: "2026-01-23"
references: 
---

# Project Modernization Blueprint: SRC Layout & PyProject

## Context
The `snpcc` project currently uses a legacy flat layout with a `setup.py` file. This structure is prone to import errors during development and lacks the declarative configuration of modern Python tooling.

## Goals
1.  Adopt the **SRC Layout** (`src/snap`, `src/snpcc.py`) to enforce installation-based testing and development.
2.  Migrate build configuration to `pyproject.toml`.
3.  Retain full backward compatibility for the CLI entry point.

## Directory Structure Target

```text
.
├── pyproject.toml       # New Configuration Source of Truth
├── src/                 # Source Root
│   ├── snap/            # Main Package
│   │   ├── __init__.py
│   │   └── ...
│   └── snpcc.py         # CLI Module
├── tests/               # (Future) Test directory
├── .gitignore
├── README.md
└── ...
```

## Migration Steps
1.  **Prepare:** Create `src/` directory.
2.  **Move:** Relocate `snap/` and `snpcc.py` into `src/`.
3.  **Configure:** Generate `pyproject.toml` with `setuptools` backend.
4.  **Cleanup:** Remove `setup.py`.
5.  **Verify:** Re-install in editable mode (`pip install -e .`) and verify CLI functionality.

## Dependencies
*   **Runtime:** `snapcast`, `click`, `pyyaml`
*   **Dev:** `pylint`, `black`, `pytest`
```

---

### 2. The Migration Script

This script automates the file movements and cleanup. It is idempotent-ish (checks for existence before moving).

file: `restructure.sh`
```bash
#!/bin/sh
# restructure.sh
# Automates the migration to SRC layout for snpcc

set -e  # Exit on error

echo ">> Starting Modernization Restructure..."

# 1. Create src directory
if [ ! -d "src" ]; then
    echo ">> Creating src/ directory"
    mkdir -p src
fi

# 2. Move snap package
if [ -d "snap" ]; then
    echo ">> Moving snap/ to src/snap/"
    mv snap src/
else
    echo "!! snap/ directory not found in root (already moved?)"
fi

# 3. Move snpcc.py module
if [ -f "snpcc.py" ]; then
    echo ">> Moving snpcc.py to src/snpcc.py"
    mv snpcc.py src/
else
    echo "!! snpcc.py not found in root (already moved?)"
fi

# 4. Remove legacy setup.py
if [ -f "setup.py" ]; then
    echo ">> Removing legacy setup.py"
    rm setup.py
fi

# 5. Cleanup artifacts
echo ">> Cleaning up build artifacts..."
rm -rf build/ dist/ *.egg-info/ src/*.egg-info/

echo ">> Restructure complete."
echo ">> Run 'pip install -e .' to re-install in editable mode."
```

---

### 3. The Project Configuration

This file replaces `setup.py` and strictly follows PEP 621.

file: `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "snpcc"
version = "0.1.0"
description = "Terminal-based user interface for controlling Snapcast servers"
readme = "README.md"
requires-python = ">=3.11"
license = {text = "GPL-2.0-only"}
authors = [
  {name = "snpcc contributors"}
]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console :: Curses",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    "Programming Language :: Python :: 3.11",
    "Topic :: Multimedia :: Sound/Audio",
]
dependencies = [
    "snapcast",
    "click",
    "pyyaml",
]

[project.scripts]
snpcc = "snpcc:cli"

[project.urls]
"Homepage" = "https://github.com/badaix/snapcast"

[project.optional-dependencies]
dev = [
    "pylint",
    "black",
    "pytest"
]

[tool.setuptools]
package-dir = {"" = "src"}
py-modules = ["snpcc"]
# 'packages' is automatically discovered by setuptools in src/

[tool.pylint.master]
fail-under = 10.0
ignore = ["CVS"]
jobs = 1

[tool.pylint.messages_control]
disable = [
    "print-statement",
    "parameter-unpacking",
    "unpacking-in-except",
    "old-raise-syntax",
    "backtick",
    "long-suffix",
    "old-ne-operator",
    "old-octal-literal",
    "import-star-module-level",
    "non-ascii-bytes-literal",
    "raw-checker-failed",
    "bad-inline-option",
    "locally-disabled",
    "file-ignored",
    "suppressed-message",
    "useless-suppression",
    "deprecated-pragma",
    "use-symbolic-message-instead",
    "apply-builtin",
    "basestring-builtin",
    "buffer-builtin",
    "cmp-builtin",
    "coerce-builtin",
    "execfile-builtin",
    "file-builtin",
    "long-builtin",
    "raw_input-builtin",
    "reduce-builtin",
    "standarderror-builtin",
    "unicode-builtin",
    "xrange-builtin",
    "coerce-method",
    "delslice-method",
    "getslice-method",
    "setslice-method",
    "no-absolute-import",
    "old-division",
    "dict-iter-method",
    "dict-view-method",
    "next-method-called",
    "metaclass-assignment",
    "indexing-exception",
    "raising-string",
    "reload-builtin",
    "oct-method",
    "hex-method",
    "nonzero-method",
    "cmp-method",
    "input-builtin",
    "round-builtin",
    "intern-builtin",
    "unichr-builtin",
    "map-builtin-not-iterating",
    "zip-builtin-not-iterating",
    "range-builtin-not-iterating",
    "filter-builtin-not-iterating",
    "using-cmp-argument",
    "eq-without-hash",
    "div-method",
    "idiv-method",
    "rdiv-method",
    "exception-message-attribute",
    "invalid-str-codec",
    "sys-max-int",
    "bad-python3-import",
    "deprecated-string-function",
    "deprecated-str-translate-call",
    "deprecated-itertools-function",
    "deprecated-types-field",
    "next-method-defined",
    "dict-items-not-iterating",
    "dict-keys-not-iterating",
    "dict-values-not-iterating",
    "deprecated-operator-function",
    "deprecated-urllib-function",
    "xreadlines-attribute",
    "deprecated-sys-function",
    "exception-escape",
    "comprehension-escape",
    "missing-module-docstring",
    "missing-class-docstring",
    "missing-function-docstring"
]

[tool.pylint.format]
max-line-length = 100
```

### 4. Verification

After running the bash script, verify the new structure works:

```python
# verification_script.py
import sys
from pathlib import Path

def verify_structure():
    root = Path(".")
    src = root / "src"
    
    assert src.exists(), "src/ directory missing"
    assert (src / "snap").exists(), "src/snap/ package missing"
    assert (src / "snpcc.py").exists(), "src/snpcc.py module missing"
    assert (root / "pyproject.toml").exists(), "pyproject.toml missing"
    assert not (root / "setup.py").exists(), "legacy setup.py still exists"
    
    print("SUCCESS: Project structure verified.")

if __name__ == "__main__":
    verify_structure()
