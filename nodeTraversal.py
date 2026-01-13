import pygame
import random
import math
import pickle
import os
import time

class Node:
    def __init__(self, payload, x, y) -> None:
        self.payload = payload
        self.edges = []
        self.x = x
        self.y = y
    
    def connect(self, node, weight):
        duplicateConnection = False
        for c in self.edges:
            if node == c[0]:
                duplicateConnection = True
                break
        if not(duplicateConnection):
            self.edges.append([node, weight])
    
    def removeConnection(self, node):
        for c in self.edges:
            if c[0] == node:
                self.edges.remove(c)


def renderGraph(graph):

    screenRect = pygame.Rect(0,0,800,800)
    screen.set_clip(screenRect)

    if end != None:
        pygame.draw.circle(screen, (255,0,0), (end.x*zoom + viewArea[0], end.y*zoom + viewArea[1]), 26*zoom)
    
    if start != None:
        pygame.draw.circle(screen, (0,255,0), (start.x*zoom + viewArea[0], start.y*zoom + viewArea[1]), 26*zoom)

    if selectedNode != None:
        pygame.draw.circle(screen, (0,255,255), (selectedNode.x*zoom + viewArea[0], selectedNode.y*zoom + viewArea[1]), 24*zoom)

    for n in graph:

        nodePos = (n.x*zoom + viewArea[0], n.y*zoom + viewArea[1])

        try:
            if nodeDists[n] >= renderDistance:
                break
        except:
            break
        
        for c in n.edges:

            try:
                if nodeDists[c[0]] >= renderDistance:
                    continue
            except:
                continue

            pygame.draw.line(screen, (255,255,255), nodePos, (c[0].x*zoom + viewArea[0], c[0].y*zoom + viewArea[1]), 1)

            A = math.atan((c[0].y - n.y) / (c[0].x - n.x)) + (math.pi if n.x <= c[0].x else 0) if c[0].x != n.x else math.pi/2
            ci = (20*math.cos(A)*zoom + c[0].x*zoom + viewArea[0], 20*math.sin(A)*zoom + c[0].y*zoom + viewArea[1])
            pygame.draw.line(screen, (255,255,255), ci, ((20*math.cos(A-0.5) + 20*math.cos(A) + c[0].x)*zoom + viewArea[0], (20*math.sin(A-0.5) + 20*math.sin(A) + c[0].y)*zoom + viewArea[1]), 1)
            pygame.draw.line(screen, (255,255,255), ci, ((20*math.cos(A+0.5) + 20*math.cos(A) + c[0].x)*zoom + viewArea[0], (20*math.sin(A+0.5) + 20*math.sin(A) + c[0].y)*zoom + viewArea[1]), 1)

            if c[1] > 1:
                my_font = pygame.font.SysFont('charter', int(20*zoom))
                text_surface = my_font.render(f"{c[1]}", False, (255,255,255))
                screen.blit(text_surface,((n.x + c[0].x)/2*zoom + viewArea[0], (n.y + c[0].y)/2*zoom + viewArea[1]))
    
    if shortestPath != None:
        previous = shortestPath[0]
        for n in shortestPath[1:]:
            pygame.draw.line(screen,(255,0,255), (previous.x*zoom + viewArea[0], previous.y*zoom + viewArea[1]), (n.x*zoom + viewArea[0], n.y*zoom + viewArea[1]), 3)
            previous = n
    
    for n in graph:

        nodePos = (n.x*zoom + viewArea[0], n.y*zoom + viewArea[1])

        try:
            if nodeDists[n] >= renderDistance:
                break
        except:
            break

        pygame.draw.circle(screen, (255,255,255), nodePos, 20*zoom)
        pygame.draw.circle(screen, (0,0,0), nodePos, 18*zoom)

        my_font = pygame.font.SysFont('charter', int(20*zoom))
        text_surface = my_font.render(f"{n.payload}", False, (255,255,255))
        screen.blit(text_surface,(nodePos[0] - text_surface.width/2, nodePos[1] - text_surface.height/2))

def renderMenu(files):
    rect = pygame.Rect(200,200,400,400)
    pygame.draw.rect(screen,(0,0,0),rect)
    drawRectOutline(rect, (255,255,255), 1)
    screen.set_clip(rect)

    my_font = pygame.font.SysFont('charter', 20)
    for i in range(len(files)):
        text_surface = my_font.render(files[i][0][:-4], False, (255,255,255))
        screen.blit(text_surface,(files[i][1].x, files[i][1].y))
        drawRectOutline(pygame.Rect(files[i][1].x - 5, files[i][1].y - 1, text_surface.width + 10, text_surface.height + 10), (255,255,255), 1)
    
    screen.set_clip(None)

def drawRectOutline(rect, color, width):
    pygame.draw.line(screen, color, rect.topleft, rect.topright, width)
    pygame.draw.line(screen, color, rect.topright, rect.bottomright, width)
    pygame.draw.line(screen, color, rect.bottomright, rect.bottomleft, width)
    pygame.draw.line(screen, color, rect.bottomleft, rect.topleft, width)

