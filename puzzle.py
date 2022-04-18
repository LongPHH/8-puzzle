from asyncore import write
from logging import raiseExceptions
import math
from copy import deepcopy

# find index of a number in current state
def find_pos(lst,num):
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            if lst[i][j] == num:
                return i,j


class Node:                             # for the state tree
    def __init__(self,data,level,f_score,curr_move=None, parent=None):
        self.data = data                # board content of each node. ex: [['0','1','2'],['3','4','5'],['6','7','8']]
        self.level = level              # current level of node in the state tree
        self.f_score = f_score          # calculated fscore
        self.move = curr_move           # how did the empty tile move (U,R,L,D) 
        self.parent = parent


class Puzzle:
    def __init__(self,file_name, h='man'):
        self.frontier = {}
        self.initial = []                   # inital state
        self.goal = []                      # goal state
        self.h = h                          # determines which heuristics
        self.reached = {}                   # dictionary containing reached state. key = state, value = node
        self.count = 0                      # total number of nodes
        self.move_lst = []                  # final move lst for output file
        self.f_scores = []                  # final f_scores for output file
        self.file_name = file_name


    
    def h1(self,start):                     # h-score for manhattan distance
        man_dist = 0
        for i in range(9):
            x1,y1 = find_pos(start,str(i))          # str
            x2,y2 = find_pos(self.goal, str(i))
            man_dist += abs(x1-x2) + abs(y1-y2)
        return man_dist


    def h2(self, start):                # h-score for nilsson Sequence
        goal_path = []                  # order of the border of goal state in clockwise direction
        for i in self.goal[0]:
            goal_path.append(i)
        for i in range(1, 3):
            goal_path.append(self.goal[i][2])
        goal_path.append(self.goal[2][1])
        goal_path.append(self.goal[2][0])
        goal_path.append(self.goal[1][0])

        current_path = []               # order of the border of current state in clockwise direction
        for i in start[0]:
            current_path.append(i)
        for i in range(1, 3):
            current_path.append(start[i][2])
        current_path.append(start[2][1])
        current_path.append(start[2][0])
        current_path.append(start[1][0])

        score = 0
        # iterating thru current path
        for i in range(len(current_path)):
            try:
                # is the next node in current path is not the same as the node in the goal path using that formula
                if current_path[i+1] != goal_path[(goal_path.index(current_path[i])+ 1) % len(goal_path)]:
                    score = score + 2
            except:
                pass
        
        if start[1][1] != self.goal[1][1]:      # if center node of initial and goal state not the same, add 1
            score = score + 1

        # manhattan distance
        p = self.h1(start)

        score = p + 3 * score

        return score

    def f_score(self,start, level):
        # heuristic function f(n) = h(n) + g(n)
        if self.h == 'man':
            return level + self.h1(start)
        elif self.h == 'nil':
            return level + self.h2(start)
        else:
            print("ERROR")


    def get_input(self):
        
        lines = []
        
        with open(self.file_name, 'r') as file:
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
        
        print(self.initial)
        print(self.goal)

    # to get the node with lowest fvalue in frontier. sorting not needed
    def find_min(self):
        min = float('INF')
        for i in self.frontier.keys():
            if self.frontier[i][0] < min:
                min = self.frontier[i][0]
                node = self.frontier[i][1]

        return node
        

    def generate_node(self, state,flag):            # generate child nodes from moving empty tiles in four directions
        children = []                   
        x,y = find_pos(state.data, '0')
        blank_coords = [((x,y-1), 'L'),((x,y+1), 'R'),((x-1,y), 'U'),((x+1,y), 'D')]        # possible moves for the blank tile. (U,D,L,R)
        for i in blank_coords:
            node = self.move_tile(state, x, y, i[0][0], i[0][1], i[1])
            if node == None:
                continue

            if str(node.data) in self.reached.keys():               # found repeated state, delete it.
                self.count = self.count + 1
                del node
                flag = True
                     
            elif str(node.data) == str(self.goal):                  # goal reached
                self.finish(node)
                flag = False
            
            else:                                                   # add to reached
                self.count = self.count + 1
                self.frontier[str(node.data)] = (node.f_score, node)
                flag = True
                
        self.reached[str(state.data)] = (state.f_score, state)

        del self.frontier[str(state.data)]
        return flag


    def move_tile(self,board,x1,y1,x2,y2, move):                                # move the empty tiles up down left or right
        # move the empty tile according to the direction from x-y coord
        if 0 <= x2 < len(board.data) and 0 <= y2 < len(board.data[0]):          # check if new coord is within border of board
            new = []
            new = deepcopy(board.data)                                          # copy current board to new
            new[x1][y1], new[x2][y2] = new[x2][y2], new[x1][y1]                 # move 0
            fscore = self.f_score(new, board.level + 1)                             

            return Node(new, board.level + 1, fscore, move, board)

        return None    

    # main solver method
    def solve(self):

        self.get_input()
        node = Node(self.initial, 0, self.f_score(self.initial, 0))             # initial state
        self.frontier[str(node.data)] = (node.f_score,node)

        flag = True
        
        while flag:
            flag = self.generate_node(self.find_min(),flag)
            
    

    # trace solution path to get move list and f-score, write to file
    def finish(self, node):                         
        temp_node = node
        # self.print(node)
        
        while temp_node != None:
            #self.print(temp_node)
            self.move_lst.append(temp_node.move)
            self.f_scores.append(temp_node.f_score)
            temp_node = temp_node.parent
       
        # print(self.move_lst)
        # print(self.f_scores)
        self.write_output(node.level)
        print("HERE")

    # function to write output file
    def write_output(self,goal_level):                   
        fname = input("Enter output file name: ")
        file = open(fname,'w')

        # initial goal
        for i in self.initial:
            for j in i:
                file.write("%s " % j)
            file.write("\n")
        file.write("\n")

        #print goal state
        for i in self.goal:
            for j in i:
                file.write("%s " % j)
            file.write("\n")
        file.write("\n")

        #print results
        file.write("%s\n" % goal_level)
        file.write("%s\n" % self.count)
        for i in range(len(self.move_lst) - 2, -1, -1):
            file.write("%s " % self.move_lst[i])
        file.write("\n")
        for i in self.f_scores:
            file.write("%s " % i)
        file.write("\n")

        


    def print(self, state):                     # for debugging 
        print("F Score", state.f_score)
        print(state.data[0])
        print(state.data[1])
        print(state.data[2])
        print()
        print('--------------------------')
        print()


def main():
    file_name = input("Enter File Name: ")

    puzzle1 = Puzzle(file_name ,'man')
    puzzle1.solve()

    print("DOENEEEE")

    # puzzle2 = Puzzle(file_name, "nil")
    # puzzle2.solve()


main()






