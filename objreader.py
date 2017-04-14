import os
import subprocess

class ObjReader:
    def read(self, flavor, path):
        return subprocess.check_output("objdump -d -M "+ flavor + " '" + path +"'", shell=True).split("\n")

    def buildCommandLine(self, flavor, path):
        return "objdump -d -M " + flavor + " '" + path +"'"
    
    def getRelativePath(sef, path):
        cwd = os.getcwd()
        commonPrefix = os.path.commonprefix([path, cwd])
        relativePath = path.replace(commonPrefix, '')
        realPath = os.path.realpath(relativePath)
        #print 'DEBUG cwd: %s\n      dir : %s\n      commonprefix: %s\n      relativePath: %s\n      realPath: %s' % (cwd, dir, commonprefix, relativePath, realPath)
        return realPath