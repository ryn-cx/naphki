<!-- TODO: Validate -->
# Naphki

[NHK World](https://www3.nhk.or.jp/nhkworld/) API wrapper built using [Good Ass
Pydantic Integrator](https://github.com/ryn-cx/good-ass-pydantic-integrator) and
[Get Around](https://github.com/ryn-cx/get-around).

## Installation

```bash
uv add git+https://github.com/ryn-cx/naphki
```

## Usage

Calling an endpoint returns the parsed model. `download()` returns the response
as text and `load()` reads that text into the model.

```python
from naphki import Naphki

client = Naphki()

# A page of episodes for one show, by its program id.
episodes = client.video_episodes("dwc", limit=20, offset=0)

# A page of episodes across every show.
everything = client.video_episodes()

# One episode, by its episode id.
episode = client.video_episode(5001461)

# One show, by its program id.
program = client.video_program("japanologyplus")

# Shows matching a search term.
results = client.shows_search("japan")

# The two halves of a call.
downloaded = client.video_program.download("japanologyplus")
program = client.video_program.load(downloaded)
```
