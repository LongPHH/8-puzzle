import math

# find index of a number in current state
def find_pos(lst,num):
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            if lst[i][j] == num:
                return i,j
class Node:
    pass

class Puzzle:
    def __init__(self, size):
        self.size = size
        self.frontier = []
        self.initial = []
        self.goal = []
        self.reached = {}           # dictionary containing reached state. key = state, value = node

    def h_score(self,start,goal):
        # h-score
        man_dist = 0
        for i in range(9):
            x1,y1 = find_pos(start,str(i))          # str
            x2,y2 = find_pos(goal, str(i))

            man_dist += abs(x1-x2) + abs(y1-y2)
        return man_dist

    def f_score(self,start,goal):
        # heuristic function f(n) = h(n) + g(n)
        pass


    def get_input(self):
        name = input("Enter file name: ")
        lines = []
        with open(name) as file:
            lines = file.readlines()
        file.close()

        line_num = 0
        for line in lines:
            if 1 <= line_num <=3:
                self.initial.append(line)

            elif 5 <= line_num <=7:
                self.goal.append(line)

            line_num += 1



