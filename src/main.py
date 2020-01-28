#!/usr/bin/env python3
from sys import argv

import Graph
import State
from operator import itemgetter, attrgetter


file=argv[1]    ####getting arguments
searchType=argv[2]
f = open(file, "r")
line=f.readline().split(" ")
w=int(line[0])
h=int(line[1])
start_i,start_j,goal_i,goal_j=0,0,0,0

puzzle = [["e" for x in range(w)] for y in range(h)] #I used "e" for empty spots
grids=f.read().splitlines()
for i in range(h):       ####   creating puzzle according to given configuration
    line=grids[i]
    for j in range(w):
        grid=line[j]
        if not grid:
            continue
        elif grid=="o":
            puzzle[i][j]="o"
        elif grid=="g":
            puzzle[i][j]="g"
            goal_i=i
            goal_j=j
        elif grid=="s":
            puzzle[i][j]="s"
            start_i=i
            start_j=j
g= Graph.Graph_Class()   #creating graph
g.createStates(puzzle,h,w)   #creating all possible states
def createEdges():      #adding edges between states
    for i in range(h):
        for j in range(w):
            loc=puzzle[i][j]
            U_s,U_h,U_v,D_v,D_h,D_s,R_h,R_s,R_v,L_s,L_h,L_v=False,False,False,False,False,False,False,False,False,False,False,False
            illegal_Hplus_State,illegal_Vplus_State,illegal_Hminus_State,illegal_Vminus_State=False,False,False,False
            if loc!="e":
                State_s=g.findState(i,j,"s")
                State_h=g.findState(i,j,"h")
                State_v=g.findState(i,j,"v")
                if j-1<0:
                    illegal_Hminus_State=True
                if j+1>=w:
                    illegal_Hplus_State=True
                if i-1<0:
                    illegal_Vminus_State=True
                if i+1>=h:
                    illegal_Vplus_State=True

                if i-1>=0 :  #finding probable states according to orientations     ###UP OPERATION
                    if puzzle[i-1][j]!="e":
                        U_v=True
                        State_up_v=g.findState(i-1,j,"s")
                        if not illegal_Hplus_State:
                            if puzzle[i-1][j+1]!="e":
                                U_h=True
                                State_up_h=g.findState(i-1,j,"h")
                        if i-2>=0:
                            if puzzle[i-2][j]!="e":
                                U_s=True
                                State_up_s=g.findState(i-2,j,"v")
                if i+1<h:                                                        ###DOWN OPERATION
                    if puzzle[i+1][j]!="e":
                        if not illegal_Hplus_State:
                            if puzzle[i+1][j+1]!="e":
                                D_h=True
                                State_down_h=g.findState(i+1,j,"h")
                        if i+2<h:
                            if puzzle[i+2][j]!="e":
                                D_v=True
                                D_s=True
                                State_down_v=g.findState(i+2,j,"s")
                                State_down_s=g.findState(i+1,j,"v")
                if j+1<w:                                                       ###RIGHT OPERATION
                    if puzzle[i][j+1]!="e":
                        if not illegal_Vplus_State:
                            if puzzle[i+1][j+1]!="e":
                                R_v=True
                                State_right_v=g.findState(i,j+1,"v")
                        if j+2<w:
                            if puzzle[i][j+2]!="e":
                                R_h=True
                                R_s=True
                                State_right_s=g.findState(i,j+1,"h")
                                State_right_h=g.findState(i,j+2,"s")
                if j-1>=0 :                                                     ####LEFT OPERATION
                    if puzzle[i][j-1]!="e":
                        L_h=True
                        State_left_h=g.findState(i,j-1,"s")
                        if not illegal_Vplus_State:
                            if puzzle[i+1][j-1]!="e":
                                L_v=True
                                State_left_v=g.findState(i,j-1,"v")
                        if j-2>=0:
                            if puzzle[i][j-2]!="e":
                                L_s=True
                                State_left_s=g.findState(i,j-2,"h")

                if U_s:
                    g.addEdge(State_s,State_up_s,1,"U")
                if U_h:
                    g.addEdge(State_h,State_up_h,1,"U")
                if U_v:
                    g.addEdge(State_v,State_up_v,3,"U")
                if D_s:
                    g.addEdge(State_s,State_down_s,1,"D")
                if D_h:
                    g.addEdge(State_h,State_down_h,1,"D")
                if D_v:
                    g.addEdge(State_v,State_down_v,3,"D")
                if R_s:
                    g.addEdge(State_s,State_right_s,1,"R")
                if R_v:
                    g.addEdge(State_v,State_right_v,1,"R")
                if R_h:
                    g.addEdge(State_h,State_right_h,3,"R")
                if L_h:
                    g.addEdge(State_h,State_left_h,3,"L")
                if L_v:
                    g.addEdge(State_v,State_left_v,1,"L")
                if L_s:
                    g.addEdge(State_s,State_left_s,1,"L")


createEdges()     #calling create edges function to create edges between states
start=g.findState(start_i,start_j,"s")     #finding start and goal state node
goal=g.findState(goal_i,goal_j,"s")

if searchType=="dfs":
    g.DFS(start,goal)
elif searchType=="bfs":
    g.BFS(start,goal)
elif searchType=="ucs":
    g.UCS(start,goal)
elif searchType=="gs":
    g.Greedy(start,goal)
elif searchType=="as":
    g.A_star(start,goal)
else:
    print("Unknown search type please use valid search types : dfs,bfs,ucs,gs,as")









