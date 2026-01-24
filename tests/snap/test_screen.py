"""Unit tests for UI rendering and string formatting."""
import pytest
from snap.screen import _volume_string, _status_string
from unittest.mock import ANY

def test_volume_string_formatting():
    """Verify the ASCII progress bar renders correctly."""
    # 0% volume
    assert _volume_string(0) == "|" + " " * 50 + "|"

    # 100% volume (50 stars)
    assert _volume_string(100) == "|" + "\u2588" * 50 + "|"

    # 50% volume (25 stars)
    assert _volume_string(50) == "|" + "\u2588" * 25 + " " * 25 + "|"

@pytest.mark.parametrize("muted,selected,expected_part", [
    (False, False, "Living Room"),
    (True, False, "Living Room (m)"),
    (False, True, "[Living Room]"),
    (True, True, "[Living Room] (m)"),
])
def test_status_string_variants(mock_snapcast_client, muted, selected, expected_part):
    """Verify that status labels correctly reflect muted and selected states."""
    mock_snapcast_client.friendly_name = "Living Room"
    mock_snapcast_client.muted = muted
    mock_snapcast_client.volume = 50

    result = _status_string(mock_snapcast_client, max_len=11, selected=selected)

    assert expected_part in result
    # Ensure the volume bar is appended
    assert _volume_string(50) in result

def test_draw_title(mock_stdscr):
    """Verify the title bar draws a horizontal line across the screen."""
    from snap.screen import MainScreen
    screen = MainScreen()

    screen.draw_title(mock_stdscr)

    # Should get width from stdscr
    mock_stdscr.getmaxyx.assert_called()
    # Should draw the title at 0,0
    mock_stdscr.addstr.assert_any_call(0, 0, "Main", ANY)
    # Should draw the line at row 1
    mock_stdscr.hline.assert_called_with(1, 0, ANY, 80)
