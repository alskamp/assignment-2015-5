import sys
import argparse
#sys.stdout = open("c:\\goat.txt", "w")
path = []

parser = argparse
parser = argparse.ArgumentParser()
parser.add_argument("graph_file", type=str)
parser.add_argument("start_node")
parser.add_argument("destination_node")
parser.add_argument("-r",action="store_true",default=False)
parser.add_argument("-b", "--blockedfile", type=str,default="empty")

args = parser.parse_args()

f = open(args.graph_file,'r')
start = int(args.start_node)
end = int(args.destination_node)
nodes = []
neighbours,relaxation,blocked = [],[],[]

for line in f:
    templist = [int(s) for s in line.split()]
    nodes.append(templist[0])
    nodes.append(templist[1])
visited = {}
for n in range(0,max(nodes)+1):
    neighbours.append([])
    relaxation.append([100000000,-1])
    blocked.append([])
    visited[n] = 0

f = open(args.graph_file,'r')
for line in f:
    templist = [int(s) for s in line.split()]
    temp1 = templist[:]
    temp2 = templist[:]
    del temp1[0]
    del temp2[1]
    neighbours[templist[0]].extend(temp1)
    neighbours[templist[1]].extend(temp2)

if args.blockedfile != "empty":
    b = open(args.blockedfile,'r')
    for line in b:
        templist = [int(s) for s in line.split()]
        temp1 = templist[:]
        temp2 = templist[:]
        del temp1[0]
        del temp2[1]
        blocked[templist[0]].extend(temp1)
        blocked[templist[1]].extend(temp2)


def dijkstra(neighbours,relaxation,visited,start,end):

    minnode = start
    for v in range(0,len(neighbours)):

        for v in range(0,len(neighbours[minnode])//2):
           if visited[neighbours[minnode][v*2]] == 0 and relaxation[neighbours[minnode][v*2]][0] > neighbours[minnode][v*2+1] + relaxation[minnode][0]:
                relaxation[neighbours[minnode][v*2]][0] = neighbours[minnode][v*2+1] + relaxation[minnode][0]
                relaxation[neighbours[minnode][v*2]][1] = minnode
        visited[minnode] = 1;

        min = 1000000
        for v in range(0,len(relaxation)):
            if relaxation[v][0] < min and visited[v] == 0:
                min =  relaxation[v][0]
                minnode = v

    path = [end]
    while end != start:
        path = [relaxation[end][1]] + path
        end = relaxation[end][1]
    return path


def driver(neighbours,relaxation,visited,start,end,blocked,nonegreedy):
    currentcost = 0
    totalcost = 0
    openpath = True
    distance = 0
    totalpath = [start]
    while end != start:
        for n in range(0,len(relaxation)):
            relaxation[n] = [100000000,-1]
            relaxation[start] = [0,start]
            visited[n] = 0
        path = dijkstra(neighbours,relaxation,visited,start,end)
        openpath = True
        n = 0
        driverpath = [start]
        currentcost = 0
        while n < (len(path)-1) and openpath:
            for k in range(0,len(neighbours[path[n]])//2):
                if neighbours[path[n]][k*2] == path[n+1]:
                    index1 = k*2
            for k in range(0,len(neighbours[path[n+1]])//2):
                if neighbours[path[n+1]][k*2] == path[n]:
                    index2 = k*2

            if path[n+1] in blocked[path[n]]:
                del neighbours[path[n]][index1]
                del neighbours[path[n]][index1]
                del neighbours[path[n+1]][index2]
                del neighbours[path[n+1]][index2]
                openpath = False
            if openpath:
                driverpath.append(path[n+1])
                totalpath.append(path[n+1])
                currentcost = currentcost + neighbours[path[n]][index1+1]
                totalcost = totalcost + neighbours[path[n]][index1+1]
                start = path[n+1]
            if openpath == False and nonegreedy == True:
                temp = driverpath[0:len(driverpath)-1]
                temp.reverse()
                totalpath = totalpath + temp
                totalcost = totalcost + currentcost
                start = 0
            n +=1

    print(totalpath)
    print(totalcost)

x = driver(neighbours,relaxation,visited,start,end,blocked,args.r)
