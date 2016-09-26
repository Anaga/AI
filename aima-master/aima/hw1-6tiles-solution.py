# -*- coding: utf-8 -*-
"""
Basic staff to solve HW1 in ITI8600.

This is a complete solution, and gives you an initial idea how to proceed. 
Currently can place all 6 tiles in a valid way
on the pyramid containing of 6 tiles.

it is posible to sped ou, if route print out to log
hw1-6tiles-solution.py > log.txt

"""
import time
import search

"""
   We actually have 6 tiles, thus we call those realTiles.
   In the instantiation of the Problem class we create all rotations.
"""
realTiles=[
   ('y','r','b','b','r','y'),
   ('y','b','r','r','b','y'),
   ('y','r','y','b','b','r'),
   ('y','b','y','r','b','r'),
   ('y','r','b','r','b','y'),
   ('y','r','y','b','r','b')
   ]
   
initialState = [None,None,None,None,None,None]

def leftShift(tup, n):  #Taken from http://stackoverflow.com/questions/5299135/how-to-efficiently-left-shift-a-tuple
    if not tup or not n:
        return tup
    n %= len(tup)
    return tup[n:] + tup[:n]

def testAxis(tilA, tilB, n):
    return tilA[n+3]==tilB[n]
    
def testX(t1,t2):
     return testAxis(t1,t2,0);

def testY(t1,t2):
     return testAxis(t1,t2,1);     
    
def testZ(t1,t2):
     return testAxis(t2,t1,2);
     
def printField(state):
    """ The tiles are arranged in such a way (the pyramid is rotated
        -90 degrees because of ascii convenience):
                  X                    Z
                 /          ___        |
                /          /   \       |
               /          /     \      |
              /       ___/   5   \     |
             /       /   \       /     |
            /       /     \     /      |
           /    ___/   2   \___/       |
          /    /   \       /   \       |
         /    /     \     /     \      |
        /    /   0   \___/   4   \     |
        \    \       /   \       /     |
         \    \     /     \     /      |
          \    \___/   1   \___/       |
           \       \       /   \       |
            \       \     /     \      |
             \       \___/   3   \     |
              \          \       /     |
               \          \     /      |
                \          \___/       |
                 \                     |
                  Y                    Z
                          
        The numbers of sides in tiles are taken to be
                     _2_
                    /   \
                   1     3
                  /       \
                  \       /
                   0     4
                    \_5_/

        (The tile is also rotated -90 degrees)
    """

    T = list()
    for s in state:
        if s is None:
            T.append ("      ")
        else: T.append(s)
              
        
    print "                   ___         "
    print "                  / %s \       "%(                                      T[5][2]       )
    print "                 /%s   %s\     "%(                                  T[5][1],T[5][3]   )
    print "             ___/   5   \      "%(                                                    )
    print "            / %s \       /     "%(                     T[2][2]                        )
    print "           /%s   %s\%s   %s/   "%(                 T[2][1],T[2][3], T[5][0],T[5][4]   )
    print "       ___/   2   \_%s_/       "%(                                      T[5][5]       )
    print "      / %s \       / %s \      "%(    T[0][2],                          T[4][2]       )
    print "     /%s   %s\%s   %s/%s   %s\ "%(T[0][1],T[0][3], T[2][0],T[2][4], T[4][1],T[4][3]   )
    print "    /   0   \_%s_/   4   \     "%(                     T[2][5]                        )
    print "    \       / %s \       /     "%(                     T[1][2]                        )
    print "     \%s   %s/%s   %s\%s   %s/ "%(T[0][0],T[0][4], T[1][1],T[1][3], T[4][0],T[4][4]   )
    print "      \_%s_/   1   \_%s_/      "%(    T[0][5],                          T[4][5]       )
    print "          \       / %s \       "%(                                      T[3][2]       )
    print "           \%s   %s/%s   %s\   "%(                 T[1][0],T[1][4], T[3][1],T[3][3]   )
    print "            \_%s_/   3   \     "%(                     T[1][5]                        )
    print "                \       /      "%(                                                    )
    print "                 \%s   %s/     "%(                                  T[3][0],T[3][4]   )
    print "                  \_%s_/       "%(                                      T[3][5]       )



