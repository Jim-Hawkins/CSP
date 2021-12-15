import sys

class Node:
    def __init__(self, info:list):
        self.state = []
        self.parent = None
        self.info = info
    
    def __str__(self):
        return str(id)+" "+self.place+" "+str(self.coord)


class Astar:

    def __init__(self, start):
        self.start = start

    def a_start_alg(self):

        open_lst = list(self.start)
        close_lst = list()

        