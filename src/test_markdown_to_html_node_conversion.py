import unittest
from markdown_to_html import *

class TestHTMLConversion(unittest.TestCase):
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        # print(f"raw node:\n{node}")
        html = node.to_html()
        # print(f"html:\n{html}")
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraph_block(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_quote_block_regular(self):
        md = """
> This is a blockquote
> that spans multiple lines
> in the original markdown
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote that spans multiple lines in the original markdown</blockquote></div>"
        )

    def test_quote_block_empty_lines(self):
        md = """
> First paragraph in quote
> 
> Second paragraph in quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote><p>First paragraph in quote</p><p>Second paragraph in quote</p></blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- first item
- second item
- third item
- fourth item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second item</li><li>third item</li><li>fourth item</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. first item
2. second item
3. third item
4. fourth item
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item</li><li>third item</li><li>fourth item</li></ol></div>"
        )

    def test_heading(self):
        md = """
# heading 1

## heading 2

### heading 3

#### heading 4

##### heading 5

###### heading 6
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>heading 1</h1><h2>heading 2</h2><h3>heading 3</h3><h4>heading 4</h4><h5>heading 5</h5><h6>heading 6</h6></div>",
        )

    def test_most_things(self):
        md = """
# Header

Paragraph

- List item
- List item

[link](somewhere)

![image](something)

_italics_

**bold**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>Header</h1><p>Paragraph</p><ul><li>List item</li><li>List item</li></ul><p><a href="somewhere">link</a></p><p><img src="something" alt="image" /></p><p><i>italics</i></p><p><b>bold</b></p></div>'
        )
