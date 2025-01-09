class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""
        return "".join(map(lambda x: " " + x + "=\"" + self.props[x] + "\"", self.props.keys()))

    def __repr__(self):
        return "HTMLNode: Tag = " + self.tag + " Value = " + self.value + \
            " Children = " + self.children + " Props = " + self.props
