class FPtree(object):

    def __init__(self, value=0, name='null', children=None):
        self.value = value
        self.name = name
        self.parent = None
        self.children = list()
        if children is not None:
            for child in children:
                self.addChild(child)

    def addChild(self, node):
        if isinstance(node, FPtree):
            node.parent = self
            self.children.append(node)

    def buildTree(self, name, count=1):
        for child in self.children:
            if child.name == name:
                child.value += count
                return child
        child = FPtree(count, name)
        child.parent = self
        self.children.append(child)
        return child

    def getPointer(self, name):
        pointer = list()
        if self.name == name:
            pointer.append(self)
        if len(self.children) > 0:
            for child in self.children:
                pointer.extend(child.getPointer(name))
        return pointer
    
    def getCount(self, name):
        count = 0
        if self.name == name:
            count += self.value
        if len(self.children) > 0:
            for child in self.children:
                count += child.getCount(name)
        return count

    def hasParent(self):
        if self.parent is not None:
            return True
        return False

    def is1Path(self):
        if len(self.children) == 1:
            return self.children[0].is1Path()
        elif len(self.children) == 0:
            return True
        else:
            return False

    def getCPB(self, pattern, targets):
        CPB = list()
        for t in targets:
            cpb = t.traceBack()
            cpb.remove(pattern)
            if len(cpb) > 0:
                cpb.reverse()
                cpb.append(t.value)
                CPB.append(cpb)
        return CPB

    def traceBack(self):
        route = [self.name]
        if self.hasParent() and self.parent.name != 'null':
            route.extend(self.parent.traceBack())
        return route
