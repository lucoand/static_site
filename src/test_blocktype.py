import unittest
from blocktype import *

class TestBlockType(unittest.TestCase):
    def test_block_to_block_type(self):
        block = "# heading 1"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.HEADING, block_type)
        block = "## heading 2"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.HEADING, block_type)
        block = "### heading 3"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.HEADING, block_type)
        block = "#### heading 4"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.HEADING, block_type)
        block = "##### heading 5"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.HEADING, block_type)
        block = "###### heading 6"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.HEADING, block_type)
        block = "####### heading 7"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
        block = "```code block\nwith newlines\nplastered all over\nx = 0\nreturn x\n```"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.CODE, block_type)
        block = ">code block\n>with newlines\n>plastered all over"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.QUOTE, block_type)
        block = "- unordered list block\n- with multiple lines\n- like this one\n- and this one\n- and one more for good measure"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.UNORDERED_LIST, block_type)
        block = "1. ordered list block\n2. with multiple lines\n3. like this one\n4. and this one\n5. and one more for good measure"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.ORDERED_LIST, block_type)
        block = "This is a normal paragraph\nwith newlines and everything\nsee!?"
        block_type = block_to_blocktype(block)
        self.assertEqual(BlockType.PARAGRAPH, block_type)
        
        

