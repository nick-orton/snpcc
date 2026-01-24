---
status: "Draft"
type: "Design"
author: "QA Automation Lead"
last_updated: "2026-01-23"
references: "designs/project-modernization-blueprint-src-layout--pyproject.md"
---

# Testing Strategy: Vybz Workbench (snpcc)

As the QA Automation Lead, I have reviewed the `snpcc` codebase. My verdict: **The code is currently a liability.** It mixes synchronous and asynchronous logic haphazardly, relies on global event loops that are deprecated in modern Python, and lacks any error handling for the most common failure mode: the network.

This plan establishes a **Hermetic Testing** regime to ensure stability during the modernization process.

## 1. Static Analysis & Risk Assessment

### High-Risk Areas
*   **`snap/api.py`**: The use of `asyncio.get_event_loop().run_until_complete()` inside a constructor (`__init__`) is a recipe for `RuntimeError` in multi-threaded or modern async environments.
*   **`snap/state.py`**: The `_find_idx` method returns `-1` on failure, but calling methods (like `next_stream`) do not check this return value before using it. This will cause index errors or unexpected behavior.
*   **`snpcc.py`**: The `server_address` function uses legacy `os.path` and `os.environ.get` without fallbacks, making it brittle across different Unix environments.

### The "Sad Path" Focus
1.  **Server Offline:** What happens when `snapcast.control.create_server` times out?
2.  **Empty Server:** What happens if `server.clients` or `server.groups` is empty? (Currently, `Api` assumes `groups[0]` exists).
3.  **Permissions:** What happens if the config file exists but is unreadable?

---

## 2. Test Architecture

### Framework Configuration
*   **Tool:** `pytest`
*   **Plugins:** `pytest-mock`, `pytest-asyncio` (though we will mock the loop to keep tests sync and fast).
*   **Structure:**
    ```text
    tests/
    ├── vybz/
    │   ├── test_api.py      # Mocks snapcast.control
    │   ├── test_client.py   # Pure logic tests (volume clamping)
    │   ├── test_screen.py   # String formatting & Curses mocks
    │   ├── test_state.py    # State machine & indexing logic
    │   └── test_snpcc.py    # CLI integration tests
    └── conftest.py          # Shared fixtures (Mocks for Server/Client)
    ```

---

## 3. Implementation Plan

### Phase 1: The "Pure" Unit Tests (Logic Only)
We start with `snap/client.py` and `snap/screen.py` because they contain the most "testable" logic without side effects.

| Module | Target | Scenario |
| :--- | :--- | :--- |
| `client.py` | `_change_vol` | Verify volume never exceeds 100 or drops below 0. |
| `screen.py` | `_volume_string` | Verify the progress bar renders correctly for 0, 50, and 100%. |
| `screen.py` | `_status_string` | Verify labels include `(m)` when muted and `[]` when selected. |

### Phase 2: Hermetic API Mocking
We will mock the `snapcast.control` objects entirely. We do not want a real server running.

**Fixture Strategy (`tests/conftest.py`):**
*   `mock_snapcast_server`: A `MagicMock` representing the Snapcast server with default groups and streams.
*   `mock_snapcast_client`: A `MagicMock` representing a single client (Mac address, name, volume).

### Phase 3: State & Transition Testing
Testing `snap/state.py` is critical for the TUI's reliability.

**Key Test Cases:**
*   `test_next_client_wraparound`: Ensure that calling `next_client` on the last client returns to the first.
*   `test_mute_all_logic`: Verify that if *one* client is unmuted, `mute_all` mutes everyone. If *all* are muted, it unmutes everyone.
*   `test_find_by_name_missing`: Verify behavior when a user tries to rename a client that doesn't exist.

---

## 4. Bug Reports (Pre-emptive)

During analysis, I am flagging the following as **Critical Bugs**:

1.  **Index Out of Bounds (`state.py`):**
    `_find_idx` returns `-1`. In `next_stream`, the code does `idx = _find_idx(...) + 1`. If `_find_idx` fails, `idx` becomes `0`, which silently returns the first stream instead of raising an error. This is "Guilty" logic.
    
2.  **Hardcoded Pathing (`api.py`):**
    The `Api` class assumes `self.server.groups[0]` always exists. If a Snapcast server has no groups configured, the TUI will crash on startup with an `IndexError`.

3.  **Blocking IO in Main Thread:**
    The TUI calls `Api._run(action)` which blocks the curses loop. This will cause the UI to "freeze" if the network latency is high.

---

## 5. Sample Test Implementation (Draft)

`tests/snap/test_client.py`

```python
import pytest
from unittest.mock import MagicMock
from snap.client import Client

@pytest.fixture
def mock_api_client():
    """Provides a mocked low-level snapcast client."""
    client = MagicMock()
    client.volume = 50
    client.muted = False
    client.friendly_name = "Test Speaker"
    return client

def test_client_volume_upper_boundary(mock_api_client, mocker):
    """Verify volume does not exceed 100%."""
    # Arrange
    mocker.patch("snap.api.Api._run")
    c = Client(mock_api_client)
    c.client.volume = 98

    # Act
    c.raise_volume() # Should add 5, but clamp at 100

    # Assert
    mock_api_client.set_volume.assert_called_once_with(100)

def test_client_volume_lower_boundary(mock_api_client, mocker):
    """Verify volume does not drop below 0%."""
    # Arrange
    mocker.patch("snap.api.Api._run")
    c = Client(mock_api_client)
    c.client.volume = 3

    # Act
    c.lower_volume()

    # Assert
    mock_api_client.set_volume.assert_called_once_with(0)
```

## Next Steps
1.  Initialize `tests/conftest.py` with `snapcast` and `curses` mocks.
2.  Implement `test_client.py` to lock down volume logic.
3.  Implement `test_state.py` to fix the indexing bugs.
