<!-- TODO: Validate -->
# Naphki

Unofficial [NHK World](https://www3.nhk.or.jp/nhkworld/) API.

`naphki` wraps NHK World's web API and parses its raw JSON into typed
[Pydantic](https://docs.pydantic.dev/) models, giving you a small, structured API for
reading data about NHK World video episodes.

## Installation

```bash
uv add git+https://github.com/ryn-cx/naphki
```

## Usage

Create a client, then call `get(...)` on an endpoint to download from NHK World and
get back a parsed, typed model.

```python
from naphki import Naphki

client = Naphki()

# A page of video episodes (across every show).
episodes = client.video_episodes.get(limit=20, offset=0)

# A page of video episodes for a single show, by its program ID.
# "dwc" is from https://www3.nhk.or.jp/nhkworld/en/shows/dwc/
show_episodes = client.video_episodes.get("dwc")

# A single show (video program), by its program ID.
program = client.video_programs.get("japanologyplus")

# Search for shows (video programs) by a search term.
results = client.shows_search.get("japan")

```
