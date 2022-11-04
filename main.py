import queue
from re import L # TO ACCESS PRIORITY QUEUE
import time # TO CALCULATE AMNT OF TIME PROGRAM TAKES
import copy # TO DEEP COPY LISTS OF LISTS (cannot lose values)


# Some puzzles taken from Dr. Keogh's project handout
default_easy = [[1, 2, 3],[4, 5, 6],[0, 7, 8]]
default = [[1, 3, 6],[5, 0, 7],[4, 8, 2]]
default_hard = [[0, 7, 2],[4, 6, 1],[3, 5, 8]]

# End-goal of what we want
goal_state = [[1, 2, 3],[4, 5, 6],[7, 8, 0]]

# Main driver class of program, calls all other functions to make program run properly
def driver():

    print("Welcome to the CS 170 Puzzle Solver...")
    print("Please select an option below to continue:")
    print("1. Default Puzzle")
    print("2. Custom Puzzle")

    # This select stores value of if user wants to use a default or custom value
    select = int(input("Selection: "))

    # IF-statement that allows user to choose from default values or create own
    if (select == 1):
        print("Please select a difficulty for the default puzzle...")
        print("1. Easy Puzzle")
        print("2. Medium Puzzle")
        print("3. Hard Puzzle")

        #this select stores user's choice of puzzle difficulty
        select2 = int(input("Selection: "))

        if (select2 == 1):
            puzzle = default_easy
        elif (select2 == 2):
            puzzle = default
        else:
            puzzle = default_hard
    elif (select == 2):
        print("Type numbers with a space between them, use '0' as the blank space...")
        print("You will type numbers per row... hit ENTER after you are done entering for that row")
        
        # User enters  puzzle to be used 

        row_one = input("Enter the first row: ")
        row_two = input("Enter the second row: ")
        row_three = input("Enter the third row: ")

        row_one = row_one.split()
        row_two = row_two.split()
        row_three = row_three.split()

        for i in range(0, 3):
            row_one[i] = int(row_one[i])
            row_two[i] = int(row_two[i])
            row_three[i] = int(row_three[i])
        
        puzzle = [row_one, row_two, row_three]

    # TAKE CREATED OR DEFAULT PUZZLE AND LET USER SELECT ALGORITHIM

    print("Select an algorithim to use with your puzzle\n1. Unform Cost Search\n2. A* with Misplaced Tile heuristic.\n3. A* with Manhattan Distance heuristic")
    select3 = int(input("Selection: "))

    if (select3 == 1): algorithim = ucs
    elif (select3 == 2): algorithim = mt
    elif (select3 == 3): algorithim = m

    start_time = time.time() # keeps track of start time of the program
    result = general_search(puzzle, algorithim)
    end_time = time.time() # same as start, tracks end time
    total_time = round(end_time-start_time, 1) # end - start = total time elapsed
    print("This attempt took: " + str(total_time) + " seconds.")

    if (result == "failed"): print("Could not complete search...")
    elif (result == "success"): 
        print("Stopping Program...")


# Simple funciton to print puzzle (taken from DK's handout)
def print_puzzle(puzzle):
    for i in range(0, 3):
        print(puzzle[i])
    print('\n')

# simple function to see if we have reaeched the goal state 
def goal(puzzle):
    if (puzzle == goal_state): return 1
    else: return 0

# Simple node class to store basic info of 8 puzzle nodes (the puzzle, cost, depth, fn, zero-index)
class Node:
    def __init__(self, state, hn, gn):
        self.state = state
        self.hn = hn
        self.gn = gn
        self.fn = hn + gn
    def getState(self):
        return self.state
    def getFn(self):
        return self.fn
    def getHn(self):
        return self.hn
    def getGn(self):
        return self.gn
    def setHn(self, new_hn):
        self.hn = new_hn
    def updateFn(self):
        self.fn = self.hn + self.gn
    def getZeroIndex(self):
        for i, k in enumerate(self.state):
            for l, m in enumerate(k):
                if m == 0: return [l, i]
    # this is used by the priority queue to determine how to order these nodes
    def __lt__(self, compare): 
        if (self.fn == compare.getFn()): return self.gn < compare.getGn()
        else: return self.fn < compare.getFn()

# function to sort PQ using Uniform Cost Search (notice we have cost set to 0 for all...
# ... operations so this is basically bfs )
def ucs(nodes, moves):
    new_nodes = nodes

    for node in moves:
        new_nodes.put(node)

    return new_nodes

# functin to sort PQ w/ the Missing Tile Heuristic
def mt(nodes, moves):

    new_nodes = nodes
    for node in moves:
        dist = 0
        node_puzzles = node.getState()
        for i in range (0, 3):
            for j in range (0, 3):
                if node_puzzles[i][j] != goal_state[i][j]: dist += 1
        node.setHn(dist)
        node.updateFn()
        new_nodes.put(node)
    return new_nodes

