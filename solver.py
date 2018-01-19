# puzzle[y][x] is the current square 

def nextsquare(y_start,x_start):
    #move across the row x by 1
    #start x over at 0 when we reach 8 and add 1 to y
    if x_start == 8:
        x = 0
        if y_start == 8:
            y = 0
        else:
            y = y_start + 1
    else:
        x = x_start + 1
        y = y_start
    return y,x


def done(puzzle):
    #check if there are no blank squares
    #check every square to see if it has a set
    for row in puzzle:
        for square in row:
            #if the square is a set, then we are not done
            if isinstance(square, set) or square == 0:
                return False
    #if we didn't find any blanks
    return True


def findpossible(puzzle,y,x):
    #we have to elimnate what is not possible
    #if there is a 1 in the row, then square is not one
    #if there is a two in the row, then square is not two
    #and so on... 
    #then check column 
    #then check section
    #start with the set of numbers 1 through 9
    possible = set([1,2,3,4,5,6,7,8,9])
    used = []
    #get all the used numbers in the row
    row = puzzle[y]
    #get all the used numbers in the column
    column = [puzzle[col][x] for col in range(9)]
    #get all the used numbers in the section
    #9 sections 
    if x<3 and y<3: 
        section = puzzle[0][0:3]+puzzle[1][0:3]+puzzle[2][0:3] 
    elif x>=3 and x<6 and y<3:
        section = puzzle[0][3:6]+puzzle[1][3:6]+puzzle[2][3:6] 
    elif x>=6 and x<9 and y<3:
        section = puzzle[0][6:9]+puzzle[1][6:9]+puzzle[2][6:9] 
    elif x<3 and y>=3 and y<6:
        section = puzzle[3][0:3]+puzzle[4][0:3]+puzzle[5][0:3]
    elif x>=3 and x<6 and y>=3 and y<6:
        section = puzzle[3][3:6]+puzzle[4][3:6]+puzzle[5][3:6] 
    elif x>=6 and x<9 and y>=3 and y<6:
        section = puzzle[3][6:9]+puzzle[4][6:9]+puzzle[5][6:9] 
    elif x<3 and y>=6 and y<9:
        section = puzzle[6][0:3]+puzzle[7][0:3]+puzzle[8][0:3]
    elif x>=3 and x<6 and y>=6 and y<9:
        section = puzzle[6][3:6]+puzzle[7][3:6]+puzzle[8][3:6] 
    elif x>=6 and x<9 and y>=6 and y<9:
        section = puzzle[6][6:9]+puzzle[7][6:9]+puzzle[8][6:9] 

    #loop through all the squares
    for i in range(9):
        #if the square is not zero and not a set, add to used numbers
        if not row[i] == 0 and not isinstance(row[i], set):
            #add it to list of used numbers
            used.append(row[i])
        if not column[i] == 0 and not isinstance(column[i],set):
            #add it to list of used numbers
            used.append(column[i])
        if not section[i] == 0 and not isinstance(section[i],set):
            #add it to list of used numbers\
            used.append(section[i])
    
    #combine all the used numbers into a set
    #set removes duplicates
    used = set(used)

    #remove the used numbers from possible numbers 
    possible = possible - used

    return possible 


def solver(puzzle):
    #we must  fill in the blank squares 
    #that are represented by zeros
    #set starting values:
    complete = False
    progress = True
    loop = 0
    max_loop = 10000
    y = 0
    x = 0

    #repeat until no blanks are left or no progress
    while progress or not complete:
        
        # check if current square is blank
        if puzzle[y][x] == 0 or isinstance(puzzle[y][x], set):
        
            #we have to eliminate what is not possible
            possible = findpossible(puzzle,y,x)
            
            progress = False
            #if only one number is left then square=that number   
            if len (possible) == 1:
                puzzle[y][x] = possible.pop()
                progress = True
            # if there are no possiblities then you went wrong 
            elif len (possible) == 0:
                print('No possiblities!')
                return False
            else:
                #save the set inside the puzzle
                puzzle [y][x] = possible

        #check if we're done
        if done(puzzle):
            print('Done!')
            break 

        #move to next square
        y,x = nextsquare(y, x)

        #add one to loop counter
        loop += 1
        if loop >= max_loop:
            print('Maximum loops done!')
            break
      
    #print that as answer
    return puzzle


question = [
    [0,0,0,2,6,0,7,0,1],
    [6,8,0,0,7,0,0,9,0],
    [1,9,0,0,0,4,5,0,0],
    [8,2,0,1,0,0,0,4,0],
    [0,0,4,6,0,2,9,0,0],
    [0,5,0,0,0,3,0,2,8],
    [0,0,9,3,0,0,0,7,4],
    [0,4,0,0,5,0,0,3,6],
    [7,0,3,0,1,8,0,0,0],
]
answer = [
    [4,3,5,2,6,9,7,8,1],
    [6,8,2,5,7,1,4,9,3],
    [1,9,7,8,3,4,5,6,2],
    [8,2,6,1,9,5,3,4,7],
    [3,7,4,6,8,2,9,1,5],
    [9,5,1,7,4,3,6,2,8],
    [5,1,9,3,2,6,8,7,4],
    [2,4,8,9,5,7,1,3,6],
    [7,6,3,4,1,8,2,5,9],
]
# start of the program
result = solver(question)
#if result matches answer then print correct else print incorrect
if result == answer:
    print('Correct answer!')
else:
    print('Incorrect answer!')

#print the result
for row in result:
    print(row)
