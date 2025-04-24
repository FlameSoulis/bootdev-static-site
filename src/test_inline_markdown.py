import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_links,
    extract_markdown_images,
    text_to_textnodes
)

from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This statement is **false**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 2
        assert new_nodes[0].text == "This statement is "
        assert new_nodes[1].text == "false"
        assert new_nodes[1].text_type == TextType.BOLD
        
        node = TextNode("_spicy_ facts", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        assert len(new_nodes) == 2
        assert new_nodes[0].text == "spicy"
        assert new_nodes[1].text == " facts"
        assert new_nodes[1].text_type == TextType.TEXT
    def test_split_nodes_delimiter_edgecase(self):
        node = TextNode("**Really****bad****idea**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "Really"
        assert new_nodes[1].text == "bad"
        assert new_nodes[2].text == "idea"
        assert new_nodes[2].text_type == TextType.BOLD
        
        node = TextNode("**Peppers** are _spicy_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        assert len(new_nodes) == 2
        assert new_nodes[0].text == "**Peppers** are "
        assert new_nodes[1].text == "spicy"
        assert new_nodes[1].text_type == TextType.ITALIC
    def test_split_nodes_delimiter_mixed(self):
        node = TextNode("**Shaken**, not _stirred_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "Shaken"
        assert new_nodes[1].text == ", not "
        assert new_nodes[2].text == "stirred"
        assert new_nodes[0].text_type == TextType.BOLD
        assert new_nodes[1].text_type == TextType.TEXT
        assert new_nodes[2].text_type == TextType.ITALIC
    def test_split_nodes_delimiter_errors(self):
        with self.assertRaises(Exception) as context:
            node = TextNode("Never ending **boldness", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertTrue("is not a valid markdown" in str(context.exception))

        with self.assertRaises(Exception) as context:
            node = TextNode("_Broken__on the__inside", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertTrue("is not a valid markdown" in str(context.exception))

    def test_extract_markdown_images(self):
        test = extract_markdown_images("This is a bird ![the bird](https://somebird.jpg)")
        assert len(test) == 1
        assert test[0][0] == "the bird"
        assert test[0][1] == "https://somebird.jpg"
    def test_extract_markdown_links(self):
        test = extract_markdown_links("This is a [link](https://google.com)")
        assert len(test) == 1
        assert test[0][0] == "link"
        assert test[0][1] == "https://google.com"
    def test_split_nodes_image(self):
        node = TextNode("This is a bird ![the bird](https://somebird.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        assert len(new_nodes) == 2
    def test_split_nodes_links(self):
        node = TextNode("This is [a link](https://google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assert len(new_nodes) == 2

        node = TextNode("This is [a link](https://google.com) and [a better site](https://flamesoulis.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        assert len(new_nodes) == 4
    def test_text_to_textnodes(self):
        test = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        assert len(test) == 10
        #print(test)


if __name__ == "__main__":
    unittest.main()
