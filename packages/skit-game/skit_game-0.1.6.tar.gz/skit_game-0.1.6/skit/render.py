from enum import Enum
import logging
import math
from PIL import Image, ImageDraw, ImageFont
from skit._types import Color, Alignment, Scale


logger = logging.getLogger(__file__)


# some defaults for fallback
try:
    _DEFAULT_FONT = ImageFont.truetype('Helvetica', 16)
except OSError:
    _DEFAULT_FONT = ImageFont.load_default()
_DEFAULT_COLOR = 'black'
_DEFAULT_THICKNESS = 1


class DrawCommand(Enum):
    TEXT = 'text'
    RECTANGLE = 'rect'
    IMAGE = 'image'


class SingleImageRenderer:
    def __init__(self, layouts):
        self._layouts = layouts

    def render(self, width: int, height: int, background: Color, commands: list[dict]) -> Image.Image:
        with Image.new('RGBA', (width, height), background) as im:
            d = ImageDraw.Draw(im)

            for cmd in commands:
                cmd = cmd.copy()    # don't destroy the original command list
                op = cmd.pop('op')
                match op:
                    case DrawCommand.TEXT:
                        self._render_text(d, **cmd)
                    case DrawCommand.RECTANGLE:
                        self._render_rectangle(d, **cmd)
                    case DrawCommand.IMAGE:
                        self._render_image(im, **cmd)
                    case _:
                        raise ValueError(cmd)

            return im

    def _render_text(self, d, layout, text, color, font):
        logger.debug(f"rendering text '{text}' at {layout}")
        layout = self._layouts[layout]

        match layout['h_align']:
            case Alignment.BEGIN:
                anchor_h = 'l'
                x = layout['x']
            case Alignment.MIDDLE:
                anchor_h = 'm'
                x = layout['x'] + (layout['width'] // 2)
            case Alignment.END:
                anchor_h = 'r'
                x = layout['x'] + layout['width']
            case _:
                raise ValueError(f"h_align value '{layout['h_align']}' unrecognized")

        match layout['v_align']:
            case Alignment.BEGIN:
                y = layout['y']
                anchor_v = 'a'
            case Alignment.MIDDLE:
                y = layout['y'] + (layout['height'] // 2)
                anchor_v = 'm'
            case Alignment.END:
                y = layout['y'] + layout['height']
                anchor_v = 'd'
            case _:
                raise ValueError(f"v_align value '{layout['v_align']}' unrecognized")

        d.text(
            [x, y],
            text,
            fill=color if color else _DEFAULT_COLOR,
            font=font if font else _DEFAULT_FONT,
            anchor=f"{anchor_h}{anchor_v}",
        )
    
    def _render_rectangle(self, d, layout, color, thickness, filled):
        logger.debug(f"rendering rectangle on {layout}")
        layout = self._layouts[layout]
        d.rectangle(
            [
                layout['x'],
                layout['y'],
                layout['x'] + layout['width'],
                layout['y'] + layout['height'],
            ],
            fill=color if filled and color else None,
            outline=color if color else _DEFAULT_COLOR,
            width=thickness if thickness else _DEFAULT_THICKNESS,
        )

    def _render_image(self, im, layout, image):
        logger.debug(f"rendering image at {layout}")
        layout = self._layouts[layout]
        with Image.open(image) as art:
            # compute new image scale
            proposed_scale = self._pick_image_size(art.width, art.height, layout['width'], layout['height'])
            match layout['scale']:
                case Scale.FIT:
                    art = art.resize(proposed_scale)
                case Scale.UP:
                    if art.width < proposed_scale[0] or art.height < proposed_scale[1]:
                        art = art.resize(proposed_scale)
                case Scale.DOWN:
                    if art.width > proposed_scale[0] or art.height > proposed_scale[1]:
                        art = art.resize(proposed_scale)
                case Scale.NONE:
                    pass    # there is nothing to do
                case _:
                    raise ValueError(f"scale value '{layout['scale']}' unrecognized")

            match layout['h_align']:
                case Alignment.BEGIN:
                    left = layout['x']
                case Alignment.MIDDLE:
                    left = layout['x'] + (layout['width'] - art.width) // 2
                case Alignment.END:
                    left = layout['x'] + layout['width'] - art.width
                case _:
                    raise ValueError(f"h_align value '{layout['h_align']}' unrecognized")

            match layout['v_align']:
                case Alignment.BEGIN:
                    top = layout['y']
                case Alignment.MIDDLE:
                    top = layout['y'] + (layout['height'] - art.height) // 2
                case Alignment.END:
                    top = layout['y'] + layout['height'] - art.height
                case _:
                    raise ValueError(f"v_align value '{layout['v_align']}' unrecognized")

            im.alpha_composite(art, (left, top))

    def _pick_image_size(self, img_width, img_height, layout_width, layout_height):
        if img_width == layout_width and img_height == layout_height:
            return img_width, img_height
        
        # unpacking the logic below...
        #   ratio_width = image.width / layout.width
        #   ratio_height = image.height / layout.height
        #   if either ratio is > 1, we are shrinking, so pick the larger one to make sure we fit
        #   if both ratios are < 1, we are growing, so pick the one closer to 1 to maximally fill
        #   either way, we're picking the largest number to use as a scale factor

        scale_factor = max(img_width / layout_width, img_height / layout_height)
        new_width = math.floor(img_width / scale_factor)
        new_height = math.floor(img_height / scale_factor)
        
        return new_width, new_height
