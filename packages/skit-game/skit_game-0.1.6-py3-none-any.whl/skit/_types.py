from enum import Enum
from typing import NamedTuple, NewType
from numbers import Real
from PIL.ImageFont import FreeTypeFont

class Rect(NamedTuple):
    "A rectangle, the basic data structure used throughout Skit."
    x: Real
    """X coordinate for start of rectangle."""
    y: Real
    """Y coordinate for start of rectangle."""
    width: Real
    """Width of rectangle."""
    height: Real
    """Height of rectangle."""


class Alignment(Enum):
    "Where to align items in a layout."
    BEGIN = 'begin'
    """Align left if horizontal or top if vertical."""
    MIDDLE = 'middle'
    """Align to the middle."""
    END = 'end'
    """Align right if horitzontal or bottom if vertical."""


class Scale(Enum):
    "How to scale images within their layout."
    FIT = 'fit'
    """Scale the image up (larger) or down (smaller) to fit the layout."""
    DOWN = 'down'
    """Only scale the image down, never up."""
    UP = 'up'
    """Only scale the image up, never down."""
    NONE = 'none'
    """Disable scaling."""


class LayoutDef(NamedTuple):
    "A box for drawing into plus alignment information for the box's contents."
    x: Real
    """X coordinate for start of layout."""
    y: Real
    """Y coordinate for start of layout."""
    width: Real
    """Width of layout."""
    height: Real
    """Height of layout."""
    h_align: Alignment = Alignment.BEGIN
    """Specify horizontal alignment."""
    v_align: Alignment = Alignment.BEGIN
    """Specify vertical alignment."""
    scale: Scale = Scale.FIT
    """Specify how (and if) images are scaled."""


# color - thin wrapper on str right now, and there are only
# some forms that PIL allows, so this should be smarter one day
# https://pillow.readthedocs.io/en/stable/reference/ImageColor.html
Color = NewType('Color', str)

__all__ = [
    'Real',
    'FreeTypeFont',
    'Rect',
    'Alignment',
    'LayoutDef',
    'Color',
]