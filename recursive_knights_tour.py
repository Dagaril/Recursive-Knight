import turtle, datetime

#Array format: [luu,ruu,ldd,rdd,lld,rrd,llu,rru]

#Define board size and starting location
boardSize = 20
startX = 1
startY = 1

reqdClsdTr = True

if boardSize%2==1 and reqdClsdTr:
	print("Can't have closed tour with odd board width and height,"+"\nCONTINUING TO LOOK FOR OPEN TOUR")
	reqdClsdTr =False
	
def _main_():
	print(datetime.datetime.now())
	a,b,c,path=_move_(startX,startY,[])
	print(datetime.datetime.now())
	print(path)
	if len(path)>1:
		_draw_(path)
	return

def _draw_(path):
	initTurtle()
	stampColor(path[0][0],path[0][1],1)
	for i in range(1,len(path)-1):
		stampAt(path[i][0],path[i][1],i+1)
	stampColor(path[len(path)-1][0],path[len(path)-1][1],len(path))

def initTurtle():
	global sqSize, fontSize
	turtle.setup(1000,1000,0,0)
	turtle.title("Knight's Tour")
	turtle.setworldcoordinates(0,1000,1000,0)
	turtle.ht()
	turtle.pen(pensize=3)
	turtle.speed(0)
	sqSize=turtle.window_height()/(boardSize)
	for r in range(0,boardSize+1): #draw horizontal rows
		goto(-2,r*sqSize-2)
		drto(boardSize*sqSize+0,r*sqSize-2)
	for c in range(0,boardSize+1): #draw vertical columns
		goto(c*sqSize-2,0)
		drto(c*sqSize-2,boardSize*sqSize+0)
	if boardSize>25:
		fontSize=10
	else:
		fontSize=16
	
def goto(x,y):
	turtle.pu()
	turtle.goto(x,y)
	turtle.pd()
	
def drto(x,y):
	turtle.goto(x,y)
	
def stampAt(c,r,step):
	goto(c*sqSize-sqSize/2,(boardSize-r+1)*sqSize-sqSize/3)
	turtle.write(step, False, "center", ("Arial",fontSize,"normal"))

def stampColor(c,r,step):
	goto(c*sqSize-sqSize/2,(boardSize-r+1)*sqSize-sqSize/3)
	turtle.pencolor("red")
	turtle.write(step, False, "center", ("Arial",fontSize,"normal"))
	turtle.pencolor("black")
   
#moves from parameter x,y to returned x,y
#return 0 = hit dead end
#return -1 = hit final condition
def _move_(x,y,prevLocs):
	prevLocs.append([x,y])
	possDirs=_findPossMoves_(x,y,prevLocs)
	movesInDir=_numInDir_(possDirs,x,y,prevLocs)
	for element in possDirs:
		if(len(prevLocs)==1):
			print(x,y,movesInDir)
		if sum(movesInDir)==0: #dead end
			if len(prevLocs)==boardSize**2-1: #skip final move and go down stack
				finalMove=possDirs.index(min(x for x in possDirs if x > 0))
				newX,newY=directionsDict(finalMove,x,y)
				if not reqdClsdTr:
					prevLocs.append([newX,newY])
					return -1,newX,newY,prevLocs
				else: #check for successful closed loop
					if _checkClosedTour_(newX,newY): #if a closed loop, finish
						prevLocs.append([newX,newY])
						return -1,newX,newY,prevLocs
					else: #not closed loop, treat as dead end
						prevLocs=prevLocs[:-1]
						x=prevLocs[len(prevLocs)-1][0]
						y=prevLocs[len(prevLocs)-1][1]
						return 0,x,y,prevLocs
#                       print([x,y], "is a dead end")
			if(len(prevLocs)==1):
				if(sum(movesInDir)==0):
					return 0,x,y,["NO SOLUTION"]
			else:
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

def _checkClosedTour_(x,y):
	for i in range(0,8):
		tempX,tempY=directionsDict(i,x,y)
		if tempX==startX and tempY==startY:
			return True
	return False
_main_()
