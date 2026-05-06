# Youtube Together Bot

Youtube Together is a lightweight Discord bot built to let users watch YouTube videos synchronously within Discord voice channels. It acts as an integration layer between Discord's native voice channel activities and the traditional bot command interface, using the `discord-together` package to generate activity invite links.

## Table of Contents

- [About the Project](#about-the-project)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Folder Structure](#folder-structure)
- [Important Code Concepts](#important-code-concepts)
- [Architectural Decisions](#architectural-decisions)
- [Data Model](#data-model)
- [Main User Flows](#main-user-flows)
- [Setup Instructions](#setup-instructions)
- [Available Scripts](#available-scripts)
- [Configuration Notes](#configuration-notes)
- [Testing](#testing)
- [Deployment](#deployment)
- [Future Improvements](#future-improvements)
- [Learning Outcomes](#learning-outcomes)
- [Screenshots](#screenshots)
- [License](#license)

## About the Project

This project solves a specific problem for Discord users: accessing Discord's hidden or experimental voice channel activities. The bot listens for a simple command (`yt!youtube`) and programmatically generates a temporary invite link that triggers the YouTube Together activity when clicked.

The current implementation is deliberately kept simple. It runs entirely in memory without a connected database, as it only needs to read the user's current voice channel state and communicate with Discord's API. Note that based on the current code, the activity generated only works on the desktop client, which is a known limitation of the underlying Discord activity implementation.

## Key Features

- **Activity Generation (`yt!youtube`)**
  If a user is inside a voice channel, the bot uses the `discord-together` client to generate a YouTube activity link tied to that specific channel.
- **Basic Error Handling**
  The bot intercepts `CommandInvokeError` events to provide a helpful message if a user tries to run the activity command without being in a voice channel.
- **Bot Analytics/Logging**
  The current code tracks when the bot joins or leaves a server, logging the server name, ID, member count, and region to a hardcoded developer channel. It also dynamically updates its status presence to show the number of servers it is in.

## Tech Stack

| Layer | Technology | Purpose |
| --- | --- | --- |
| Runtime | Python 3.8+ | Core execution environment |
| Framework | discord / discord.py (v1.7.3) | Handles the Discord API connection, events, and command routing |
| Integration | discord-together (v1.0.7) | Bridges the bot with Discord's undocumented voice activities API |
| Package Manager | Poetry | Manages dependencies and creates the virtual environment |

## System Architecture

The bot uses an event-driven architecture based on `discord.py`. Everything is contained in a single process.

```txt
User (in Voice Channel)
  ↓
Types `yt!youtube`
  ↓
Discord Event Loop (main.py)
  ↓
Command Router checks context
  ↓
discord-together API Call
  ↓
Discord Voice Channel generates activity
  ↓
Bot returns Embed with Link to User
```

## Folder Structure

The repository is kept as a minimal Python project.

```txt
./
  main.py            # Main entry point containing all bot commands and events
  pyproject.toml     # Poetry configuration and dependency definitions
  poetry.lock        # Locked dependency versions
```

## Important Code Concepts

- **Command Context (`ctx`)**
  The bot relies heavily on the context object provided by `discord.ext.commands` to verify the state of the user. For example, it reads `ctx.author.voice.channel.id` to know where to bind the YouTube activity.
- **Event Listeners (`@client.event`)**
  We use event hooks like `on_guild_join` and `on_guild_remove` to trigger side effects. Currently, these construct detailed embeds and push them to a specific internal channel for basic usage tracking.
- **External Integration (`DiscordTogether`)**
  The `discord-together` class is initialized alongside the main bot client and manages the HTTP requests necessary to start the hidden Discord activities.

## Architectural Decisions

- **Single-File Entry Point**
  Currently, all commands, events, and error handling live inside `main.py`. This structure suggests the project was designed as a quick proof-of-concept. The tradeoff is that as the bot adds more commands or activities, this file will become difficult to navigate.
- **Environment-Based Secrets**
  The bot uses `os.environ['TOKEN']` to authenticate. This prevents the secret from being hardcoded in the source, which is standard practice, but it also means the app will immediately crash with a `KeyError` if the environment isn't set up correctly.
- **No Persistence Layer**
  The application does not use a database. Given the current feature set, this tradeoff makes sense because the bot's only job is to react to immediate user commands and format API responses.

## Data Model

Because the bot relies entirely on real-time data from the Discord API and does not persist user information, there is no formal database schema or data model in this repository. The main data structures dealt with are transient `discord.Guild`, `discord.Member`, and `discord.Embed` objects.

## Main User Flows

**Starting a Watch Party**
1. A Discord user joins a voice channel.
2. The user types `yt!youtube` in a text channel.
3. The bot reads the user's voice state and passes the channel ID to `togetherControl.create_link`.
4. The bot replies with an embed containing a clickable hyperlink.
5. The user clicks the link, which opens the YouTube player inside their Discord voice channel UI.

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Poetry installed globally (`pip install poetry` or `pipx install poetry`)
- A registered Discord Bot application with a valid token

### Installation

Clone the repository and use Poetry to install dependencies:

```bash
git clone <repository-url>
cd <repository-folder>
poetry install
```

### Environment Variables

The application requires one environment variable to authenticate with Discord.

```env
TOKEN=your_discord_bot_token_here
```

### Running Locally

To start the bot, run the main script inside the Poetry environment. You must pass the token inline or set it in your environment beforehand.

```bash
TOKEN=your_token_here poetry run python main.py
```

## Available Scripts

Since this project uses Poetry, you can run the main file using:

| Command | Description |
| --- | --- |
| `poetry run python main.py` | Starts the bot process |
| `poetry env info` | Shows details about the virtual environment |

## Configuration Notes

- `pyproject.toml` configures the project metadata and exact dependency bounds for `discord.py` and `discord-together`.
- The bot prefix is hardcoded as `yt!` in `commands.Bot(command_prefix="yt!")`.

## Testing

Automated tests are not currently included in the repository.

Since the project relies heavily on async API interactions, testing this would likely require a framework like `pytest-asyncio` combined with a mocking library (like `dpytest`) to simulate Discord contexts and command invocations.

## Deployment

No deployment-specific configuration (like Dockerfiles or Procfiles) was found. Since this is a standalone Python process, it can generally be deployed to a basic VPS or a service like Render or Heroku by wrapping the run command in a simple startup script and providing the `TOKEN` environment variable.

## Future Improvements

- **Refactor Command Structure:** Split commands and events into Discord Cogs instead of keeping everything in `main.py`. This will improve maintainability.
- **Better Configuration Handling:** Use a `.env` file parser (like `python-dotenv`) so developers don't have to manually export the token into their shell environment.
- **Remove Hardcoded Channel IDs:** The `log_channel` ID inside the guild join/remove events (`832944803338911765`) is hardcoded. This should be moved to a configuration file or environment variable so anyone can deploy their own version of the bot without hitting an error.
- **Help Command Customization:** The current `help` command is a basic string response. It could be upgraded to a formatted embed.

## Learning Outcomes

This project demonstrates practical experience working with external APIs and asynchronous Python programming. It shows an understanding of event-driven architectures, where an application must sit idle and react predictably to unpredictable user input. Setting up the `CommandInvokeError` handler specifically shows an awareness of how user error (like using the command outside a voice channel) can break assumptions in the code.

## Screenshots

```md
Screenshots can be added here to show the bot's embeds and the YouTube activity interface inside Discord.
```

## License

License information has not been specified yet.
