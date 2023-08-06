from collections.abc import Sequence
import logging
from pathlib import Path
from typing import Mapping
from PIL import Image
from skit._types import Real, LayoutDef, Color, FreeTypeFont, Alignment
from skit.render import DrawCommand, SingleImageRenderer
from abc import ABC, abstractmethod


logger = logging.getLogger(__file__)


class CardManipulation(ABC):
    @abstractmethod
    def background(self, color: str): pass

    @abstractmethod
    def layout(self, name: str, layoutdef: LayoutDef): pass

    @abstractmethod
    def layouts(self, names: Sequence[str], layoutdefs: Sequence[LayoutDef]): pass

    @abstractmethod
    def layouts_map(self, layouts: Mapping[str, LayoutDef]): pass

    @abstractmethod
    def text(
        self, text: str,
        layout: str,
        font: FreeTypeFont | None,
        color: Color | None,
    ): pass

    @abstractmethod
    def rectangle(
        self,
        layout: str,
        color: Color | None,
        thickness: Real | None,
    ): pass

    @abstractmethod
    def filled_rectangle(
        self,
        layout: str,
        color: Color,
    ): pass

    @abstractmethod
    def image(
        self,
        image: Path,
        layout: str,
    ): pass

    @abstractmethod
    def render_png(self, filename: str): pass

    @abstractmethod
    def render_pdf(self, filename: str, resolution: int, single_file: bool): pass


class Card(CardManipulation):
    "A single card."
    def __init__(self, width: int = 750, height: int = 1050):
        """Create a new card of a certain `width` and `height`."""
        self._width = width
        self._height = height
        self._layouts = {}
        self._background = '#ffffff00'
        self._commands = []

    def background(self, color: str):
        "Set the background color for this card."
        assert type(color) is str

        logger.debug(f"setting background to {color}")
        self._background = color

    def layout(self, name: str, layoutdef: LayoutDef):
        "Create a new layout for this card."
        assert Alignment(layoutdef.h_align)
        assert Alignment(layoutdef.v_align)

        logger.debug(f"creating layout area {name}")
        self._layouts[name] = {
            'x': layoutdef.x,
            'y': layoutdef.y,
            'width': layoutdef.width,
            'height': layoutdef.height,
            'h_align': layoutdef.h_align,
            'v_align': layoutdef.v_align,
            'scale': layoutdef.scale,
        }
    
    def layouts(self, names: Sequence[str], layoutdefs: Sequence[LayoutDef]):
        "Create multiple layouts for this card."
        assert len(names) == len(layoutdefs), "mismatched names/layoutdefs arguments"
        
        for name, layoutdef in zip(names, layoutdefs):
            self.layout(name, layoutdef)

    def layouts_map(self, layouts: Mapping[str, LayoutDef]):
        "Create multiple layouts from a dictionary."
        for name, layoutdef in layouts.items():
            self.layout(name, layoutdef)

    def text(self, text: str, layout: str, font: FreeTypeFont | None = None, color: Color | None = None):
        "Add text to this card."
        assert type(text) is str

        if layout in self._layouts:
            logger.debug(f"adding '{text}' in {layout}")
            self._commands.append({
                'op': DrawCommand.TEXT,
                'layout': layout,
                'text': text,
                'font': font,
                'color': color,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def rectangle(self, layout: str, color: Color | None = None, thickness: Real | None = None):
        "Draw a rectangle on this card."
        if layout in self._layouts:
            logger.debug(f"adding rectangle for {layout}")
            self._commands.append({
                'op': DrawCommand.RECTANGLE,
                'layout': layout,
                'color': color,
                'thickness': thickness,
                'filled': False,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def filled_rectangle(self, layout: str, color: Color):
        "Draw a filled rectangle on this card."
        if layout in self._layouts:
            logger.debug(f"adding rectangle for {layout}")
            self._commands.append({
                'op': DrawCommand.RECTANGLE,
                'layout': layout,
                'color': color,
                'thickness': 1,
                'filled': True,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def image(self, image: Path, layout: str):
        "Draw an external image on this card."
        if layout in self._layouts:
            logger.debug(f"adding image for {layout}")
            self._commands.append({
                'op': DrawCommand.IMAGE,
                'layout': layout,
                'image': image,
            })
        else:
            raise KeyError(f"missing layout '{layout}'")

    def render_png(self, filename: str):
        "Render this card as a PNG."
        logger.debug(f"rendering {filename}")

        im = (
            SingleImageRenderer(self._layouts)
            .render(self._width, self._height, self._background, self._commands)
        )
        im.save(filename, format='PNG')

    def render_pdf(self, filename: str, resolution: int, single_file=True):
        """
        Render this card as a PDF. It makes no sense to render a single
        card to multiple files, so `single_file` is ignored. PDFs don't
        support the alpha channel, so remove it.
        """
        logger.debug(f"rendering {filename}")

        im = self._get_rgb_image_for_pdf(resolution)
        im.save(filename, format='PDF', resolution=resolution)

    def _get_rgb_image_for_pdf(self, resolution: int):
        logging.debug(f"rendering RGB image")

        im = (
            SingleImageRenderer(self._layouts)
            .render(self._width, self._height, self._background, self._commands)
        )
        final = Image.new('RGB', im.size, self._background)
        final.paste(im)
        return final
