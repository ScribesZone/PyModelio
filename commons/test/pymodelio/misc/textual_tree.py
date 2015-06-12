# -*- coding: utf-8 -*-

from pymodelio.misc.textual_tree import TextualTreeReader


text = """
AAA
  BBB
  CCC
DDD
"""

def test_TextualTree():
    reader = TextualTreeReader(linesOrFilename=text.split('\n'))
    tree = reader.getTextualTree()
    print tree.text()
