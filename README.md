# snpcc

**snpcc** is a terminal-based user interface (TUI) and command-line interface
(CLI) for controlling [Snapcast](https://github.com/badaix/snapcast) servers.
Inspired by lightweight clients like `mpc` and `ncmpc`, it provides a fast,
keyboard-driven environment for managing multi-room audio.

## Prerequisites

*   **Python 3.11+**
*   A running **Snapcast Server** reachable via the network.
*   A POSIX-compliant terminal (Linux/BSD/macOS).

## Installation

Install `snpcc` directly from the source code. Using a virtual environment is
recommended to isolate dependencies.

```bash
# Clone the repository (if applicable) or navigate to source
cd /path/to/snpcc

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in editable mode
pip install --editable .
```

## Configuration

`snpcc` requires a configuration file to locate your Snapcast server. By
default, it looks for `snpcc.yml` in your standard configuration directory
(e.g., `~/.config/` or `$XDG_CONFIG_HOME`).

1.  Create the configuration directory:
    ```bash
    mkdir -p ~/.config
    ```

2.  Create the configuration file `~/.config/snpcc.yml`:
    ```yaml
    # ~/.config/snpcc.yml
    server: 192.168.1.50
    ```

If no configuration file is found, the client defaults to `localhost`.

## Usage: TUI (Interactive Mode)

To launch the interactive Terminal User Interface, run the command without
arguments:

```bash
snpcc
```

### Keybindings

**Navigation**
*   `j` / `k` : Select next/previous client.
*   `s`     : Cycle through available streams for the selected group.

**Volume Control**
*   `h`     : Lower volume of selected client (5%).
*   `l`     : Raise volume of selected client (5%).
*   `H`     : Lower volume of **all** clients.
*   `L`     : Raise volume of **all** clients.

**State Management**
*   `m`     : Toggle mute for selected client.
*   `a` / `M` : Toggle mute for **all** clients.
*   `Space` : Force refresh the screen/state.

**Screens**
*   `1` / `?` : Help screen.
*   `2`     : Main screen (Client list and volumes).
*   `3`     : Client details screen.
*   `q`     : Quit application.

## Usage: CLI (Command Line Mode)

You can use `snpcc` for one-off commands and scripting without entering the
interactive interface.

### List Clients
Displays an indexed list of connected clients and their current volume.

```bash
snpcc list
# Output:
# 1 Kitchen Speaker  80
# 2 Living Room      -- (indicates muted)
```

### Volume Control
Adjust volume for a specific client using the index provided by the `list`
command. If no index is provided, the command applies to **all** clients.

```bash
# Raise volume of client #1 by 5%
snpcc up 1

# Lower volume of ALL clients by 5%
snpcc down
```

### Mute Control
Toggle the mute state. Like volume controls, omitting the index applies the
action globally.

```bash
# Toggle mute for client #2
snpcc mute 2

# Mute/Unmute ALL clients
snpcc mute
```

### Renaming Clients
Assign a new friendly name to a client. This uses the current name as the
lookup key.

```bash
snpcc rename "Kitchen Speaker" "Kitchen"
```

## Development

To contribute to `snpcc`, set up a development environment.

1.  **Install Dependencies:**
    ```bash
    pip install click pyyaml snapcast pylint
    ```

2.  **Linting:**
    Ensure code adheres to the project's `.pylintrc` standards.
    ```bash
    pylint snpcc.py snap/
    ```

## Architecture

*   **`snpcc.py`**: Entry point. Handles CLI argument parsing via `click` and
    initializes state.
*   **`snap/tui.py`**: Manages the `curses` event loop and input handling.
*   **`snap/state.py`**: Manages application state, acting as the bridge
    between the UI and the API.
*   **`snap/api.py`**: Wraps `asyncio` calls to the `snapcast` library.
*   **`snap/screen.py`**: Handles drawing logic for specific UI views.

## License

This project is licensed under the GNU General Public License v2.0. See the
`LICENSE` file for details.

