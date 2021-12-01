'''
Crear grafos aleatorios de ciudad y 

20/11/2021
'''
import random as rd
import random
from mesa import Agent, Model #These are the base classes in our mesa model. 
from mesa.time import RandomActivation # schedule you use for activation of agents each period
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

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


class Car(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        self.type = "Car"
        self.end = []

    def getDestiny(self):
        nodo = random.choice(list(self.model.cityGraph.keys()))
        self.end = (int(nodo[0]),int(nodo[-1]))

    def setInitPos(self, newPos):
        self.pos = newPos

    def move(self):
        posibleMove = self.model.cityGraph[str(self.pos[0])+','+str(self.pos[1])]
        nextPos = random.choice(posibleMove)
        self.model.grid.move_agent(self, (nextPos[0],nextPos[1]))

    def step(self):
        self.move()

    def __str__(self): 
        return "{} -> {}".format(self.inicio, self.fin)

class TrafficLight(Agent):
    def __init__(self, unique_id: int, model, nodeFlow):
        super().__init__(unique_id, model)
        self.state = False
        self.type = "TrafficLight"
        self.nodeFlow = nodeFlow
        self.steps = 3
        
    def move(self):
        self.model.grid.move_agent(self, self.pos)

    def getLight(self):
        return self.state

    def step(self):
        if self.steps == 0:
            self.state = random.choice([True, False])
            self.steps = 4
        self.steps -= 1
        self.move()

class City(Model):

    def __init__(self, size, percent, N):
        self.size = size
        self.percent = percent
        self.idCounter = 0
        self.TrafficLights = {}

        self.N = N
        self.grid = MultiGrid(size, size, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.carritosPos = []

        self.streets = []
        self.initMap()

    def initMap(self):
        self.cityMap = [[ 1 for i in range(self.size)] for i in range(self.size)]
        self.nodeCount = (self.size ** 2) * self.percent // 100
        self.cityGraph = dict()
        self.fillMap(self.nodeCount)
        self.showCity()
        self.matrixToGraph()
        self.initTraffic()
        self.initCarritos()

    def initCarritos(self):
        graph = self.cityGraph

        for i in range(self.N):
            car = Car(self.idCounter, self)
            car.getDestiny()
            node = random.choice(list(graph.keys()))
            self.schedule.add(car)
            self.grid.place_agent(car, (int(node[0]),int(node[-1])))
            self.carritosPos.append(car)
            self.idCounter += 1


    def initTraffic(self):
        for key, value in self.cityGraph.items():
            if(len(value) > 2):
                for i in range(len(value)):
                    ag = TrafficLight(self.idCounter, self, (value[i][0],value[i][1]))
                    self.schedule.add(ag)
                    self.grid.place_agent(ag, (int(key[0]),int(key[-1]))) 
                    self.TrafficLights[int(key[0]),int(key[-1])] = ag
                    self.idCounter += 1

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
    
    def step(self):
        self.schedule.step()
        newPos = self.getPositions()
        return newPos
    
    def getPositions(self):
        carritos = self.carritosPos
        result = {}
        for i in carritos:
            result[i.unique_id] = i.pos
        return result
    
    def getTrafficLight(self):
        result = {}
        for key, val in self.TrafficLights.items():
            result[str(key[0])+","+str(key[-1])] = [val.nodeFlow, val.state]
        return result
