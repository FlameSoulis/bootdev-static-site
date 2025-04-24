import unittest
from blocktype import (
	BlockType,
	block_to_block_type
)

class TestBlockType(unittest.TestCase):
	def test_block_to_block_type_headers(self):
		assert block_to_block_type("# A Header") == BlockType.HEADING
		assert block_to_block_type("## A Header") == BlockType.HEADING
		assert block_to_block_type("### A Header") == BlockType.HEADING
		assert block_to_block_type("#### A Header") == BlockType.HEADING
		assert block_to_block_type("##### A Header") == BlockType.HEADING
		assert block_to_block_type("###### A Header") == BlockType.HEADING
		assert block_to_block_type("####### NOT A Header") == BlockType.PARAGRAPH
		assert block_to_block_type("######") == BlockType.PARAGRAPH
	def test_block_to_block_type_code(self):
		assert block_to_block_type("```dank code```") == BlockType.CODE
		assert block_to_block_type("```python\nprint('Hello World!')```") == BlockType.CODE
		assert block_to_block_type("```This statement is false") == BlockType.PARAGRAPH
		assert block_to_block_type("`Me too`") == BlockType.PARAGRAPH
	def test_block_to_block_type_quote(self):
		assert block_to_block_type(">A quote?") == BlockType.QUOTE
		assert block_to_block_type(">A quote!\n> This is nice") == BlockType.QUOTE
		assert block_to_block_type(">A quote?\nNo, not quite") == BlockType.PARAGRAPH
	def test_block_to_block_type_unordered(self):
		assert block_to_block_type("- A list?") == BlockType.UNORDERED_LIST
		assert block_to_block_type("- A list!\n- This is also nice") == BlockType.UNORDERED_LIST
		assert block_to_block_type("- List?\n-No, not quite") == BlockType.PARAGRAPH
	def test_block_to_block_type_ordered(self):
		assert block_to_block_type("1. A fresh start") == BlockType.ORDERED_LIST
		assert block_to_block_type("1. Type Code\n2. Hit build\n3. ???\n4. Profit") == BlockType.ORDERED_LIST
		assert block_to_block_type("1. Start here\n3. Wait, what?") == BlockType.PARAGRAPH
