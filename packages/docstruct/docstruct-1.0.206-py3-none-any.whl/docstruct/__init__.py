from .bounding_box import BoundingBox
from .drawer import Drawer
from .hocr_parser import HocrParser
from .page_creator import PageCreator
from .point import Point
from .searchable_pdf import save_searchable_pdf
from .segment import Segment
from .text_block import (
    Character,
    Document,
    Page,
    Area,
    Line,
    Paragraph,
    TextBlock,
    Word,
    Table,
    TableColumn,
    TableCell,
)
from .text_block_splitter import TextBlockSplitter
from .textract_parser import TextractParser

__version__ = "1.0.206"
