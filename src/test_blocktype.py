import unittest

from blocktype import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("A normal paragraph."), BlockType.PARAGRAPH)

    def test_headings_one_through_six(self):
        for count in range(1, 7):
            self.assertEqual(
                block_to_block_type("#" * count + " Heading"),
                BlockType.HEADING,
            )

    def test_invalid_heading_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')\n```"),
            BlockType.CODE,
        )

    def test_invalid_code_block_is_paragraph(self):
        self.assertEqual(block_to_block_type("```not multiline```"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("```\nmissing ending"), BlockType.PARAGRAPH)

    def test_quote_block(self):
        self.assertEqual(
            block_to_block_type("> first quote\n>second quote"),
            BlockType.QUOTE,
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- first\n- second\n- third"),
            BlockType.UNORDERED_LIST,
        )

    def test_ordered_list_must_start_at_one_and_increment(self):
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"),
            BlockType.ORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("2. second\n3. third"),
            BlockType.PARAGRAPH,
        )
        self.assertEqual(
            block_to_block_type("1. first\n3. third"),
            BlockType.PARAGRAPH,
        )

    def test_mixed_list_markers_are_paragraphs(self):
        self.assertEqual(
            block_to_block_type("- first\n1. second"),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
