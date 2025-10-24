from textnode import TextNode , TextType

class HTMLNode():
    def __init__(self,tag=None,value=None,children=None,props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("not Implemented")
    def props_to_html(self):
        rslt = ""
        for name,value in self.props.items():
            rslt += f" {name}={value}"
        return rslt
    def __repr__(self):
        return f"<{self.tag}> {self.value} </{self.tag}> \n props:{self.props_to_html()} \n {self.children}"
    
def text_node_to_html_node(text_node):
    
    match (text_node.text_type):
        case (TextType.TEXT):
            return LeafNode(None,text_node.text)
        case (TextType.BOLD):
            return LeafNode("b",text_node.text)
        case (TextType.ITALIC):
            return LeafNode("i",text_node.text)
        case (TextType.CODE):
            return LeafNode("code",text_node.text)
        case (TextType.LINK):
            return LeafNode("a",text_node.text,{"href": text_node.url})
        case (TextType.IMAGE): 
            return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
        case (_):
            raise ValueError("Input TextNode is invalid")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props={}):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("All parent nodes must have a tag")
        if self.children == None or type(self.children) != list or self.children == []:
            raise ValueError("Must specify children and in list form")
        
        child_html = ""
        for child in self.children:
            child_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"
    



