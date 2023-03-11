
import numpy as np

class Network():

    #Initializing the network
    def __init__(self, path):
        self.path = path
        self.tempArcs =[]
        self.parser(self.path)
        self.arcs = np.array(self.tempArcs, dtype=int)  #Converting arc information from string to numeric values

    #Method to read the network from txt file
    def parser(self, path):
        startedReadingArcs = False
        with open(path, 'r') as f:
            #Reading each line
            for line in f:
                splitLine = line.split()    #Splitting 
                if startedReadingArcs:
                    self.tempArcs.append(splitLine)
                else:
                    #Reading each word
                    
                    for word in splitLine:
                        if (word == 'nNodes'):                           
                            self.nNodes = int(splitLine[len(splitLine)-1])
                            continue
                        elif (word == 'wTime'):                            
                            self.wTime = int(splitLine[len(splitLine)-1])
                            continue
                        elif (word == 'wInco'):           
                            self.wInco = int(splitLine[len(splitLine)-1])
                            continue
                        elif (word == 'Network'):
                            startedReadingArcs = True
                            break

