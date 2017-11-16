import collections,random,math,time,numpy
import cPickle as pickle
'''
Author : Aditya Sundaram

'''

class LizardBFSState(object): #Class to represent the state for BFS/DFS algorithms
	def __init__(self,board,lizardsLeft,lizards,n,row,rowMapOfLizards,colMapOfLizards,posdiagMapOfLizards,negdiagMapOfLizards):
		self.board = board
		self.size = n
		self.lizardsLeft = lizardsLeft
		self.row = row
		self.rowMapOfLizards = rowMapOfLizards
		self.colMapOfLizards = colMapOfLizards
		self.posdiagMapOfLizards = posdiagMapOfLizards
		self.negdiagMapOfLizards = negdiagMapOfLizards
		self.hashKey = None

	#To ensure that the queen being placed does not clash with previous placed Lizards
	def checkValid(self,i,j):
		if(self.board[i][j] == 2 or self.board[i][j] == 1):
			return False

		if j in self.colMapOfLizards:
			if j in treeColMap:
				queenx,queeny = self.colMapOfLizards[j][-1]
				possArray = []
				for x in treeColMap[j]:
					if x[0] < i and x[0] > queenx:
						possArray.append((x[0],x[1]))
				if len(possArray) == 0:
					return False

			else:
				return False

		if i in self.rowMapOfLizards:
			if i in treeRowMap:
				queenx,queeny = self.rowMapOfLizards[i][-1]
				possArray = []
				for x in treeRowMap[i]:
					if x[1] < j and x[1] > queeny:
						possArray.append((x[0],x[1]))
				if len(possArray) == 0:
					return False
			else:
				return False

		if i-j in self.posdiagMapOfLizards:
			if i-j in treePosDiagMap:
				queenx,queeny = self.posdiagMapOfLizards[i-j][-1]
				possArray = []
				for x in treePosDiagMap[i-j]:
					if x[1] < j and x[1] > queeny and x[0] < i and x[0] > queenx:
						possArray.append((x[0],x[1]))
				if len(possArray) == 0:
					return False
			else:
				return False

		if i+j in self.negdiagMapOfLizards:
			if i+j in treeNegDiagMap:
				queenx,queeny = self.negdiagMapOfLizards[i+j][-1]
				possArray = []
				for x in treeNegDiagMap[i+j]:
					if x[1] > j and x[1] < queeny and x[0] < i and x[0] > queenx:
						possArray.append((x[0],x[1]))
				if len(possArray) == 0:
					return False

			else:
				return False
		return True

	#Check if we have obtained a goal state
	def checkGoalState(self):
		if(self.lizardsLeft == 0):
			return True
		else:
			return False

	#Adding Lizards to board
	def addLizardToBoard(self, i, j):
		self.board[i][j] = 1
		if i not in self.rowMapOfLizards:
			self.rowMapOfLizards[i] = []
		self.rowMapOfLizards[i].append([i,j])
		if j not in self.colMapOfLizards:
			self.colMapOfLizards[j] = []
		self.colMapOfLizards[j].append([i,j])
		if i-j not in self.posdiagMapOfLizards :
			self.posdiagMapOfLizards[i-j] = []
		self.posdiagMapOfLizards[i-j].append([i,j])
		if i+j not in self.negdiagMapOfLizards:
			self.negdiagMapOfLizards[i+j] = []
		self.negdiagMapOfLizards[i+j].append([i,j])

	#Print the board This was specifically for debugging
	def printNursery(self):
		print self.board

	#Check if row has valid positions
	def canPlaceLizardsAfterMe(self, x, y):
		for i in range(y,self.size):
			if self.board[x,i] == 2 and i!=n-1 and self.board[x,i+1] == 0:
				return i+1
		return None

	#Expand node with possible moves
	def expandNearestNeighbours(self,currentRow):
		validMoves = []
		if self.row is None:
			validMoves=list()
		else:
			i = self.row
			j = self.rowMapOfLizards[self.row][-1][1]
			nextLocation = self.canPlaceLizardsAfterMe(i, j)

			if nextLocation is not None:
				for y in range(nextLocation,n):
					if(self.checkValid(i,y)):
						newState = pickle.loads(pickle.dumps(self,-1))
						newState.addLizardToBoard(i, y)
						newState.lizardsLeft = newState.lizardsLeft - 1
						newState.row = self.row
						newState.hashKey = hash((newState.board.ravel().tostring(), newState.row))
						validMoves.append(newState)

		row = currentRow
		while row < n:
			validCols = []
			for i in range(n):
				if(self.checkValid(row,i)):
					validCols.append(i)
			if len(validCols) == 0:
				row = row + 1
				continue
			else:
				for i in validCols:
					newState = pickle.loads(pickle.dumps(self,-1))
					#x = copy.deepcopy(current)
					newState.addLizardToBoard(row, i)
					#x.printNursery()
					#inx = raw_input("Enter something to continue")
					newState.lizardsLeft = newState.lizardsLeft -1
					newState.row = row
					newState.hashKey = hash((newState.board.ravel().tostring(), newState.row))
					validMoves.append(newState)
				break
		return validMoves

