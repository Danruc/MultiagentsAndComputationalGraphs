import random
import sys
from mesa import Agent, Model #These are the base classes in our mesa model. 
from mesa.time import RandomActivation # schedule you use for activation of agents each period
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

finput = open(".\map.txt")

class Car(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    def step(self):
        print("webardo")

    def show(self):
        print("estoy aquí", self.unique_id)

class TrafficIntersection(Agent):
    def __init__(self, unique_id, model, tl1, tl2):
        super().__init__(unique_id, model)
        self.tl1 = tl1
        self. tl2 = tl2
        self.state = 0
        self.steps = 4
    
    def step(self):
        self.steps -= 1
        if self.steps == 0:
            self.state = random.choice([False, True])
            self.tl1.setState(self.state)
            self.tl2.setState(not(self.state))
            print(self.tl1.unique_id, self.tl1.state)
            print(self.tl2.unique_id, self.tl2.state)
            self.steps = 4

class TrafficLight(Agent):
    def __init__(self, unique_id, model, posFlow):
        super().__init__(unique_id, model)
        self.posFlow = posFlow
        self.state = False

    def setState(self, newState):
        self.state = newState

    def getState(self):
        a = self.state
        return a
    
    def getUniqueId(self):
        b = self.unique_id
        return b
        
class City(Model):
    def __init__(self, N, width, height):
        self.N = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.trafficLights = []
        self.initMap()

    def initMap(self):
        G = dict()
        num = finput.readline()
        for a in range(int(num)):
            x, y, size = finput.readline().strip().split(" ")
            key = str(x)+","+str(y)
            G[key] = []
            for i in range(int(size)):
                pos = list(map(int,finput.readline().strip().split(" ")))
                G[key].append(pos)
        num = finput.readline()
        for a in range(int(num)):
            data = []
            for i in range(3):
                data.append(list(map(int,finput.readline().strip().split(" "))))
            a = TrafficLight(str(data[0][0])+str(data[0][1])+str(data[2][0])+str(data[2][1]), self, data[2])
            b = TrafficLight(str(data[1][0])+str(data[1][1])+str(data[2][0])+str(data[2][1]), self, data[2])
            s = TrafficIntersection("t"+str(a), self, a, b)
            self.schedule.add(s)
            self.trafficLights.append(s)

    def step(self):
        self.schedule.step()

City = City(10, 10, 10)
for i in range(10):
    City.step()