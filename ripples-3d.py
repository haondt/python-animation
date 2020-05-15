import pygame, math, random, time
from pygame.locals import *


class App:
	def __init__(self):
		pygame.init()
		self.size = self.width, self.height = 1000, 1000
		self.screen = pygame.display.set_mode([self.width, self.height])
		self.running = False
		self.colors = ((157,205,155),(0,0,48),(99,154,170))
		self.angle = 0.5
		self.clock = pygame.time.Clock()
		self.saveframes = False # set to true to save one round of frames to /tmp
		self.framecount = 0
		self.firstRectHeight = None


		self.rectColor = (0, 0, 255)
		self.numRects = 15
		self.rectMinHeight = 200
		self.rectWidth = ((self.width - 200) // self.numRects)
		self.rectMaxHeight = self.height-100-self.numRects*self.angle*self.rectWidth
		self.x = 0
		self.old_time = time.time()
		self.rects = [[0 for i in range(self.numRects)] for j in range(self.numRects)]
		self.locationMap = self.makeLocationMap()
		self.Rects = self.initRects()
		self.drawOrder = []
		for row in self.makeIndexMap():
			for col in row:
				self.drawOrder.append(col)

	def initRects(self):
		return [[Rect(self.locationMap[i][j],
			self.rectWidth,
			self.colors,
			self.rectMinHeight,
			self.rectMaxHeight,
			self.angle,
			(self.get1DScaleVale(i,self.numRects)+self.get1DScaleVale(j,self.numRects))/2)
			for j in range(self.numRects)]
			for i in range(self.numRects)]

	def makeIndexMap(self):
		"""
		Create a matrix that maps indexes in the diagonal (angled) matrix to
		positions in the square (2d) matrix
		:return:
		"""
		n = self.numRects
		halfList = [[(j,n-1-i+j) for j in range(i+1)] for i in range(n)]
		fullList = halfList + [[(j[1],j[0]) for j in i] for i in halfList[n-2::-1]]
		return fullList

	def makeLocationMap(self):
		"""
		Create a square (2d) matrix of xy coordinates based on the diagonal mapping
		:return:
		"""
		locationMap = [[(0,0) for i in range(self.numRects)] for j in range(self.numRects)]
		startTop = 0.5*(self.height-self.numRects*self.angle*self.rectWidth)
		startLeft = (self.width/2)-(self.numRects/2)*self.rectWidth
		for row in enumerate(self.makeIndexMap()):
			for col in row[1]:
				locationMap[col[0]][col[1]] = \
					(startLeft+(col[0]+col[1])*self.rectWidth/2,
					startTop+(row[0]+1)*0.5*self.angle*self.rectWidth)
		return locationMap



	def start(self):
		self.running = True
		while self.running:
			for event in pygame.event.get():
				self.handleEvent(event)

			self.onFlip()

			pygame.display.flip()

	def handleEvent(self, event):
		if event.type == pygame.QUIT:
			self.running = False

	def onFlip(self):
		self.clock.tick(60)
		self.screen.fill((255, 255, 255))

		self.drawRects()
		self.updateRects()
		if self.saveframes:
			frh = round(self.Rects[0][0].getHeight())
			if self.firstRectHeight == None:
				self.firstRectHeight = frh
			elif self.firstRectHeight == frh:
				self.saveframes = False
			else:
				pygame.image.save(self.screen, "tmp/frame_{}.png".format(self.framecount))
				self.framecount += 1

		#self.drawSquares()
		#self.set2DScaleVals()

	def drawRects(self):
		for index in self.drawOrder:
			self.Rects[index[0]][index[1]].draw((self.screen))

	def updateRects(self):
		for index in self.drawOrder:
			self.Rects[index[0]][index[1]].step()


	def _drawRects(self, numRects):
		offset = 0
		rects = []
		if numRects % 2 != 0:
			# draw rect in center
			centerRect = Rect(self.width / 2 - self.rectWidth/2,
				(self.height - self.rectMaxHeight)/ 2,
				self.rectWidth,
				self.rectMaxHeight)
			rects.append(centerRect)
			numRects -= 1
			offset += self.rectWidth
		else:
			offset += self.rectWidth /2

		for i in range(numRects//2):
			leftRect = Rect(self.width/2-offset-self.rectWidth/2,
				(self.height - self.rectMaxHeight)/2,
				self.rectWidth,
				self.rectMaxHeight)
			rightRect = Rect(self.width//2+offset-self.rectWidth/2,
				(self.height - self.rectMaxHeight)/2,
				self.rectWidth,
				self.rectMaxHeight)
			rects.append(leftRect)
			rects.append(rightRect)
			offset += self.rectWidth
		rects = sorted(rects, key=lambda r: r.left)



		for rect in enumerate(rects):
			heightScaler = self.get1DScaleVal(rects[0], self.numRects)
			height = self.rectMinHeight + \
				(heightScaler*(self.rectMaxHeight-self.rectMinHeight))
			rect[1].top = rect[1].top + (self.rectMaxHeight /2) -height / 2
			rect[1].height = height
			rect[1].left -= self.rectWidth *0.5*rect[0]
			rect[1].top += self.angle*self.rectWidth*rect[0]*0.5


			#rect[1].top += int(self.rectMaxHeight * -xVal + self.rectMinHeight)
			#rect[1].height = self.rectMaxHeight * xVal + self.rectMinHeight - rect[1].top
			#pygame.draw.rect(self.screen,
			#	tuple(random.randrange(256) for i in range(3)), rect[1])
			self.drawRect(rect[1].top, rect[1].left,rect[1].width, rect[1].height)
			#pygame.draw.rect(self.screen, (0,0,255), rect[1])
		self.x -= 0.0013*1.5

	def _get1DScaleVal(self,pos, numRects):
		scaler = math.pi / (numRects*2 - 1)
		v = abs(pos - ((numRects-1)/2))*2
		xv = v *2*scaler-math.pi+math.pi*self.x
		hS = (math.cos(xv)/1.75 +1)/2
		return hS

	def get1DScaleVale(self,pos,numRects):
		# Return a scale along a circular path
		#return math.sqrt(1-abs(1-pos/((numRects-1)/2))**2)
		# Return a scale along a sine wave path
		return 0.5 -0.5*math.cos(pos/((numRects-1)/(2*math.pi)))


	def _set2DScaleVals(self):
		self.x -= 0.0013*20
		self.rects = [[0 for i in range(self.numRects)] for j in range(self.numRects)]
		for col in range(self.numRects):
			for row in range(self.numRects):
				self.rects[row][col] += self.get1DScaleVal(col,self.numRects)/2
				self.rects[col][row] += self.get1DScaleVal(col,self.numRects)/2

	def scaleToRectHeight(self,x):
		return self.rectMinHeight + x*(self.rectMaxHeight-self.rectMinHeight)

	def drawSquares(self):
		for r in self.makeIndexMap():
			for c in r:
				row,col = c
				pos = self.locationMap[row][col]
				rectHeight = self.scaleToRectHeight(self.rects[row][col])
				top = pos[1]-rectHeight/2

				self.drawRect(top,pos[0],self.rectWidth,rectHeight)




class Rect:
	def __init__(self, pos, width, colors, minHeight, maxHeight,angle,ossPoint=0.0):
		self.pos = pos
		self.colors = colors
		self.minHeight = minHeight
		self.maxHeight = maxHeight
		self.width = width
		self.ossPoint = ossPoint
		self.ossRate = 0.0125/1.5
		self.angle = angle


	def getHeight(self):
		return self.minHeight + self.ossPoint*(self.maxHeight-self.minHeight)

	def getAccelerationMultiplier(self):
		mode = 2
		x = self.getHeight()
		m = self.minHeight
		M = self.maxHeight
		scaleMax = 4
		if mode == 0:
			# compute the multiplier as a sine wave
			return (scaleMax+1)/2-math.cos((x-m)/((M-m)/(2*math.pi)))*((scaleMax-1)/2)
		elif mode == 1:
			# compute the multiplier as a semicircle
			return math.sqrt((1-abs(1-((x-m)/((M-m)/2)))**2))+1
		elif mode == 2:
			# compute the multiplier as a triangle
			return (scaleMax-1)*math.sqrt(1-((abs(((M-m)/2)-(x-m)))/((M-m)/2))**2)+1
		else:
			return None

	def step(self):
		self.ossPoint += self.ossRate*self.getAccelerationMultiplier()
		if(self.ossPoint > 1):
			self.ossPoint = 1.0
			self.ossRate *= -1
		elif(self.ossPoint < 0):
			self.ossPoint = 0.0
			self.ossRate *= -1



	def draw(self, canvas):
		"""
		Add a tilted rectangle to the canvas at the specified coordinates
		:param top: y-value of top left point
		:param left: x-value of top left point
		:param width: width of rectangle
		:param height: height of rectangle (length of side straight edge)
		:return: none
		"""

		left = self.pos[0]
		width = self.width
		height = self.getHeight()
		top = self.pos[1] - height/2

		# outline perimeter
		x = 0.5 * self.angle * width
		A = (left, top)
		C = (left, top + height)
		E = (left + 0.5 * width, top + height + x)
		D = (left + width, C[1])
		B = (left + width, top)
		F = (left + 0.5 * width, top + x)
		G = (left + 0.5 * width, top - x)

		# define points of 3 shapes
		left_p = (A, C, E, F)
		right_p = (E, D, B, F)
		top_p = (B, G, A, F)

		# draw shapes
		for i in range(3):
			pygame.draw.polygon(canvas, self.colors[i], [left_p, right_p, top_p][i])
			pygame.draw.aalines(canvas, self.colors[i], True, [left_p, right_p, top_p][i])


if __name__ == "__main__":
	app = App()
	app.start()
