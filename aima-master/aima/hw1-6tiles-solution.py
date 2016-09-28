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
    if tilB[n]== ' ':           #spesial test for VOID tile
        return True
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
        """
        В этом цикле считается число возможных вариантов сопрекосновений ребер?
        И затем печатается. В случае 6 фигурок : 6x6=36; в случае 15 будет 15x6?

        Нет.
        Этот цикл нужен для того, чтобы на основании 6 "realTiles" сделать 36 "self.tiles" в которых будут все повороты фишек.
        Пример из двух фишек
        realTiles=[
           ('y','r','b','b','r','y'),
           ('y','b','r','r','b','y')]
        Даст 2х6=12 фишек с вращением :
         ('y','r','b','b','r','y'),
         ('y','y','r','b','b','r'),
         ('r','y','y','r','b','b'),
         ('b','r','y','y','r','b'),
         ('b','b','r','y','y','r'),
         ('r','b','b','r','y','y'),
         
         ('y','b','r','r','b','y'),
         ('y','y','b','r','r','b'),
         ('b','y','y','b','r','r'),
         ('r','b','y','y','b','r'),
         ('r','r','b','y','y','b'),   
         ('b','r','r','b','y','y'), 
        
        Именно из этого глобального поля возможностей будут потом отобраны те фишки, что мы вернем в функции actions -  return enabledActions 
        
        """
    def getCellNumberToTest(self, cell_ID):
        # return  nr_X, nr_Y, nr_Z, -1 for void tile
        if cell_ID == 1: return -1, 0, -1
        if cell_ID == 2: return  0, -1, 1
        if cell_ID == 3: return -1, 1, -1
        if cell_ID == 4: return  1, 2,  3
        if cell_ID == 5: return  2, -1, 4
        if cell_ID == 6: return -1, 1, -1

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
        #print "i = %d "%i
        enabledActions=set(self.tiles)
        toRemove=[]  # list of the tiles that do not have matching color     
        """
        Функция  def actions
        Не совсем понимаем что происходит здесь:
        """        
        if i == 0:
            return enabledActions
        else:
            for j in range(i):  # go over all puted tiles and 
                for k in range(0,6): #remove all rotation of choisen tile
                   enabledActions.remove(leftShift(state[j],k))                   
                   """
                   Начнем с того, что  i это сколько ячеек поля уже занято фишками
                   Если ноль, то в первую ячейку можно положить любую из 36 фишек
                    if i == 0: return enabledActions

                   если сколько то фишек уже лежит на поле, то нужно удалить из списка возможных 36 фишек те 6 вариантов, которые связаны с этой конкретной фишкой.
                   """
        
        nr_X, nr_Y, nr_Z = self.getCellNumberToTest(i)
        
        #print nr_X, nr_Y, nr_Z 
        
        T = list()
        for s in state:
          T.append(s)    # get the i-st tile 
          
        for t in enabledActions:  # go over all lefted tiles and if this tile 't' not match to t0, remove it from enabledActions   
            if False == ( self.generalTest(T,t ,nr_X, nr_Y, nr_Z) ): toRemove.append(t)            
            """
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
            """
            
        for t in toRemove:
            #print t
            enabledActions.remove(t)
        #print "return enabledActions" 
        #print enabledActions
        return enabledActions
        
        """
         Можем в крации описать как работает алгоритм сравнения цветов
         в функции actions? Понятно, что ищются возможные actions, 
         и  в ходе проверки на несовпадение, удаляются, если не совпали.
         Не ясна сама проверка по какому принципу происходит.
         '          ___
         '         /   \                    _2_
         '        /     \                  /   \
         '    ___/   2   \                1     3
         '   /   \       /               /       \
         '  /     \     /                \       /
         ' /   0   \___/                  0     4
         ' \       /   \                   \_5_/
         '  \     /     \ 
         '   \___/   1   \
         '       \       /
         '        \     / 
         '         \___/                     
         '        
         Когда ставим фишку с номером 1, то проверяем, 
         чтобы цвет на грани 4 фишки с номером 0 
         совпадал с цветом грани 1 у фишки 1, делаем проверку по оси Y - testY(T[0], t)
           
         Когда ставим фишку с номером 2, то проверяем, 
         чтобы цвет на грани 3 фишки с номером 0 
         совпадал с цветом грани 0 у фишки 2, делаем проверку по оси X
         А так же чтобы цвет на грани 2 фишки с номером 1 
         совпадал с цветом грани 5 у фишки 2, делаем проверку по оси Z  (testX(T[0],t) and testZ(T[1],t)):
        """
                
    def result(self, state, action):
        newState = list(state)
        i = state.index(None)
        newState[i] = action
        return tuple(newState)
        
        """
        Что именно делалет функция def result?
        На основании текущего состояния - state, 
        находит номер не занятой ячейки  = state.index(None)
        И помещяает в эту свободную ячейку фишку из списка action:
        newState[i] = action
        ну и возвращает новое состояние            
        """
    
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
"""
localtime = time.asctime( time.localtime(time.time()) )
print "Ready to start depth_first_graph_search"  
print "Local current time :", localtime
search.depth_first_graph_search(tp6)

localtime = time.asctime( time.localtime(time.time()) )
print "Ready to start breadth_first_search"
print "Local current time :", localtime
search.breadth_first_search(tp6)


Функция:
search.compare_searchers

Выдает следующее:
algorithm                   Tantrix pyramid 6     
breadth_first_tree_search   <9331/9332/23496/(('b>
depth_first_tree_search     <   7/   8/  63/(('r> 
depth_first_graph_search    <   7/   8/  63/(('r> 
breadth_first_search        <6971/9332/9336/(('b> 

Слева понятно - названия алгоритмов.
Что значат значения в правом столбце?

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
    ])"""
print "End"
"""END"""

"""
Вопрос про initialState = [None,None,None,None,None,None].
Вроде нам понятно что это значет, но на всякий случай уточни что это.
initialState = [None,None,None,None,None,None].
Вначале на поле из 6 ячеек нет ничего


Потом алгоритм поиска будет выкладывать в первую ячейку одну фишку, например  ('r','y','y','r','b','b'),
и состояние поля будет State = [('r','y','y','r','b','b'),None,None,None,None,None].
Потом мы этим циклом выкинем все 6 вращенией первой фишки:
for k in range(0,6): #remove all rotation of choisen tile
    enabledActions.remove(leftShift(state[i],k))

(удалим эти элементы из начального массива:
 ('y','r','b','b','r','y'),
 ('y','y','r','b','b','r'),
 ('r','y','y','r','b','b'),
 ('b','r','y','y','r','b'),
 ('b','b','r','y','y','r'),
 ('r','b','b','r','y','y'),
у нас останетцв 30 фишек.

Потом мы проверим, и удалим все фишки, которые не могут лечь на ячейку 1, потому что
цвет на грани 4 фишки с номером 0 (b)
совпадал с цветом грани 1 у фишки 1, делаем проверку по оси Y
testY(T[0], t)


и на втором шаге мы можем выложить эту фишку
('r','b','y','y','b','r'),
И тогда состояние поля будет 
State = [('r','y','y','r','B','b'),('r','B','y','y','b','r'),None,None,None,None].

И так далее
"""