#function to sort PQ w/ the Manhattan Heuristic
def m(nodes, moves):
    new_nodes = nodes
    for node in moves:
        dist = 0
        node_puzzles = node.getState()
        print_puzzle(node_puzzles)
        for i in range (0, 3):
            for j in range (0, 3):
                if node_puzzles[i][j] == goal_state[i][j]: continue
                else:
                    match node_puzzles[i][j]:
                        case 1: dist += abs(j - 0) + abs(i - 0)
                        case 2: dist += abs(j - 1) + abs(i - 0)
                        case 3: dist += abs(j - 2) + abs(i - 0)
                        case 4: dist += abs(j - 0) + abs(i - 1)
                        case 5: dist += abs(j - 1) + abs(i - 1)
                        case 6: dist += abs(j - 2) + abs(i - 1)
                        case 7: dist += abs(j - 0) + abs(i - 2)
                        case 8: dist += abs(j - 1) + abs(i - 2)
        node.setHn(dist)
        node.updateFn()
        new_nodes.put(node)
    
    return new_nodes

def expand(currNode, repeatStates):

    zeroXY = currNode.getZeroIndex() # get 0-index (where there blank space is)

    # Need to decompose to their own variables 
    zeroX = zeroXY[0]
    zeroY = zeroXY[1]

    # list to store moves being added to PQ after this expansion
    moves = []

    # Check if blank is allowed to move up (i.e. not against the top edge), 
    # then deepcopy and check for repeat state, if all is good then add to move list
    if (zeroY != 0):
        up_copy = copy.deepcopy(currNode.getState())
        up_copy[zeroY][zeroX] = up_copy[zeroY - 1][zeroX]
        up_copy[zeroY - 1][zeroX] = 0
        if repeatStates.get(tuple(tuple(s) for s in up_copy)) != 'R':
            up_node = Node(up_copy,  currNode.getHn(), currNode.getGn() + 1)
            moves.append(up_node)

    # Same concept as up except for down (not against bottom edge...)
    if (zeroY != 2):
        down_copy = copy.deepcopy(currNode.getState())
        down_copy[zeroY][zeroX] = down_copy[zeroY + 1][zeroX]
        down_copy[zeroY + 1][zeroX] = 0
        if repeatStates.get(tuple(tuple(s) for s in down_copy)) != 'R':
            down_node = Node(down_copy,  currNode.getHn(), currNode.getGn() + 1)
            moves.append(down_node)

    # Same concept as up except for left (not against left edge...)
    if (zeroX != 0):
        left_copy = copy.deepcopy(currNode.getState())
        left_copy[zeroY][zeroX] = left_copy[zeroY][zeroX - 1]
        left_copy[zeroY][zeroX - 1] = 0
        if repeatStates.get(tuple(tuple(s) for s in left_copy)) != 'R':
            left_node = Node(left_copy,  currNode.getHn(), currNode.getGn() + 1)
            moves.append(left_node)

    # Same concept as up except for right (not against right edge...)
    if (zeroX != 2):
        right_copy = copy.deepcopy(currNode.getState())
        right_copy[zeroY][zeroX] = right_copy[zeroY][zeroX + 1]
        right_copy[zeroY][zeroX + 1] = 0
        if repeatStates.get(tuple(tuple(s) for s in right_copy)) != 'R':
            right_node = Node(right_copy, currNode.getHn(), currNode.getGn() + 1)
            moves.append(right_node)
    
    return moves

def general_search(puzzle, algorithim):

    # Create Priority Queue, declare initalize needed variables
    nodes = queue.PriorityQueue()
    repeatStates = {} # using a python dictonary
    maxQueueSize = 1
    numNodesExpanded = 0

    # Add inital problem state as first node
    initalState = Node(puzzle, 0, 0)
    nodes.put(initalState)
    print("Starting State:")
    print_puzzle(initalState.getState())
    
    # Ensures no repeat of the inital state by adding to dict (need to convert to tuple) 
    # and having index be the puzzle already found
    stateTuple = tuple(tuple(s) for s in initalState.getState())
    repeatStates[stateTuple] = "R"
    
    while(1):
        # no solution and no nodes left, search failed...
        if (nodes.empty()): return "failed"

        # pop current node off PQ
        currNode = nodes.get()

         # check if goal state reached
        if (goal(currNode.getState()) == 1):
            print("----------------\n")
            print_puzzle(currNode.getState())
            print("\n!!! REACHED GOAL STATE !!!")
            print("----------------")
            print("Num of nodes expanded: " + str(numNodesExpanded))
            print("Max queue size: " + str(maxQueueSize))
            print("Depth: " + str(currNode.getGn()))
            return "success"
        
        # If not goal, then we need to expand it
        print("The best state to expand with a g(n) = " + str(currNode.getGn()) + " and h(n) = " + str(currNode.getHn()) + " is...")
        print_puzzle(currNode.getState())
        
        # EXPAND to find new moves (need to do this sep. becasuse of how my repeat check works)
        new_moves = expand(currNode, repeatStates)
        
        # Need to sure no repeats of moves we already found through expanding
        for move in new_moves:
            t = tuple(tuple(x) for x in move.getState())
            repeatStates[t] = 'R'

        # Use queueing function selected to order PQ to better come up with solution
        nodes = algorithim(nodes, new_moves)
        numNodesExpanded+=1

        # Checking if max q size has been overtaken 
        if (nodes.qsize() > maxQueueSize): 
            maxQueueSize = nodes.qsize()

driver()