def randomGraph(n):
    result = []

    for k in range(n):
        newNode = Node(k, random.randrange(0, 800), random.randrange(0, 800))
        result.append(newNode)
    
    for n in result:
        connectionCount = random.randint(1,4)
        connectionOptions = result.copy()
        connectionOptions.remove(n)
        for k in range(connectionCount):
            choice = random.choice(connectionOptions)
            connectionOptions.remove(choice)
            n.connect(choice, random.randint(1,4))
    
    return result

def dijkstraPathFind(graph, start, end):
    dist = {}
    prev = {}
    explored = {}
    for n in graph:
        dist[n] = math.inf
        prev[n] = None
        explored[n] = False
    
    dist[start] = 0
    while not(explored[end]):
        minDist = math.inf
        c = None
        for n in graph:
            if dist[n] < minDist and not(explored[n]):
                c = n
                minDist = dist[n]
        if c == None:
            return None
        explored[c] = True
        for e in c.edges:
            if dist[c] + e[1] < dist[e[0]]:
                dist[e[0]] = dist[c] + e[1]
                prev[e[0]] = c
    
    path = []
    c = end
    while prev[c] != None:
        path.append(c)
        c = prev[c]
    path.append(c)
    
    return path

def saveGraph(graph, graphName):
    with open(graphName + ".pkl", 'wb') as outp:
        pickle.dump(graph, outp, pickle.HIGHEST_PROTOCOL)
    os.rename("/Users/chrisguzun/Desktop/NodeTraversal/" + graphName + ".pkl", "/Users/chrisguzun/Desktop/NodeTraversal/graphs/" + graphName + ".pkl")

def sortGraph():
    c = 400
    graph.sort(key = lambda a : math.sqrt(math.pow(a.x*zoom  + viewArea[0] - c,2) + math.pow(a.y*zoom  + viewArea[1] - c,2)))
    for n in graph:
        d = math.sqrt(math.pow(n.x*zoom  + viewArea[0] - c,2) + math.pow(n.y*zoom  + viewArea[1] - c,2))
        nodeDists[n] = d
        if d >= renderDistance:
            break

def spaceOutNodes():
    push = {}
    R = 30 # repulsion to other nodes
    C = 1  # attraction through edges
    P = 1/25 # pull to center
    for n in graph:
        push[n] = [0,0]
        for k in graph:
            A = math.atan((n.y - k.y) / (n.x - k.x)) + (math.pi if k.x <= n.x else 0) if n.x != k.x else math.pi/2
            d = math.sqrt(math.pow(n.x - k.x,2) + math.pow(n.y - k.y,2))
            if d < 20:
                d = 20
            push[n][0] = push[n][0] - R*math.cos(A)/d
            push[n][1] = push[n][1] - R*math.sin(A)/d
        
        for e in n.edges:
            A = math.atan((n.y - e[0].y) / (n.x - e[0].x)) + (math.pi if e[0].x <= n.x else 0) if n.x != e[0].x else math.pi/2
            push[n][0] = push[n][0] + C*math.cos(A)/e[1]
            push[n][1] = push[n][1] + C*math.sin(A)/e[1]
        
        A = math.atan((n.y - 400) / (n.x - 400)) + (math.pi if 400 <= n.x else 0) if n.x != 400 else math.pi/2
        d = math.sqrt(math.pow(n.x - 400,2) + math.pow(n.y - 400,2))
        if d < 20:
            d = 20
        if d > 50:
            d = 50
        push[n][0] = push[n][0] + P*math.cos(A)*d
        push[n][1] = push[n][1] + P*math.sin(A)*d
    
    for n in graph:
        n.x = n.x + push[n][0]
        n.y = n.y + push[n][1]
            

pygame.init()
pygame.font.init()
screenSize = (800,800)
screen = pygame.display.set_mode(screenSize,pygame.RESIZABLE)
viewArea = [0,0]
mousePos = None
selectedNode = None
menu = False
scroll = 0
zoom = 1
files = []
timer = time.time()
renderDistance = 5000

graph = []

nodeDists = {}

shortestPath = None

start = None
end = None

"""with open("/Users/chrisguzun/Desktop/NodeTraversal/graphs/wordTree.pkl", 'rb') as inp:
    wordTree = pickle.load(inp)

def convertTreeToGraph(n, x, y):
    print(n.e)
    node = Node(n.e, x, y)
    for c in range(len(n.children)):
        childNode = convertTreeToGraph(n.children[c],x + c*50, y + 50)
        node.connect(childNode, 1)
    return node

def loadTreeInGraph(root):
    convertedWordTree.append(root)
    for c in root.edges:
        loadTreeInGraph(c[0])

convertedWordTreeRoot = convertTreeToGraph(wordTree, 200, 200)
convertedWordTree = []
loadTreeInGraph(convertedWordTreeRoot)

with open("convertedWordTree.pkl", 'wb') as outp:
    pickle.dump(convertedWordTree, outp, pickle.HIGHEST_PROTOCOL)"""


