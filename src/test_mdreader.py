import unittest

from mdreader import *



class TestTextNode(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks2(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

### this is a header

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "### this is a header",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_extra(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



### this is a header



- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "### this is a header",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_spaces(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

      ### this is a header

        - This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "### this is a header",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks3(self):
        md = """
This is **bolded** paragraph
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line\n\n\n### this is a header

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "### this is a header",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_simple(self):
        md = """
- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_none(self):
        md = """
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                
            ],
        )
    def test_markdown_to_blocks_only_newline(self):
        md = """\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                
            ],
        )
    def test_markdown_to_blocks_only_newline2(self):
        md = """ \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                
            ],
        )
    def test_markdown_to_blocks_only_newline3(self):
        md = """ \n \n \n \n \n \n n\n \n \n \n \n \n \n \n \n \n \n \n """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "n",
            ],
        )
    def test_block_to_block_type(self):
        md = "this is a paragraph"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        md = ">this is a quote"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.QUOTE)
    def test_block_to_block_type_quote_multiple(self):
        md = """>this is a quote
>this is a quote
>this is a quote
"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.QUOTE)
    def test_block_to_block_type_not_quote(self):
        md = """>this is a quote
>this is a quote
this is not a quote
"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.PARAGRAPH)
    def test_block_to_block_type_heading(self):
        md = "# this is a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.HEADING)
    def test_block_to_block_type_heading2(self):
        md = "###### this is a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.HEADING)
    def test_block_to_block_type_not_heading(self):
        md = "####### this is a heading"
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.PARAGRAPH)
    def test_block_to_block_type_code(self):
        md = """```test
sdds
fjkdls
```"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.CODE)
    def test_block_to_block_type_code_single(self):
        md = """```test```"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.CODE)
    def test_block_to_block_type_unordered(self):
        md = """- test
- sdds
- fjkdls"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.UNORDERED)
    def test_block_to_block_type_not_unordered(self):
        md = """test
- sdds
- fjkdls"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.PARAGRAPH)
    def test_block_to_block_type_ordered(self):
        md = """1. test
2. sdds
3. fjkdls"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.ORDERED)
    def test_block_to_block_type_not_ordered(self):
        md = """test
2. sdds
3. fjkdls"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.PARAGRAPH)
    def test_block_to_block_type_not_ordered2(self):
        md = """3. test
2. sdds
3. fjkdls"""
        block_type = block_to_block_type(md)
        self.assertEqual(block_type,BlockType.PARAGRAPH)
if __name__ == "__main__":
    unittest.main()

