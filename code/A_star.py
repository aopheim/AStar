from PIL import Image           #For creating images of the labyrinth


class Node(object):
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.g = 1000
        self.h = 1000
        self.cost = 2000
        self.f = 2000
        self.parent = self
        self.start = False
        self.end = False
        self.free = False
        self.wall = False


    def gFunc(self, start, node): #Calculates the distance from the root to the node (Manhattan distance)
        return manhattanDist(start, node)

    def hFunc(self, node, end):
        return manhattanDist(node, end)

    def fFunc(self):
        self.f = self.g + self.h

    def printNode(self):
        print(
            "\n\nPosition: \t[", self.row, " ", self.col, "]",
            "\nStart: \t", self.start,
            "\nEnd: \t", self.end,
            "\ng: \t", self.g,
            "\nh: \t", self.h,
            "\nCost: \t", self.cost,
            "\nf: \t", self.f,
            "\nFree: \t", self.free,
            "\nWall: \t", self.wall,
            "\nValue: \t", self.value,
            "\nParent: \t[", (self.parent).row, " ", (self.parent).col, "]", end=""
        )



def manhattanDist(start, end):
    xDist = abs(end.col - start.col)
    yDist = abs(end.row - start.row)
    #print("xDist: ", xDist, ", yDist: ", yDist)
    return xDist + yDist


def readFromTxt(filePath):
    file = open(filePath, "r")
    lines = file.readlines()
    #print(lines)
    return lines

def generateBoard(board, fileName):
    img = Image.new('RGB', (len(board[0]), len(board)), "white")        # Creates image object in the size of the board.
    pixels = img.load()             # creating a pixel map

    for line in range(0, len(board)):
        for char in range(0, len(board[0])):
            if (board[line][char] == "."):
                pixels[char, line] = (192,192,192)      # open pixels appear grey

            if (board[line][char] == "#"):
                pixels[char, line] = (0,0,0)      # border pixels appear black

            if (board[line][char] == "A"):
                pixels[char, line] = (255,255,0)      # start pixel appear blue

            if (board[line][char] == "B"):
                pixels[char, line] = (255,0,0)      # end pixel appear red

            if (board[line][char] == "w"):
                pixels[char, line] = (0,0,255)      # Water

            if (board[line][char] == "m"):
                pixels[char, line] = (128,128,128)      # mountains

            if (board[line][char] == "f"):
                pixels[char, line] = (0,102,0)      # forest

            if (board[line][char] == "g"):
                pixels[char, line] = (102,204,0)      # grass

            if (board[line][char] == "r"):
                pixels[char, line] = (153,76,0)      # roads

    img.save(fileName, "PNG")
    return img


def colorPixel(fileName, img, node, color):


    pixels = img.load()
    pixels[node.col, node.row] = color        # Marking the pixel with a color
    if (fileName != False):     # if image file is to be created
        img.save(fileName, "PNG")

    return img



def convertToNodes(board):
    # Converting the board with characters to nodes
    nodeList = []       #nodeList: List in list indexed nodeList[row][col]
    for i in range(0, len(board)):
        new = []
        for j in range(0, len(board[0])):
            new.append(Node(i,j, board[i][j]))
        nodeList.append(new)

    # Filling in necessery information for the node class
    for i in range(0, len(board)):
        for j in range(0, len(board[0])):
            if (nodeList[i][j].value == "A"):
                nodeList[i][j].start = True
                nodeList[i][j].free = True
                start = nodeList[i][j]

            if (nodeList[i][j].value == "B"):
                nodeList[i][j].end = True
                nodeList[i][j].free = True
                end = nodeList[i][j]

            if (nodeList[i][j].value == "."):
                nodeList[i][j].free = True

            if (nodeList[i][j].value == "#"):
                nodeList[i][j].wall = True

            if (nodeList[i][j].value == "w"):
                nodeList[i][j].cost = 100
                nodeList[i][j].free = True

            if (nodeList[i][j].value == "m"):
                nodeList[i][j].cost = 50
                nodeList[i][j].free = True

            if (nodeList[i][j].value == "f"):
                nodeList[i][j].cost = 10
                nodeList[i][j].free = True

            if (nodeList[i][j].value == "g"):
                nodeList[i][j].cost = 5
                nodeList[i][j].free = True

            if (nodeList[i][j].value == "r"):
                nodeList[i][j].cost = 1
                nodeList[i][j].free = True

    return [nodeList, start, end]