running = True
while running:
    pygame.draw.rect(screen, (0,0,0), (0, 0, screenSize[0], screenSize[1]))
    screenRect = pygame.Rect(0,0,800,800)

    if time.time() - timer > 0.5:
        nodeDists = {}
        sortGraph()
        timer = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = event.pos
            if menu and pygame.Rect(200,200,400,400).collidepoint(event.pos) and event.button == 1:
                for f in files:
                    if f[1].collidepoint(mousePos):
                        with open("/Users/chrisguzun/Desktop/NodeTraversal/graphs/" + f[0], 'rb') as inp:
                            graph = pickle.load(inp)
                            nodeDists = {}
                            sortGraph()
                            if len(graph) > 100:
                                renderDistance = 500
                            start = None
                            end = None
                            shortestPath = None
            else:
                if event.button == 1:
                    nodeClicked = False
                    for n in graph:

                        try:
                            if nodeDists[n] >= renderDistance:
                                break
                        except:
                            break

                        if math.sqrt(math.pow(mousePos[0] - viewArea[0] - n.x*zoom,2) + math.pow(mousePos[1] - viewArea[1] - n.y*zoom,2)) <= 20*zoom:
                            nodeClicked = True
                            if selectedNode == n:
                                selectedNode = None
                            else:
                                if selectedNode == None:
                                    selectedNode = n
                                else:
                                    selectedNode.connect(n, 1)
                                    shortestPath = None
                    if not(nodeClicked):
                        selectedNode = None
                
                if event.button == 3:
                    for n in graph:

                        try:
                            if nodeDists[n] >= renderDistance:
                                break
                        except:
                            break

                        if math.sqrt(math.pow(mousePos[0] - viewArea[0] - n.x*zoom,2) + math.pow(mousePos[1] - viewArea[1] - n.y*zoom,2)) <= 20*zoom:
                            if start == n:
                                start = None
                            else:
                                if n != end:
                                    start = n
                                    if start != None and end != None:
                                        shortestPath = dijkstraPathFind(graph, start, end)
                
                if event.button == 2:
                    for n in graph:

                        try:
                            if nodeDists[n] >= renderDistance:
                                break
                        except:
                            break

                        if math.sqrt(math.pow(mousePos[0] - viewArea[0] - n.x*zoom,2) + math.pow(mousePos[1] - viewArea[1] - n.y*zoom,2)) <= 20*zoom:
                            if end == n:
                                end = None
                            else:
                                if n != start:
                                    end = n
                                    if start != None and end != None:
                                        shortestPath = dijkstraPathFind(graph, start, end)
        
        if event.type == pygame.MOUSEBUTTONUP:
            mousePos = None
        
        if event.type == pygame.MOUSEMOTION:
            if mousePos != None:
                viewArea[0] = viewArea[0] + (event.pos[0] - mousePos[0])
                viewArea[1] = viewArea[1] + (event.pos[1] - mousePos[1])
                mousePos = event.pos
        
        if event.type == pygame.MOUSEWHEEL:
            if menu:
                if event.y < 0 and files[-1][1].y+files[-1][1].height > 550:
                    scroll = scroll - event.y*-2
                if event.y > 0:
                    scroll = scroll + event.y*2
                if scroll > 0:
                    scroll = 0
            else:
                if event.y < 0:
                    zoom = zoom - event.y*-0.02
                if event.y > 0:
                    zoom = zoom + event.y*0.02
                if zoom < 0.1:
                    zoom = 0.1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                graph.append(Node(graph[-1].payload + 1 if len(graph) > 0 else 1, pygame.mouse.get_pos()[0] - viewArea[0], pygame.mouse.get_pos()[1] - viewArea[1]))
            
            if event.key == pygame.K_BACKSPACE:
                if selectedNode != None:
                    if selectedNode == start:
                        start = None
                    if selectedNode == end:
                        end = None
                    graph.remove(selectedNode)
                    for n in graph:
                        n.removeConnection(selectedNode)
                    selectedNode = None
                    if start != None and end != None:
                        shortestPath = dijkstraPathFind(graph, start, end)
            
            if event.key == pygame.K_p:
                if start != None and end != None:
                    shortestPath = dijkstraPathFind(graph, start, end)
            
            if event.key == pygame.K_m:
                if menu:
                    menu = False
                else:
                    menu = True
            
            if event.key == pygame.K_s:
                print("Enter your name:")
                saveGraph(graph, input())
            
            if event.key == pygame.K_c:
                graph = []
            
            if event.key == pygame.K_r:
                graph = graph + randomGraph(10)
    
    dir_list = os.listdir("/Users/chrisguzun/Desktop/NodeTraversal/graphs")
    for k in dir_list:
        if k[0] == ".":
            dir_list.remove(k)
    files = []
    my_font = pygame.font.SysFont('charter', 20)
    for i in range(len(dir_list)):
        text_surface = my_font.render(dir_list[i], False, (255,255,255))
        rect = pygame.Rect(250, 250 + i*50 + scroll, text_surface.width, text_surface.height)
        files.append([dir_list[i],rect])
    
    renderGraph(graph)

    if menu:
        renderMenu(files)

    pygame.display.flip()

    #spaceOutNodes()

pygame.quit()