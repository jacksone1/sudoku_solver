from copy import deepcopy

def print_puzzle(puzzle):
    if not puzzle:
        print("No solution")
        return
    for i in range(9):
        for j in range(9):
            square = puzzle[i][j]
            if square == 0 or isinstance(square, set):
                print('.', end='')
            else:
                print(square, end='')
            if (j + 1) % 3 == 0 and j < 8:
                print(' |', end='')

            if j != 8:
                print(' ', end='')
        print('\n', end='')
        if (i + 1) % 3 == 0 and i < 8:
            print("- - - + - - - + - - -\n")


def done(puzzle):
    #check if there are no blank squares
    #check every square to see if it has a set
    for row in puzzle:
        for square in row:
            #if the square is a set, then we are not done
            if isinstance(square, set):
                return False
    #if we didn't find any blanks
    return True


def findpossible(puzzle):
    #we have to eliminate what is not possible
    #if there is a 1 in the row, then square is not one
    #if there is a two in the row, then square is not two
    #and so on... 
    #then check column 
    #then check section

    #assume no progress until we solve one square 
    progress = False
    #assume we can solve the puzzle until we have no possibilities
    solvable = True 

    #loop through each row
    for y in range(9):
        #get the current row
        row = puzzle[y]
        #get the used numbers from the current row
        #the used numbers are the ones that aren't blanks (sets)
        used = set([square for square in row if not isinstance(square, set)])
        #loop through each square in the current row
        for x in range(9):
            if isinstance(puzzle[y][x], set):
                #subtract the used numbers from the possible numbers
                puzzle[y][x] -= used
                #if only one number is left then square=that number   
                if len(puzzle[y][x]) == 1:
                    puzzle[y][x] = puzzle[y][x].pop()
                    #we solved a square, so progress is true
                    progress = True
                # if there are no possiblities then we went wrong 
                elif len(puzzle[y][x]) == 0:
                    solvable = False
                    progress = None 
                    return solvable, progress 
    #loop through each column
    for x in range(9):
        #get the current column
        column = [puzzle[y][x] for y in range(9)]
        #get the used numbers from the current column
        #the used numbers are the ones that aren't blanks (sets)
        used = set([x for x in column if not isinstance(x, set)])
        #loop through each square in the current column
        for y in range(9):
            #if the square is a blank (set)
            if isinstance(puzzle[y][x], set):
                #subtract the used numbers from the possible numbers
                puzzle[y][x] -= used
                #if only one number is left then square=that number   
                if len(puzzle[y][x]) == 1:
                    puzzle[y][x] = puzzle[y][x].pop()
                    progress = True
                # if there are no possiblities then we went wrong 
                elif len(puzzle[y][x]) == 0:
                    solvable = False
                    progress = None 
                    return solvable, progress 
    #loop through each section
    for x in range(3):
        for y in range(3):
            used = set()
            for i in range(3*x, 3*x+3):
                for j in range(3*y, 3*y+3):
                    square = puzzle[i][j]
                    if not isinstance(square, set):
                        used.add(square)
            for i in range(3*x, 3*x+3):
                for j in range(3*y, 3*y+3):
                    if isinstance(puzzle[i][j], set):
                        #subtract the used numbers from the possible numbers
                        puzzle[i][j] -= used
                        #if only one number is left then square=that number   
                        if len(puzzle[i][j]) == 1:
                            puzzle[i][j] = puzzle[i][j].pop()
                            progress = True
                        # if there are no possiblities then we went wrong 
                        elif len(puzzle[i][j]) == 0:
                            return False, None

    return True, progress


def loop(puzzle):
    #loop until we can't eliminate any more possibilities
    #or until the puzzle can't be solved
    solvable = True 
    progress = True 
    while solvable and progress:
        solvable, progress = findpossible(puzzle)

    if not solvable:
        return None

    if done(puzzle):
        return puzzle

    for y in range(9):
        for x in range(9):
            square = puzzle[y][x]
            #if the square is blank
            if isinstance(square, set):
                #try all remaining possible values
                for value in square:
                    #make a new copy of the puzzle
                    puzzle_copy = deepcopy(puzzle)
                    #try the current number from the set of possible values
                    puzzle_copy[y][x] = value
                    #repeat the steps above for the new puzzle
                    solved = loop(puzzle_copy)
                    if solved is not None:
                        return solved
                #if we've finished looping through all possible values
                #and still haven't found a solution, then
                #the puzzle is not solvable. 
                return None


def solver(start_puzzle):
    #make a copy of the puzzle
    puzzle = deepcopy(start_puzzle)

    #find all the blank squares
    #at first blanks are zeroes
    #we will put sets of possible numbers into all blanks

    #loop through all squares in puzzle
    #column 0-8
    for y in range(9):
        #row 0-8
        for x in range(9):
            #get the current square
            square = puzzle[y][x]
            #if the square is 0, then it's blank
            if square == 0:
                #put the set 1-9 in all the blanks
                #we will remove the numbers that don't work
                puzzle[y][x] = set(range(1,10))
    
    #now all the blanks have sets of possible numbers
    #start checking them until we find the right answer
    result = loop(puzzle)
    return result 


#easy
question = [
    [0,9,5,0,0,7,0,6,0],
    [0,7,1,0,0,9,5,0,4],
    [0,0,6,0,8,0,7,3,0],
    [0,0,0,0,3,0,1,0,0],
    [2,0,0,4,7,1,0,0,5],
    [0,0,9,0,2,0,0,0,0],
    [0,8,7,0,1,0,4,0,0],
    [1,0,4,8,0,0,6,2,0],
    [0,3,0,7,0,0,9,1,0],
]
#difficult
# question = [
#     [4,0,0,5,0,0,0,0,6],
#     [0,0,0,0,0,0,0,2,0],
#     [1,0,9,0,0,7,0,5,0],
#     [0,0,0,7,0,0,0,0,0],
#     [0,4,0,0,0,0,0,0,0],
#     [7,0,6,0,0,3,1,0,8],
#     [0,0,0,2,0,0,0,0,5],
#     [0,8,0,0,9,0,7,0,0],
#     [0,0,3,0,8,0,0,0,4],
# ]

#input the question
# question = [
#     [4,0,0,5,0,0,0,0,6],
#     [0,0,0,0,0,0,0,2,0],
#     [1,0,9,0,0,7,0,5,0],
#     [0,0,0,7,0,0,0,0,0],
#     [0,4,0,0,0,0,0,0,0],
#     [7,0,6,0,0,3,1,0,8],
#     [0,0,0,2,0,0,0,0,5],
#     [0,8,0,0,9,0,7,0,0],
#     [0,0,3,0,8,0,0,0,4],
# ]

result = solver(question)
print_puzzle(result)