def generateAllSucc(node, nodeList):
    colStart = 0
    colEnd = len(nodeList[0])
    rowStart = 0
    rowEnd = len(nodeList)
    #print("colEnd: ", colEnd, "rowEnd: ", rowEnd)

    iNorth = node.row - 1
    iSouth = node.row + 1
    iEast = node.col + 1
    iWest = node.col - 1


    neighbourList = []
    # If indexes are outside the board, set them as "invalid"
    if (iNorth < rowStart or (nodeList[iNorth][node.col].free == False)): # if over the array or not free
        iNorth = None
    else:
        neighbourList.append(nodeList[iNorth][node.col])

    if (iEast > colEnd - 1 or (nodeList[node.row][iEast].free == False)):
        iEast = None
    else:
        neighbourList.append(nodeList[node.row][iEast])

    if ((iSouth > rowEnd - 1) or (nodeList[iSouth][node.col].free == False)):
        iSouth = None
    else:
        neighbourList.append(nodeList[iSouth][node.col])

    if ((iWest < colStart) or (nodeList[node.row][iWest].free == False)):
        iWest = None
    else:
        neighbourList.append(nodeList[node.row][iWest])

    #print("neighbourList: ", neighbourList)
    return neighbourList




def getSolution(lastNode, solution):
    if ((lastNode.parent).start != True):
        par = lastNode.parent
        solution.append(par)
        getSolution(lastNode.parent, solution)

    #solution.append(lastNode.parent)
    return solution


def colorSolution(solution, img, fileName):
    for el in solution:
        colorPixel(fileName, img, el, (204, 0, 204))      # colouring the path

    # Coloring the start pixel:
    colorPixel(fileName, img, solution[len(solution) - 1], (255, 255, 0))

    #Coloring the end pixel:
    colorPixel(fileName, img, solution[0], (255, 0, 0) )


openedColor = (255, 255, 255)
closedColor = (102, 51, 0)

