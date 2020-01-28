from operator import itemgetter

import State
class Graph_Class:
    states=[]      #states list
    dict={}         #dictionary for node-neighbour list
    edges={}         #dictionary for edges
    def addEdge(self,node,neighbour,cost,opr):     ##function for adding edge
        if node not in self.dict:
            self.dict[node]=[neighbour]
        else:
            self.dict[node].append(neighbour)
        self.edges[(node,neighbour)]=[(cost,opr)]


    def findState(self,i,j,type):    ### function for finding a node for given location and type
        for node in self.states:
            if node.checkLoc(i,j,type):
                return node

    def createStates(self,puzzle,h,w):     #creating possible state nodes for all locations
        for i in range(h):
            for j in range(w):
                if puzzle[i][j]!="e":
                    self.states.append(State.State(i,j,"h"))
                    self.states.append(State.State(i,j,"v"))
                    self.states.append(State.State(i,j,"s"))

    def find_opr_p(self,node,child):  #for BFS and UCS operation priority compare

        opr=self.edges.get((node,child))[0][1]
        opr_p=0
        if opr=="L":
            opr_p=1
        elif opr=="U":
            opr_p=2
        elif opr=="R":
            opr_p=3
        elif opr=="D":
            opr_p=4
        return opr_p
    def find_opr_p_2(self,node,child):  #for DFS operation priority compare

        opr=self.edges.get((node,child))[0][1]
        opr_p=0
        if opr=="L":
            opr_p=4
        elif opr=="U":
            opr_p=3
        elif opr=="R":
            opr_p=2
        elif opr=="D":
            opr_p=1
        return opr_p
    def Heuristic(self,node,goal):     ###Heuristic function that returns a heuristic value
        manhattan=abs(node.i-goal.i)+abs(node.j-goal.j)
        if node.type=="s":  ##grids that is single and having high possibility to reach goal
            if abs(node.i-goal.i)/3==0 and abs(node.j-goal.j)/3==0:
                return manhattan/1.5
        elif node.type=="v":  ##grids that is vertical and having high possibility to reach goal
            if (abs(node.i-goal.i)-2)/3==0:
                return manhattan/1.5
        else:
            if (abs(node.j-goal.j)-2)/3==0:     ###grids that is horizontal and having high possibility to reach goal
                return manhattan/1.5
        return manhattan      ##### if this grid is not a special one than return manhattan as a heuristic value

    def BFS(self,start,g):   ###BFS function
        visited={}
        depth=0
        for i in self.dict:    ###assign unvisited to all nodes and delete all parent,depth relations.
            visited[i]=False
            i.parent=None
            i.depth=0
        queue=[]
        queue.append((start,depth,0))    ####put nodes in the queue as tuple(stateNode,depth,operation priority)
        visited[start]=True
        nodeCount=0
        while len(queue)!=0:
            queue=sorted(queue,key=itemgetter(1,2))     #sort acc.to depth if equal than operation priority
            element=queue.pop(0)
            s=element[0]
            depth=element[1]
            if s is g:                              #### if s is goal state than break
                break
            nodeCount+=1      #####node count for the explored states
            for node in self.dict[s]:
                if not visited.get(node):
                    visited[node]=True
                    node.parent=s
                    queue.append((node,depth+1,self.find_opr_p(s,node)))      ####put nodes in the queue as tuple(stateNode,depth,operation priority)
        path=g
        stack=[]
        pathCost=0
        while not (path is start):              ###finding path and path cost from start to goal
            old=path
            path=path.parent
            stack.append(self.edges.get((path,old))[0][1])
            pathCost+=int(self.edges.get((path,old))[0][0])
        queueNodeCount=0                        #To count number of unvisited nodes in the queue
        while(queue):
            s=queue.pop(0)[0]
            if not visited[s]:
                queueNodeCount+=1

        print(str(pathCost) +" "+str(nodeCount-queueNodeCount)+" "+str(depth)+" "+str(depth))
        soln=""
        while len(stack):
            soln+=stack.pop()
        print(soln)    ####printing resulting path

    def DFS(self,start,g):
        visited={}
        maxDepth=0
        depth=0
        for i in self.dict:  ###assign unvisited to all nodes and delete all parent,depth relations.
            visited[i]=False
            i.parent=None
            i.depth=0
        queue=[]
        queue.append((start,depth,0))  ####put nodes in the queue as tuple(stateNode,depth,operation priority)
        visited[start]=True
        nodeCount=0
        while len(queue)!=0:
            queue=sorted(queue,key=itemgetter(1,2),reverse=True)    #sort acc.to depth if equal than operation priority
            element=queue.pop(0)
            s=element[0]
            depth=element[1]
            maxDepth=max(maxDepth,depth)
            if s is g:#### if s is goal state than break
                break
            nodeCount+=1    ###node count for the explored states
            for node in self.dict[s]:
                if not visited.get(node):
                    visited[node]=True
                    node.parent=s
                    queue.append((node,depth+1,self.find_opr_p_2(s,node)))     ####put nodes in the queue as tuple(stateNode,depth,operation priority)
        path=g
        stack=[]
        pathCost=0
        while not (path is start):    ###finding path and path cost from start to goal
            old=path
            path=path.parent
            stack.append(self.edges.get((path,old))[0][1])
            pathCost+=int(self.edges.get((path,old))[0][0])
        queueNodeCount=0                #To count number of unvisited nodes in the queue
        while(queue):
            s=queue.pop(0)[0]
            if not visited[s]:
                queueNodeCount+=1

        print(str(pathCost) +" "+str(nodeCount-queueNodeCount)+" "+str(depth)+" "+str(depth))
        soln=""
        while len(stack):
            soln+=stack.pop()
        print(soln)   ####printing resulting path

    def UCS(self,start,g):
        visited={}
        depth=0
        for i in self.dict:   ###assign unvisited to all nodes and delete all parent,depth relations.
            visited[i]=False
            i.parent=None
            i.depth=0
        queue=[]
        queue.append((start,depth,0,0))      ####put nodes in the queue as tuple(stateNode,depth,operation priority,cost)
        visited[start]=True
        nodeCount=0
        while len(queue)!=0:
            queue=sorted(queue,key=itemgetter(3,2))   #sort acc.to cost if equal than operation priority
            element=queue.pop(0)
            s=element[0]
            depth=element[1]
            cost=element[3]
            if s is g:
                break
            nodeCount+=1
            for node in self.dict[s]:
                if not visited.get(node):
                    visited[node]=True
                    node.parent=s
                    queue.append((node,depth+1,self.find_opr_p(s,node),cost+int(self.edges.get((s,node))[0][0])))  ####put nodes in the queue as tuple(stateNode,depth,operation priority,cost)
        path=g
        stack=[]
        pathCost=0
        while not (path is start):    ###finding path and path cost
            old=path
            path=path.parent
            stack.append(self.edges.get((path,old))[0][1])
            pathCost+=int(self.edges.get((path,old))[0][0])
        queueNodeCount=0                #To count number of unvisited nodes in the queue
        while(queue):
            s=queue.pop(0)[0]
            if not visited[s]:
                queueNodeCount+=1

        print(str(pathCost) +" "+str(nodeCount-queueNodeCount)+" "+str(depth)+" "+str(depth))
        soln=""
        while len(stack):
            soln+=stack.pop()
        print(soln)    #printing resulting path

    def Greedy(self,start,g):
        visited={}
        depth=0
        for i in self.dict:   ###assign unvisited to all nodes and delete all parent,depth relations.
            visited[i]=False
            i.parent=None
            i.depth=0
        queue=[]
        queue.append((start,depth,self.Heuristic(start,g)))   ####put nodes in the queue as tuple(stateNode,depth,heuristic value)
        visited[start]=True
        nodeCount=0
        while len(queue)!=0:
            queue=sorted(queue,key=itemgetter(2))  ##Sort according to heuristic value
            element=queue.pop(0)
            s=element[0]
            depth=element[1]
            heuristic=element[2]
            if s is g:
                break
            nodeCount+=1
            for node in self.dict[s]:
                if not visited.get(node):
                    visited[node]=True
                    node.parent=s
                    queue.append((node,depth+1,self.Heuristic(node,g)))
        path=g
        stack=[]
        pathCost=0
        while not (path is start):    ###finding path cost and path
            old=path
            path=path.parent
            stack.append(self.edges.get((path,old))[0][1])
            pathCost+=int(self.edges.get((path,old))[0][0])
        queueNodeCount=0    #To count number of unvisited nodes in the queue
        while(queue):
            s=queue.pop(0)[0]
            if not visited[s]:
                queueNodeCount+=1

        print(str(pathCost) +" "+str(nodeCount-queueNodeCount)+" "+str(depth)+" "+str(depth))
        soln=""
        while len(stack):
            soln+=stack.pop()
        print(soln)   #print resulting path

    def A_star(self,start,g):
        visited={}
        depth=0
        for i in self.dict:  ###assign unvisited to all nodes and delete all parent,depth relations.
            visited[i]=False
            i.parent=None
            i.depth=0
        queue=[]
        cost=0
        queue.append((start,depth,self.Heuristic(start,g)+cost,cost))  ####put nodes in the queue as tuple(stateNode,depth,heuristic value+cost,cost)
        visited[start]=True
        nodeCount=0
        while len(queue)!=0:
            queue=sorted(queue,key=itemgetter(2))  ##Sort according to evaluation function (heuristic with a cost)
            element=queue.pop(0)
            s=element[0]
            depth=element[1]
            functionValue=element[2]
            cost=element[3]
            if s is g:
                break
            nodeCount+=1
            for node in self.dict[s]:
                if not visited.get(node):
                    visited[node]=True
                    node.parent=s
                    newcost=cost+int(self.edges.get((s,node))[0][0])
                    queue.append((node,depth+1,self.Heuristic(node,g)+newcost,newcost))
        path=g
        stack=[]
        pathCost=0
        while not (path is start):   #finding path and path cost
            old=path
            path=path.parent
            stack.append(self.edges.get((path,old))[0][1])
            pathCost+=int(self.edges.get((path,old))[0][0])
        queueNodeCount=0   #To count number of unvisited nodes in the queue
        while(queue):
            s=queue.pop(0)[0]
            if not visited[s]:
                queueNodeCount+=1

        print(str(pathCost) +" "+str(nodeCount-queueNodeCount)+" "+str(depth)+" "+str(depth))
        soln=""
        while len(stack):
            soln+=stack.pop()
        print(soln)   #prints resulting path

