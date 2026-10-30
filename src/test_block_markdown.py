import unittest

from block_markdown import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\n"
                "This is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_strips_block_whitespace(self):
        markdown = "  first block  \n\n\tsecond block\t  "
        self.assertEqual(markdown_to_blocks(markdown), ["first block", "second block"])

    def test_ignores_empty_blocks(self):
        markdown = "\n\nfirst\n\n\n\nsecond\n\n"
        self.assertEqual(markdown_to_blocks(markdown), ["first", "second"])

    def test_empty_markdown_returns_empty_list(self):
        self.assertEqual(markdown_to_blocks("\n\n  \n\n"), [])

    def test_single_block_is_preserved(self):
        self.assertEqual(markdown_to_blocks("single paragraph"), ["single paragraph"])

    def test_tilde_fences_keep_blank_lines_inside_code(self):
        markdown = "before\n\n~~~python\nprint('one')\n\nprint('two')\n~~~\n\nafter"
        self.assertEqual(
            markdown_to_blocks(markdown),
            ["before", "~~~python\nprint('one')\n\nprint('two')\n~~~", "after"],
        )

    def test_fence_language_may_be_separated_by_space(self):
        self.assertEqual(
            markdown_to_blocks("``` python\nprint('hello')\n```"),
            ["``` python\nprint('hello')\n```"],
        )


if __name__ == "__main__":
    unittest.main()
