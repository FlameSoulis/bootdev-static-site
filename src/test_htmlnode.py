import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "A Paragraph")
        node2 = HTMLNode("p", "A Paragraph")
        self.assertEqual(node, node2)
    def test_eq_props(self):
        node = HTMLNode("a", "My Page", None,{"target":"_blank", "href":"https://flamesoulis.com"})
        node2 = HTMLNode("a", "My Page", None,{"target":"_blank", "href":"https://flamesoulis.com"})
        self.assertEqual(node, node2)
    def test_neq_tag(self):
        node = HTMLNode("p", "A Paragraph")
        node2 = HTMLNode("a", "A Paragraph")
        self.assertNotEqual(node, node2)
    def test_neq_value(self):
        node = HTMLNode("p", "A Paragraph")
        node2 = HTMLNode("p", "A Different Paragraph")
        self.assertNotEqual(node, node2)
    def test_neq_props(self):
        node = HTMLNode("a", "My Page", None,{"target":"_blank", "href":"https://flamesoulis.com"})
        node2 = HTMLNode("a", "My Page", None,{"target":"_blank", "href":"https://google.com"})
        self.assertNotEqual(node, node2)
    def test_props_to_html_empty(self):
        node = HTMLNode("div", "Hello", None, {})
        assert node.props_to_html() == ""
    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        assert node.props_to_html() == ' href="https://example.com"'

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_raw(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    def test_leaf_to_html_props(self):
        node = LeafNode("a", "My site", {"target":"_blank", "href":"https://flamesoulis.com"})
        self.assertEqual(node.to_html(), "<a target=\"_blank\" href=\"https://flamesoulis.com\">My site</a>")
    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_parent_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )
    def test_parent_no_value(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, None)
            node.to_html()
    def test_parent_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()