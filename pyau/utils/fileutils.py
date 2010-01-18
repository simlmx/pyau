from __future__ import with_statement
import cPickle as pickle
import os

"""
Misc file utilities
"""

def getFiles(rootDir,ext='.mp3',verbose=True) :
    """
    Returns a list of files
    """
    fileList=[]
    if verbose:
        print "Populating %s files..."%ext
    for (root,dirs,files) in os.walk(rootDir) :
        for f in files :
            if f.endswith(ext) :
                filePath=os.path.join(root,f)
                fileList.append(filePath)
    if verbose:
        print "%i files found."%len(fileList)
    return fileList
    
def parseFile(filePath):
    """
    Parses the file path and returns (root,fileName,ext)
    """
    root,file=os.path.split(filePath)
    fileName,fileExt=os.path.splitext(file)
    return (root,fileName,fileExt)

def loadPickle(pickleFile):
    with open(pickleFile,'r') as infoFile:
        return pickle.load(infoFile)

def writePickle(data,pickleFile):
    with open(pickleFile,'w') as infoFile:
        pickle.dump(data,infoFile)