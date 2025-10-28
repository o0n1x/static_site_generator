from mdreader import *
from inlinereader import *
from htmlnode import *
import os

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, file)) :
            html_file = file.replace("md","html")
            generate_page(os.path.join(dir_path_content, file) , template_path , os.path.join(dest_dir_path, html_file))
        else:
            generate_pages_recursive(os.path.join(dir_path_content, file),template_path,os.path.join(dest_dir_path, file))


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = open(from_path,"r", encoding="utf-8").read()
    template = open(template_path,"r", encoding="utf-8").read()
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Content }}",content)
    template = template.replace("{{ Title }}",title)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    open(dest_path,"w").write(template)


def extract_title(markdown):
    matches = re.search(r"^\s*#{1} ([^\n]+)",markdown,flags=re.M)
    if not matches:
        raise Exception("title not found")
    return matches.group(1) 


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
    new_nodes = []
    for node in leafnodes:
        splitted = re.match(r"(\d+\. )(.*)",node.value)
        node.value = splitted.group(2) if splitted else ""
        children = text_to_textnodes(node.value)
        parent = ParentNode("li",[])
        for child in children:
            parent.children.append(text_node_to_html_node(child))
        new_nodes.append(parent)
    return new_nodes

def unorderblock_to_leafnodes(text):
    leafnodes = listblock_to_leafnodes(text)
    new_nodes = []
    for node in leafnodes:
        node.value = node.value[2:]
        children = text_to_textnodes(node.value)
        parent = ParentNode("li",[])
        for child in children:
            parent.children.append(text_node_to_html_node(child))
        new_nodes.append(parent)
    return new_nodes

def quote_to_leafnode(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    for node in leaf_nodes:
        node.value = node.value.replace("> ","")
        node.value = re.sub(' +', ' ', node.value)
    return leaf_nodes