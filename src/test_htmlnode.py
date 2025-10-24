import unittest

from htmlnode import HTMLNode , LeafNode


class TestTextNode(unittest.TestCase):
    #tests for parent class HTMLNode

    def test_print(self):
        node = HTMLNode("a","this is a test",[],{"href": "https://www.google.com"})
        self.assertEqual(str(node),"<a> this is a test </a> \n props: href=https://www.google.com \n []")
    def test_props1(self):
        node = HTMLNode("a","this is a test",[],{"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html()," href=https://www.google.com")
    def test_props2(self):
        node1 = HTMLNode("a","this is a test",[],{"href": "https://www.google.com","test1": "https://www.boot.dev"})
        self.assertEqual(node1.props_to_html()," href=https://www.google.com test1=https://www.boot.dev")
    def test_properties(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {})
    
    #tests for class LeafNode
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!") 
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me.. I dare you",{"href": '"https://www.facebook.com"'})
        self.assertEqual(node.to_html(), '<a href="https://www.facebook.com">Click me.. I dare you</a>')
    def test_leaf_to_html_text(self):
        node = LeafNode(None,"Hello, world?") 
        self.assertEqual(node.to_html(), "Hello, world?")

if __name__ == "__main__":
    unittest.main()