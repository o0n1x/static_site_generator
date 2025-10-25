
from htmlnode import TextNode , TextType
import re

def split_nodes_delimiter(old_nodes,delimiter,text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        in_delimit = False
        while text != "":
            delimited = text.split(delimiter,maxsplit=1)
            if delimited[0] == "" and in_delimit:
                new_nodes.append(TextNode(delimited[0],text_type))
            elif delimited[0] == "":
                pass
            elif not in_delimit:
                new_nodes.append(TextNode(delimited[0],TextType.TEXT))
            elif in_delimit:
                new_nodes.append(TextNode(delimited[0],text_type))
            if len(delimited) > 1:
                text = delimited[1]
            else:
                break
            in_delimit = not in_delimit
        if in_delimit:
            raise Exception(f"a delimiter {delimiter} is not closed in {node.text}")
    return new_nodes
        
def extract_markdown_links(text):
    regex = r"(?<!!)\[([^[\]]*)\]\(([^[\]]*)\)" # [anything](anything . anything)
    return re.findall(regex,text)

def extract_markdown_images(text):
    regex = r"!\[([^[\]]*)\]\(([^[\]]*)\)" # ![anything](anything . anything)
    return re.findall(regex,text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        img_list = extract_markdown_images(text)
        for img_text in img_list:
            texts = text.split(f"![{img_text[0]}]({img_text[1]})",1)
            if texts[0] != "":
                new_nodes.append(TextNode(texts[0],TextType.TEXT))
            new_nodes.append(TextNode(img_text[0],TextType.IMAGE,img_text[1]))
            if len(texts) > 1:
                text = texts[1]
            else:
                text = ""
        if text != "":
            new_nodes.append(TextNode(text,TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        text = node.text
        link_list = extract_markdown_links(text)
        for link_text in link_list:
            texts = text.split(f"[{link_text[0]}]({link_text[1]})",1)
            if texts[0] != "":
                new_nodes.append(TextNode(texts[0],TextType.TEXT))
            new_nodes.append(TextNode(link_text[0],TextType.LINK,link_text[1]))
            if len(texts) > 1:
                text = texts[1]
            else:
                text = ""
        if text != "":
            new_nodes.append(TextNode(text,TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text,TextType.TEXT)
    new_nodes = split_nodes_delimiter([text_node],"**",TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes,"_",TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes,"`",TextType.CODE)
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes