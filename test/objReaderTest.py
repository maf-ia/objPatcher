# coding=utf8
import unittest
import os

from ..model.section import *
from ..model.function import *
from ..model.line  import *
from ..objreader import ObjReader
from ..parser import Parser

class ParserTest(unittest.TestCase):
    def test_build_commandLine(self):
        reader = ObjReader()
        dir = os.path.dirname(__file__)
        commandLine = reader.buildCommandLine('intel', reader.getRelativePath(os.path.join(dir, '../sample/step1.bin'))) 
        expectedCommandLine = "objdump -d -M intel '/objPatcher/sample/step1.bin'"
        self.assertEqual(expectedCommandLine, commandLine)
    
if __name__ == '__main__':
    unittest.main()