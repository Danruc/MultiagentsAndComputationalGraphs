INF = 99999

def Astar(D):
    n = len(D)
    end = [n-1, n-1]
    visited = []
    agent = [(0,0), (-1,-1)]
    visited.append(agent)
    direcciones = {"U":[-1,0], "D":[1,0], "L":[0,-1], "R":[0,1]}
    cost = {(0,0): INF}
    while cost != {} and agent[0] != (n-1, n-1):
        for direc in direcciones:
            if validPos(n, D, agent[0], direcciones[direc], visited):
                newY = agent[0][0] + direcciones[direc][0]
                newX = agent[0][1] + direcciones[direc][1]
                cost[(newY, newX)] = 1 + Manhattan([newY, newX], end)
        temp = [min(cost, key = cost.get), agent[0]]
        agent = temp
        visited.append(agent)
        cost.pop(agent[0])
    print(pathRecovery(visited))

def pathRecovery(visited):
    direcciones = {(1,0):"U", (-1,0):"D", (0,1):"L", (0,-1):"R"}
    notDirec = [(1,1), (1,-1), (-1,1), (-1,-1)]
    path = ""
    for i, x in enumerate(visited):
        if i+1 < len(visited):
            temp = visited[i+1]
            if (x[0][0] - temp[0][0], x[0][1] - temp[0][1]) not in notDirec:
                direc = (x[0][0] - temp[0][0], x[0][1] - temp[0][1])
                path += direcciones[direc]
            else:
                path = path[:-1]
                temp = visited[i-1]
                temp2 = visited[i+1]
                direc = (temp[0][0] - temp2[0][0], temp[0][1] - temp2[0][1])
                path += direcciones[direc]
    return path
            

def validPos(n, D, agent, move, visited):
    newY = agent[0] + move[0]
    newX = agent[1] + move[1]
    if newX >= 0 and newX < n and newY >= 0 and newY < n and D[newY][newX] == 1 and (newY,newX) not in visited:
        return True
    return False

def G(street):
    return street.getStreet()
        

def Manhattan(pos, nexPos):
    return abs(pos[0] - nexPos[0]) + abs(pos[1] - nexPos[1])

size = int(input())
D = []
for i in range(int(size)):
    D.append(list(map(int, input().strip().split(" "))))
Astar(D)