"""Unit tests for the Client wrapper logic."""
import pytest
from unittest.mock import MagicMock
from snap.client import Client

def test_client_initialization(mock_snapcast_client):
    """Verify the wrapper correctly extracts attributes from the low-level client."""
    c = Client(mock_snapcast_client)
    assert c.friendly_name == "Living Room"
    assert c.identifier == "test_client_id_1"
    assert c.volume == 50
    assert not c.muted

def test_volume_clamping_upper(mock_snapcast_client, mocker):
    """Verify volume is clamped at 100%."""
    # Arrange: Mock Api._run to prevent actual async execution
    patch_run = mocker.patch("snap.api.Api._run")
    c = Client(mock_snapcast_client)
    mock_snapcast_client.volume = 98

    # Act: Raise volume by 5%
    c.raise_volume()

    # Assert: Should be 100, not 103
    # We check the call to the underlying low-level client's async method
    # Note: Api._run receives the coroutine object
    assert patch_run.called
    mock_snapcast_client.set_volume.assert_called_once_with(100)

def test_volume_clamping_lower(mock_snapcast_client, mocker):
    """Verify volume is clamped at 0%."""
    patch_run = mocker.patch("snap.api.Api._run")
    c = Client(mock_snapcast_client)
    mock_snapcast_client.volume = 3

    # Act
    c.lower_volume()

    # Assert
    mock_snapcast_client.set_volume.assert_called_once_with(0)

def test_toggle_mute_logic(mock_snapcast_client, mocker):
    """Verify toggle_mute flips the current state correctly."""
    patch_run = mocker.patch("snap.api.Api._run")
    c = Client(mock_snapcast_client)

    # Scenario 1: Currently Unmuted -> Mute
    mock_snapcast_client.muted = False
    c.toggle_mute()
    mock_snapcast_client.set_muted.assert_called_with(True)

    # Scenario 2: Currently Muted -> Unmute
    mock_snapcast_client.muted = True
    c.toggle_mute()
    mock_snapcast_client.set_muted.assert_called_with(False)

