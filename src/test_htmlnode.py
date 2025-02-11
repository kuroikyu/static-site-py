import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_props(self):
        node = HTMLNode("div", "Hello World!", None, {
                        "class": "greeting", "href": "https://test.cat"})
        self.assertEqual(node.props_to_html(),
                         ' class="greeting" href="https://test.cat"')

    def test_values(self):
        node = HTMLNode("p", "My beautiful content")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "My beautiful content")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)


class TestLeafNode(unittest.TestCase):
    def test_leaf_full(self):
        node1 = LeafNode("a", "Click me!", {
                         "href": "http://example.com", "target": "_blank"})
        target = '<a href="http://example.com" target="_blank">Click me!</a>'
        self.assertEqual(node1.to_html(), target)

    def test_leaf_no_props(self):
        node1 = LeafNode("p", "Welcome to my blog")
        target = '<p>Welcome to my blog</p>'
        self.assertEqual(node1.to_html(), target)

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Oh my!")
        self.assertEqual(node.to_html(), "Oh my!")


class TestParentNode(unittest.TestCase):
    child_node = LeafNode("a", "Click me!", {
        "href": "http://example.com", "target": "_blank"})

    def test_Parent_to_html(self):
        node = ParentNode("p", self.child_node)
        self.assertEqual(node.to_html(
        ), '<p><a href="http://example.com" target="_blank">Click me!</a></p>')

    def test_2_parent_to_html(self):
        parent_node1 = ParentNode("p", self.child_node)
        parent_node2 = ParentNode("div", parent_node1)
        self.assertEqual(parent_node2.to_html(
        ), '<div><p><a href="http://example.com" target="_blank">Click me!</a></p></div>')

    def test_parent_many_children(self):
        node = ParentNode(
            "p", [self.child_node, self.child_node, self.child_node, self.child_node])
        self.assertEqual(node.to_html(),
                         '<p><a href="http://example.com" target="_blank">Click me!</a><a href="http://example.com" target="_blank">Click me!</a><a href="http://example.com" target="_blank">Click me!</a><a href="http://example.com" target="_blank">Click me!</a></p>'
                         )


if __name__ == "__main__":
    unittest.main()