class TantrixPyramid6(search.Problem):
    tiles = set()

    def __init__(self,initial,realTiles):
        self.initial = tuple(initial)
        self.gameSet = initial #for good printing
        for tile in realTiles:
            for i in range(0,6):
                self.tiles.add(leftShift(tile,i))
        print "Init compled, total we have %d tiles, including all rotations" % len(self.tiles)   
        printField(self.gameSet )
        
    def actions(self,state):    
        #print "function to return possible actions from current state"
        #print state
        i =  state.index(None)
        #print "i = %d "%i
        enabledActions=set(self.tiles)
        toRemove=[]  # list of the tiles that do not have matching color     
        
        if i == 0:
            return enabledActions
        else:
            for j in range(i):  # go over all puted tiles and 
                for k in range(0,6): #remove all rotation of choisen tile
                   enabledActions.remove(leftShift(state[j],k))
        
        T = list()
        for s in state:
          T.append(s)    # get the i-st tile 
          
        for t in enabledActions:  # go over all lefted tiles and if this tile 't' not match to t0, remove it from enabledActions   
            if i == 1: # T1, check for T0-Y
                # we check match T0 and T1, so check only Y axis            
                if False == testY(T[0], t): toRemove.append(t)

            if i == 2: # T2, check for T0-X, T1-Z 
                #  we check match T0 and T2 on X axis                           
                # and check match T1 and T2 on Z axis  
                if False == (testX(T[0],t) and testZ(T[1],t)): toRemove.append(t)

            if i == 3:  # T3, check for T1-Y                    
                if False == testY(T[1], t):  toRemove.append(t)             
                
            if i == 4:  # T4, check for T1-X, T2-Y, T3-Z 
                if False == (testX(T[1], t) and testY(T[2], t) and testZ(T[3], t)): toRemove.append(t)
        
            if i == 5: # T5, check for T2-X, T4-Z          
                if False == (testX(T[2], t) and testZ(T[4], t)): toRemove.append(t)
                    
        for t in toRemove:
            #print t
            enabledActions.remove(t)
        #print "return enabledActions" 
        #print enabledActions
        return enabledActions
                
    def result(self, state, action):
        newState = list(state)
        i = state.index(None)
        newState[i] = action
        return tuple(newState)
    
    def goal_test(self, state):
        self.gameSet = state
        i = state.count(None)
        #print "plase %d ties"%(6-i)
        #printField(self.gameSet )
        for el in state:           
            if el is None:
                return False
        print "We finde the solution!"
        localtime = time.asctime( time.localtime(time.time()) )
        print "Local current time :", localtime
        printField(self.gameSet )
        return True

    def prin(self):
        print "TantrixPyramid6"
        print "Current State:"
        printField(self.gameSet )
        
print "Start up"  
tp6 = TantrixPyramid6(initialState,realTiles)
localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime
"""
def breadth_first_tree_search(problem):
    "Search the shallowest nodes in the search tree first."
    return tree_search(problem, FIFOQueue())

def depth_first_tree_search(problem):
    "Search the deepest nodes in the search tree first."
    return tree_search(problem, Stack())

def depth_first_graph_search(problem):
    "Search the deepest nodes in the search tree first."
    return graph_search(problem, Stack())

def breadth_first_search(problem):
"""

print "Ready to start breadth_first_tree_search"  
search.breadth_first_tree_search(tp6)

localtime = time.asctime( time.localtime(time.time()) )
print "Ready to start depth_first_tree_search"  
print "Local current time :", localtime
search.depth_first_tree_search(tp6)

localtime = time.asctime( time.localtime(time.time()) )
print "Ready to start depth_first_graph_search"  
print "Local current time :", localtime
search.depth_first_graph_search(tp6)

localtime = time.asctime( time.localtime(time.time()) )
print "Ready to start breadth_first_search"
print "Local current time :", localtime
search.breadth_first_search(tp6)

"""
   There are tools available to compare
   search algorithms. The stats contain the following data:
   number of successors /
   number of goal tests /
   number of states /
   first 4 bytes of the found goal
"""
search.compare_searchers([tp6],["algorithm","Tantrix pyramid 6"],[
        search.breadth_first_tree_search,
        search.depth_first_tree_search,        
        search.depth_first_graph_search,
        search.breadth_first_search
    ])
print "End"
"""END"""
