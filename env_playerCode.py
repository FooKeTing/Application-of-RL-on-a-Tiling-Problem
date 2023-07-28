from gym import Env
from gym import spaces
import random
import numpy as np

# global constant
# game board values
NOTHING = 0
MARKED_POINT = 1
PLAYER = 2
WALL = 3
# action values
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
UP_LEFT = 4
UP_RIGHT = 5
DOWN_LEFT = 6
DOWN_RIGHT = 7
# orientation values
HORIZONTAL = 1
VERTICAL = 2
DIAGONAL_LEFT = 3
DIAGONAL_RIGHT = 4

# user defined values
# penalty value when player out of boundary
PENALTY = 5
# the number of player
NUM_PLAYER = 2
# the number of row and column of grid
BOARD_ROWS = 4
BOARD_COLS = 4
# the value of player orientation
PLAYER_ORIENTATION = 1

class playernum():
    def __init__(self):
        # get the grid size from user
        self.boardRows = BOARD_ROWS
        self.boardCols = BOARD_COLS
            
        # get the number of point that user would like to use
        self.promptNum = NUM_PLAYER
        
        # set a 2D dynamic array 
        self.game = [[NOTHING for j in range(self.boardCols)] for i in range(self.boardRows)]

        self.drawWall()

        # convert the list into a numpy array 
        self.state = np.array(self.game, dtype=np.int16).reshape(-1)

        # calculate the element in array (included the wall)
        self.elementNum = len(self.state)
        
        self.show_menuOrientation()

    def show_menuOrientation(self):
        choice = PLAYER_ORIENTATION
        # generate the selected player's orientation that user select
        # generate a horizontal orientation
        if choice == HORIZONTAL:
            # check the number of prompt is same as boardCols
            # if yes, the player position will be on second column randomly
            # if no, the player position will be within the grid randomly
            if self.promptNum == self.boardCols:
                secondCols_num = [] 
                # calculate the element number for the second column of grid
                for num in range(self.newCols * self.newRows):
                    if num > self.newCols and num < ((self.newCols - 1 ) * self.newCols) and (num % self.newCols) == 1:
                        secondCols_num.append(num)
                # select the position within the second column randomly
                self.player_position = random.choice(secondCols_num)
            else:
                # assign first point to a position randomly 
                self.player_position = random.randrange(0,self.elementNum)

                # make sure the first player point do not overlap with the wall
                while self.state[self.player_position] == WALL:
                    self.player_position = random.randrange(0,self.elementNum)
            # append the player position value as 2 at the self.state list
            self.state[self.player_position] = PLAYER

            # find the position value of the first point
            self.player_position = next(i for i, x in enumerate(self.state) if x == PLAYER)

            # assign the value of player position into list
            self.player_positionList = []
            self.player_positionList.append(self.player_position)

            for i in range(1, self.promptNum): 
                # assign next point to the right of the first point
                if self.player_position not in self.get_lastNCols():
                    self.player_position_i = self.player_position + i 
                # assign next point to the left of the first point
                else:
                    self.player_position_i = self.player_position - i

                # append the list to store all player position
                self.player_positionList.append(self.player_position_i)
                self.state[self.player_position_i] = PLAYER
            print('List of player position:', self.player_positionList)

        # generate a vertical orientation
        elif choice == VERTICAL:
            # check the number of prompt is same as boardCols
            # if yes, the player position will be on second row randomly
            # if no, the player position will be within the grid randomly
            if self.promptNum == self.boardCols:
                secondRows_num = [] 
                # calculate the element number for the second row of grid
                for num in range(self.newCols * self.newRows):
                    if num > self.newCols and num < (self.newCols - 1 + self.newCols): 
                        secondRows_num.append(num)
                # select the position within the second row randomly
                self.player_position = random.choice(secondRows_num)
            else:
                # assign first point to a position randomly 
                self.player_position = random.randrange(0,self.elementNum)

                # make sure the first player point do not overlap with the wall
                while self.state[self.player_position] == WALL:
                    self.player_position = random.randrange(0,self.elementNum)
            # append the player position value as 2 at the self.state list
            self.state[self.player_position] = PLAYER

            # find the position of the first point
            self.player_position = next(i for i, x in enumerate(self.state) if x == PLAYER)

            # assign the value of player position into list
            self.player_positionList = []
            self.player_positionList.append(self.player_position)

            for i in range(1, self.promptNum):
                # assign next point to the right of the first point
                if self.player_position not in self.get_lastNRows():
                    self.player_position_i = self.player_position + (self.newCols * i)
                # assign next point to the left of the first point
                else:
                    self.player_position_i = self.player_position - (self.newCols * i)

                # append the list to store all player position
                self.player_positionList.append(self.player_position_i)
                self.state[self.player_position_i] = PLAYER
            print('List of player position:', self.player_positionList)

        # generate a diagonal left orientation
        elif choice == DIAGONAL_LEFT:
            # get two slice of first_NCols and last_NCols list from the get_firstLastNCols() function 
            # combine two sliced list into one list
            excluded_Num = (self.get_firstLastNCols()[1])[(self.promptNum - 1):((self.promptNum - 1) * self.promptNum)] + (self.get_firstLastNCols()[0])[-((self.promptNum - 1) * self.promptNum):-(self.promptNum - 1)]
            # sort the element in ascending order
            excluded_Num = sorted(excluded_Num)
            print('not use element:',excluded_Num)

            # assign first point to a position randomly 
            self.player_position = random.randrange(0,self.elementNum)
            # make sure the first player point do not overlap with the wall
            while self.state[self.player_position] == WALL or self.player_position in excluded_Num:
                self.player_position = random.randrange(0,self.elementNum)
            # append the player position value as 2 at the self.state list
            self.state[self.player_position] = PLAYER

            # find the position of the first point
            self.player_position = next(i for i, x in enumerate(self.state) if x == PLAYER)

            last_NRows = []
            # find the number of position that next player can be placed with non default position formula
            for num in range(self.newCols * self.newRows):
                if num > (self.newCols - 2) * self.newCols and num < (self.newCols - 1) * self.newCols and (num % self.newCols) != (self.newCols - 1) and (num % self.newCols) != 0 and num not in excluded_Num:
                    last_NRows.append(num)

            # get a slice of last_NCols from the get_firstLastNCols() function 
            # combine the sliced list with the lastNRows()
            position_Num = (self.get_firstLastNCols()[1])[((self.promptNum - 1) * self.promptNum):-(self.promptNum - 1)] + last_NRows
            # remove duplicated element value
            # sort the element in ascending order
            position_Num = sorted(set(position_Num))
            print('non default', position_Num)

            # assign the value of player position into list
            self.player_positionList = []
            self.player_positionList.append(self.player_position)

            for i in range(1, self.promptNum):
                if self.player_position not in position_Num:
                    # assign second point to the right down of the first point 
                    self.player_position_i = self.player_position + (self.newCols + 1 ) * i 
                else:
                    self.player_position_i = self.player_position - (self.newCols + 1 ) * i  

                # append the list to store all player position
                self.player_positionList.append(self.player_position_i)
                self.state[self.player_position_i] = PLAYER
            print('List of player position:', self.player_positionList)

        # generate a diagonal left orientation
        elif choice == DIAGONAL_RIGHT:
            # get slice of last_NCols and first_NCols list from the get_firstLastNCols() function 
            # combine two sliced list into one list 
            excluded_Num = (self.get_firstLastNCols()[0])[(self.promptNum - 1):((self.promptNum - 1) * self.promptNum)] + (self.get_firstLastNCols()[1])[-((self.promptNum - 1) * self.promptNum):-(self.promptNum - 1)]
            # sort the element in ascending order
            excluded_Num = sorted(excluded_Num)
            print('not use element:',excluded_Num)

            # assign first point to a position randomly 
            self.player_position = random.randrange(0,self.elementNum)
            # make sure the first player point do not overlap with the wall
            while self.state[self.player_position] == WALL or self.player_position in excluded_Num:
                self.player_position = random.randrange(0,self.elementNum)
            # append the player position value as 2 at the self.state list
            self.state[self.player_position] = PLAYER

            # find the position of the first point
            self.player_position = next(i for i, x in enumerate(self.state) if x == PLAYER)

            first_NRows = []
            # find the number of position that next player can be placed with non default position formula
            for num in range(self.newCols * self.newRows):
                if num > self.newCols and num < self.promptNum * self.newCols and (num % self.newCols) != (self.newCols - 1) and (num % self.newCols) != 0 and num not in excluded_Num:
                    first_NRows.append(num)

            # get a slice of last_NCols from the get_firstLastNCols() function 
            # combine the sliced list with the lastNRows()
            position_Num = (self.get_firstLastNCols()[1])[(self.promptNum - 1): -((self.promptNum - 1) * self.promptNum)] + first_NRows
            # remove duplicated element value 
            # sort the element in ascending order
            position_Num = sorted(set(position_Num))
            print('non default', position_Num)

            # assign the value of player position into list
            self.player_positionList = []
            self.player_positionList.append(self.player_position)

            for i in range(1, self.promptNum):
                if self.player_position not in position_Num:
                    # assign second point to the right down of the first point 
                    self.player_position_i = self.player_position - (self.newCols * i) + i
                else:
                    self.player_position_i = self.player_position + (self.newCols* i) - i 

                # append the list to store all player position
                self.player_positionList.append(self.player_position_i)
                self.state[self.player_position_i] = PLAYER
            print('List of player position:', self.player_positionList)
        
    def drawWall(self):
        # add WALL to the first column and last column of the grid
        for row in self.game:
            row.insert(0,WALL)
        for row in self.game:
            row.append(WALL)
        
        # add 2 column and row to boardCols and boardRows respectively
        self.newCols = self.boardCols + 2
        self.newRows = self.boardRows + 2
        
        # create 1D array of WALL
        self.wall = [WALL for i in range(self.newCols)]
        
        # add WALL in the fist row and last row of the grid
        self.game.insert(0,self.wall)
        self.game.append(self.wall)
        
    def get_lastNCols(self):
        # get the number that the next player position will definitelly overlap with the WALL 
        # no matter with default or non-default formula
        startCols = self.newCols - self.promptNum
        excludedNums = []
        for row in range(self.newRows):
            for column in range(startCols, self.newCols):
                excludedNum = (row * self.newCols) + column
                excludedNums.append(excludedNum)
        return excludedNums
    
    def get_lastNRows(self):
        # get the number that the next player position will definitelly overlap with the WALL 
        # no matter with default or non-default formula
        startRows = self.newCols - self.promptNum 
        excluded_positionNum = []
        for num in range(self.newRows * self.newCols):
            if num >= (startRows * self.newCols) and num < self.elementNum:
                excluded_positionNum.append(num)
        return excluded_positionNum
    
    def get_firstLastNCols(self):
        # get the number that the next player position will definitelly overlap with the WALL 
        # no matter with default or non-default formula
        last_NCols = []
        first_NCols = []
        for num in range((self.newCols) * (self.newRows)):
            for i in range(1, self.promptNum + 1):
                if (num % self.newCols) == (self.newCols - i) and (num % self.newCols) != (self.newCols - 1):
                    last_NCols.append(num)
                if (num % self.newCols) != 0 and (num % self.newCols) == (i-1):
                    first_NCols.append(num)
        return first_NCols, last_NCols

