# -*- coding: utf-8 -*-
"""
prog to solve HW1 in ITI8600.

it is posible to sped ou, if route print out to log
hw1-6tiles-solution.py > log.txt

"""
import time
import search

"""
   We actually have 15 tiles, thus we call those realTiles.
   In the instantiation of the Problem class we create all rotations. (15*6=90)
"""
realTiles=[
   ('y','r','b','b','r','y'),
   ('y','b','r','r','b','y'),
   ('y','r','y','b','b','r'),
   ('y','b','y','r','b','r'),
   ('y','r','b','r','b','y'),
   ('y','r','y','b','r','b')
   ]

realTiles15 = [
    ('r','y','g','r','g','y'),
    
    ('y','r','b','r','y','b'),
    ('y','b','g','b','g','y'),

    ('y','b','y','g','g','b'),
    ('r','y','r','y','b','b'),
    ('r','b','r','g','b','g'),
    
    ('y','y','r','b','b','r'),
    ('b','r','r','b','y','y'),
    ('r','y','y','b','b','r'),
    ('b','b','y','y','r','r'),
    
    ('g','g','y','b','b','y'),    
    ('b','r','b','y','r','y'),
    ('g','y','y','g','r','r'),
    ('y','y','g','g','b','b'),
    ('y','r','b','r','b','y')
    ]

   
initialState = [None,None,None,None,None,None]   
initialState15 = [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]


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

def formatTile(tile, spases= 0):
    """
     ' for big field it is  better to print out tiles seperatly
     '    _______
     '   /   2   \
     '  /1       3\
     ' /           \
     ' \           /
     '  \0       4/
     '   \___3___/     
     '           
     """
 
    s = """   _______
  /   2   \\
 /1       3\\
/           \\
\\           /
 \\0       4/
  \\___5___/ """
           
    for i in range(6):
        color_pos = '%d'%i
        color_value = tile[i]
        s = s.replace(color_pos, color_value) 
    return s    

s = ''    
for t in realTiles15:    
    s +="print out tile %s \n"%str(t)
    s += formatTile(t) + "\n"
print s


def printField(state):
    field_letters =('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O')
    empty_field = """  
     ' The game field for tiles are arranged in such a way. 
     ' each game field have own letters (A-O)
     '  (A B C D E F G H I J K L M N O)
     '               /X                              _______      Z 
     '              /                               /   2   \     |  
     '             /                               /1       3\    |  
     '            /                        _______/     O     \   |  
     '           /                        /   2   \     O     /   |  
     '          /                        /1       3\0       4/    |  
     '         /                 _______/     J     \___5___/     |                      
     '        /                 /   2   \     J     /   2   \     |                       
     '       /                 /1       3\0       4/1       3\    |                  
     '      /          _______/     F     \___5___/     N     \   |                          
     '     /          /   2   \     F     /   2   \     N     /   |                          
     '    /          /1       3\0       4/1       3\0       4/    |                       
     '   /   _______/     C     \___5___/     I     \___5___/     |                      
     '  /   /   2   \     C     /   2   \     I     /   2   \     |                       
     ' /   /1       3\0       4/1       3\0       4/1       3\    |                      
     '/   /     A     \___5___/     E     \___5___/     M     \   |                   
     '\   \     A     /   2   \     E     /   2   \     M     /   |             
     ' \   \0       4/1       3\0       4/1       3\0       4/    |              
     '  \   \___5___/     B     \___5___/     H     \___5___/     |                      
     '   \          \     B     /   2   \     H     /   2   \     |               
     '    \          \0       4/1       3\0       4/1       3\    |          
     '     \          \___5___/     D     \___5___/     L     \   |             
     '      \                 \     D     /   2   \     L     /   |             
     '       \                 \0       4/1       3\0       4/    |             
     '        \                 \___5___/     G     \___5___/     |   
     '         \                        \     G     /   2   \     | 
     '          \                        \0       4/1       3\    | 
     '           \                        \___5___/     K     \   | 
     '            \                               \     K     /   | 
     '             \                               \0       4/    | 
     '              \Y                              \___5___/     Z
     '      """
     
    plase_holder = """  
     '                                              _______      
     '                                             /   2   \     
     '                                            /1       3\    
     '                                    _______/     O     \   
     '                                   /   2   \     O     /   
     '                                  /1       3\\0       4/   
     '                          _______/     J     \___5___/                      
     '                         /   F2   \     J     /   2   \                       
     '                        /F1       F3\\0       4/1       3\                 
     '                _______/           \___5___/     N     \                        
     '               /   C2   \           /   2   \     N     /                    
     '              /C1       C3\\F0       F4/1       3\\0       4/                        
     '      _______/           \___F5___/     I     \___5___/                      
     '     /   A2   \           /   E2   \     I     /   2   \                        
     '    /A1       A3\\C0       C4/E1       E3\\0       4/1       3\                       
     '   /           \___C5___/           \___5___/     M     \                  
     '   \           /   B2   \           /   2   \     M     /            
     '    \\A0       A4/B1       B3\\E0       E4/1       3\\0       4/               
     '     \___A5___/           \___E5___/     H     \___5___/                       
     '             \           /   D2   \     H     /   2   \                
     '              \\B0       B4/D1       D3\\0       4/1       3\           
     '               \___B5___/           \___5___/     L     \      
     '                       \           /   2   \     L     /      
     '                        \\D0       D4/1       3\\0       4/       
     '                         \___D5___/     G     \___5___/    
     '                                 \     G     /   2   \    
     '                                  \\0       4/1       3\  
     '                                   \___5___/     K     \  
     '                                           \     K     /  
     '                                            \\0       4/  
     '                                             \___5___/    
     '  """
    T = list()  
    for s in state:
        if s is None:
            T.append ("      ")
        else: T.append(s)
    for letter in field_letters:
        T.append ("      ")
   
    l=0    
   
    
    for let in field_letters:
        for i in range(6):
            color_pos = '%s%d'%(let,i)
            color_value = T[l][i]
            plase_holder = plase_holder.replace(color_pos, color_value)
        l+=1
    print plase_holder    

    
