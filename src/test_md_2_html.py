import unittest

from md_2_html import *



class TestTextNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
    def test_paragraphs_2(self):
        md = """This is **bolded** paragraph This is another paragraph with _italic_ text and `code` here"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_quoteblock(self):
        md = """
> test Quote indeed
> test Quote indeed
> test Quote indeed
> test Quote indeed
> test Quote indeed
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>test Quote indeed\ntest Quote indeed\ntest Quote indeed\ntest Quote indeed\ntest Quote indeed</blockquote></div>",
        )
    def test_headingblock(self):
        md = """
### This is a h3 paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a h3 paragraph</h3></div>",
        )
    def test_headingblock2(self):
        md = """
###### This is a h6 paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>This is a h6 paragraph</h6></div>",
        )
    def test_headingblock3(self):
        md = """
#######This is not a heading paragraph
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>#######This is not a heading paragraph</p></div>",
        )
    def test_unordered(self):
        md = """
- test unordered indeed
- test unordered indeed
- test unordered indeed
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>test unordered indeed</li><li>test unordered indeed</li><li>test unordered indeed</li></ul></div>",
        )
    def test_ordered(self):
        md = """
1. test unordered indeed
2. test unordered indeed
3. test unordered indeed
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>test unordered indeed</li><li>test unordered indeed</li><li>test unordered indeed</li></ol></div>",
        )
    def test_ordered_false(self):
        md = """
1.test unordered indeed
2.test unordered indeed
3.test unordered indeed
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>1.test unordered indeed 2.test unordered indeed 3.test unordered indeed</p></div>",
        )
    def test_ordered_mix(self):
        md = """
1. test unordered indeed
2. test unordered indeed
3. test unordered indeed

- test unordered indeed
- test unordered indeed
- test unordered indeed
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>test unordered indeed</li><li>test unordered indeed</li><li>test unordered indeed</li></ol><ul><li>test unordered indeed</li><li>test unordered indeed</li><li>test unordered indeed</li></ul></div>",
        )
    
    
if __name__ == "__main__":
    unittest.main()

