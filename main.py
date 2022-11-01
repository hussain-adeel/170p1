

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

    solve(puzzle, select3)

def solve(puzzle, algorithim):
    if (algorithim == 1):
        unicost(puzzle)
    elif (algorithim == 2):
        misplace(puzzle)
    elif (algorithim == 3):
        manhattan(puzzle)

driver();
