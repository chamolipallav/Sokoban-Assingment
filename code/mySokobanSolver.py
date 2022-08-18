
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2021-08-17  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [(10635700, 'Pallav','Chamoli'),(9641556, 'Tan', 'Zhi On') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag one as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    
    remove_squares = ['@', '$']
    target_squares = ['.', '!', '*']
    wall_squares = '#'
    taboocell_squares = 'X'
    
    def cornerCell(warehouse, x, y, wall = 0):
        count_upDown = 0
        count_leftRight = 0
        
        for (posX, posY) in [(0,1), (0,-1)]:
            if warehouse[y+posY][x+posX] == wall_squares:
                count_upDown = count_upDown + 1
                
        for (posX, posY) in [(1,0), (-1,0)]:
            if warehouse[y+posY][x+posX] == wall_squares:
                count_leftRight = count_leftRight + 1
        
        if wall: 
            return(count_upDown >= 1) or (count_leftRight >= 1) 
        else:
            return(count_upDown >= 1) and (count_leftRight >= 1) 
        
    #string warehouse
    stringWarehouse = str(warehouse)
        
    #remove target squares
    for character in remove_squares:
        stringWarehouse = stringWarehouse.replace(character, ' ')
    
    # string to 2d array 
    warehouse2d = [list(row) for row in stringWarehouse.split('\n')]
    
    
    #rule 1 
    for posY in range(len(warehouse2d) - 1):
        checkInside = False
        for posX in range(len(warehouse2d[0]) - 1):

            
            if checkInside == False:
                if warehouse2d[posY][posX] == wall_squares:
                    checkInside = True
            else:

                #checking if cell is empty on the right 
                if all([cell == ' ' for cell in warehouse2d[posY][posX:]]):
                    break
                if warehouse2d[posY][posX] not in target_squares:
                    if warehouse2d[posY][posX] != wall_squares:
                        if cornerCell(warehouse2d, posX, posY):
                            warehouse2d[posY][posX] = taboocell_squares
    
    # rule 2 
    for posY in range(1, len(warehouse2d) - 1):
        for posX in range(1, len(warehouse2d[0]) - 1):
            if warehouse2d[posY][posX] == taboocell_squares and cornerCell(warehouse2d, posX, posY):
                row = warehouse2d[posY][posX + 1:]
                col = [row[posX] for row in warehouse2d[posY + 1:][:]]
                # fill in taboo_cells in row to the right of corner taboo cell
                for posX2 in range(len(row)):
                    if row[posX2] in target_squares or row[posX2] == wall_squares:
                        break
                    if row[posX2] == taboocell_squares and cornerCell(warehouse2d, posX2 + posX + 1, posY):
                        if all([cornerCell(warehouse2d, posX3, posY, 1) for posX3 in range(posX + 1, posX2 + posX + 1)]):
                            for posX4 in range(posX + 1, posX2 + posX + 1):
                                warehouse2d[posY][posX4] = 'X'
                # fill in taboo_cells in column moving down from corner taboo
                # cell
                for posY2 in range(len(col)):
                    if col[posY2] in target_squares or col[posY2] == wall_squares:
                        break
                    if col[posY2] == taboocell_squares \
                            and cornerCell(warehouse2d, posX, posY2 + posY + 1):
                        if all([cornerCell(warehouse2d, posX, posY3, 1) for posY3 in range(posY + 1, posY2 + posY + 1)]):
                            for posY4 in range(posY + 1, posY2 + posY + 1):
                                warehouse2d[posY4][posX] = 'X'
   


    # 2d array to string 
    stringWarehouse = '\n'.join([''.join(row) for row in warehouse2d])

    # remove target squares
    for char in target_squares:
        stringWarehouse = stringWarehouse.replace(char, ' ')
    
    return stringWarehouse
   

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''    
    
    def __init__(self, warehouse):
        self.initial = warehouse
        goal = None
        
        if goal is None:
            self.goal = warehouse.copy()
            self.goal.boxes = self.goal.targets
            self.alt_goal = False
            
        else:
            
            self.goal = warehouse.copy()
            self.goal.worker = goal
            self.alt_goal = True
            
        #self.dead_lock =get_deadlock(warehouse)
        
        self.orginal_boxes = []
        self.orginal_worker = self.goal.worker
        


    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        actions = ['Left', 'Down', 'Right', 'Up']
        action_valid = []
        
        self.orginal_boxes =state.boxes.copy()
        self.orginal_worker = state.worker
        
        for action in actions:
            
            
            # use this when check_action is defined in taboo_cells
            temp = check_elem_action_seq(state.copy(worker = self.original_worker, boxes=state.boxes.copy()), [action])
            
            if type(temp)!= str:
                
                if set(temp.boxes) & self.dead_locks == set():
                    
                    action_valid.append(action)
                    
        return action_valid
   

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    
    for action in action_seq:
        worker_pos_x, worker_pos_y = warehouse.worker
        
        #Location of cells
        if action == 'Left':
            cell1 = (worker_pos_x-1, worker_pos_y)
            cell2 = (worker_pos_x-2, worker_pos_y)
            
        elif action == 'Right':
            cell1 = (worker_pos_x+1, worker_pos_y)
            cell2 = (worker_pos_x+2, worker_pos_y)
        
        elif action == 'Up':
            cell1 = (worker_pos_x, worker_pos_y-1)
            cell2 = (worker_pos_x, worker_pos_y-2)
        
        elif action == 'Down':
            cell1 = (worker_pos_x, worker_pos_y+1)
            cell2 = (worker_pos_x, worker_pos_y+2)            
        
        #checks worker pushing walls
        if cell1 in warehouse.walls:
            return 'Impossible'

        if cell1 in warehouse.boxes:
            if cell2 in warehouse.boxes or cell2 in warehouse.walls:
                #push two boxes or the box has already nearby the wall
                #then
                return 'Impossible'
            
            #Only oen box at a  time
            warehouse.boxes.remove(cell1)
            warehouse.boxes.append(cell2)

        warehouse.worker = cell1 

    return warehouse
            
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    raise NotImplementedError()
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

