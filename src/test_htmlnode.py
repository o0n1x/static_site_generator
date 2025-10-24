import unittest

from htmlnode import HTMLNode , LeafNode , ParentNode


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


    #tests for class ParentNode
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_2_children(self):
        child_node = LeafNode("span", "child")
        child_node1 = LeafNode("a", "child2")
        parent_node = ParentNode("div", [child_node,child_node1])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><a>child2</a></div>")
    def test_to_html_children_error(self):
        parent_node = ParentNode("div", {})
        self.assertRaises(ValueError,parent_node.to_html)
    def test_parent_node_children_error2(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError,parent_node.to_html)
    def test_parent_node_children_error3(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError,parent_node.to_html)
if __name__ == "__main__":
    unittest.main()