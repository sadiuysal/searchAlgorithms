from filecmp import cmp
import Graph
class State:    #State class for nodes in the graph
    parent=None    #parent state node
    def __init__(self,i,j,type):
        self.i = i   ###location x in the puzzle
        self.j=j     ###location y in the puzzle
        self.type=type   #type h or v or s

    def checkLoc(self,i,j,type):    #check location function if given location and type same as this node than return true
        if self.i==i and self.j==j and self.type==type:
            return True
        else:
            return False



