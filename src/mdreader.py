
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
    regex = r"[^!]\[([^[\]]*)\]\(([^[\]]*)\)" # [anything](anything . anything)
    return re.findall(regex,text)

def extract_markdown_images(text):
    regex = r"!\[([^[\]]*)\]\(([^[\]]*)\)" # ![anything](anything . anything)
    return re.findall(regex,text)


        