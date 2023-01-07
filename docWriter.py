def numLevelSpaces() -> int:
    return 2

# This is text element and not a Tag but we use it in the same hierarchy to support multiple texts
class ElementText():
    def __init__(self, _text):
        self.type = "ElementText"
        self.elementText = _text
    def Write(self, _level):
        return self.elementText

#This is a single style definition for a single/multiple class names. Name defines the scope of this style class
#It may be a single class.
#No inheritance should be made from this class.
class StyleClass():
    def __init__(self, _name):
        self.name = _name
        self.type = "StyleClass"
        self.dict = {}
        self.newLine = "\n"
    def __setitem__(self, _key, _value):
        self.dict[_key] = _value
    def __getitem__(self, _key):
        return self.dict[_key]
    def __delitem__(self, _key):
        self.dict.pop(_key)
    def SetItem(self, _key, _value):
        self.dict[_key] = _value
        return self
    def getClassString(self, _level):
        #for brackets
        prefix = self.newLine.ljust(_level * numLevelSpaces())
        #for style parameters
        pprefix = self.newLine.ljust((_level + 1) * numLevelSpaces())
        text = prefix + f'{self.name} ' + '{'
        for key in self.dict:
            text += pprefix + f'{key}: {self.dict[key]};'
        text += prefix + '}'
        return text
    def Write(self, _level):
        return self.getClassString(_level)

class Tag:
    def __init__(self, _type, _closeline=True, _newline="\n"):
        self.type = _type
        self.text = ""
        self.children = []
        self.attributes = {}
        self.elementText = ""
        self.text = ""
        self.newLine = _newline
        self.closeline = _closeline
        self.parent = None
    
    def AddChild(self, _child):
        self.children.append(_child)
        _child.parent = self
    
    def AddText(self, _text):
        self.children.append(ElementText(_text))
    
    def AddAttribute(self, _key, _val):
        if _key in self.attributes:
            self.attributes[_key].append(_val)
        else:
            self.attributes[_key] = [_val]
    
    def ClearStream(self):
        self.text = ""
        
    def WriteStream(self, _string):
        self.text += _string
        
    def WriteOpenTagA(self, _level):
        # add check if the tag should start from new line
        prefix = ""
        if self.newLine == "\n" and _level > 0:
            prefix = self.newLine.ljust(_level * numLevelSpaces())
        self.WriteStream(prefix + "<" + self.type)
    
    def WriteOpenTagB(self):
        self.WriteStream(">")
        
    def WriteAttributes(self):
        for attr in self.attributes.keys():
            self.WriteStream(" " + attr + "=\"")
            vals = self.attributes[attr]
            iVal = 0
            lVal = len(vals) - 1
            for val in vals:
                if iVal == lVal:
                    self.WriteStream(val)
                else:
                    self.WriteStream(val + " ")
                iVal += 1
            self.WriteStream("\"")
        
    def WriteText(self):
        self.WriteStream(self.text)
        
    def WriteChildren(self, _level):
        for ch in self.children:
            self.text += ch.Write(_level + 1)
            
    def WriteCloseTag(self, _level):
        prefix = ""
        if self.newLine == "\n" and len(self.children) > 0 and (self.children[-1].type != "ElementText" \
        or self.children[-1].elementText.find('\n') > -1) and self.closeline == True:
            prefix = self.newLine.ljust(_level * numLevelSpaces())
        self.WriteStream(prefix + "</" + self.type + ">")
        
    def Write(self, _level):
        self.ClearStream()
        self.WriteOpenTagA(_level)
        self.WriteAttributes()
        self.WriteOpenTagB()
        self.WriteChildren(_level)
        self.WriteCloseTag(_level)
        return self.text
        
class Div(Tag):
    def __init__(self, _closeline=True):
        super(Div, self).__init__("div", _closeline)
        
class SingleTag(Tag):
    def __init__(self, _name):
        super(SingleTag, self).__init__(_name)
        self.newLine = ""   
    def WriteCloseTag(self, _level):
        pass

class Img(SingleTag):
    def __init__(self):
        super(Img, self).__init__("img")

class Style(Tag):
    def __init__(self):
        super(Style, self).__init__("style")
    def AddStyle(self, _class):
        if (type(_class) == StyleClass):
            self.children.append(_class)

class Script(Tag):
    def __init__(self):
        super(Script, self).__init__("script")
    def WriteChildren(self, _level):
        prefix = self.newLine.ljust((_level + 1) * numLevelSpaces())
        for ch in self.children:
            self.text += (prefix + ch.elementText.replace('\n', prefix))