#! /usr/bin/env python
#
#Utilities to easily use h5 files
#For simplicity, we only use nodes in root directory of h5 file
#
#Created by
#Philippe Hamel
#November 7 2008

from __future__ import with_statement

from tables import openFile

def readNode(nodeName,h5FileName):
    """
    Reads node 'nodeName' from 'h5FileName'
    Returns the content of the node
    """
    with openFile(h5FileName,'r') as h5File:
        content= h5File.getNode(h5File.root,nodeName)[:]
    return content

def writeNode(content,nodeName,h5FileName):
    """
    Writes content in nodeName of h5FileName
    """
    with openFile(h5FileName,'a') as h5File:
        _writeNodeInFile(content,nodeName,h5File)
        
def _writeNodeInFile(content,nodeName,h5File):
    if nodeName in h5File.root:
        _deleteNode(nodeName, h5File)
    h5File.createArray('/',nodeName,content)

def listNodes(h5FileName):
    """
    Returns the list of all node names in 'h5FileName'
    """
    with openFile(h5FileName,'r') as h5File:
        nodesList = _listNodes(h5File)
    return nodesList

def _listNodes(h5File):
    return h5File.root._v_children.keys()


def readAllNodes(h5FileName):
    """
    Returns the content of all nodes of h5FileName in a dictionary
    """
    with openFile(h5FileName,'r') as h5File:
        keys=h5File.root._v_children.keys()
        values=[]
        for nodeName in keys:
            values.append(h5File.getNode(h5File.root,nodeName)[:])
        nodeDict=dict(zip(keys,values))
    return nodeDict

def writeAllNodes(dataDict,h5FileName):
    """
    Writes a dictionary to h5FileName
    WARNING : This will remove all existing nodes in the file
    """
    with openFile(h5FileName,'a') as h5File:
        for k,v in dataDict.iteritems():
            _writeNodeInFile(v,str(k),h5File)

    
def deleteNode(nodeName,h5FileName):
    """
    Deletes a node from a h5 file
    """
    with openFile(h5FileName,'a') as h5File:
        _deleteNode(nodeName, h5File)
        
def _deleteNode(nodeName, h5File):
       h5File.getNode(h5File.root,nodeName).remove()

def renameNode(oldNodeName,newNodeName,h5FileName):
    """
    Renames a node in a h5 file
    """
    with openFile(h5FileName,'a') as h5File:
       content=h5File.getNode(h5File.root,oldNodeName)[:]
       _deleteNode(oldNodeName, h5File)
       _writeNodeInFile(content,newNodeName,h5File)



