import unittest

from textnode import TextNode, TextType
from mdreader import split_nodes_delimiter , extract_markdown_images , extract_markdown_links


class TestTextNode(unittest.TestCase):
    def test_simple(self):
        node = TextNode("This is a **text** node", TextType.TEXT)
        resultnode1 = TextNode("This is a ", TextType.TEXT)
        resultnode2 = TextNode("text", TextType.BOLD)
        resultnode3 = TextNode(" node", TextType.TEXT)
        correct = [resultnode1,resultnode2,resultnode3]
        self.assertEqual(correct,split_nodes_delimiter([node],"**",TextType.BOLD))
    def test_empty(self):
        node = TextNode("This is a **** node", TextType.TEXT)
        resultnode1 = TextNode("This is a ", TextType.TEXT)
        resultnode2 = TextNode("", TextType.BOLD)
        resultnode3 = TextNode(" node", TextType.TEXT)
        correct = [resultnode1,resultnode2,resultnode3]
        self.assertEqual(correct,split_nodes_delimiter([node],"**",TextType.BOLD))
    def test_front_edge(self):
        node = TextNode("**text** node", TextType.TEXT)
        resultnode2 = TextNode("text", TextType.BOLD)
        resultnode3 = TextNode(" node", TextType.TEXT)
        correct = [resultnode2,resultnode3]
        self.assertEqual(correct,split_nodes_delimiter([node],"**",TextType.BOLD))
    def test_end_edge(self):
        node = TextNode("This is a **text**", TextType.TEXT)
        resultnode1 = TextNode("This is a ", TextType.TEXT)
        resultnode2 = TextNode("text", TextType.BOLD)
        correct = [resultnode1,resultnode2]
        self.assertEqual(correct,split_nodes_delimiter([node],"**",TextType.BOLD))
    def test_multiple(self):
        node = TextNode("This is a **text** node **text** node", TextType.TEXT)
        resultnode1 = TextNode("This is a ", TextType.TEXT)
        resultnode2 = TextNode("text", TextType.BOLD)
        resultnode3 = TextNode(" node ", TextType.TEXT)
        resultnode4 = TextNode("text", TextType.BOLD)
        resultnode5 = TextNode(" node", TextType.TEXT)
        correct = [resultnode1,resultnode2,resultnode3,resultnode4,resultnode5]
        self.assertEqual(correct,split_nodes_delimiter([node],"**",TextType.BOLD))
    def test_simple_italic(self):
        node = TextNode("This is a _text_ node", TextType.TEXT)
        resultnode1 = TextNode("This is a ", TextType.TEXT)
        resultnode2 = TextNode("text", TextType.ITALIC)
        resultnode3 = TextNode(" node", TextType.TEXT)
        correct = [resultnode1,resultnode2,resultnode3]
        self.assertEqual(correct,split_nodes_delimiter([node],"_",TextType.ITALIC))
    def test_simple_code(self):
        node = TextNode("This is a `text` node", TextType.TEXT)
        resultnode1 = TextNode("This is a ", TextType.TEXT)
        resultnode2 = TextNode("text", TextType.CODE)
        resultnode3 = TextNode(" node", TextType.TEXT)
        correct = [resultnode1,resultnode2,resultnode3]
        self.assertEqual(correct,split_nodes_delimiter([node],"`",TextType.CODE))
    def test_multiple_diffrent(self):
        node = TextNode("This is a _text_ node _text_ node", TextType.TEXT)
        resultnode1 = TextNode("This is a ", TextType.TEXT)
        resultnode2 = TextNode("text", TextType.ITALIC)
        resultnode3 = TextNode(" node ", TextType.TEXT)
        resultnode4 = TextNode("text", TextType.ITALIC)
        resultnode5 = TextNode(" node", TextType.TEXT)
        correct = [resultnode1,resultnode2,resultnode3,resultnode4,resultnode5]
        self.assertEqual(correct,split_nodes_delimiter([node],"_",TextType.ITALIC))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
    def test_extract_markdown_images_empty(self):
        matches = extract_markdown_images(
            "This is text with an ![image]()"
        )
        self.assertListEqual([("image","")], matches)
    def test_extract_markdown_images_empty2(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("","https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)


    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links_empty(self):
        matches = extract_markdown_links(
            "This is text with an [](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links_empty(self):
        matches = extract_markdown_links(
            "This is text with an [image]()"
        )
        self.assertListEqual([("image", "")], matches)
    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links(
            "This is text with an [image(https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
    def test_extract_markdown_links_none2(self):
        matches = extract_markdown_links(
            "This is text with an [image]https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
    def test_extract_markdown_links_none3(self):
        matches = extract_markdown_links(
            "This is text with an (https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
    def test_extract_markdown_links_none4(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)
    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
    
if __name__ == "__main__":
    unittest.main()

