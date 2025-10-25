from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered list"
    ORDERED = "ordered list"



def markdown_to_blocks(markdown):
    split_md = markdown.split("\n\n")
    for i in range(len(split_md)):
        split_md[i] = split_md[i].strip(" \n")
    
    return list(filter(lambda x: False if x == "" else True,split_md))


def block_to_block_type(markdown):
    if re.fullmatch(r"#{1,6}[^#]*",markdown):
        return BlockType.HEADING
    if re.fullmatch(r"```[\s\S]*```",markdown):
        return BlockType.CODE
    if re.fullmatch(r"((>.*)\n*)+",markdown):
        return BlockType.QUOTE
    if re.fullmatch(r"((- .*)\n*)+",markdown):
        return BlockType.UNORDERED
    if re.fullmatch(r"((\d+\. .*)\n*)+",markdown):
        num = 0
        is_ordered = True
        for line in markdown.split("\n"):
            num += 1
            if re.match(r"\d+",line).group()[0] == str(num):
                pass
            else:
                is_ordered = False
        if is_ordered:
            return BlockType.ORDERED
    return BlockType.PARAGRAPH


