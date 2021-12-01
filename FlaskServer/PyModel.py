import random
import sys
from mesa import Agent, Model #These are the base classes in our mesa model. 
from mesa.time import RandomActivation # schedule you use for activation of agents each period
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


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
        #checar si ya llego al destino?
        if(self.pos == (self.end[0],self.end[1])):
            self.getDestiny()
        else:
            #ruta mas rapida
            #nos regresa una lista
            posibleMove = self.bestRute()
            isCar = self.model.isCar(posibleMove)
            isTl = self.model.isTrafficLight(posibleMove,self.pos)
            #checamos coche y semaforo
            if(not isCar and isTl):
                self.model.grid.move_agent(self, (posibleMove[0],posibleMove[1]))
    
    def bestRute(self):
        #las posibles direcciones del agente
        moveOp = self.model.cityGraph[str(self.pos[0])+","+str(self.pos[-1])]
        carsPosition = []
        for i in self.model.carritosPos:
            carsPosition.append(i.pos)

        if(len(moveOp) == 1):
            return (moveOp[0][0],moveOp[0][1])
        else:
            count = [0 for i in moveOp]
            #iteramos sobre las posibles direcciones
            for index, element in enumerate(moveOp):
                #las posibles direcciones de la posible direccion del agente
                tmp = self.model.cityGraph[str(element[0])+","+str(element[-1])]
                while(len(tmp) <=1):
                    if((tmp[0][0],tmp[0][1]) in carsPosition):
                        count[index] += 1
                    #sacamos los hijos del inception
                    tmp = self.model.cityGraph[str(tmp[0][0])+","+str(tmp[0][-1])]
                
                count[index] += self.heuristic(element)
            
            return moveOp[count.index(min(count))]

    def heuristic(self,fisrtPos):
        firstX = fisrtPos[0]
        firstY = fisrtPos[-1]

        secondX = self.end[0]
        secondY = self.end[1]

        return (firstX-secondX)**2 + (firstY - secondY)**2

    def step(self):
        self.move()

    def __str__(self): 
        return "{} -> {}".format(self.inicio, self.fin)


class TrafficIntersection(Agent):
    def __init__(self, unique_id, model, tl1, tl2):
        super().__init__(unique_id, model)
        self.tl1 = tl1
        self.tl2 = tl2
        self.state = 0
        self.steps = 4
    
    def step(self):
        self.steps -= 1
        if self.steps == 0:
            self.state = random.choice([False, True])
            self.tl1.setState(self.state)
            self.tl2.setState(not(self.state))
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

#Ambiente
class City(Model):
    def __init__(self, N, width, height):
        global finput
        #finput = open("map.txt")
        finput = open("D:\MultiagentsAndComputationalGraphs\FlaskServer\map.txt")
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.N = N
        self.trafficLights = []
        self.carritosPos = []
        self.cityGraph = {}
        self.initMap()
        self.initCarritos()
        finput.close()

    def isTrafficLight(self, posMov, carPos):
        actualPosID = str(carPos[0])+str(carPos[1])+str(posMov[0])+str(posMov[1])
        streetLightID = []

        for i in self.trafficLights:
            if(i.tl1.unique_id == actualPosID):
                return i.tl1.state
            elif(i.tl2.unique_id == actualPosID):
                return i.tl2.state
        return True;

    def isCar(self, carPos):
        carsPosition = (carPos[0],carPos[1])

        for i in self.carritosPos:
            if(carsPosition == i.pos):
                return True
        
        return False

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
        
        self.cityGraph = G

    def initCarritos(self):
        graph = self.cityGraph

        for i in range(self.N):
            car = Car(i, self)
            car.getDestiny()
            node = random.choice(list(graph.keys()))
            self.schedule.add(car)
            self.grid.place_agent(car, (int(node[0]),int(node[-1])))
            self.carritosPos.append(car)

    def getCity(self):
        self.showGraph()
        return self.cityGraph
    
    def showGraph(self):
            for key, value in self.cityGraph.items():
                print(key, len(value))
                for val in value:
                    print(val)

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
    
    def getTL(self):
        result = ""
        for i in self.trafficLights:
            if i.state:
                result += '1'
            else:
                result += '0'
        return result

    def getGoal(self):
        result = ""
        for i in self.carritosPos:
            if(i.pos == i.end):
                result += "1"
            else:
                result += "0"
        return result



