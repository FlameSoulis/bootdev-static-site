from textnode import *
from htmlnode import *
from blocktype import *
from inline_markdown import *

def markdown_to_html_node(markdown):
	#break it down
	blocks = markdown_to_blocks(markdown)
	#Prepare the master node
	master_parent_node = ParentNode("div",[])
	#Begin the loop
	for block in blocks:
		#Determine block type
		block_type = block_to_block_type(block)
		#Do some work
		match block_type:
			case BlockType.CODE:
				master_parent_node.children.append(handle_block_code(block))
			case BlockType.PARAGRAPH:
				master_parent_node.children.append(handle_block_paragraph(block))
			case BlockType.QUOTE:
				master_parent_node.children.append(handle_block_quote(block))
			case BlockType.UNORDERED_LIST:
				master_parent_node.children.append(handle_block_unorderedlist(block))
			case BlockType.ORDERED_LIST:
				master_parent_node.children.append(handle_block_orderedlist(block))
			case BlockType.HEADING:
				master_parent_node.children.append(handle_block_headers(block))
	return master_parent_node


def text_to_children(text):
	#Get the TextNodes
	text_nodes = text_to_textnodes(text)
	#Turn the text nodes to htmlnodes (well leaf, but you get the idea)
	leaf_nodes = list(map(text_node_to_html_node, text_nodes))
	return leaf_nodes

def handle_block_code(block):
	# Remove the tags
	body = block[3:-3].lstrip()
	processed_body = text_node_to_html_node(TextNode(body,TextType.TEXT))
	code_node = ParentNode("code", [processed_body])
	pre_node = ParentNode("pre", [code_node])
	return pre_node

def handle_block_paragraph(text):
	text = text.replace("\n", " ")
	children = text_to_children(text)
	return ParentNode("p",children)

def handle_block_quote(text):
	lines = text.split("\n")
	for i,line in enumerate(lines):
		#Remove the "> "
		lines[i]=line[2:]
	new_text = " ".join(lines)
	children = text_to_children(new_text)
	return ParentNode("blockquote",children)

def handle_block_unorderedlist(text):
	lines = text.split("\n")
	children = []
	for i,line in enumerate(lines):
		#Remove the "- "
		children.append(ParentNode("li", text_to_children(line[2:])))
	return ParentNode("ul", children)

def handle_block_orderedlist(text):
	lines = text.split("\n")
	children = []
	for i,line in enumerate(lines):
		#Remove the "- "
		filtered_line = line.split(". ",1)
		children.append(ParentNode("li", text_to_children(filtered_line[1])))
	return ParentNode("ol", children)

def handle_block_headers(text):
	filtered_text = text.split(" ",1)
	header_size = len(filtered_text[0])
	return ParentNode(f"h{header_size}", text_to_children(filtered_text[1]))

def extract_title(markdown):
	# First split the stuff up
	lines = markdown.split("\n")
	# Run through them
	for line in lines:
		#Check if it's a header 'block'
		if block_to_block_type(line) ==  BlockType.HEADING:
			# Check if it's an H1
			split_check = line.split(" ", 1)
			if split_check[0] == "#":
				return split_check[1].strip()
	raise Exception("Header not found in markdown!")
