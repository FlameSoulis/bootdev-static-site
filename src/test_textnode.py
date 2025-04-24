import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_neq_string(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is also a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    def test_neq_url(self):
        node = TextNode("The best search engine ever", TextType.LINK, "https://bing.com")
        node2 = TextNode("The best search engine ever", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)
    def test_link_nourl(self):
        node = TextNode("Did I remember a link?", TextType.LINK)
        node2 = TextNode("Did I remember a link?", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()
