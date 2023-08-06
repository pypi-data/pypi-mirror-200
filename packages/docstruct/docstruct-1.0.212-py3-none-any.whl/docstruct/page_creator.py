import logging

import cv2

from docstruct.visual_detection.bordered_table_extraction import BorderedTableExtractor
from docstruct.visual_detection.vis_line_detection import VisLineDetector, VisLineMerger

from .hocr_parser import HocrParser
from .text_block import Page, Word
from .textract_parser import TextractParser


class PageCreator:
    def __init__(
        self,
        image_path: str,
        textract_response: dict = None,
        hocr_path: str = None,
    ):
        self.image_path = image_path

        self.textract_response = textract_response
        self.hocr_path = hocr_path
        self.image = cv2.imread(image_path)
        self.image_height, self.image_width = self.image.shape[:2]
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def get_average_word_height(self, words: list[Word]) -> float:
        """Get the average size of a list of words."""
        heights = [word.bounding_box.get_height() for word in words]
        if not heights:
            return 0
        return sum(heights) / len(heights)

    def parse_page(self) -> Page:
        if self.textract_response:
            parser = TextractParser(self.textract_response)
            page = parser.parse_response()
        else:
            parser = HocrParser(self.hocr_path)
            page = parser.parse_page()

        words = list(page.get_all(Word))
        if not words:
            return page
        try:
            hor_threshold = self.get_average_word_height(page)
            ver_threshold = hor_threshold * self.image_height / self.image_width
            length_threshold = int(hor_threshold * self.image_height)

            line_detector = VisLineDetector(self.gray_image, length_threshold)
            hor_lines, ver_lines = line_detector.main()
            hor_line_merger = VisLineMerger(hor_lines, hor_threshold)
            merged_hor_lines = hor_line_merger.main()

            ver_line_merger = VisLineMerger(ver_lines, ver_threshold)
            merged_ver_lines = ver_line_merger.main()
            page.set_vis_lines(merged_hor_lines, merged_ver_lines)
            table_detector = BorderedTableExtractor(
                merged_hor_lines, merged_ver_lines, hor_threshold, ver_threshold
            )
            tables = table_detector.main()
            for table in tables:
                table.group_words_into_cells(words)
            page.set_tables(tables)
        except Exception as e:
            logging.error(e)
        return page
