# coding=utf8
import unittest

from ..model.section import *
from ..model.function import *
from ..model.line  import *
from ..parser import Parser

class ParserTest(unittest.TestCase):
    def test_create_sections(self):
        code = """
Déassemblage de la section .init :

00000000004004d0 <_init>:
  4004d0:	48 83 ec 08          	sub    $0x8,%rsp

Déassemblage de la section .text : 
"""
        parser = Parser()
        sections = parser.parse(code)
        expectedSections = [Section('init', [Function('_init', [Line('4004d0', '48 83 ec 08', 'sub    $0x8,%rsp', '')])]), \
                            Section('text', [])]
        self.assertEqual(expectedSections, sections)

    def test_create_section(self):
        code = "Déassemblage de la section .init :"
        parser = Parser()
        section = parser.extractSection(code)
        expectedSection = Section('init', [])
        self.assertEqual(expectedSection, section)

    def test_create_function(self):
        code = "00000000004004f0 <puts@plt-0x10>:"
        parser = Parser()
        function = parser.extractFunction(code)
        expectedFunction = Function('puts@plt-0x10', [])
        self.assertEqual(expectedFunction, function)

    def test_create_line_with_comment(self):
        code = '400500:	ff 25 aa 45 23 00    	jmpq   *0x2345aa(%rip)        # 634ab0 <_GLOBAL_OFFSET_TABLE_+0x18>'
        parser = Parser()
        line = parser.extractLine(code)
        expectedLine = Line('400500', 'ff 25 aa 45 23 00', 'jmpq   *0x2345aa(%rip)', '634ab0 <_GLOBAL_OFFSET_TABLE_+0x18>')
        self.assertEqual(expectedLine, line)

    def test_create_line_without_comment(self):
        code = '400516:	68 01 00 00 00       	pushq  $0x1'
        parser = Parser()
        line = parser.extractLine(code)
        expectedLine = Line('400516', '68 01 00 00 00', 'pushq  $0x1', '')
        self.assertEqual(expectedLine, line)
if __name__ == '__main__':
    unittest.main()