"""
.. include:: ../README.md
"""
import copy
import warnings
from .deck import Deck
from .card import Card
from ._types import Rect, Color, Alignment, Scale, LayoutDef

from PIL import ImageFont


# expose ImageFont.truetype() as skit.load_font()
load_font = copy.copy(ImageFont.truetype)
load_font.__doc__ = f"""
A rename/import of [PIL.ImageFont.truetype][truetypedocs].

Required arguments are:
- `font`: A filename or file-like object containing a TrueType font.
If the file is not found in this filename, the loader may also search in other directories, such as the `fonts/`
directory on Windows or `/Library/Fonts/`, `/System/Library/Fonts/` and `~/Library/Fonts/` on macOS.
- `size`: The requested size, in pixels.

See the [upstream documentation][truetypedocs] for the remaining optional parameters.

[truetypedocs]: https://pillow.readthedocs.io/en/stable/reference/ImageFont.html#PIL.ImageFont.truetype
"""


def as_layoutdef(incoming_dict: dict) -> dict | LayoutDef:
    """
    A helper for converting dicts into `Rect`s. Useful parsing layouts from data
    files.

    Pass this to the `object_hook` parameter of `json.load()` to automatically
    convert dictionaries with the correct keys  into `LayoutDef`s.
    Correct keys are `x`, `y`, `width`, and `height`, plus optional
    `h_align`, `v_align`, and `scale`.

    Example:

    ```python
    with open('my_layout.json') as json_in:
        layouts = json.load(json_in, object_hook=skit.json_layout_hook)
    
    # assuming my_layout.json looked like this:
    # {
    #   "mybox": {
    #     "x": 0,
    #     "y": 0,
    #     "width": 100,
    #     "height": 25
    # }

    # then layouts will be:
    layouts = {
        'mybox': LayoutDef(
            x=0, y=0, width=100, height=25,
            h_align=Alignment.BEGIN, v_align=Alignment.BEGIN,
            scale=Scale.FIT,
        ),
    }

    ```
    """
    match incoming_dict:
        case { 'x': _, 'y': _, 'width': _, 'height': _, **rest }:
            if 'h_align' in rest:
                rest['h_align'] = Alignment(incoming_dict['h_align'])
            if 'v_align' in rest:
                rest['v_align'] = Alignment(incoming_dict['v_align'])
            if 'scale' in rest:
                rest['scale'] = Scale(incoming_dict['scale'])
            try:
                vals = incoming_dict.copy()
                vals.update(rest)
                return LayoutDef(**vals)
            except TypeError:
                # If there was something in the incoming data that doesn't
                # belong in LayoutDef, we'll hit this branch. We simply return
                # the dictionary we would have otherwise seen
                warnings.warn(f"{incoming_dict} has keys not convertible to LayoutDef")
                return incoming_dict
        case _:
            return incoming_dict


__all__ = [
    'Deck',
    'Card',
    'Rect',
    'Color',
    'Alignment',
    'Scale',
    'LayoutDef',
    'load_font',
    'as_layoutdef',
]
