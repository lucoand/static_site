import unittest
from extract import *

class TestExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
                "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_images_with_a_link(self):
        matches = extract_markdown_images(
                "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([], matches)
            
    def test_extract_markdown_links_with_images(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Text [link1](www.url.com) more text [link2](www.boot.dev) ![image](img.path/img.png)"
        )
        self.assertListEqual([("link1", "www.url.com"), ("link2", "www.boot.dev")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![image1](url.com/image1.png) some text [link](www.boot.dev) more text ![image2](img.path/image2.png)"
        )
        self.assertEqual([("image1", "url.com/image1.png"), ("image2", "img.path/image2.png")], matches)

    def test_extract_markdown_images_and_extract_markdown_links_with_nothing(self):
        matches = extract_markdown_images(
            "this is a lot of text with no images or links embedded at all!"
        )
        self.assertEqual([], matches)

    def test_extract_title(self):
        md = "# Title"
        title = extract_title(md)
        self.assertEqual("Title", title)
        md = "## Title"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found!")
        md = "### Title"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found!")
        md = "#### Title"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found!")
        md = "##### Title"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found!")
        md = "###### Title"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found!")
        md = "Title"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found!")
        md = """
# Title

Paragraph 1

Paragraph 2

Other stuff [link](somewhere)

"""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found!")





