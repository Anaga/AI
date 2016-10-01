# -*- coding: utf-8 -*-
"""
prog to solve HW1 in ITI8600.

it is posible to sped ou, if route print out to log
hw1-15tiles-solution.py > log.txt

"""
import time
import search

"""
   We actually have 15 tiles, thus we call those realTiles.
   For the demo propos, we can decrease the cout on tiles, to get fast result.
   6 is wery fast
   10 is take some time,
   15 can be hours.
   
   In the instantiation of the Problem class we create all rotations. (15*6=90)
"""

realTilesSet = [
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
    ('y','r','b','r','b','y') ] 

def N_Tailes(N):
    print "Now we try to solve %d tailes"%N
    tryTails = []
    for i in range(N):
        tryTails.append(realTilesSet[i])
    return tryTails

realTiles15 = N_Tailes(8)
"""    
    ('r','y','g','r','g','y'),
    
    ('y','r','b','r','y','b'),
    ('y','b','g','b','g','y'),

    ('y','b','y','g','g','b'),
    ('r','y','r','y','b','b'),
    ('r','b','r','g','b','g'),
        
    ('y','y','r','b','b','r'),
    ('b','r','r','b','y','y'),
    ('r','y','y','b','b','r'),
    ('b','b','y','y','r','r')
    
    ('g','g','y','b','b','y'),    
    ('b','r','b','y','r','y'),
    ('g','y','y','g','r','r'),
    ('y','y','g','g','b','b'),
    ('y','r','b','r','b','y')   ]
    """
    
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
     '        /                 /   2   \     J     /   2   \     |          X, Y, Z 
     '       /                 /1       3\0       4/1       3\    |  A check -, -, -     
     '      /          _______/     F     \___5___/     N     \   |  B check -, A, -   if cell_ID == 1: return -1, 0, -1                    
     '     /          /   2   \     F     /   2   \     N     /   |  C check A, -, B   if cell_ID == 2: return  0, -1, 1                                    
     '    /          /1       3\0       4/1       3\0       4/    |  D check -, B, -   if cell_ID == 3: return -1, 1, -1                                          
     '   /   _______/     C     \___5___/     I     \___5___/     |  E check B, C, D   if cell_ID == 4: return  1, 2,  3                        
     '  /   /   2   \     C     /   2   \     I     /   2   \     |  F check C, -, E   if cell_ID == 5: return  2, -1, 4                   
     ' /   /1       3\0       4/1       3\0       4/1       3\    |  G check -, D, -   if cell_ID == 6: return -1, 3, -1                     
     '/   /     A     \___5___/     E     \___5___/     M     \   |  H check D, E, G   if cell_ID == 7: return  3, 4,  6                  
     '\   \     A     /   2   \     E     /   2   \     M     /   |  I check E, F, H   if cell_ID == 8: return  4, 5,  7            
     ' \   \0       4/1       3\0       4/1       3\0       4/    |  J check F, -, I   if cell_ID == 9: return  5, -1, 8    
     '  \   \___5___/     B     \___5___/     H     \___5___/     |  K check -, G, -   if cell_ID ==10: return -1, 6, -1                       
     '   \          \     B     /   2   \     H     /   2   \     |  L check G, H, K   if cell_ID ==11: return  6, 7, 10                
     '    \          \0       4/1       3\0       4/1       3\    |  M check H, I, L   if cell_ID ==12: return  7, 8, 11           
     '     \          \___5___/     D     \___5___/     L     \   |  N check D, E, M   if cell_ID ==13: return  8, 9, 12              
     '      \                 \     D     /   2   \     L     /   |  O check J, -, H   if cell_ID ==14: return  9, -, 13              
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
     '                                             /   O2   \     
     '                                            /O1       O3\    
     '                                    _______/           \   
     '                                   /   J2   \           /   
     '                                  /J1       J3\\O0       O4/   
     '                          _______/           \___O5___/                      
     '                         /   F2   \           /   N2   \                       
     '                        /F1       F3\\J0       J4/N1       N3\                 
     '                _______/           \___J5___/           \                        
     '               /   C2   \           /   I2   \           /                    
     '              /C1       C3\\F0       F4/I1       I3\\N0       N4/                        
     '      _______/           \___F5___/           \___N5___/                      
     '     /   A2   \           /   E2   \           /   M2   \                        
     '    /A1       A3\\C0       C4/E1       E3\\I0       I4/M1       M3\                       
     '   /           \___C5___/           \___I5___/           \                  
     '   \           /   B2   \           /   H2   \           /            
     '    \\A0       A4/B1       B3\\E0       E4/H1       H3\\M0       M4/               
     '     \___A5___/           \___E5___/           \___M5___/                       
     '             \           /   D2   \           /   L2   \                
     '              \\B0       B4/D1       D3\\H0       H4/L1       L3\           
     '               \___B5___/           \___H5___/           \      
     '                       \           /   G2   \           /      
     '                        \\D0       D4/G1       G3\\L0       L4/       
     '                         \___D5___/           \___L5___/    
     '                                 \           /   K2   \    
     '                                  \\G0       G4/K1       K3\  
     '                                   \___G5___/           \  
     '                                           \           /  
     '                                            \\K0       K4/  
     '                                             \___K5___/    
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
        self.gameTiles = realTiles15
        for tile in realTiles15:
            for i in range(0,6):
                self.tiles.add(leftShift(tile,i))
        print "Init compled, total we have %d tiles, including all rotations" % len(self.tiles)
        self.number_of_puted_tiles = 0
        printField(self.gameSet)
    
    def getCellNumberToTest(self, cell_ID):
        # return  nr_X, nr_Y, nr_Z, -1 for void tile        
        if cell_ID == 1: return -1, 0, -1
        if cell_ID == 2: return  0, -1, 1
        if cell_ID == 3: return -1, 1, -1
        if cell_ID == 4: return  1, 2,  3  
        if cell_ID == 5: return  2, -1, 4
        if cell_ID == 6: return -1, 3, -1  
        if cell_ID == 7: return  3, 4,  6  
        if cell_ID == 8: return  4, 5,  7  
        if cell_ID == 9: return  5, -1, 8  
        if cell_ID ==10: return -1, 6, -1  
        if cell_ID ==11: return  6, 7, 10  
        if cell_ID ==12: return  7, 8, 11  
        if cell_ID ==13: return  8, 9, 12  
        if cell_ID ==14: return  9,-1, 13 

    def generalTest(self, T, tileToTest, nr_X, nr_Y, nr_Z):
        if nr_X == -1: X= True
        else: X = (testX(T[nr_X], tileToTest))
        
        if nr_Y == -1: Y= True
        else: Y = (testY(T[nr_Y], tileToTest))    

        if nr_Z == -1: Z= True
        else: Z = (testZ(T[nr_Z], tileToTest))
        
        return ( X and Y and Z)
        
    def actions(self,state):    
        #print "function to return possible actions from current state"
        #print state
        i =  state.index(None)
        
        if (i!= self.number_of_puted_tiles):
            self.number_of_puted_tiles = i        
            #print "number_of_puted_tiles = %d "%i
            #printField(self.gameSet)
        enabledActions=set(self.tiles)
        toRemove=[]  # list of the tiles that do not have matching color     
        
        if i == 0:
            return enabledActions
        else:
            for j in range(i):  # go over all puted tiles and 
                for k in range(0,6): #remove all rotation of choisen tile
                   enabledActions.remove(leftShift(state[j],k))
        
        nr_X, nr_Y, nr_Z = self.getCellNumberToTest(i)
        
        T = list()
        for s in state:
          T.append(s)    # get the i-st tile 
          
        for t in enabledActions:  # go over all lefted tiles and if this tile 't' not match, remove it from enabledActions   
            if False == ( self.generalTest(T, t , nr_X, nr_Y, nr_Z) ): toRemove.append(t)
                   
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
        number_of_puted_tiles = (15 - i)
        
        if (number_of_puted_tiles != self.number_of_puted_tiles):
          """
          localtime = time.asctime( time.localtime(time.time()) )
          print "Local current time :", localtime
          printField(self.gameSet )
          print "total gameTiles is %d" %len(self.gameTiles)
          print "plase %d ties"%(number_of_puted_tiles)
          """
          self.number_of_puted_tiles = number_of_puted_tiles

        if (number_of_puted_tiles != len(self.gameTiles)): return False

        print "We finde the solution!"
        localtime = time.asctime( time.localtime(time.time()) )
        print "Local current time :", localtime
        printField(self.gameSet )
        return True
        
    def h(self,state):
	    return 1

    def prin(self):
        print "TantrixPyramid15"
        print "Current State:"
        printField(self.gameSet )
        
