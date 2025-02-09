import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    tag = "h1"
    value = "Hello World!"
    children = "<p>Lorem ipsum...</p>"
    props = {"href": "http://example.com", "target": "_blank"}

    def test_eq(self):
        node1 = HTMLNode(self.tag, self.value, self.children, self.props)
        node2 = HTMLNode(self.tag, self.value, self.children, self.props)
        self.assertEqual(node1, node2)

    def test_tag(self):
        node1 = HTMLNode(self.tag, self.value, self.children, self.props)
        node2 = HTMLNode("a", self.value, self.children, self.props)
        self.assertNotEqual(node1, node2)

    def test_vaule(self):
        node1 = HTMLNode(self.tag, self.value, self.children, self.props)
        node2 = HTMLNode(self.tag, "TEST", self.children, self.props)
        self.assertNotEqual(node1, node2)

    def test_children(self):
        node1 = HTMLNode(self.tag, self.value, self.children, self.props)
        node2 = HTMLNode(self.tag, self.value, None, self.props)
        self.assertNotEqual(node1, node2)

    def test_props(self):
        node1 = HTMLNode(self.tag, self.value, self.children, self.props)
        node2 = HTMLNode(self.tag, self.value, self.children)
        self.assertNotEqual(node1, node2)

    def test_props_html(self):
        node1 = HTMLNode(self.tag, self.value, self.children, self.props)
        node2 = HTMLNode(self.tag, self.value, self.children)

        self.assertEqual(node1.props_to_html(),
                         ' href="http://example.com" target="_blank"')
        self.assertEqual(node2.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
