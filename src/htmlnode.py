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


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode without a value")

        if self.tag is None:
            # if there is no tag, we just return the raw value
            return self.value
    
        # otherwise create the HTML string
        return "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + \
            self.tag + ">"

    def __repr__(self):
        return "LeafNode(" + self.tag + ", " + self.value + ", " + self.props + ")"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode without a tag")

        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode with no children")

        html = "<" + self.tag + self.props_to_html() + ">"
        for child in self.children:
            html += child.to_html()

        return html + "</" + self.tag + ">"

    def __repr__(self):
        return "ParentNode(" + self.tag + ", " + self.children + ", " + \
            self.props + ")"