def A_star(nodes, start, end, img_object):
    # Initializing the closed and open lists, containing elements already evaluated.
    open = []
    closed = []

    # Initializing the start node:
    start.g = 0
    start.h = start.hFunc(start, end)
    start.f = start.cost
    start.parent = start

    #print("Start: ")
    #start.printNode()
    #print("End: ")
    #end.printNode()


    # Appending the start node to the set of opened nodes
    open.append(start)

    success = False
    while((len(open) > 0) and (success == False)):       # while the open list is not empty
        #print("\n*************************************************\nOpen contains: \n")
        #for el in open:
            #el.printNode()
        #print("\n*************************************************\n")

        q = open.pop(0)         # popping the first element of the open array, the one with the lowest f value.
        #print("\n------------CURRENT NODE-------------------\n")
        #q.printNode()

        #img_object = colorPixel(False, img_object, q, (255, 255, 102))
        succ = generateAllSucc(q, nodes)     # Generating all valid neighbouring elements of q

        #print("\n********************************************")
        #print("\nValid neighbours of [", q.row, ", ", q.col, "]: ")
        #for S in succ:
            #S.printNode()
        #print("\n********************************************\n")

        for S in succ:
            #print("In succ")
            #S.printNode()
            if (S.end == True):         # If the neighbouring element is the goal, end the while loop
                print("\n\nEnd node is found!")
                success = True
                lastNode = S
                S.parent = q
                break
            tmp_S_g = q.g + manhattanDist(q, S) # Updating the neighbour's g value
            tmp_S_h = S.hFunc(S, end)
            tmp_cost = q.cost + S.cost
            tmp_S_f = tmp_S_g + tmp_S_h + S.cost

            # If the node is already in the closed or open list, but with lower f value, skip adding it that neighbour
            if ((S in open) and (S.f <= tmp_S_f)):
                #print("\nS in open with <= f")
                continue
            if ((S in closed) and (S.f <= tmp_S_f)):
                #print("\nS in closed with <= f")
                continue

            else:  #Otherwise, add the neighbour to the open list, and set its f, g and h values
                #print("\n\nAdding node")
                S.g = tmp_S_g
                S.h = tmp_S_h
                S.cost = tmp_cost
                S.f = tmp_S_f
                S.parent = q
                #S.printNode()
                open.append(S)      # Adding S to the open list.
                open.sort(key=lambda Node: Node.f)      # TODO: check if correct. sorting the opened list after f value.
                #colorPixel(False, img_object, S, openedColor)

        closed.append(q) # adding q to the closed list
        #colorPixel(False, img_object, q, closedColor)

    # Outside while loop
    solution = []
    solution = getSolution(lastNode, solution)
    # Adding the start and end node, as the getSolution does not add them
    solution.append(start)
    solution.insert(0, end)

    print("A* solution is, from end to start: \n")
    for el in solution:
        print("[", el.row, " ", el.col, "] ")


    return [img_object, solution]

def dijkstra(nodes, start, end, img_object):
    # Initializing the closed and open lists, containing elements already evaluated.
    open = []
    closed = []

    # Initializing the start node:
    start.g = start.cost
    #start.h = start.hFunc(start, end)
    start.f = start.g
    start.parent = start

    #print("Start: ")
    #start.printNode()
    #print("End: ")
    #end.printNode()


    # Appending the start node to the set of opened nodes
    open.append(start)

    success = False
    while((len(open) > 0) and (success == False)):       # while the open list is not empty
        #print("\n*************************************************\nOpen contains: \n")
        #for el in open:
            #el.printNode()
        #print("\n*************************************************\n")

        q = open.pop(0)         # popping the first element of the open array, the one with the lowest g value.
        #print("\n------------CURRENT NODE-------------------\n")
        #q.printNode()

        #img_object = colorPixel(False, img_object, q, (255, 255, 102))
        succ = generateAllSucc(q, nodes)     # Generating all valid neighbouring elements of q

        #print("\n********************************************")
        #print("\nValid neighbours of [", q.row, ", ", q.col, "]: ")
        #for S in succ:
            #S.printNode()
        #print("\n********************************************\n")

        for S in succ:
            #print("In succ")
            #S.printNode()
            if (S.end == True):         # If the neighbouring element is the goal, end the while loop
                print("\n\nEnd node is found!")
                success = True
                lastNode = S
                S.parent = q
                break

            tmp_S_g = q.g + S.cost        # Updating the neighbour's g value
            #tmp_S_f = q.f + S.cost

            # If the node is already in the closed or open list, but with lower f value, skip adding it that neighbour
            if ((S in open) and (S.f <= tmp_S_g)):
                #print("\nS in open with <= f")
                continue
            if ((S in closed) and (S.f <= tmp_S_g)):
                #print("\nS in closed with <= f")
                continue

            else:  #Otherwise, add the neighbour to the open list, and set its f, g and h values
                print("\n\nAdding node")
                S.g = tmp_S_g
                #S.h = tmp_S_h
                #S.cost = tmp_cost
                #S.f = tmp_S_f
                S.parent = q
                S.printNode()
                open.append(S)      # Adding S to the open list.
                open.sort(key=lambda Node: Node.g)      # Dijkstra: Sort the opened list by the g value
                colorPixel(False, img_object, S, openedColor)

        closed.append(q) # adding q to the closed list
        colorPixel(False, img_object, S, closedColor)

    # Outside while loop
    solution = []
    solution = getSolution(lastNode, solution)
    # Adding the start and end node, as the getSolution does not add them
    solution.append(start)
    solution.insert(0, end)

    print("Dijkstra solution is, from end to start: \n")
    for el in solution:
        print("[", el.row, " ", el.col, "] ")

    return [img_object, solution]