class squarestate(playernum, Env):
    def __init__(self):
        super().__init__()
        self.cumulative_reward = 0
        self.boundary_number = 0
        
        # reshape the numpy array to 2D
        self.board = self.state.reshape(self.newRows,self.newCols)
        
        # observation space (valid ranges for observations in the state)
        self.observation_space = spaces.Box(np.zeros(self.elementNum), np.ones(self.elementNum) * 3, dtype=np.int16)
        
        # valid actions:
        #   0 = up
        #   1 = down
        #   2 = left
        #   3 = right
        #   4 = up_left
        #   5 = up_right
        #   6 = down_left
        #   7 = down_right
        self.action_space = spaces.Discrete(8)
        
    def render(self):
        # visualize the board
        # dictionary to map board values to tokens
        token_dict ={
            NOTHING:'  0  ',
            PLAYER:'  A  ',
            MARKED_POINT:'  X  ',
            WALL:'\033[44m     \033[0m'
            }

        print(f'Cumulative Reward: {self.cumulative_reward}')
        print(f'Cumulative Number for Out-of-Bounday: {self.boundary_number}')
        print()
        for i in range(0,self.newRows):
            print('+-----'*(self.newCols) + "+")
            out = '|'
            for j in range(0,self.newCols):
                token = token_dict[self.board[i,j]]
                out += token +'|'
            print(out)
        print('+-----'*(self.newCols) + "+")

    def step(self,action):
        # set default values for done, reward, outofBoundary, and outBoundNum before the action is taken
        done = False
        reward = 1
        outofBoundary = False
        outBoundNum = 1
        
        self.player_positionListCopy = []
        # assign previous player position to a new list named player_positionListCopy
        for x in self.player_positionList:
            self.player_positionListCopy.append(x)
        print('Here is previous position:', self.player_positionListCopy)
            
        self.newPlayer_positionList = []
        if action == UP:
            for curr_position in self.player_positionList:
                # calculate new player position
                new_position = curr_position - self.newCols
                
                # assign into a list named newPlayer_positionList
                self.newPlayer_positionList.append(new_position)
                # replace the player_positionList to newPlayer_positionList
                self.player_positionList = self.newPlayer_positionList
                
            # check overlap between the player and the coated grid
            # lose game when overlapping occurred
            # give penalty when the player is out of boundary
            if all(element >= 0 for element in self.player_positionList): 
                if any(self.state[element] == PLAYER for element in self.player_positionList):
                    print('Up, overlap with players')
                    done = True
                elif any(self.state[element] == MARKED_POINT for element in self.player_positionList):
                    print('Up, overlap with marked points')
                    done =True
                elif any(element < self.newCols for element in self.player_positionList):
                    if all(self.state[element] == WALL for element in self.player_positionList):
                        # give more penalty since more players are out of boundary
                        reward = -(self.promptNum * PENALTY)
                        outofBoundary = True  
                        print('ATTENTION! The players have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                    else:
                        reward = -PENALTY
                        outofBoundary = True  
                        print('ATTENTION! A player have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                else: 
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
            else:
                # player moved out of the board boundaries again
                # player maintain in the same position
                # give more penalty since the player out of boundary again
                reward = -(self.promptNum * PENALTY)
                outofBoundary = True  
                print('Again! Cannot move up anymore!') 
                self.player_positionList = self.player_positionListCopy
                
        elif action == DOWN:
            for curr_position in self.player_positionList:
                # calculate new player position
                new_position = curr_position + self.newCols
                
                # assign into a list named newPlayer_positionList
                self.newPlayer_positionList.append(new_position)
                # replace the player_positionList to newPlayer_positionList
                self.player_positionList = self.newPlayer_positionList
                
            # check overlap between the player and the coated grid
            # lose game when overlapping occurred
            # give penalty when the player is out of boundary
            if all(element <self.elementNum for element in self.player_positionList):
                if any(self.state[element] == PLAYER for element in self.player_positionList):
                    print('Down, overlap with players')
                    done = True
                elif any(self.state[element] == MARKED_POINT for element in self.player_positionList):
                    print('Down, overlap with marked points')
                    done =True
                elif any(element >(self.elementNum - self.newCols) for element in self.player_positionList):
                    if all(self.state[element] == WALL for element in self.player_positionList):
                        # give more penalty since more players are out of boundary
                        reward = -(self.promptNum * PENALTY)
                        outofBoundary = True  
                        print('ATTENTION! The players have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                    else:
                        reward = -PENALTY
                        outofBoundary = True  
                        print('ATTENTION! A player have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                else:
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
            else:
                # player moved out of the board boundaries again
                # player maintain in the same position
                # give more penalty since the player out of boundary again
                reward = -(self.promptNum * PENALTY)
                outofBoundary = True  
                print('Again! Cannot move down anymore! ') 
                self.player_positionList = self.player_positionListCopy
                
        elif action == LEFT:
            for curr_position in self.player_positionList:
                # calculate new player position
                new_position = curr_position - 1
                
                # assign into a list named newPlayer_positionList
                self.newPlayer_positionList.append(new_position)
                # replace the player_positionList to newPlayer_positionList
                self.player_positionList = self.newPlayer_positionList
                
            # check overlap between the player and the coated grid
            # lose game when overlapping occurred
            # give penalty when the player is out of boundary
            if all(element in self.positionNum()[1] for element in self.player_positionListCopy):
                if any(self.state[element] == PLAYER for element in self.player_positionList):
                    print('Left, overlap with players')
                    done = True
                elif any(self.state[element] == MARKED_POINT for element in self.player_positionList):
                    print('Left, overlap with marked points')
                    done =True
                elif all(self.state[element] == WALL for element in self.player_positionList): 
                    # give more penalty since more players are out of boundary
                    reward = -(self.promptNum * PENALTY)
                    outofBoundary = True  
                    print('ATTENTION! The players have moved into the wall!')
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
                elif any(self.state[element] == WALL for element in self.player_positionList):
                    reward = -PENALTY
                    outofBoundary = True  
                    print('ATTENTION! A player have moved into the wall!')
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
                else:
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
            else: 
                # player moved out of the board boundaries again
                # player maintain in the same position
                # give more penalty since the player out of boundary again
                reward = -(self.promptNum * PENALTY)
                outofBoundary = True  
                print('Again! Cannot move left anymore! ') 
                self.player_positionList = self.player_positionListCopy
                
        elif action == RIGHT:
            for curr_position in self.player_positionList:
                # calculate new player position
                new_position = curr_position + 1
                
                # assign into a list named newPlayer_positionList
                self.newPlayer_positionList.append(new_position)
                # replace the player_positionList to newPlayer_positionList
                self.player_positionList = self.newPlayer_positionList
                
            # check overlap between the player and the coated grid
            # lose game when overlapping occurred
            # give penalty when the player is out of boundary
            if all(element in self.positionNum()[3] for element in self.player_positionListCopy):
                if any(self.state[element] == PLAYER for element in self.player_positionList):
                    print('Right, overlap with players')
                    done = True
                elif any(self.state[element] == MARKED_POINT for element in self.player_positionList):
                    print('Right, overlap with marked points')
                    done =True
                elif all(self.state[element] == WALL for element in self.player_positionList):  
                    # give more penalty since more players are out of boundary
                    reward = -(self.promptNum * PENALTY)
                    outofBoundary = True  
                    print('ATTENTION! The players have moved into the wall!')
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
                elif any(self.state[element] == WALL for element in self.player_positionList):
                    reward = -PENALTY
                    outofBoundary = True  
                    print('ATTENTION! A player have moved into the wall!')
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
                else:
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
            else: 
                # player moved out of the board boundaries again
                # player maintain in the same position
                # give more penalty since the player out of boundary again
                reward = -(self.promptNum * PENALTY)
                outofBoundary = True  
                print('Again! Cannot move right anymore! ') 
                self.player_positionList = self.player_positionListCopy
                
        elif action == UP_LEFT:
            for curr_position in self.player_positionList:
                # calculate new player position
                new_position = curr_position - (self.newCols + 1)
                
                # assign into a list named newPlayer_positionList
                self.newPlayer_positionList.append(new_position)
                # replace the player_positionList to newPlayer_positionList
                self.player_positionList = self.newPlayer_positionList
                
            # check overlap between the player and the coated grid
            # lose game when overlapping occurred
            # give penalty when the player is out of boundary
            if all(element >= 0 for element in self.player_positionList) and all(element in self.positionNum()[1] for element in self.player_positionListCopy): 
                if any(self.state[element] == PLAYER for element in self.player_positionList):
                    print('Up left, overlap with players')
                    done = True
                elif any(self.state[element] == MARKED_POINT for element in self.player_positionList):
                    print('Up left, overlap with marked points')
                    done =True
                elif any(element < self.newCols for element in self.player_positionList) or any(element in self.positionNum()[0] for element in self.player_positionList):
                    if all(self.state[element] == WALL for element in self.player_positionList):
                        # give more penalty since more players are out of boundary
                        reward = -(self.promptNum * PENALTY)
                        outofBoundary = True  
                        print('ATTENTION! The players have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                    else:
                        reward = -PENALTY
                        outofBoundary = True  
                        print('ATTENTION! A player have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                else:
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
            else:
                # player moved out of the board boundaries again
                # player maintain in the same position
                # give more penalty since the player out of boundary again
                reward = -(self.promptNum * PENALTY)
                outofBoundary = True  
                print('Again! Cannot move up left anymore! ') 
                self.player_positionList = self.player_positionListCopy
                
        elif action == UP_RIGHT:
            for curr_position in self.player_positionList:
                # calculate new player position
                new_position = curr_position - (self.newCols - 1)
                
                # assign into a list named newPlayer_positionList
                self.newPlayer_positionList.append(new_position)
                # replace the player_positionList to newPlayer_positionList
                self.player_positionList = self.newPlayer_positionList
                
            # check overlap between the player and the coated grid
            # lose game when overlapping occurred
            # give penalty when the player is out of boundary
            if all(element >= 0 for element in self.player_positionList) and all(element in self.positionNum()[3] for element in self.player_positionListCopy): 
                if any(self.state[element] == PLAYER for element in self.player_positionList):
                    print('Up right, overlap with players')
                    done = True
                elif any(self.state[element] == MARKED_POINT for element in self.player_positionList):
                    print('Up right, overlap with marked points')
                    done =True
                elif any(element < self.newCols for element in self.player_positionList) or any(element in self.positionNum()[2] for element in self.player_positionList):
                    if all(self.state[element] == WALL for element in self.player_positionList):
                        # give more penalty since more players are out of boundary
                        reward = -(self.promptNum * PENALTY)
                        outofBoundary = True  
                        print('ATTENTION! The players have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                    else:
                        reward = -PENALTY
                        outofBoundary = True  
                        print('ATTENTION! A player have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                else:
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
            else:
                # player moved out of the board boundaries again
                # player maintain in the same position
                # give more penalty since the player out of boundary again
                reward = -(self.promptNum * PENALTY)
                outofBoundary = True  
                print('Again! Cannot move up right anymore! ') 
                self.player_positionList = self.player_positionListCopy
                
        elif action == DOWN_LEFT:
            for curr_position in self.player_positionList :
                # calculate new player position
                new_position = curr_position + (self.newCols - 1)
                
                # assign into a list named newPlayer_positionList
                self.newPlayer_positionList.append(new_position)
                # replace the player_positionList to newPlayer_positionList
                self.player_positionList = self.newPlayer_positionList
                
            # check overlap between the player and the coated grid
            # lose game when overlapping occurred
            # give penalty when the player is out of boundary
            if all(element <self.elementNum for element in self.player_positionList) and all(element in self.positionNum()[1] for element in self.player_positionListCopy):
                if any(self.state[element] == PLAYER for element in self.player_positionList):
                    print('Down left, overlap with players')
                    done = True
                elif any(self.state[element] == MARKED_POINT for element in self.player_positionList):
                    print('Down left, overlap with marked points')
                    done =True
                elif any(element >(self.elementNum - self.newCols) for element in self.player_positionList) or any(element in self.positionNum()[0] for element in self.player_positionList):
                    if all(self.state[element] == WALL for element in self.player_positionList):
                        # give more penalty since more players are out of boundary
                        reward = -(self.promptNum * PENALTY)
                        outofBoundary = True  
                        print('ATTENTION! The players have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                    else:
                        reward = -PENALTY
                        outofBoundary = True  
                        print('ATTENTION! A player have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                else:
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
            else:
                # player moved out of the board boundaries again
                # player maintain in the same position
                # give more penalty since the player out of boundary again
                reward = -(self.promptNum * PENALTY)
                outofBoundary = True  
                print('Again! Cannot move down left anymore!') 
                self.player_positionList = self.player_positionListCopy
                
        elif action == DOWN_RIGHT:
            for curr_position in self.player_positionList:
                # calculate new player position
                new_position = curr_position + (self.newCols + 1)
                
                # assign into a list named newPlayer_positionList
                self.newPlayer_positionList.append(new_position)
                # replace the player_positionList to newPlayer_positionList
                self.player_positionList = self.newPlayer_positionList
                
            # check overlap between the player and the coated grid
            # lose game when overlapping occurred
            # give penalty when the player is out of boundary
            if all(element <self.elementNum for element in self.player_positionList) and all(element in self.positionNum()[3] for element in self.player_positionListCopy):
                if any(self.state[element] == PLAYER for element in self.player_positionList):
                    print('Down right, overlap with players')
                    done = True
                elif any(self.state[element] == MARKED_POINT for element in self.player_positionList):
                    print('Down right, overlap with marked points')
                    done =True
                elif any(element >(self.elementNum - self.newCols) for element in self.player_positionList) or any(element in self.positionNum()[2] for element in self.player_positionList):
                    if all(self.state[element] == WALL for element in self.player_positionList):
                        # give more penalty since more players are out of boundary
                        reward = -(self.promptNum * PENALTY)
                        outofBoundary = True  
                        print('ATTENTION! The players have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                    else:
                        reward = -PENALTY
                        outofBoundary = True  
                        print('ATTENTION! A player have moved into the wall!')
                        # update the player position
                        for pos in self.player_positionListCopy:
                            self.state[pos] = MARKED_POINT
                        for currentPos in self.newPlayer_positionList:
                            self.state[currentPos] = PLAYER
                else:
                    # update the player position
                    for pos in self.player_positionListCopy:
                        self.state[pos] = MARKED_POINT
                    for currentPos in self.newPlayer_positionList:
                        self.state[currentPos] = PLAYER
            else:
                # player moved out of the board boundaries again
                # player maintain in the same position
                # give more penalty since the player out of boundary again
                reward = -(self.promptNum * PENALTY)
                outofBoundary = True  
                print('Again! Cannot move down right anymore!') 
                self.player_positionList = self.player_positionListCopy
                
        print('New player position', self.player_positionList)

        # continue the game when position is available
        if not done and not outofBoundary :
            self.render()
            self.cumulative_reward += reward

        # calculate the number of time that player out of boundary
        elif outofBoundary == True:
            self.render()
            self.boundary_number += outBoundNum      
            self.cumulative_reward += reward
            # end game when the player reached maximum number of out of boundary
            if self.boundary_number == (self.promptNum * self.boardCols):
                self.render()
                done = True
                print('LOSE! Reached maximum number of out-of-boundary!')

        # win the game if no available position
        if len(self.availablePosition())== 0:
            reward = self.boardRows * self.boardCols * self.promptNum
            self.render()
            self.cumulative_reward += reward
            done = True
            # show the message of congratulations message
            print('Win!!')
            print(f'Cumulative Reward: {self.cumulative_reward}')
            
        # lose the game if overlapping occur
        elif done == True:
            reward = -(self.boardRows * self.boardCols * self.promptNum)
            self.render()
            self.cumulative_reward += reward
            # calculate the number of zero in the numpy array
            unmarkedPoint = np.count_nonzero(self.state==0)
            # calculate the percentage of unfilled grid
            self.unmarkedPoint_Percentage = ( unmarkedPoint / (self.boardCols * self.boardRows))*100
            # show the message of percentage of unfilled grid
            print('There are',self.unmarkedPoint_Percentage, '% unfilled grid!')
            print(f'Cumulative Reward: {self.cumulative_reward}')

        # placeholder of cumulative reward, cumulative number that player out of boundary and current state for debugging information during training
        info = {'cumulative_reward': self.cumulative_reward, 'number_outBoundary':self.boundary_number, 'next_state': self.state, 'done': done}
         
        return self.state, reward, done, info
    
    def positionNum(self):
        # find the number of position for the 2nd last column
        # to avoid the player position overlap with the WALL
        self.firstCols = []
        self.remainingfirstCols = []
        self.lastCols = []
        self.remaininglastCols = []
        for num in range ((self.newCols) * (self.newRows)):
            if (num % self.newCols) == 0:
                self.firstCols.append(num)
            else:
                self.remainingfirstCols.append(num)
        for num in range ((self.newCols) * (self.newRows)):
            if (num % self.newCols) == self.boardCols + 1 :
                self.lastCols.append(num)
            else:
                self.remaininglastCols.append(num)
        return self.firstCols, self.remainingfirstCols, self.lastCols, self.remaininglastCols
        
    def availablePosition(self):
        # scan any available position
        position =[]
        for i in range(0, self.elementNum):
                if self.state[i] == 0:
                    position.append(i)
        return position
    
    def reset(self):
        playernum.__init__(self)
        self.cumulative_reward = 0
        self.boundary_number = 0
        
        # reshape the numpy array to 2D
        self.board = self.state.reshape(self.newRows,self.newCols)
        
        return self.state
