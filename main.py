import queue
import time
import copy


default_easy = [[1, 2, 3],[4, 5, 6],[7, 0, 8]]
default = [[0, 1, 2],[4, 5, 3],[7, 8, 6]]
default_hard = [[8, 7, 1],[6, 0, 2],[5, 4, 3]]
goal_state = [[1, 2, 3],[4, 5, 6],[7, 8, 0]]

def driver():
    print("Welcome to the CS 170 Puzzle Solver...")
    print("Please select an option below to continue:")
    print("1. Default Puzzle")
    print("2. Custom Puzzle")

    select = int(input("Selection: "));

    # USER SELECTS PUZZLE OR CREATES CUSTOM PUZZLE
    if (select == 1):
        print("Please select a difficulty for the default puzzle...")
        print("1. Easy Puzzle")
        print("2. Medium Puzzle")
        print("3. Hard Puzzle")

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

    start_time = time.time()
    result = general_search(puzzle, select3)
    end_time = time.time()
    total_time = round(end_time-start_time, 1)
    print("This attempt took: " + str(total_time) + " seconds.")

    if (result == "failed"): print("Could not complete search...")
    elif (result == "success"): print("REACH...")

def print_puzzle(puzzle):
    for i in range(0, 3):
        print(puzzle[i])
    print('\n')

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
    
        # we need: hn, fn, gn

def goal(puzzle):
    if (puzzle == goal_state): return 1
    else: return 0

def general_search(puzzle, algorithim):
    nodes = queue.PriorityQueue();
    initalState = Node(puzzle, 0, 0)
    nodes.put(initalState) #inital state
    print("Starting State:")
    print_puzzle(initalState.getState())
    repeatStates = {};

    while(1):
        if (nodes.empty()): return "failed"
        currNode = nodes.get()
        if (goal(currNode.getState()) == 1): return "success"
        repeatStates += currNode.getState();


driver();