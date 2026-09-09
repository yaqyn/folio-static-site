import unittest

from inline_markdown import split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) "
            "and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            split_nodes_image([node]),
        )

    def test_image_at_start_and_end(self):
        node = TextNode("![start](start.png)middle![end](end.png)", TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("start", TextType.IMAGE, "start.png"),
                TextNode("middle", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "end.png"),
            ],
        )

    def test_image_splitter_preserves_other_nodes(self):
        node = TextNode("already bold", TextType.BOLD)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_image_splitter_keeps_text_without_images(self):
        node = TextNode("plain text", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_link_splitter_does_not_split_images(self):
        image = TextNode("![image](image.png)", TextType.TEXT)
        self.assertEqual(split_nodes_link([image]), [image])

    def test_link_splitter_preserves_other_nodes(self):
        node = TextNode("already italic", TextType.ITALIC)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_link_splitter_keeps_text_without_links(self):
        node = TextNode("plain text", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])


if __name__ == "__main__":
    unittest.main()
