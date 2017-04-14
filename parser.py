import sys
import re

from .model.section import *
from .model.line import *
from .model.function import *

class Parser:
    def parse(self, code):
        sections = []
        currentSection = None
        currentFunction = None
        
        lines = code.split('\n')
        for line in lines:
            print 'DEBUG line %s' % line
            if line == "": # nothing
                continue 
            if (line[0] == "0"): # function
                currentFunction = self.extractFunction(line)
                currentSection.functions.append(currentFunction)
                continue
            if (line[0] == " "): # line
                codeLine = self.extractLine(line)
                currentFunction.lines.append(codeLine)
                continue
            # section
            currentSection = self.extractSection(line)
            sections.append(currentSection)
        return sections

    def extractSection(self, line):
        print 'DEBUG section'
        match = re.match('.*?\.(\w+)', line)
        section = match.groups()[0]
        return Section(section, [])

    def extractFunction(self, line):
        print 'DEBUG function'
        match = re.match('.*?<([\w@-]+)>', line)
        function = match.groups()[0]
        return Function(function, [])
    
    def extractLine(self, line):
        print 'DEBUG line'
        addr = ""
        hexa = ""
        code = ""
        comment = ""
        
        elts = line.split( "\t" )
        if len(elts) > 0:
            addr = elts[0][:-1].strip()
            
        if len(elts) > 1:
            hexa = elts[1].strip()
            
        if len(elts) > 2:
            codeElts = elts[2].split( "#" )
            code = codeElts[0].strip()  
            if len(codeElts) > 1:
                comment = codeElts[1].strip()
        #print 'addr: %s hexa: %s code: %s comment: %s' % (addr, hexa, code, comment)
        return Line(addr, hexa, code, comment)