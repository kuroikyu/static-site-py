class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        content = None
        if self.value is not None:
            content = str(self.value)
        if self.children is not None:
            content = str(self.children)
        if content is None:
            return ""
        if self.tag is None:
            return content

        return f"<{self.tag}{self.props_to_html()}>{content}</{self.tag}>"

    def props_to_html(self):
        if self.props is None:
            return ""

        return "".join(list(map(
            lambda prop: f" {prop[0]}=\"{prop[1]}\"", self.props.items()
        )))

    def __eq__(self, other):
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props_to_html() == other.props_to_html()
        )

    def __repr__(self):
        return f"<{self.tag}{self.props_to_html()}>Value? {self.value} | Children? {self.children}</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        return super().to_html()


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Missing tag")
        if self.children is None:
            raise ValueError("Missing children")
        children_html = []
        if self.children is None:
            pass
        if isinstance(self.children, list):
            children_html + \
                list(map(lambda c: children_html.append(c.to_html()), self.children))
        else:
            children_html.append(self.children.to_html())
        return f"<{self.tag}>" + "".join(children_html) + f"</{self.tag}>"
