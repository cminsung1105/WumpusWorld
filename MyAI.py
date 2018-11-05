from Agent import Agent
from collections import defaultdict
import random


class MyAI (Agent):

    def __init__(self):
        #Dictionary of all the possible moves of every visited cell. 
        self.poss_moves = defaultdict(list)
        self.curr = (1,1)
        self.prev = (1,1)
        
        self.grab = False
        self.direction_change = False
        
        #list of all the previously visited cells.
        self.direction = 2             #left = 0, up = 1, right = 2, down = 3
        self.safe_moves = {(1,1)}       #include everytime there is a safe move.
        self.visited = [(1,1)]
        
        self.move = (0,0)
        self.direction_change = False
                
        #list of all the adjacent cells of a breeze cell.
        self.breeze_list = []
        #list of all the adjacent cells of a stench cell.
        self.stench_list = []
        #dictionary with the probability of every cell of containing a pit.
        self.pit = defaultdict(int)
        #dictionary with the probability of every cell of containing a wumpus.
        self.wumpus = defaultdict(int)
        
        #boolean to check if the agent backtracked
        self.back_track = False
        
        #boolean to check if there is a bump
        self.bump = False
        
        self.counter = 2
        self.go_back = False
        self.grab = False
        
        self.x = 7
        self.y = 7
        
    def getAction( self, stench, breeze, glitter, bump, scream ):
        if self.go_back == True:
            if self.curr == (1, 1):
                return Agent.Action.CLIMB
            self.move = self.visited[len(self.visited)-self.counter]

            new_direction = self.direction_decide(self.curr, self.move)
            if new_direction != self.direction:
                dirr = self.direction_changer(new_direction)
                if dirr == "right":
                    return Agent.Action.TURN_RIGHT
                elif dirr == "left":
                    return Agent.Action.TURN_LEFT
            else:
                self.prev = self.curr
                self.curr = self.move
                if (self.curr not in self.visited):
                    self.visited.append(self.curr)
                self.counter+=1
                return Agent.Action.FORWARD
        
        if glitter:
            self.go_back = True
            self.grab = True
            return Agent.Action.GRAB
        
        if self.grab == True:
            self.go_back = True
            self.move = self.visited[len(self.visitied)-self.counter]
             
            new_direction = self.direction_decide(self.curr, selfmove)
            if new_direction != self.direction:
                dirr = self.direction_changer(new_direction)
                if dirr == "right":
                    return Agent.Action.TURN_RIGHT
                elif dirr == "left":
                    return Agent.Action.TURN_LEFT
            else:
                self.prev = self.curr
                self.curr = self.move
                if (self.curr not in self.visited):
                    self.visited.append(self.curr)
                return Agent.Action.FORWARD  
        
        if bump:
            self.bump = True
            self.visited.pop(-1)
            self.safe_moves.remove(self.curr)
            
            if self.curr[0] >= self.curr[1]:
                self.x = self.curr[0]
            elif self.curr[1] >= self.curr[0]:
                self.y = self.curr[1]
            
            self.curr = self.visited[-1]
            self.prev = self.visited[-2]
                       
        if self.direction_change == False:   

            if self.back_track == False and self.bump == False:
                self.checkCurrent(breeze, stench)
                pmoves = self.nextMoves(self.curr, self.prev, self.safe_moves, self.stench_list, self.breeze_list)
                self.poss_moves[self.curr] = pmoves
                
                for m in pmoves:
                    self.safe_moves.add(m)
                                            
            is_empty = True
            for key in self.poss_moves.keys():
                if len(self.poss_moves[key]) != 0:
                    is_empty = False
                            
            if is_empty:
                self.go_back = True
                self.grab = True
                if self.direction != 3:
                    self.direction += 1
                elif self.direction == 3:
                    self.direction = 0
                return Agent.Action.TURN_RIGHT

            else:
                if self.poss_moves[self.curr] != []:
                    self.back_track = False
                    self.move = random.choice(self.poss_moves[self.curr])
                    self.poss_moves[self.curr].remove(self.move)
                else:
                    self.back_track = True
                    self.visited.pop(-1)
                    self.move = self.visited[-1]
                
        self.bump = False
                    
        new_direction = self.direction_decide(self.curr, self.move)
        if new_direction != self.direction:
            dirr = self.direction_changer(new_direction)
            if dirr == "right":
                self.direction_change = True
                return Agent.Action.TURN_RIGHT
            elif dirr == "left":
                self.direction_change = True
                return Agent.Action.TURN_LEFT
        else:
            self.prev = self.curr
            self.curr = self.move
            if self.curr != self.visited[-1]:
                self.visited.append(self.curr)
            self.safe_moves.add(self.curr)
            self.direction_change = False
            return Agent.Action.FORWARD
            
    def checkCurrent(self, breeze, stench):
        if breeze:
            self.breeze_list = self.adjacentCells()
            for breezy in self.breeze_list:
                if breezy not in self.safe_moves:
                    self.pit[breezy] += 1
            
        if stench:
            self.stench_list = self.adjacentCells()
            for stenchy in self.stench_list:
                if stenchy not in self.safe_moves:
                    self.wumpus[stenchy] += 1                    
                    
    def direction_decide(self, curr_coord, next_coord):
        if next_coord[0] > curr_coord[0]:
            newdirection = 2
        elif next_coord[0] < curr_coord[0]:
            newdirection = 0
        elif next_coord[1] > curr_coord[1]:
            newdirection = 1
        elif next_coord[1] < curr_coord[1]:
            newdirection = 3
        return newdirection
    
    def direction_changer(self, new_direction):
        if (self.direction < new_direction):        #turn right
            self.direction += 1
            return "right"
        elif (self.direction > new_direction):      #turn left
            self.direction -= 1
            return "left"
            
    def adjacentCells(self):
        moves = list()
        if (self.curr[0]-1) >= 1 and (self.curr[0]-1, self.curr[1]) != self.prev:
            moves.append((self.curr[0]-1, self.curr[1]))
        if (self.curr[1]-1) >= 1 and (self.curr[0], self.curr[1]-1) != self.prev:
            moves.append((self.curr[0], self.curr[1]-1))
        if (self.curr[0]+1 < self.x) and (self.curr[0]+1, self.curr[1]) != self.prev:
            moves.append((self.curr[0]+1, self.curr[1]))
        if (self.curr[1]+1 < self.y) and (self.curr[0], self.curr[1]+1) != self.prev:
            moves.append((self.curr[0], self.curr[1]+1))
        return moves
    
    def nextMoves(self, curr, prev, safe_moves, stench_list, breeze_list):
        next_moves = list()
        left = (curr[0]-1, curr[1])
        down = (curr[0], curr[1]-1)
        right = (curr[0]+1, curr[1])
        up = (curr[0], curr[1]+1)
        
        if (left[0]-1 >= 1) and (left != prev) and (left not in safe_moves) and (left not in stench_list) and (left not in breeze_list):
            next_moves.append(left)
        if (down[1]-1 >= 1) and (down != prev) and (down not in safe_moves) and (down not in stench_list) and (down not in breeze_list):
            next_moves.append(down)
        if (right[0]+1 < self.x) and (right != prev) and (right not in safe_moves) and (right not in stench_list) and (right not in breeze_list):
            next_moves.append(right)
        if (down[1]+1 < self.y) and (up != prev) and (up not in safe_moves) and (up not in stench_list) and (up not in breeze_list):
            next_moves.append(up)
        
        return next_moves

