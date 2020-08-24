class Node:
    def __init__(self):
        pass

class NodeList:
    def __init__(self, *args):
        self.nodeList = []
        self.nodeIdx = 0
        for node in args:
            self.append(node)
    
    def append(self, node):
        if issubclass(Node, type(node)):
            raise ValueError("Argument must be subtype of Node")
        self.nodeList.append(node)
    
    def __iter__(self):
        return iter(self.nodeList)
    
    def __getitem__(self, idx):
        if not isinstance(idx, int):
            raise IndexError("NodeList index must be of type int")
        try:
            return self.nodeList[idx]
        except Exception:
            raise IndexError("NodeList index out of range")
    
    def __len__(self):
        return len(self.nodeList)
    
    def __repr__(self):
        return str([el for el in self])