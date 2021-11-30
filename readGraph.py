import sys

finput = open(sys.argv[1],"r") if len(sys.argv) > 1 else sys.stdin
G = dict()
num = finput.readline()
for a in range(int(num)):
    x, y, size = finput.readline().strip().split(" ")
    key = str(x)+","+str(y)
    G[key] = []
    for i in range(int(size)):
        pos = list(map(int,finput.readline().strip().split(" ")))
        G[key].append(pos)
print(G)
finput.close()