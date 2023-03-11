import numpy as np

class Label():

    #Initializing the label
    def __init__(self):
        self.cost = 0
        self.time = 0
        self.inco = 0
        self.path = [1]
        self.done = False


class eLabel():
    #Initializing the label
    def __init__(self, nNodes):
        self.cost = 0
        self.time = 0
        self.inco = 0
        self.elem = [0]*nNodes
        self.elem[0] = 1
        self.path = [1]
        self.done = False

class epLabel():
    #Initializing the label
    def __init__(self, nNodes):
        self.cost = 0
        self.time = 0
        self.inco = 0
        self.elem = [0]*nNodes
        self.elem[0] = 1
        self.pair = 0
        self.path = [1]
        self.done = False