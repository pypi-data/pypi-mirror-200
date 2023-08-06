# Skit

A tool for prototyping card games.

Inspired by [squib][squib], but I could never quite get my head around Ruby.

[squib]: https://github.com/andymeneely/squib

## Installation

PyPI didn't like the name `skit`, so it's called `skit-game`:

```ShellSession
pip install skit-game
# or
poetry add skit-game
```

But the package inside is just called `skit`.

## Usage

See the [examples](https://github.com/vtbassmatt/skit/blob/main/examples) for basic usage.

```python
from skit import Deck

d = Deck(3) # make a deck of 3 cards, default size
d.background('#cccccc') # set a gray background
d.render_png('basic_{index}.png') # render basic_0.png, basic_1.png, and basic_2.png
```

## Credits

- Andy Meneely for the idea, and for the awesome Squib!
- game-icons.net for icons used in the examples
