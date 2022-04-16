import math
from copy import deepcopy

# find index of a number in current state
def find_pos(lst,num):
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            if lst[i][j] == num:
                return i,j


class Node:                     # for the state tree
    def __init__(self,data,level,f_score,curr_move):
        self.data = data                # board content of each node. ex: [['0','1','2'],['3','4','5'],['6','7','8']]
        self.level = level              # current level of node in the state tree
        self.f_score = f_score          # calculated fscore
        self.move = curr_move           # how did the empty tile move (U,R,L,D) 


    def generate_node(self):            # generate child node from moving empty tiles in four directions
        children = []                   
        x,y = find_pos(self.data, '0')
        blank_coords = [(x,y-1),(x,y+1),(x-1,y),(x+1,y)]        # possible moves for the blank tile. (U,D,L,R)

        pass

    def move_tile(self):                # move the empty tiles up down left or right
        pass

    def copy(self):
        pass


class Puzzle:
    def __init__(self, size):
        self.size = size                    # number of rows in the puzzle
        self.frontier = []
        self.initial = []
        self.goal = []
        self.reached = {}           # dictionary containing reached state. key = state, value = node


    
    def h1(self,start):     # h-score for manhattan distance
        man_dist = 0
        for i in range(9):
            x1,y1 = find_pos(start,str(i))          # str
            x2,y2 = find_pos(self.goal, str(i))
            man_dist += abs(x1-x2) + abs(y1-y2)
        return man_dist

    def h2(self, start):               # h-score for nilsson Sequence
        goal_path = []
        for i in self.goal[0]:
            goal_path.append(i)
        for i in range(1, 3):
            goal_path.append(self.goal[i][2])
        goal_path.append(self.goal[2][1])
        goal_path.append(self.goal[2][0])
        goal_path.append(self.goal[1][0])

        current_path = []
        for i in start[0]:
            current_path.append(i)
        for i in range(1, 3):
            current_path.append(start[i][2])
        current_path.append(start[2][1])
        current_path.append(start[2][0])
        current_path.append(start[1][0])

        score = 0
        for i in range(len(current_path)):
            try:
                if current_path[i+1] != goal_path[(goal_path.index(current_path[i])+ 1) % len(goal_path)]:
                    score = score + 2
            except:
                pass
        
        if start[1][1] != self.goal[1][1]:
            score = score + 1

        p = self.h1(start)

        score = p + 3 * score

        return score

    def f_score(self,start):
        # heuristic function f(n) = h(n) + g(n)
        pass


    def get_input(self):
        #fname = input("Enter file name: ")
        #print(fname)
        lines = []
        
        with open("Sample_Input.txt", 'r') as file:
            lines = file.readlines()
        file.close()

        line_num = 0
        for line in lines:
            curr_line = line.strip().split(" ")

            if line_num <=2:
                self.initial.append(curr_line)
            elif 4 <= line_num <=7:
                self.goal.append(curr_line)

            line_num += 1

        # print(self.initial)
        # print(self.goal)

    







def main():
    puzzle = Puzzle(3)
    puzzle.get_input()
    print("H1 score: ", puzzle.h1(puzzle.initial))
    print("H2 score: ", puzzle.h2(puzzle.initial))


main()


