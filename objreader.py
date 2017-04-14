import os

class ObjReader:
    def buildCommandLine(self, flavor, path):
        return "objdump -d -M " + flavor + " '" + path +"'"
    
    def getRelativePath(sef, dir, obj):
        cwd = os.getcwd()
        commonPrefix = os.path.commonprefix([dir, cwd])
        objAbsolutePath = os.path.join(dir, obj) 
        relativePath = objAbsolutePath.replace(commonprefix, '')
        realPath = os.path.realpath(relativePath)
        #print 'DEBUG cwd: %s\n      dir : %s\n      commonprefix: %s\n      absolutePath: %s\n      relativePath: %s\n      realPath: %s' % (cwd, dir, commonprefix, objAbsolutePath, relativePath, realPath)
        return realPath