---
status: "Draft"
type: "Bug"
author: "QA Automation Lead"
last_updated: "2026-01-23"
references: "src/snap/api.py, src/snpcc.py"
---

As the **QA Automation Lead**, I have reproduced the reported failure. The root cause is **exception leakage** from the asynchronous `snapcast` library into the synchronous TUI/CLI initialization sequence.

### Bug Analysis: The "Guilty" Initialization
In `src/snap/api.py`, the constructor attempts a blocking network call:
```python
self.server = self.loop.run_until_complete(snapcast.control.create_server(self.loop, addr))
```
If `create_server` fails (e.g., DNS failure, connection refused, or timeout), it raises a raw `OSError` or `socket.gaierror`. Because the `Api` class does not wrap this in a `try/except` block, and the calling `State` and `snpcc.py` modules assume success, the exception bubbles up to the top-level interpreter, resulting in a stack trace.

### Proving the Crash
I am implementing a CLI-level integration test using `click.testing.CliRunner`. This test simulates a network failure and verifies that the application currently fails with a "naked" exception rather than a controlled error message.

**File:** `tests/test_snpcc.py`

```python
"""Integration tests for the snpcc CLI entry point."""
import pytest
from click.testing import CliRunner
from snpcc import cli

def test_cli_initialization_crash_on_network_error(mocker):
    """
    PROVE THE BUG: Verify that a network failure during startup
    results in a raw OSError stack trace.
    """
    # Arrange: Force the underlying snapcast library to fail
    # We must patch 'snapcast.control.create_server' because that is the
    # actual point of failure called inside Api.__init__
    mocker.patch(
        "snapcast.control.create_server",
        side_effect=OSError("Connection refused: 127.0.0.1:1705")
    )

    runner = CliRunner()

    # Act: Attempt to run any command (e.g., 'list')
    result = runner.invoke(cli, ["list"])

    # Assert:
    # 1. The process exited with an error code
    assert result.exit_code != 0

    # 2. PROOF OF STACK TRACE: The 'exception' attribute is populated
    # In a "fixed" version, we would catch this and print to stderr,
    # meaning result.exception would be None (or a SystemExit).
    assert result.exception is not None
    assert isinstance(result.exception, OSError)
    assert "Connection refused" in str(result.exception)

def test_cli_config_file_not_found_default_behavior(mocker):
    """
    Verify that if the config file is missing, we default to localhost.
    This tests the 'server_address' logic in snpcc.py.
    """
    # Arrange: Mock os.path.join to point to a non-existent file
    mocker.patch("os.path.exists", return_value=False)
    # Mock open to raise FileNotFoundError just in case
    mocker.patch("builtins.open", side_effect=FileNotFoundError)

    from snpcc import server_address

    # Act
    addr = server_address()

    # Assert
    assert addr == "localhost"
```

### Remediation Strategy (For Developers)
To resolve this, we must implement the **Guard Clause** pattern in `src/snap/api.py` or the `init_state` function in `src/snpcc.py`.

1.  **Catch at the Source:** Wrap the `run_until_complete` call in `Api.__init__` with a `try/except (OSError, asyncio.TimeoutError)`.
2.  **Raise a Custom Exception:** Raise a domain-specific error (e.g., `SnapcastConnectionError`).
3.  **Handle in CLI:** In `snpcc.py`, catch this domain error and use `click.ClickException` or `sys.exit("Error: Could not connect to Snapcast server at ...")`.

### Execution
Run this test to see the failure:
```bash
pytest tests/test_snpcc.py
```

Once the code is fixed, we will update this test to assert that `result.exception` is `None` and `result.output` contains the "nice" error message.