def BFS(nodes, start, end, img_object):
    # Initializing the closed and open lists, containing elements already evaluated.
    open = []
    closed = []

    # Initializing the start node:
    #start.g = 0
    #start.h = start.hFunc(start, end)
    start.f = 0
    start.parent = start

    #print("Start: ")
    #start.printNode()
    #print("End: ")
    #end.printNode()


    # Appending the start node to the set of opened nodes
    open.append(start)

    success = False
    while((len(open) > 0) and (success == False)):       # while the open list is not empty
        #print("\n*************************************************\nOpen contains: \n")
        #for el in open:
            #el.printNode()
        #print("\n*************************************************\n")

        q = open.pop(0)         # popping the first element of the open array, the one with the lowest f value.
        #print("\n------------CURRENT NODE-------------------\n")
        #q.printNode()

        #img_object = colorPixel(False, img_object, q, (255, 255, 102))
        succ = generateAllSucc(q, nodes)     # Generating all valid neighbouring elements of q

        #print("\n********************************************")
        #print("\nValid neighbours of [", q.row, ", ", q.col, "]: ")
        #for S in succ:
            #S.printNode()
        #print("\n********************************************\n")

        for S in succ:
            #print("In succ")
            #S.printNode()
            if (S.end == True):         # If the neighbouring element is the goal, end the while loop
                print("\n\nEnd node is found!")
                success = True
                lastNode = S
                S.parent = q
                break
            #tmp_S_g = q.g + manhattanDist(q, S) # Updating the neighbour's g value
            #tmp_S_h = S.hFunc(S, end)
            #tmp_cost = q.cost + S.cost
            tmp_S_f = q.f + S.cost

            # If the node is already in the closed or open list, but with lower f value, skip adding it that neighbour
            if ((S in open) and (S.f <= tmp_S_f)):
                #print("\nS in open with <= f")
                continue
            if ((S in closed) and (S.f <= tmp_S_f)):
                #print("\nS in closed with <= f")
                continue

            else:  #Otherwise, add the neighbour to the open list, and set its f, g and h values
                #print("\n\nAdding node")
                #S.g = tmp_S_g
                #S.h = tmp_S_h
                #S.cost = tmp_cost
                S.f = tmp_S_f
                S.parent = q
                #S.printNode()
                open.insert(0, S)      # Adding S to the open list at first position. FIFO, used in BFS
                colorPixel(False, img_object, S, openedColor)

        closed.append(q) # adding q to the closed list
        colorPixel(False, img_object, q, closedColor)

    # Outside while loop
    solution = []
    solution = getSolution(lastNode, solution)
    # Adding the start and end node, as the getSolution does not add them
    solution.append(start)
    solution.insert(0, end)

    print("Breadth-first solution is, from end to start: \n")
    for el in solution:
        print("[", el.row, " ", el.col, "] ")

    return [img_object, solution]




