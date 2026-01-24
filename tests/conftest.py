import pytest
import curses
from unittest.mock import MagicMock, AsyncMock

@pytest.fixture(scope="session", autouse=True)
def shim_curses():
    """
    Injects missing curses constants that are usually initialized at runtime.
    This prevents AttributeErrors when running in non-interactive environments.
    """
    # Standard attributes
    if not hasattr(curses, "A_BOLD"):
        curses.A_BOLD = 2048

    # Alternative Character Set (ACS) constants
    # These are usually initialized by curses.initscr()
    acs_constants = [
        "ACS_HLINE", "ACS_VLINE", "ACS_LTEE", "ACS_RTEE",
        "ACS_ULCORNER", "ACS_URCORNER", "ACS_LLCORNER", "ACS_LRCORNER"
    ]
    for const in acs_constants:
        if not hasattr(curses, const):
            setattr(curses, const, ord('-')) # Default to a simple dash for testing

    # Mock color_pair function as it requires a terminal
    if not hasattr(curses, "color_pair"):
        curses.color_pair = lambda n: n

    yield

@pytest.fixture
def mock_snapcast_client():
    """Provides a mocked low-level snapcast client."""
    client = MagicMock()
    client.identifier = "test_client_id_1"
    client.friendly_name = "Living Room"
    client.volume = 50
    client.muted = False
    client.latency = 0
    client.version = "0.26.0"

    # Snapcast control methods are async
    client.set_volume = AsyncMock()
    client.set_muted = AsyncMock()
    client.set_name = AsyncMock()
    return client

@pytest.fixture
def mock_snapcast_stream():
    """Provides a mocked snapcast stream."""
    stream = MagicMock()
    stream.identifier = "stream_1"
    stream.name = "Spotify"
    return stream

@pytest.fixture
def mock_snapcast_group(mock_snapcast_stream):
    """Provides a mocked snapcast group."""
    group = MagicMock()
    group.identifier = "group_1"
    group.stream = mock_snapcast_stream.identifier
    return group

@pytest.fixture
def mock_snapcast_server(mock_snapcast_client, mock_snapcast_stream, mock_snapcast_group):
    """Provides a fully populated mocked Snapcast server."""
    server = MagicMock()
    server.clients = [mock_snapcast_client]
    server.streams = [mock_snapcast_stream]
    server.groups = [mock_snapcast_group]

    # Helper for server.stream(id)
    def get_stream(stream_id):
        for s in server.streams:
            if s.identifier == stream_id:
                return s
        return None

    server.stream.side_effect = get_stream
    server.group_stream = AsyncMock()
    return server

@pytest.fixture(autouse=True)
def patch_api_init(mocker, mock_snapcast_server):
    """
    Aggressively patches snapcast.control.create_server.

    This is critical because the Api class calls run_until_complete
    in __init__, which would otherwise attempt real network IO.
    """
    return mocker.patch(
        "snapcast.control.create_server",
        return_value=mock_snapcast_server
    )

@pytest.fixture
def mock_stdscr():
    """Provides a mocked curses window (stdscr)."""
    stdscr = MagicMock()
    # Default terminal size: 24 lines, 80 columns
    stdscr.getmaxyx.return_value = (24, 80)
    # Mock getch to return 'q' by default to prevent infinite loops
    stdscr.getch.return_value = ord('q')
    return stdscr

@pytest.fixture
def mock_api(mocker, mock_snapcast_server):
    """
    Provides a mock of our internal Api wrapper.
    Used for testing State and TUI without triggering real async loops.
    """
    api = MagicMock()
    api.server = mock_snapcast_server
    api.active_stream.return_value = mock_snapcast_server.streams[0]
    return api