#Write to file
def PrintBoard(current, n):
	with open('output.txt', 'w') as out:
		out.write("OK\r\n")
		for i in range(n):
			line = ""
			for j in range(n):
				line = line + str(current.board[i][j])
			out.write(line + '\r\n')
	out.close()
	return

#Write fail to file
def PrintFail():
	with open('output.txt', 'w') as output_file:
		output_file.write("FAIL\r\n")
	exit(0)

#Push into Queue basis algorithm
def pushNeighbour(algo, node, queue, visited):
	if algo == "DFS":
		if node.hashKey not in visited:
			queue.appendleft(node)
			visited[node.hashKey] = 1
	else:
		if node.hashKey not in visited:
			queue.append(node)
			visited[node.hashKey] = 1

#Solve BFS/DFS
def solve(lizLeft,row,col,board,n,algo,end_time):
	queue = collections.deque()
	initState = LizardBFSState(board,lizLeft,{},n,None,{},{},{},{})
	initState.hashKey = hash((initState.board.ravel().tostring(), initState.row))
	count = 0
	queue.append(initState)
	visited = {}
	visited[initState.hashKey] = 1
	while queue:
		current = queue.popleft()
		count = count + 1
		#current.printNursery()
		#raw_input("")
		#if count%100000 == 0:
		#print "Reached iteration " + str(count) + " and at level " + str(current.row)
		if current.checkGoalState():
			PrintBoard(current, n)
			return True
		now_time = time.time()
		if now_time > end_time:
			PrintFail()
		rowRightNow = 0
		if len(current.rowMapOfLizards) == 0:
			rowRightNow = 0
		else:
			rowRightNow = len(current.rowMapOfLizards)
		Neighbours = current.expandNearestNeighbours(rowRightNow)
		for node in Neighbours:
			pushNeighbour(algo, node, queue, visited)

	with open('output.txt', 'w') as output_file:
		output_file.write("FAIL\r\n")

#Print board for SA
def printBoard(current,n):
	with open('output.txt', 'w') as out:
		out.write("OK\r\n")
		for i in range(n):
			line = ""
			for j in range(n):
				line = line + str(current.board[i][j])
			out.write(line + '\r\n')
	out.close()

#Print fail for SA
def printFail():
	with open('output.txt', 'w') as output_file:
		output_file.write("FAIL\r\n")

#Initialize the board randomly
def initialize(board,lizards,n,rowMap,colMap,posDiagMap,negDiagMap,lizardsArray):
	numLeft = lizards
	rows = range(n)
	cols = range(n)
	while numLeft:
		x = random.choice(rows)
		y = random.choice(cols)
		if board[x][y]!=2 and board[x][y]!=1:
			board[x][y]=1
			if x not in rowMap:
				rowMap[x] = []
			if y not in colMap:
				colMap[y] = []
			if x-y not in posDiagMap:
				posDiagMap[x-y] = []
			if x+y not in negDiagMap:
				negDiagMap[x+y] = []
			rowMap[x].append((x,y))
			colMap[y].append((x,y))
			posDiagMap[x-y].append((x,y))
			negDiagMap[x+y].append((x,y))
			lizardsArray.append((x,y))
			numLeft = numLeft - 1
	return board

#Class that represents the state for Simulated Annealing
class SA(object):
	def __init__(self,board,rowMap,colMap,posDiagMap,negDiagMap,lizardsArray):
		self.board = board
		self.rowMap = rowMap
		self.colMap = colMap
		self.posDiagMap = posDiagMap
		self.negDiagMap = negDiagMap
		self.lizardsArray = lizardsArray

	#Count conflicts for a given queen
	def checkConflicts(self,i,j):
		countConflicts = 0
		if j in self.colMap:
			if len(self.colMap[j]) >1 and j in treeColMap:
				queenList = [x for x in self.colMap[j] if x[0] > i]
				for queen in queenList:
					possArray = []
					for x in treeColMap[j]:
						if x[0] > i and x[0] < queen[0]:
							possArray.append((x[0],x[1]))
					if len(possArray) == 0:
						countConflicts = countConflicts + 1
			if len(self.colMap[j]) >1 and j not in treeColMap:
				countConflicts = countConflicts + len([x for x in self.colMap[j] if x[0] > i])


		if i in self.rowMap:
			if len(self.rowMap[i]) > 1 and i in treeRowMap:
				queenList = [x for x in self.rowMap[i] if x[1] > j]
				for queen in queenList:
					possArray = []
					for x in treeRowMap[i]:
						if x[1] > j and x[1] < queen[1]:
							possArray.append((x[0],x[1]))
					if len(possArray) == 0:
						countConflicts = countConflicts + 1
			if len(self.rowMap[i]) > 1 and i not in treeRowMap:
				countConflicts = countConflicts + len([x for x in self.rowMap[i] if x[1] > j])

		if i-j in self.posDiagMap:
			if len(self.posDiagMap[i-j])>1 and i-j in treePosDiagMap:
				queenList = [x for x in self.posDiagMap[i-j] if x[1] > j and x[0] > i]
				for queen in queenList:
					possArray = []
					for x in treePosDiagMap[i-j]:
						if x[1] > j and x[1] < queen[1] and x[0] > i and x[0] < queen[0]:
							possArray.append((x[0],x[1]))
					if len(possArray) == 0:
						countConflicts = countConflicts + 1
			if len(self.posDiagMap[i-j])>1 and i-j not in treePosDiagMap:
				countConflicts = countConflicts + len([x for x in self.posDiagMap[i-j] if x[1] > j and x[0] > i])

		if i+j in self.negDiagMap:
			if len(self.negDiagMap[i+j]) > 1 and i+j in treeNegDiagMap:
				queenList = [x for x in self.negDiagMap[i+j] if x[1] > j and x[0] < i]
				for queen in queenList:
					possArray = []
					for x in treeNegDiagMap[i+j]:
						if x[1] > j and x[1] < queen[1] and x[0] < i and x[0] > queen[0]:
							possArray.append((x[0],x[1]))
					if len(possArray) == 0:
						countConflicts = countConflicts + 1
			if len(self.negDiagMap[i+j]) > 1 and i+j not in treeNegDiagMap:
				countConflicts = countConflicts + len([x for x in self.negDiagMap[i+j] if x[1] > j and x[0] < i])

		return countConflicts

	#Count all conflicst for the board
	def checkCollisions(self):
		collisions = 0
		row = 0
		while row < n:
			lizardsInThisRow = []
			if row in self.rowMap:
				lizardsInThisRow = self.rowMap[row]
			if len(lizardsInThisRow) > 0:
				for ele in lizardsInThisRow:
					collisions = collisions + self.checkConflicts(ele[0],ele[1])
			row = row + 1
		return collisions

#Check if a wrong move is possible at current temperature
def canAcceptMove(threshold):
	val = random.uniform(0,1)
	if val <= threshold:
		return True
	else:
		return False

#Generate a random move for a randomly picked queen
def makeRandomMove(currentState):
	newState = pickle.loads(pickle.dumps(currentState,-1))
	LizardsList = newState.lizardsArray

	while True:
		x,y = random.choice(LizardsList)
		x1 = random.choice(range(n))
		y1 = random.choice(range(n))
		if (newState.board[x1][y1] == 1 or newState.board[x1][y1] == 2):
			continue
		elif(x!=x1 and y!=y1):
			#print "Moving from " + str(x) + "," + str(y) + " ->" + str(x1) + "," + str(y1)
			newState.board[x][y] = 0
			newState.board[x1][y1] = 1
			newState.rowMap[x].remove((x,y))
			if len(newState.rowMap[x]) == 0:
				del newState.rowMap[x]
			if x1 not in newState.rowMap:
				newState.rowMap[x1] = []
			newState.rowMap[x1].append((x1,y1))
			newState.colMap[y].remove((x,y))
			if len(newState.colMap[y]) == 0:
				del newState.colMap[y]
			if y1 not in newState.colMap:
				newState.colMap[y1] = []
			newState.colMap[y1].append((x1,y1))
			newState.posDiagMap[x-y].remove((x,y))
			if len(newState.posDiagMap[x-y]) == 0:
				del newState.posDiagMap[x-y]
			if x1-y1 not in newState.posDiagMap:
				newState.posDiagMap[x1-y1] = []
			newState.posDiagMap[x1-y1].append((x1,y1))
			newState.negDiagMap[x+y].remove((x,y))
			if len(newState.negDiagMap[x+y]) == 0:
				del newState.negDiagMap[x+y]
			if x1+y1 not in newState.negDiagMap:
				newState.negDiagMap[x1+y1] = []
			newState.negDiagMap[x1+y1].append((x1,y1))
			newState.lizardsArray.remove((x,y))
			newState.lizardsArray.append((x1,y1))
			return newState
		else:
			continue

#Solve board by Simulated Annealing
def solveSA(board,n,lizards,end_time):
	rowMap =  {}
	colMap = {}
	posDiagMap = {}
	negDiagMap = {}
	lizardsArray = []
	Temperature = 5000000
	board = initialize(board,lizards,n,rowMap,colMap,posDiagMap,negDiagMap,lizardsArray)
	currentboard = SA(board,rowMap,colMap,posDiagMap,negDiagMap,lizardsArray)
	iterCount = 0
	while True:
		currentCollisions = currentboard.checkCollisions()
		print str(Temperature) + "---> "  + str(currentCollisions)
		#print iterCount
		#print currentboard.board
		#raw_input("")
		if currentCollisions == 0:
			#print currentboard.board
			printBoard(currentboard,n)
			break
		now_time = time.time()
		if now_time > end_time:
			with open('output.txt', 'w') as  output_file:
				output_file.write("FAIL\r\n")
			exit(0)
		newboard = makeRandomMove(currentboard)
		newCollisions = newboard.checkCollisions()
		if newCollisions < currentCollisions:
			currentboard = newboard
		else:
			theta = math.exp((-(newCollisions-currentCollisions))/Temperature)
			if canAcceptMove(theta):
				currentboard = newboard
			#print "Accepted"
			#print theta
		Temperature = 1/math.log((n+lizards),2)
		iterCount = iterCount + 1
		if Temperature < 0:
			printFail()
			break
		else:
			continue


#Input file
with open('input.txt') as f:
	lines = f.readlines()


#Process input and call algorithms

algo = lines[0].strip('\n')
n = int(lines[1].strip('\n'))
queens = int(lines[2].strip('\n'))
board=numpy.empty(shape=(n,n))
treeRowMap = {}
treeColMap = {}
treePosDiagMap = {}
treeNegDiagMap = {}
for i in range(n):
	for j in range(n):
		board[i][j] = int(lines[i+3][j])
		if(board[i][j] == 2):
			if i not in treeRowMap:
				treeRowMap[i] = []
			if j not in treeColMap:
				treeColMap[j] = []
			if i-j not in treePosDiagMap:
				treePosDiagMap[i-j] = []
			if i+j not in  treeNegDiagMap:
				treeNegDiagMap[i+j] = []
			treeRowMap[i].append([i,j])
			treeColMap[j].append([i,j])
			treePosDiagMap[i-j].append([i,j])
			treeNegDiagMap[i+j].append([i,j])

board = board.astype(int)
start_time = time.time()
end_time = start_time + 275
if algo=="BFS" or algo == "DFS":
	output = solve(queens,0,0,board,n,algo,end_time)
elif algo == "SA":
	output = solveSA(board,n,queens,end_time)
#print output