print "Start up" 
time_format = "%c, %H:%M:%S"
tp15 = TantrixPyramid15(initialState15,realTiles15)
localtime = time.strftime(time_format, time.localtime(time.time()) )
print "Startup time is:", localtime
tp15.prin()

print "Ready to start astar_search"  
start = time.time()
search.astar_search(tp15)
end = time.time()
localtime = time.strftime(time_format, time.localtime(end) )
print "Now the astar_search complited, current time is:%s,  take %s sec " % (localtime, str(end - start))
print "\n"


print "Ready to start breadth_first_tree_search"  
start = time.time()
search.breadth_first_tree_search(tp15)
end = time.time()
localtime = time.strftime(time_format, time.localtime(end) )
print "Now the breadth_first_tree_search complited,  current time is:%s,  take %s sec " % (localtime, str(end - start))
print "\n"


print "Ready to start depth_first_tree_search"  
start = time.time()
search.depth_first_tree_search(tp15)
end = time.time()
localtime = time.strftime(time_format, time.localtime(end) )
print "Now the depth_first_tree_search complited,  current time is:%s,  take %s sec " % (localtime, str(end - start))
print "\n"


print "Ready to start depth_first_graph_search"  
start = time.time()
search.depth_first_graph_search(tp15)
end = time.time()
localtime = time.strftime(time_format, time.localtime(end) )
print "Now the depth_first_graph_search complited,  current time is:%s,  take %s sec " % (localtime, str(end - start))
print "\n"


print "Ready to start breadth_first_search"
start = time.time()
search.breadth_first_search(tp15)
end = time.time()
localtime = time.strftime(time_format, time.localtime(end) )
print "Now the breadth_first_search complited, current time is:%s,  take %s sec " % (localtime, str(end - start))
print "\n"


"""
   There are tools available to compare
   search algorithms. The stats contain the following data:
   number of successors /
   number of goal tests /
   number of states /
   first 4 bytes of the found goal
"""  

search.compare_searchers([tp15],["algorithm","Tantrix pyramid 15"],[
        search.astar_search,
        search.breadth_first_tree_search,
        search.depth_first_tree_search,        
        search.depth_first_graph_search,
        search.breadth_first_search
    ])

 
print "End"

