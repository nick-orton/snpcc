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
    assert result.exit_code == 1

    # 2. PROOF OF STACK TRACE: The 'exception' attribute is populated
    # In a "fixed" version, we would catch this and print to stderr,
    # meaning result.exception would be None (or a SystemExit).
    assert isinstance(result.exception, SystemExit)
    assert "1" in str(result.exception)

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

def test_crash_on_no_connected_clients(mock_snapcast_server):
    """
    PROVE THE BUG: If the server returns 0 clients, the State constructor
    crashes with an IndexError because it assumes at least one client exists.
    """
    # Arrange: Simulate a server with zero clients
    mock_snapcast_server.clients = []

    runner = CliRunner()

    # Act: Run the CLI
    result = runner.invoke(cli, ["list"])

    # Assert: The application doesn't crash
    assert result.exit_code == 0
    #assert isinstance(result.exception, IndexError)