class TantrixPyramid15(search.Problem):
    tiles = set()
    def __init__(self,initial15,realTiles15):
        self.initial = tuple(initial15)
        self.gameSet = initial15 #for good printing
        for tile in realTiles15:
            for i in range(0,6):
                self.tiles.add(leftShift(tile,i))
        print "Init compled, total we have %d tiles, including all rotations" % len(self.tiles)   
        printField(self.gameSet )
        
    def actions(self,state):    
        #print "function to return possible actions from current state"
        #print state
        i =  state.index(None)
        print "i = %d "%i
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
                
                #printField(self.gameSet )

            if i == 2: # T2, check for T0-X, T1-Z 
                #  we check match T0 and T2 on X axis                           
                # and check match T1 and T2 on Z axis  
                if False == (testX(T[0],t) and testZ(T[1],t)): toRemove.append(t)

            if i == 3:  # T3, check for T1-Y                    
                if False == testY(T[1], t):  toRemove.append(t)             
                
            if i == 4:  # T4, check for T1-X, T2-Y, T3-Z 
                if False == (testX(T[1], t) and testY(T[2], t) and testZ(T[3], t)): toRemove.append(t)
                printField(self.gameSet )
                
        
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
        print "TantrixPyramid15"
        print "Current State:"
        printField(self.gameSet )
        
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
        print "function to return possible actions from current state"
        print state
        i =  state.index(None)
        print "i = %d "%i
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


tp15 = TantrixPyramid15(initialState15,realTiles15)
localtime = time.asctime( time.localtime(time.time()) )
print "Local current time :", localtime
tp15.prin()

print "Ready to start breadth_first_tree_search"  
search.breadth_first_tree_search(tp15)

localtime = time.asctime( time.localtime(time.time()) )
print "Ready to start depth_first_tree_search"  
"""
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
"""
   There are tools available to compare
   search algorithms. The stats contain the following data:
   number of successors /
   number of goal tests /
   number of states /
   first 4 bytes of the found goal

search.compare_searchers([tp6],["algorithm","Tantrix pyramid 6"],[
        search.breadth_first_tree_search,
        search.depth_first_tree_search,        
        search.depth_first_graph_search,
        search.breadth_first_search
    ])
"""    
print "End"
"""END"""