def main():
    '''
    #For Part 1:
    board_1_1 = readFromTxt("C:\\Users\\adria\\Documents\\Dokumenter\\NTNU\\Introduksjon til kunstig intelligens\\Assignments\\A3_A_star\\boards\\boards\\board-1-1.txt")

    board_1_2 = readFromTxt("C:\\Users\\adria\\Documents\\Dokumenter\\NTNU\\Introduksjon til kunstig intelligens\\Assignments\\A3_A_star\\boards\\boards\\board-1-2.txt")
    board_1_3 = readFromTxt("C:\\Users\\adria\\Documents\\Dokumenter\\NTNU\\Introduksjon til kunstig intelligens\\Assignments\\A3_A_star\\boards\\boards\\board-1-3.txt")
    '''
    board_1_4 = readFromTxt("C:\\Users\\adria\\Documents\\Dokumenter\\NTNU\\Introduksjon til kunstig intelligens\\Assignments\\A3_A_star\\boards\\boards\\board-1-4.txt")

    # For part 2:
    board_2_1 = readFromTxt("C:\\Users\\adria\\Documents\\Dokumenter\\NTNU\\Introduksjon til kunstig intelligens\\Assignments\\A3_A_star\\boards\\boards\\board-2-1.txt")
    board_2_2 = readFromTxt("C:\\Users\\adria\\Documents\\Dokumenter\\NTNU\\Introduksjon til kunstig intelligens\\Assignments\\A3_A_star\\boards\\boards\\board-2-2.txt")
    board_2_3 = readFromTxt("C:\\Users\\adria\\Documents\\Dokumenter\\NTNU\\Introduksjon til kunstig intelligens\\Assignments\\A3_A_star\\boards\\boards\\board-2-3.txt")
    board_2_4 = readFromTxt("C:\\Users\\adria\\Documents\\Dokumenter\\NTNU\\Introduksjon til kunstig intelligens\\Assignments\\A3_A_star\\boards\\boards\\board-2-4.txt")
    '''
    img_1_1 = generateBoard(board_1_1, "board_1_1.png")
    img_1_2 = generateBoard(board_1_2, "board_1_2.png")
    img_1_3 = generateBoard(board_1_3, "board_1_3.png")

    '''
    img_1_4_Astar = generateBoard(board_1_4, "board_1_4.png")
    img_1_4_dij = generateBoard(board_1_4, "board_1_4.png")
    img_1_4_BFS = generateBoard(board_1_4, "board_1_4.png")


    img_2_1_Astar = generateBoard(board_2_1, "board_2_1.png")
    img_2_1_dij = generateBoard(board_2_1, "board_2_1.png")
    img_2_1_BFS = generateBoard(board_2_1, "board_2_1.png")

    img_2_2_Astar = generateBoard(board_2_2, "board_2_2.png")
    img_2_2_dij = generateBoard(board_2_2, "board_2_2.png")
    img_2_2_BFS = generateBoard(board_2_2, "board_2_2.png")

    img_2_3_Astar = generateBoard(board_2_3, "board_2_3.png")
    img_2_3_dij = generateBoard(board_2_3, "board_2_3.png")
    img_2_3_BFS = generateBoard(board_2_3, "board_2_3.png")


    img_2_4_Astar = generateBoard(board_2_4, "board_2_4.png")
    img_2_4_dij = generateBoard(board_2_4, "board_2_4.png")
    img_2_4_BFS = generateBoard(board_2_4, "board_2_4.png")



    '''
    [nodes, start, end] = convertToNodes(board_1_1)
    [img_1_1, sol_1_1] = A_star(nodes, start, end, img_1_1)
    colorSolution(sol_1_1, img_1_1, "board_1_1_path_Astar.png")

    [nodes, start, end] = convertToNodes(board_1_2)
    [img_1_2, sol_1_2] = A_star(nodes, start, end, img_1_2)
    colorSolution(sol_1_2, img_1_2, "board_1_2_path_Astar.png")

    [nodes, start, end] = convertToNodes(board_1_3)
    [img_1_3, sol_1_3] = A_star(nodes, start, end, img_1_3)
    colorSolution(sol_1_3, img_1_3, "board_1_3_path_Astar.png")
    '''

    [nodes, start, end] = convertToNodes(board_1_4)
    [img_1_4_Astar, sol_1_4_Astar] = A_star(nodes, start, end, img_1_4_Astar)
    colorSolution(sol_1_4_Astar, img_1_4_Astar, "board_1_4_path_Astar.png")


    [nodes, start, end] = convertToNodes(board_1_4)
    [img_1_4_dij, sol_1_4_dij] = dijkstra(nodes, start, end, img_1_4_dij)
    colorSolution(sol_1_4_dij, img_1_4_dij, "board_1_4_path_dij.png")

    [nodes, start, end] = convertToNodes(board_1_4)
    [img_1_4_BFS, sol_1_4_BFS] = BFS(nodes, start, end, img_1_4_BFS)
    colorSolution(sol_1_4_BFS, img_1_4_BFS, "board_1_4_path_BFS.png")


    #BOARD 2.1
    [nodes, start, end] = convertToNodes(board_2_1)
    [img_2_1_Astar, sol_2_1_Astar] = A_star(nodes, start, end, img_2_1_Astar)
    colorSolution(sol_2_1_Astar, img_2_1_Astar, "board_2_1_path_Astar.png")

    [nodes, start, end] = convertToNodes(board_2_1)
    [img_2_1_dij, sol_2_1_dij] = dijkstra(nodes, start, end, img_2_1_dij)
    colorSolution(sol_2_1_dij, img_2_1_dij, "board_2_1_path_dij.png")

    [nodes, start, end] = convertToNodes(board_2_1)
    [img_2_1_BFS, sol_2_1_BFS] = BFS(nodes, start, end, img_2_1_BFS)
    colorSolution(sol_2_1_BFS, img_2_1_BFS, "board_2_1_path_BFS.png")




    #BOARD 2.2
    #[nodes, start, end] = convertToNodes(board_2_2)
    #[img_2_2_Astar, sol_2_2_Astar] = A_star(nodes, start, end, img_2_2_Astar)
    #colorSolution(sol_2_2_Astar, img_2_2_Astar, "board_2_2_path_Astar.png")

    #[nodes, start, end] = convertToNodes(board_2_2)
    #[img_2_2_dij, sol_2_2_dij] = dijkstra(nodes, start, end, img_2_2_dij)
    #colorSolution(sol_2_2_dij, img_2_2_dij, "board_2_2_path_dij.png")

    #[nodes, start, end] = convertToNodes(board_2_2)
    #[img_2_2_BFS, sol_2_2_BFS] = BFS(nodes, start, end, img_2_2_BFS)
    #colorSolution(sol_2_2_dij, img_2_2_dij, "board_2_2_path_dij.png")


    #BOARD 2.3
    #[nodes, start, end] = convertToNodes(board_2_3)
    #[img_2_3_Astar, sol_2_3_Astar] = A_star(nodes, start, end, img_2_3_Astar)
    #colorSolution(sol_2_3_Astar, img_2_3_Astar, "board_2_3_path_Astar.png")

    #[nodes, start, end] = convertToNodes(board_2_3)
    #[img_2_3_dij, sol_2_3_dij] = dijkstra(nodes, start, end, img_2_3_dij)
    #colorSolution(sol_2_3_dij, img_2_3_dij, "board_2_3_path_dij.png")



    #BOARD 2.4
    #[nodes, start, end] = convertToNodes(board_2_4)
    #[img_2_4_Astar, sol_2_4_Astar] = A_star(nodes, start, end, img_2_4_Astar)
    #colorSolution(sol_2_4_Astar, img_2_4_Astar, "board_2_4_path_Astar.png")

    #[nodes, start, end] = convertToNodes(board_2_4)
    #[img_2_4_dij, sol_2_4_dij] = dijkstra(nodes, start, end, img_2_4_dij)
    #colorSolution(sol_2_4_dij, img_2_4_dij, "board_2_4_path_dij.png")

    #[nodes, start, end] = convertToNodes(board_2_4)
    #[img_2_4_BFS, sol_2_4_BFS] = BFS(nodes, start, end, img_2_4_BFS)
    #colorSolution(sol_2_4_BFS, img_2_4_BFS, "board_2_4_path_BFS.png")


if __name__ == "__main__":
	main()
