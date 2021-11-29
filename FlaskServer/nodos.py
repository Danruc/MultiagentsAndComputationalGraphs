'''
Crear grafos aleatorios de ciudad y 

20/11/2021
'''
import random as rd

class Street:  
    def __init__(self, inicio, fin):
        self.inicio = inicio
        self.fin = fin
        self.peso = 0

    def addCar(self):
        self.peso += 1
    
    def deleteCar(self):
        self.peso -= 1

    def getStreet(self):
        return [self.fin[0], self.fin[1]]

    def __str__(self): 
        return "{} -> {}".format(self.inicio, self.fin)

class City:
    def __init__(self, size, percent):
        self.size = size
        self.percent = percent
        self.initMap()

    def initMap(self):
        self.cityMap = [[ 1 for i in range(self.size)] for i in range(self.size)]
        self.nodeCount = (self.size ** 2) * self.percent // 100
        self.cityGraph = dict()
        '''
        while self.nodeCount != 0:
            row = rd.randrange(0, self.size)
            col = rd.randrange(0, self.size)
            if self.cityMap[row][col] == 1:
                self.cityMap[row][col] = 0
                self.cityGraph[(row,col)] = []
                count += 1
                self.nodeCount -= 1
        '''
        self.fillMap(self.nodeCount)
        self.showCity()
        self.matrixToGraph()
    
    def fillMap(self, count):
        directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        startPos = [rd.randrange(0, self.size), rd.randrange(0, self.size)]
        pos = startPos
        cont = 0
        while self.nodeCount != 0:
            move = rd.choice(directions)
            if self.validPosition(pos, move):
                pos = [pos[0] + move[0], pos[1] + move[1]]
                if self.cityMap[pos[0]][pos[1]] == 1:
                    cont += 1
                    self.cityMap[pos[0]][pos[1]] = 0
                    string = str(pos[0]) + "," + str(pos[1])
                    self.cityGraph[string] = []
                    self.nodeCount -= 1

    def matrixToGraph(self):
        directions = [[-1, 0], [1, 0], [0, 1], [0, -1]]
        for key, value in self.cityGraph.items():
            for y, x in directions:
                if self.validPosition(key, [y,x]) and self.cityMap[int(key[0])+y][int(key[-1])+x] == 0:
                    strett = Street(key, (int(key[0])+y, int(key[-1])+x))
                    self.cityGraph[key].append(strett.getStreet())
        self.showGraph()

    def validPosition(self, currPos, move):
        xPos = int(currPos[0])
        yPos = int(currPos[-1])
        newX = xPos + move[0]
        newY = yPos + move[1]

        if newX < self.size and  newX >= 0 and newY < self.size and  newY >= 0:
            return True
        return False
    
    def showCity(self):
        for row in self.cityMap:
            for cell in row:
                print(cell, end = " ")
            print()

    def showGraph(self):
        for key, value in self.cityGraph.items():
            print(key, len(value))
            for val in value:
                print(val)

    def getCity(self):
        return self.cityGraph
