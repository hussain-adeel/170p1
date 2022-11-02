import queue
import time
import copy


default_easy = [[1, 2, 3],[4, 0, 6],[7, 5, 8]]
default = [[0, 1, 2],[4, 5, 3],[7, 8, 6]]
default_hard = [[8, 7, 1],[6, 0, 2],[5, 4, 3]]
goal_state = [[1, 2, 3],[4, 5, 6],[7, 8, 0]]
nodes_expanded = 0


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

    if (select3 == 1): algorithim = ucs
    elif (select3 == 2): algorithim = mt
    elif (select3 == 3): algorithim = m

    start_time = time.time()
    result = general_search(puzzle, algorithim)
    end_time = time.time()
    total_time = round(end_time-start_time, 1)
    print("This attempt took: " + str(total_time) + " seconds.")

    if (result == "failed"): print("Could not complete search...")
    elif (result == "success"): 
        print("Stopping Program...")


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
    def getZeroIndex(self):
        for i, k in enumerate(self.state):
            for l, m in enumerate(k):
                if m == 0: return [l, i]
    def __lt__(self, compare):
        return self.fn < compare.getFn()


def goal(puzzle):
    if (puzzle == goal_state): return 1
    else: return 0

def ucs(nodes, expanded):
    nodes_copy = nodes;

    for n in expanded:
        nodes_copy.put(n)

    return nodes_copy

def mt(nodes, moves):
    return
def m(nodes, moves):
    return

numNodesExpanded = 0

def expand(currNode, repeatStates):
    # NEED INDEX OF 0 STATE

    zeroXY = currNode.getZeroIndex()
    zeroX = zeroXY[0]; 
    zeroY = zeroXY[1];
    moves = list();
    global numNodesExpanded

    # CHECK UP
    if (zeroY != 0):
        up_copy = copy.deepcopy(currNode.getState())
        up_copy[zeroY][zeroX] = up_copy[zeroY - 1][zeroX]
        up_copy[zeroY - 1][zeroX] = 0
        if repeatStates.get(tuple(tuple(s) for s in up_copy)) != 'R':
            #print("append up")
            up_node = Node(up_copy,  currNode.getHn(), currNode.getGn() + 1);
            moves.append(up_node);
            numNodesExpanded+=1;

    # CHECK DOWN
    if (zeroY != 2):
        down_copy = copy.deepcopy(currNode.getState())
        down_copy[zeroY][zeroX] = down_copy[zeroY + 1][zeroX]
        down_copy[zeroY + 1][zeroX] = 0
        if repeatStates.get(tuple(tuple(s) for s in down_copy)) != 'R':
            #print("append down")
            down_node = Node(down_copy,  currNode.getHn(), currNode.getGn() + 1);
            moves.append(down_node);
            numNodesExpanded+=1;

    # CHECK LEFT
    if (zeroX != 0):
        left_copy = copy.deepcopy(currNode.getState())
        left_copy[zeroY][zeroX] = left_copy[zeroY][zeroX - 1]
        left_copy[zeroY][zeroX - 1] = 0
        
        if repeatStates.get(tuple(tuple(s) for s in left_copy)) != 'R':
            #print("append left")
            left_node = Node(left_copy,  currNode.getHn(), currNode.getGn() + 1);
            moves.append(left_node);
            numNodesExpanded+=1;

    # CHECK RIGHT
    if (zeroX != 2):
        right_copy = copy.deepcopy(currNode.getState())
        right_copy[zeroY][zeroX] = right_copy[zeroY][zeroX + 1]
        right_copy[zeroY][zeroX + 1] = 0
        if repeatStates.get(tuple(tuple(s) for s in right_copy)) != 'R':
            #print("append right");
            right_node = Node(right_copy, currNode.getHn(), currNode.getGn() + 1);
            moves.append(right_node);
            numNodesExpanded+=1;



    #for move in moves:
    #    print_puzzle(move.getState());

    return moves

def general_search(puzzle, algorithim):
    global numNodesExpanded
    nodes = queue.PriorityQueue();
    initalState = Node(puzzle, 0, 0)
    nodes.put(initalState) #inital state
    print("Starting State:")
    print_puzzle(initalState.getState())
    repeatStates = {};
    maxQueueSize = 1;

    while(1):
        if (nodes.empty()): return "failed"
        currNode = nodes.get()
        if (goal(currNode.getState()) == 1):
            print("REACHED GOAL STATE!")
            print("The maximum queue size was: " + str(maxQueueSize))
            print("The depth was: " + str(currNode.getGn()))
            print("The number of nodes expanded was: " + str(numNodesExpanded))
            return "success"
        stateTuple = tuple(tuple(s) for s in currNode.getState())
        repeatStates[stateTuple] = "R"
        print(stateTuple)
        print("The best state to expand with a g(n) = " + str(currNode.getGn()) + " and h(n) = " + str(currNode.getHn()) + " is...")
        nodes = algorithim(nodes, expand(currNode, repeatStates))
        print_puzzle(currNode.getState());
        if (nodes.qsize() > maxQueueSize): maxQueueSize = nodes.qsize();

driver();