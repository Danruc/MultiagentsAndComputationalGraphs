import random
from mesa import Agent, Model #These are the base classes in our mesa model. 
from mesa.time import RandomActivation # schedule you use for activation of agents each period
from mesa.space import MultiGrid
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

class Street(Agent):
    def __init__(self, unique_id, model,):
        super().__init__(unique_id, model)
        
        self.type = "street"

class Car(Agent):
    def __init__(self, unique_id, model, hor):
        super().__init__(unique_id, model)
        
        self.type = "Car"
        self.hor = hor
     
    def move(self):
        

        trafficID = self.unique_id - 5
        trafficCoord = self.model.locations[trafficID]
        trafficState = self.model.grid.get_cell_list_contents(trafficCoord)
        
        var = 0
        for i in trafficState:
            if i.type == "TrafficLight":
                var = i.getLight()

        if self.pos == self.model.stopLocations[trafficID] and not var:
            print("se detiene")
        else:
            if self.hor == False:
                if self.unique_id %2:
                    self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))
                else:
                    self.model.grid.move_agent(self, (self.pos[0] - 1, self.pos[1]))
                
            else:
                if self.unique_id %2:
                    self.model.grid.move_agent(self, (self.pos[0] , self.pos[1]+1))
                else:
                    self.model.grid.move_agent(self, (self.pos[0] , self.pos[1]-1))
            
        
    
    def setInitPos(self, newPos):
        self.pos = newPos

    def step(self):
        self.move()
 

class TrafficLight(Agent):
    def __init__(self, unique_id: int, model):
        super().__init__(unique_id, model)
        self.state = False
        self.type = "TrafficLight"
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
        

class Streets(Model):
    def __init__(self, N, width, height):
        self.N = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True
        
        self.stopLocations = [(4,5), (7,6), (6,4), (5,7)]
        self.locations = [(5,5),(6,6),(6,5),(5,6)]
        locationsCars = [(0,5), (11,6), (6, 0), (5, 11)]
        cont = 5
        for i in range(4):
            ag = TrafficLight(i, self)
            if i >=2:
                car = Car(cont, self, True)
            else:
                car = Car(cont, self, False)
            self.schedule.add(ag)
            self.schedule.add(car)
            self.grid.place_agent(ag, self.locations[i]) 
            self.grid.place_agent(car, locationsCars[i])
            cont += 1
        
        for i in range(12):
            a = Street(50+i,self)
            b = Street(100+i,self)
            c = Street(150+i,self)
            d = Street(200+i,self)
            self.grid.place_agent(a, (5, i))
            self.grid.place_agent(b,(6, i))
            self.grid.place_agent(c, (i,5))
            self.grid.place_agent(d, (i,6))

    def step(self):
        self.schedule.step()
    

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.type == "Car":
        
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
    elif agent.type == "TrafficLight":

        portrayal["Shape"] = "rect"
        if agent.pos == (5,5) or agent.pos == (6,6):
            portrayal["w"] = 0.2
            portrayal["h"] = 0.5
        else:
            portrayal["w"] = 0.5
            portrayal["h"] = 0.2
        
        if agent.state == False:
            portrayal["Color"] = "red"
        else:
            portrayal["Color"] = "green"
        portrayal["Layer"] = 1

    elif agent.type == "street":
        portrayal["Shape"] = "rect"
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Color"]="black"
        portrayal["Layer"]=0
        

    return portrayal


w=12
h =12

grid = CanvasGrid(agent_portrayal,w, h, 600, 600)
server = ModularServer(Streets,[grid],"Streets Model",{"N":2, "width": w, "height": h})
server.port = 8521
server.launch()
