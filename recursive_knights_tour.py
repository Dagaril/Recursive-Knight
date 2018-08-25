#import pygame

#Array format: [luu,ruu,ldd,rdd,lld,rrd,llu,rru]

#Define board size and starting location
boardSize = 5
startX = 1
startY = 5

def _debug_():
	x=1
	y=5
	a,b,c,path=_move_(x,y,[])
	print(path)
	return

	
def _main_():
	return
'''
#moves from parameter x,y to returned x,y
def _move_(x,y,prevLocs):
	possDirections = _findPossMoves_(x,y,prevLocs)
	if sum(possDirections)==0:#dead end
		print(str(x)+","+str(y)+" is a dead end")
		return 0,prevLocs
	if len(prevLocs)==boardSize**2: #final condition
		return -1,prevLocs
	prevLocs.append([x,y])
	numMovesInDir=_numInDir_(possDirections,x,y,prevLocs)
	for i in range(len(possDirections)):
		if sum(possDirections)==0:#dead end
			print(str(x)+","+str(y)+" is a dead end")
			prevLocs=prevLocs[:-1]
			return 0,prevLocs
		minI=numMovesInDir.index(min(x for x in numMovesInDir if x > 0))
		x,y=directionsDict(minI,x,y)
		print([x,y])
		possDirections[minI],prevLocs=_move_(x,y,prevLocs)
		if possDirections[minI]==0:
			numMovesInDir[minI]=0
			x=prevLocs[len(prevLocs)-1][0]
			y=prevLocs[len(prevLocs)-1][1]
		if possDirections[minI]==-1:
			break

	print("FINISHED",prevLocs)
'''
		
#moves from parameter x,y to returned x,y
#return 0 = hit dead end
#return -1 = hit final condition
def _move_(x,y,prevLocs):
	prevLocs.append([x,y])
	print([x,y])
	if len(prevLocs)==boardSize**2: #final condition
		return -1,x,y,prevLocs
	possDirs=_findPossMoves_(x,y,prevLocs)
	movesInDir=_numInDir_(possDirs,x,y,prevLocs)
	for element in possDirs:
		if sum(movesInDir)==0: #dead end
			if len(prevLocs)==boardSize**2-1:
				finalMove=possDirs.index(min(x for x in possDirs if x > 0))
				newX,newY=directionsDict(finalMove,x,y)
				movesInDir[finalMove],x,y,prevLocs=_move_(newX,newY,prevLocs)
				return -1,x,y,prevLocs
			print([x,y], "is a dead end")
			prevLocs=prevLocs[:-1]
			x=prevLocs[len(prevLocs)-1][0]
			y=prevLocs[len(prevLocs)-1][1]
			return 0,x,y,prevLocs
	
		dirWMinMoves=movesInDir.index(min(x for x in movesInDir if x > 0))
		newX,newY=directionsDict(dirWMinMoves,x,y)
		movesInDir[dirWMinMoves],x,y,prevLocs=_move_(newX,newY,prevLocs)
		if movesInDir[dirWMinMoves]==-1:
			return -1,x,y,prevLocs
	
	
#returns array of legal directions to move in excluding
#ones that would return to location that was previously touched 
def _findPossMoves_(x,y,prevLocs):
	retArr=[0,0,0,0,0,0,0,0]
	#x-1 y+2        #x+1 y+2
	if y+2<=boardSize:
		if x-1 >0:
			retArr[0]=1 #luu
		if x+1 <=boardSize:
			retArr[1]=1 #ruu
	#x-1 y-2        #x+1 y-2
	if y-2>0:
		if x-1>0:
			retArr[2]=1 #ldd
		if x+1<=boardSize:
			retArr[3]=1 #rdd
	#x-2 y-1        #x+2 y-1
	if y-1>0:
		if x-2>0:
			retArr[4]=1 #lld
		if x+2<=boardSize:
			retArr[5]=1 #rrd
	#x-2 y+1        #x+2 y+1
	if y+1<=boardSize:
		if x-2>0:
			retArr[6]=1 #llu
		if x+2<=boardSize:
			retArr[7]=1 #rru
	retArr = _removePrevious_(x,y,retArr,prevLocs)
	return retArr
	

#checks all surrounding possible moves, and removes the ones that would
#return knight to a previous location
#arr is array of directions in format [luu,ruu,ldd,rdd,lld,rrd,llu,rru]
def _removePrevious_(x,y, arr, prevLocs):
	if arr[0] ==1 and [x-1,y+2] in prevLocs:
		arr[0]=0
	if arr[1]==1 and [x+1,y+2] in prevLocs:
		arr[1]=0
	if arr[2]==1 and [x-1,y-2] in prevLocs:
		arr[2]=0
	if arr[3]==1 and [x+1,y-2] in prevLocs:
		arr[3]=0
	if arr[4]==1 and [x-2,y-1] in prevLocs:
		arr[4]=0
	if arr[5]==1 and [x+2,y-1] in prevLocs:
		arr[5]=0
	if arr[6]==1 and [x-2,y+1] in prevLocs:
		arr[6]=0
	if arr[7]==1 and [x+2,y+1] in prevLocs:
		arr[7]=0
	return arr


#looks at all legal nearby cells and returns array of 
#the number possible moves from every legal cell
def _numInDir_(dirs,x,y, prevLocs):
	retArr=[]
	for element in dirs:
		retArr.append(element)
	for i in range(len(dirs)):
		if(dirs[i]==1):
			newX,newY=directionsDict(i,x,y)
			retArr[i]=sum(_findPossMoves_(newX,newY,prevLocs))
	return retArr


#Input index of directions array, x, and y
#Return updated x and y based on that index
def directionsDict(index,x,y):
	if(index==0):
		return x-1,y+2
	elif(index==1):
		return x+1,y+2
	elif(index==2):
		return x-1,y-2
	elif(index==3):
		return x+1,y-2
	elif(index==4):
		return x-2,y-1
	elif(index==5):
		return x+2,y-1
	elif(index==6):
		return x-2,y+1
	elif(index==7):
		return x+2,y+1
	
_debug_()
