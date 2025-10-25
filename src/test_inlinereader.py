import unittest

from textnode import TextNode, TextType
from inlinereader import *


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
    




    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_images_alone(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                
            ],
            new_nodes,
        )
    def test_split_images_same(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
            ],
            new_nodes,
        )
    def test_split_images_none(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
                
            ],
            new_nodes,
        )





    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_link_alone(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                
            ],
            new_nodes,
        )
    def test_split_links_none(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
                
            ],
            new_nodes,
        )
    def test_split_links_same(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )




        
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)

        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
    def test_text_to_textnodes_all_text(self):
        text = "This is text with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [TextNode("This is text with an italic word and a code block and an obi wan image https://i.imgur.com/fJRm4Vk.jpeg and a link https://boot.dev",TextType.TEXT)],
            new_nodes,
        )

if __name__ == "__main__":
    unittest.main()

