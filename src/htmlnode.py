class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

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
