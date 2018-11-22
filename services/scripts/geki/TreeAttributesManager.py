import xml.etree.ElementTree

class TreeAttributesManager():

    def __init__(self, path):
        
        xmlTree = xml.etree.ElementTree.parse(path)
        self.__id = xmlTree.getroot().attrib["id"]
    
    def getId(self):
        return self.__id