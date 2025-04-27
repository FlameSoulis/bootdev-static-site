from textnode import TextNode, TextType

class HTMLNode():
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props
	def to_html(self):
		raise NotImplementedError()
	def props_to_html(self):
		if not self.props:
			return ""
		return " " + " ".join(map(lambda x: f"{x[0]}=\"{x[1]}\"", self.props.items()))
	def __eq__(self,other):
		return (
            self.tag == other.tag and 
            self.value == other.value and 
            self.children == other.children and
            self.props == other.props
        )
	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.prop})"

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props = None):
		super().__init__(tag, value, None, props)
	def to_html(self):
		if self.value == None:
			raise ValueError("All leaf nodes must have a value.")
		if self.tag == None:
			return self.value
		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
	def __eq__(self,other):
		return (
            self.tag == other.tag and 
            self.value == other.value and 
            self.props == other.props
        )
	def __repr__(self):
		return f"LeafNode({self.tag}, {self.value}, {self.prop})"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		super().__init__(tag, None, children, props)
	def to_html(self):
		if self.tag == None:
			raise ValueError("All parent nodes must have a tag.")
		if self.children == None:
			raise ValueError("All parent nodes must have a child.")
		return f"<{self.tag}{self.props_to_html()}>" \
			+ "".join(map(lambda x: x.to_html(),self.children)) \
			+ f"</{self.tag}>"
	def __eq__(self,other):
		return (
            self.tag == other.tag and 
            self.value == other.value and 
            self.children == other.children and
            self.props == other.props
        )
	def __repr__(self):
		return f"ParentNode({self.tag}, {self.value}, {self.prop})"

def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.IMAGE:
			return LeafNode("img", "", {"alt":text_node.text, "src":text_node.url})
		case _:
			raise ValueError("TextType doesn't exist!")