import unittest

from pospider import *


class TestImage(unittest.TestCase):
    def test_wc(self):
        txt2wordcloud(filename=r'./test.txt')

