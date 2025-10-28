from mdreader import *
from inlinereader import *
from htmlnode import *
import math

def markdown_to_html_node(markdown):
    
    md_blocks = markdown_to_blocks(markdown)

    root_node = ParentNode("div",[])

    for block in md_blocks:
        root_node.children.append(block_to_node(block))
    return root_node

def block_to_node(block):
    block_type = block_to_block_type(block)
    html_node = None
    match (block_type):
        case (BlockType.PARAGRAPH):
            html_node = ParentNode("p",textnodes_to_leafnodes(block))
        case (BlockType.HEADING):
            heading = 0
            for i in block[0:7]:
                if i == "#":
                    heading += 1
                else:
                    break
            html_node = ParentNode("h"+str(heading),textnodes_to_leafnodes(block[heading+1:]))
        case (BlockType.CODE):
            clean_block = block[3:-3]
            if clean_block[0] == "\n":
                clean_block = clean_block[1:]
            html_node = ParentNode("pre",[text_node_to_html_node(TextNode(clean_block,TextType.CODE))])
        case (BlockType.QUOTE):
            html_node = ParentNode("blockquote",quote_to_leafnode(block))
        case (BlockType.UNORDERED):
            html_node = ParentNode("ul",unorderblock_to_leafnodes(block))
        case (BlockType.ORDERED):
            html_node = ParentNode("ol",orderblock_to_leafnodes(block))
        case _:
            pass
    return html_node

def textnodes_to_leafnodes(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    for node in leaf_nodes:
        node.value = node.value.replace("\n"," ")
        node.value = re.sub(' +', ' ', node.value)
    return leaf_nodes

def listblock_to_leafnodes(text):
    nodes = text.split("\n")
    leafnodes = []
    for node in nodes:
        leafnodes.append(LeafNode("li",node))
    return leafnodes

def orderblock_to_leafnodes(text):
    leafnodes = listblock_to_leafnodes(text)
    for node in leafnodes:
        splitted = re.match(r"(\d+\. )(.*)",node.value)
        node.value = splitted.group(2) if splitted else ""
    return leafnodes

def unorderblock_to_leafnodes(text):
    leafnodes = listblock_to_leafnodes(text)

    for node in leafnodes:
        node.value = node.value[2:]
    return leafnodes

def quote_to_leafnode(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    for node in leaf_nodes:
        node.value = node.value.replace("> ","")
        node.value = re.sub(' +', ' ', node.value)
    return leaf_nodes