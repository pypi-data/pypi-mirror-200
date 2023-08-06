import random
from enum import Enum

from PIL import Image, ImageDraw

from docstruct.visual_detection.vis_line import Orientation, VisLine

from .text_block import Cell, Character, Line, Page, Paragraph, Table, TextBlock, Word


class Color(Enum):
    LIGHT_PINK = (255, 182, 193)
    PEACH = (255, 218, 185)
    SKY_BLUE = (135, 206, 235)
    LAVENDER = (230, 230, 250)
    MINT_GREEN = (152, 255, 152)
    LIGHT_YELLOW = (255, 255, 224)
    PALE_GREEN = (152, 251, 152)
    POWDER_BLUE = (176, 224, 230)
    BEIGE = (245, 245, 220)
    CREAM = (255, 253, 208)
    LIGHT_CORAL = (240, 128, 128)
    PALE_TRRQUOISE = (175, 238, 238)
    LIGHT_BLUE_SKY = (135, 206, 250)
    LIGHT_STEEL_BLUE = (176, 196, 222)
    THISTLE = (216, 191, 216)
    GOLD = (255, 215, 0)


COLORS_MAP = {
    Character: "purple",
    Word: "blue",
    Line: "green",
    Paragraph: "yellow",
    Page: "red",
}
WIDTHS_MAP = {Character: 1, Word: 2, Line: 3, Cell: 3, Paragraph: 4, Table: 4, Page: 5}


def get_random_rgb_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Drawer:
    """
    This class is used to draw bounding boxes of text blocks on an image.
    Example:

    from docstruct import TextBlockDrawer
    image_path = 'foo.png'
    page = Page() ...
    drawer = TextBlockDrawer(image_path)
    drawer.draw(page)
    drawer.show()
    """

    def __init__(self, image_path: str):
        self.image_path = image_path
        self.rgb_image = Image.open(image_path)
        self.alpha_image = Image.new("RGBA", self.rgb_image.size, (255, 255, 255, 0))
        self.width, self.height = self.rgb_image.size
        self.image_drawer = ImageDraw.Draw(self.alpha_image)

    def draw_block_index(self, block: TextBlock, draw_right: bool, draw_top: bool):
        """
        Draws the index of the block on the right top corner of the block.
        """
        bb = block.bounding_box
        top_left = bb.get_top_left()
        left, top = top_left.x * self.width, top_left.y * self.height
        bottom_right = bb.get_bottom_right()
        right, bottom = bottom_right.x * self.width, bottom_right.y * self.height
        top, bottom = self.height - top, self.height - bottom
        hor = right if draw_right else left
        ver = top if draw_top else bottom
        self.image_drawer.text(
            [hor, ver],
            str(block.get_relative_order()),
            fill="black",
        )

    def draw_text_block(
        self, block: TextBlock, color: str = "black", fill: bool = False, width: int = 1
    ):
        """
        Draws the bounding box of the text block on the image, not including it's children.
        """
        bbox = block.bounding_box
        bbox.draw_on_image(
            self.image_drawer, color, self.width, self.height, fill=fill, width=width
        )

    def draw(self, block: TextBlock, *to_draw: list[str]):
        """
        Draws the bounding boxes of the text block on the image, including it's children.
        """
        blocks = list(block.post_order_traversal(block))

        if not to_draw:
            to_draw = list((key.__name__.lower() for key in COLORS_MAP))
        for block in blocks:
            name = type(block).__name__.lower()
            if name not in to_draw:
                continue
            self.draw_text_block(
                block,
                color=COLORS_MAP[type(block)],
                fill=False,
                width=WIDTHS_MAP[type(block)],
            )

        for block in blocks:
            name = type(block).__name__.lower()
            if name not in to_draw:
                continue
            if name == "paragraph":
                self.draw_block_index(block, draw_right=True, draw_top=True)
            elif name == "line":
                self.draw_block_index(block, draw_right=False, draw_top=False)

    def draw_cell(self, cell: Cell, random_color: bool = False):
        if random_color:
            color = get_random_rgb_color()
        else:
            color = (255, 0, 0)
        color = (*color, 100)
        cell.bounding_box.draw_on_image(
            self.image_drawer, color, self.width, self.height, fill=True
        )

    def draw_table(self, table: Table, cell_random_color: bool = True):
        for cell in table.cells:
            self.draw_cell(cell, cell_random_color)
        table.bounding_box.draw_on_image(
            self.image_drawer,
            Color.GOLD.value,
            self.width,
            self.height,
            fill=False,
            width=3,
        )

    def draw_vis_line(self, vis_line: VisLine, color: tuple[int, int, int]):
        if vis_line.orientation == Orientation.HORIZONTAL:
            x0 = vis_line.start * self.width
            x1 = vis_line.end * self.width
            y = self.height - vis_line.axis * self.height
            self.image_drawer.line(
                [x0, y, x1, y],
                fill=color,
                width=3,
            )

        elif vis_line.orientation == Orientation.VERTICAL:
            y0 = self.height - vis_line.start * self.height
            y1 = self.height - vis_line.end * self.height
            x = vis_line.axis * self.width
            self.image_drawer.line(
                [x, y0, x, y1],
                fill=color,
                width=3,
            )

    def draw_vis_lines(
        self,
        vis_lines: list[VisLine],
        random_color: bool = False,
        draw_index: bool = False,
    ):
        for i, vis_line in enumerate(vis_lines):
            if random_color:
                # color = next(self.rgb_generator)
                color = get_random_rgb_color()
            else:
                color = (255, 0, 0)
            self.draw_vis_line(vis_line=vis_line, color=color)

            left = vis_line.start * self.width
            top = self.height - vis_line.axis * self.height
            if draw_index:
                self.image_drawer.text(
                    [left, top],
                    str(i),
                    fill="black",
                )

    def save(self, out_path: str):
        """
        Saves the image to the given path.
        """
        result_image = Image.alpha_composite(
            self.rgb_image.convert("RGBA"), self.alpha_image
        )

        # result_image.show()
        result_image.save(out_path)

    def show(self):
        result_image = Image.alpha_composite(
            self.rgb_image.convert("RGBA"), self.alpha_image
        )

        result_image.show()
