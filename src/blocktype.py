from enum import Enum
import re

class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered list"
	ORDERED_LIST = "ordered list"

def block_to_block_type(block):
	#Arth thou a header?
	if re.match(r"^(#{1,6} )", block):
		return BlockType.HEADING
	if block.startswith("```") and block.endswith("```") and len(block) > 6:
		return BlockType.CODE
	# this part is more involved so...
	if block[0] == ">":
		for line in block.split("\n"):
			if line[0] != ">":
				return BlockType.PARAGRAPH
		return BlockType.QUOTE
	if block.startswith("- "):
		for line in block.split("\n"):
			if not line.startswith("- "):
				return BlockType.PARAGRAPH
		return BlockType.UNORDERED_LIST
	if block.startswith("1. "):
		for i,line in enumerate(block.split("\n")):
			if not line.startswith(f"{i+1}. "):
				return BlockType.PARAGRAPH
		return BlockType.ORDERED_LIST
	# If we are STILL a paragraph type, then just return it!
	return BlockType.PARAGRAPH
