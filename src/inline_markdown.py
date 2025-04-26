import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        #Skip non-text for now
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        #Remember the base type
        base_node_type = node.text_type
        #If it's not found, then we can also skip!
        if node.text.find(delimiter) == -1:
            new_nodes.append(node)
            continue
        #Let the rat race begin!
        delimiter_pos = delimiter_next_pos = 0
        #Find the first delimiter
        delimiter_next_pos = node.text.find(delimiter, delimiter_pos)
        while delimiter_next_pos != -1:
            #Make the beginning its own node, unless it's blank
            if delimiter_pos < delimiter_next_pos:
                new_nodes.append(TextNode(node.text[delimiter_pos:delimiter_next_pos], base_node_type))
            #Mark the new beginning
            delimiter_pos = delimiter_next_pos + len(delimiter)
            #Find the next delimiter
            delimiter_next_pos = node.text.find(delimiter, delimiter_pos)
            #If it's -1, well that isn't right
            if(delimiter_next_pos == -1):
                raise Exception(f"\"{node.text}\" is not a valid markdown ({text_type})")
            #Add our new node (via its text_type)
            new_nodes.append(TextNode(node.text[delimiter_pos:delimiter_next_pos], text_type))
            #Offset and check agian
            delimiter_pos = delimiter_next_pos + len(delimiter)
            delimiter_next_pos = node.text.find(delimiter, delimiter_pos)
        #Wrap it up!
        if delimiter_pos < len(node.text):
            new_nodes.append(TextNode(node.text[delimiter_pos:], base_node_type))
    return new_nodes

def extract_markdown_images(text):
    #I literally do not care I 'cheated'
    image_exp = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_exp, text)

def extract_markdown_links(text):
    link_exp = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_exp, text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        #Skip non-text for now
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        #Search up!
        image_urls = extract_markdown_images(node.text)
        #If it's not found, then we can also skip!
        if len(image_urls) == 0:
            new_nodes.append(node)
            continue
        original_text = node.text
        for image_url in image_urls:
            sections = original_text.split(f"![{image_url[0]}]({image_url[1]})", 1)
            if(len(sections[0]) != 0):
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_url[0], TextType.IMAGE, image_url[1]))
            original_text = sections[1]
        if(len(original_text) != 0):
                new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        #Skip non-text for now
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        #Search up!
        link_urls = extract_markdown_links(node.text)
        #If it's not found, then we can also skip!
        if len(link_urls) == 0:
            new_nodes.append(node)
            continue
        original_text = node.text
        for image_url in link_urls:
            sections = original_text.split(f"[{image_url[0]}]({image_url[1]})", 1)
            if(len(sections[0]) != 0):
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_url[0], TextType.LINK, image_url[1]))
            original_text = sections[1]
        if(len(original_text) != 0):
                new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    original_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_delimiter([original_node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes

def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if len(block) == 0:
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks