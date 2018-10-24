def printOut():
	getDual()
	nCost = 0
	print(' ' * 6, end=' ')
	for x in range(1, m + 1):
		colName = 'B' + str(x)
		print('{0:10}'.format(colName), end=' ')
	print('SUPPLY')
	for x in range(n):
		rowName = 'A' + str(x + 1)
		print('{0:6}'.format(rowName), end=' ')
		for y in range(m):
			nCost += aCost[x][y] * aRoute[x][y]
			if aRoute[x][y] == 0:
				print('[<%2i>%4i]' % (aCost[x][y], aDual[x][y]), end=' ')
			else:
				print('[<%2i>(%2i)]' % (aCost[x][y], aRoute[x][y] + 0.5), end=' ')
		print('%6i' % aSupply[x])
	print('DEMAND', end=' ')
	for x in range(m):
		print('%10i' % aDemand[x], end=' ')
	print('\nCost: ', nCost)
	print('Press ENTER to continue\n')
	input()
	

def northWest():
	''' The simplest method to get an initial solution.
	Not the most efficient'''
	global aRoute
	u = 0
	v = 0
	aS = [0] * m
	aD = [0] * n
	while u <= n - 1 and v <= m - 1:
		if aDemand[v] - aS[v] < aSupply[u] - aD[u]:
			z = aDemand[v] - aS[v]
			aRoute[u][v] = z
			aS[v]        += z
			aD[u]        += z
			v            += 1
		else:
			z = aSupply[u] - aD[u]
			aRoute[u][v] = z
			aS[v]        += z
			aD[u]        += z
			u            += 1


def allIsDistributed():
	global heap
	for i in range(len(aDemand)):
		if aDemand[i] > eps * 2:
			if i == len(aDemand) - 1:
			   heap = True
			return False
	for sup in aSupply:
		if sup > eps:
			return False
	return True


def minElementMethod():
	global aRoute
	while allIsDistributed() is False:
		min = float('inf')
		iMin = -1
		jMin = -1
		for i in range(len(aCost)):
			if aSupply[i] > 0:
				for j in range(len(aCost[i])):
					if aDemand[j] > 0:
						if ((aCost[i][j] < min) and (aCost[i][j] > 0)) or (heap is True):
							min = aCost[i][j]
							iMin = i
							jMin = j
		aRoute[iMin][jMin] = aDemand[jMin] if aDemand[jMin] < aSupply[iMin] else aSupply[iMin]
		aDemand[jMin] -= aRoute[iMin][jMin]
		aSupply[iMin] -= aRoute[iMin][jMin]


def notOptimal():
	global PivotN
	global PivotM
	nMax = -infinity
	getDual()
	for u in range(0, n):
		for v in range(0, m):
			x = aDual[u][v]
			if x > nMax:
				nMax = x
				PivotN = u
				PivotM = v
	return (nMax > 0)


def getDual():
	global aDual
	for u in range(0, n):
		for v in range(0, m):
			aDual[u][v] = -0.5 # null value
			if aRoute[u][v] == 0:
				aPath = findPath(u, v)
				z = -1
				x = 0
				for w in aPath:
					x += z * aCost[w[0]][w[1]]
					z *= -1
				aDual[u][v] = x

				
def findPath(u, v):
	aPath = [[u, v]]
	if not lookHorizontaly(aPath, u, v, u, v):
		print('Path error, press key', u, v)
		input()
	return aPath


def lookHorizontaly(aPath, u, v, u1, v1):
	for i in range(0, m):
		if i != v and aRoute[u][i] != 0:
			if i == v1:
				aPath.append([u, i])
				return True # complete circuit
			if lookVerticaly(aPath, u, i, u1, v1):
				aPath.append([u, i])
				return True
	return False # not found


def lookVerticaly(aPath, u, v, u1, v1):
	for i in range(0, n):
		if i != u and aRoute[i][v] != 0:
			if lookHorizontaly(aPath, i, v, u1, v1):
				aPath.append([i, v])
				return True
	return False # not found


def betterOptimal():
	global aRoute
	aPath = findPath(PivotN, PivotM)
	nMin = infinity
	for w in range(1, len(aPath), 2):
		t = aRoute[aPath[w][0]][aPath[w][1]]
		if t < nMin:
			nMin = t
	for w in range(1 , len(aPath), 2):
		aRoute[aPath[w][0]][aPath[w][1]]         -= nMin
		aRoute[aPath[w - 1][0]][aPath[w - 1][1]] += nMin


def correctSourceTable():
	global aSupply, aDemand, aCost
	sumSupply = 0
	sumDemand = 0

	for sup in aSupply:
		sumSupply += sup
	for dem in aDemand:
		sumDemand += dem

	if sumSupply > sumDemand:
		aDemand.append(sumSupply - sumDemand)
		for i in range(len(aCost)):
			aCost[i].append(0)


aCost = [[1, 2, 4]
		,[1, 3, 4]
		,[2, 2, 3]]

aDemand = [50, 60, 10]
aSupply = [90, 30, 40]

heap = False

correctSourceTable()

n = len(aSupply)
m = len(aDemand)
infinity = float('inf')

# add a small amount to prevent degeneracy
# degeneracy can occur when the sums of subsets of supply and demand equal
eps = 0.00001
for k in aDemand:
	k += eps / len(aDemand)
aSupply[1] += eps
# initialisation
aRoute = []
for x in range(n):
	aRoute.append([0] * m)
aDual = []
for x in range(n):
	aDual.append([-1] * m)

#northWest()
minElementMethod()

PivotN = -1
PivotM = -1
printOut()
# MAIN
while notOptimal():
	print('PIVOTING ON', PivotN, PivotM)
	betterOptimal()
	printOut()
print("FINISHED")
