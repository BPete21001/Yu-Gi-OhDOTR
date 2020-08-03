# Import and initialize the pygame library
import pygame
from copy import copy, deepcopy
pygame.font.init()
from random import randint

FONT = pygame.font.SysFont("Segoe UI Semibold", 20)
SOFT_BLACK = (34, 38, 41)
BLACK = (0, 0, 0)
BROWN = (210, 180, 140)
DARK_BROWN = (101, 67, 33)
Blue = (135, 206, 250)
Red = (255, 72, 81)
YELLOW = (255, 255, 0)
GREY = (133, 144, 170)
red = (200, 0, 0)
GREEN = (56, 173, 56)
DARK_BLUE = (0, 0, 255)

class Card(object):
	def __init__(self, name, activeXPos, activeYPos, previewXPos, previewYPos, previousXPos, previousYPos, canMove, owner, face, previewFace, mode, idNum):
		self.name = name
		self.activeXPos = activeXPos
		self.activeYPos = activeYPos
		self.previewXPos = previewXPos
		self.previewYPos = previewYPos
		self.previousXPos = previousXPos
		self.previousYPos = previousYPos
		self.canMove = canMove
		self.owner = owner
		self.face = face
		self.previewFace = previewFace
		self.mode = mode
		self.idNum = idNum

class Player(object):
	def __init__(self, name, color, lifePoints):
		self.name = name
		self.color = color
		self.lifePoints = lifePoints
	def search(self):
		return "Player"

class Leader(Card):
	def __init__(self, name, activeXPos, activeYPos, previewXPos, previewYPos, previousXPos, previousYPos, canMove, owner, face, previewFace, mode, idNum, canSummon):
		super().__init__(name, activeXPos, activeYPos, previewXPos, previewYPos, previousXPos, previousYPos, canMove, owner, face, previewFace, mode, idNum)
		self.canSummon = canSummon
	def search(self):
		return "Leader"

class Monster(Card):
	def __init__(self, name, activeXPos, activeYPos, previewXPos, previewYPos, previousXPos, previousYPos, canMove, 
			owner, face, previewFace, mode, idNum, baseAtk, activeAtk, baseDef, activeDef, species, status, cost):
		super().__init__(name, activeXPos, activeYPos, previewXPos, previewYPos, previousXPos, previousYPos, canMove, owner, face, previewFace, mode, idNum)
		self.baseAtk = baseAtk
		self.activeAtk = activeAtk
		self.baseDef = baseDef
		self.activeDef = activeDef
		self.species = species
		self.status = status
		self.cost = cost
	def search(self):
		return "Monster"

class Magic(Card):
	def __init__(self, name, activeXPos, activeYPos, previewXPos, previewYPos, previousXPos, previousYPos, canMove,
		owner, face, previewFace, mode, idNum, equip):
		super().__init__(name, activeXPos, activeYPos, previewXPos, previewYPos, previousXPos, previousYPos, canMove, owner, face, previewFace, mode, idNum)
		self.equip = equip
	def search(self):
		return "Magic"

class Trap(Card):
	def __init__(self, name, activeXPos, activeYPos, previewXPos, previewYPos, previousXPos, previousYPos, canMove, 
			owner, face, previewFace, mode, idNum, effect, trigRange):
		super().__init__(name, activeXPos, activeYPos, previewXPos, previewYPos, previousXPos, previousYPos, canMove, owner, face, previewFace, idNum)
		self.effect = effect
		self.trigRange = trigRange
	def search(self):
		return "Trap"

def findDuplicateIndex(userList):
	setList = set()
	result = []
	for index, value in enumerate(userList):
		if value not in setList:
			setList.add(value)
		else:
			return index
	return -1

def drawGrid():
    blockSize = 110 #Set the size of the grid block
    offset = 31
    for x in range(7):
        for y in range(7):
            rect = pygame.Rect(x*blockSize + offset, y*blockSize + offset,
                               blockSize, blockSize)
            pygame.draw.rect(screen, GREY, rect, 3)

def clearBoard():
	blockSize = 110 #Set the size of the grid block
	offset = 32
	for x in range(7):
		for y in range(7):
			rect = pygame.Rect(x*blockSize + offset, y*blockSize + offset,
                               blockSize-3, blockSize-3)
			pygame.draw.rect(screen, BLACK, rect, 0)

def outlineSpot(x, y, color):
	blockSize = 110
	offset = 31
	rect = pygame.Rect(x*blockSize + offset, y*blockSize + offset,
                               blockSize, blockSize)
	pygame.draw.rect(screen, color, rect, 3)

def drawLeaders(activeLeaders):
	blockSize = 110
	offset = (31 + 15)
	for leader in activeLeaders:
		screen.blit(pygame.image.load(str(leader.idNum) + ".png"), (leader.previewXPos*blockSize + offset, leader.previewYPos*blockSize + offset))

def drawCards(activeCards):
	xOffset = 65
	yOffset = 55
	blockSize = 110
	xImageOffset = 4
	yImageOffset = 8
	
	cardCoords = []

	for card in activeCards:
		if("Monster" in card.search()):	
			if(card.owner == "Blue"):
				if(card.mode == "ATK"):
					if(card.previewFace == "DOWN"):
						back = pygame.image.load("blueCardBackL.png").convert()
						screen.blit(pygame.transform.scale(back, (40, 60)), (card.previewXPos*blockSize + xOffset, card.previewYPos*blockSize + yOffset))
					else:
						front = pygame.image.load("blueCardFrontL.png").convert()
						image = pygame.image.load(str(card.idNum) + ".png").convert()
						screen.blit(pygame.transform.scale(front, (40, 60)), (card.previewXPos*blockSize + xOffset, card.previewYPos*blockSize + yOffset))	
						screen.blit(pygame.transform.scale(image, (32, 32)), (card.previewXPos*blockSize + xOffset + xImageOffset , card.previewYPos*blockSize + yOffset + yImageOffset))
				else:
					if(card.previewFace == "DOWN"):
						back = pygame.image.load("blueCardBackL.png").convert()
						screen.blit(rotImage(pygame.transform.scale(back, (40, 60)), 90), (card.previewXPos*blockSize + yOffset, card.previewYPos*blockSize + xOffset))
					else:
						front = pygame.image.load("blueCardFrontL.png").convert()
						image = pygame.image.load(str(card.idNum) + ".png").convert()
						screen.blit(rotImage(pygame.transform.scale(front, (40, 60)), 90), (card.previewXPos*blockSize + yOffset, card.previewYPos*blockSize + xOffset))	
						screen.blit(rotImage(pygame.transform.scale(image, (32, 32)), 90), (card.previewXPos*blockSize + yOffset + yImageOffset , card.previewYPos*blockSize + xOffset + xImageOffset))
			if(card.owner == "Red"):
				if(card.mode == "ATK"):
					if(card.previewFace == "DOWN"):
						back = pygame.image.load("redCardBackL.png").convert()
						screen.blit(pygame.transform.scale(back, (40, 60)), (card.previewXPos*blockSize + xOffset, card.previewYPos*blockSize + yOffset))
					else:
						front = pygame.image.load("redCardFrontL.png").convert()
						image = pygame.image.load(str(card.idNum) + ".png").convert()
						screen.blit(pygame.transform.scale(front, (40, 60)), (card.previewXPos*blockSize + xOffset, card.previewYPos*blockSize + yOffset))
						screen.blit(pygame.transform.scale(image, (32, 32)), (card.previewXPos*blockSize + xOffset + xImageOffset , card.previewYPos*blockSize + yOffset + yImageOffset))
				else:
					if(card.previewFace == "DOWN"):
						back = pygame.image.load("redCardBackL.png").convert()
						screen.blit(rotImage(pygame.transform.scale(back, (40, 60)), 90), (card.previewXPos*blockSize + yOffset, card.previewYPos*blockSize + xOffset))
					else:
						front = pygame.image.load("redCardFrontL.png").convert()
						image = pygame.image.load(str(card.idNum) + ".png").convert()
						screen.blit(rotImage(pygame.transform.scale(front, (40, 60)), 90), (card.previewXPos*blockSize + yOffset, card.previewYPos*blockSize + xOffset))
						screen.blit(rotImage(pygame.transform.scale(image, (32, 32)), 90), (card.previewXPos*blockSize + yOffset + yImageOffset , card.previewYPos*blockSize + xOffset + xImageOffset))
		elif("Magic" in card.search()):	
			if(card.owner == "Blue"):
				if(card.mode == "ATK"):
					if(card.previewFace == "DOWN"):
						back = pygame.image.load("blueCardBackL.png").convert()
						screen.blit(pygame.transform.scale(back, (40, 60)), (card.previewXPos*blockSize + xOffset, card.previewYPos*blockSize + yOffset))
					else:
						front = pygame.image.load("blueCardFrontMag.png").convert()
						image = pygame.image.load(str(card.idNum) + ".png").convert()
						screen.blit(pygame.transform.scale(front, (40, 60)), (card.previewXPos*blockSize + xOffset, card.previewYPos*blockSize + yOffset))	
						screen.blit(pygame.transform.scale(image, (32, 32)), (card.previewXPos*blockSize + xOffset + xImageOffset , card.previewYPos*blockSize + yOffset + yImageOffset))
				else:
					if(card.previewFace == "DOWN"):
						back = pygame.image.load("blueCardBackL.png").convert()
						screen.blit(rotImage(pygame.transform.scale(back, (40, 60)), 90), (card.previewXPos*blockSize + yOffset, card.previewYPos*blockSize + xOffset))
					else:
						front = pygame.image.load("blueCardFrontMag.png").convert()
						image = pygame.image.load(str(card.idNum) + ".png").convert()
						screen.blit(rotImage(pygame.transform.scale(front, (40, 60)), 90), (card.previewXPos*blockSize + yOffset, card.previewYPos*blockSize + xOffset))	
						screen.blit(rotImage(pygame.transform.scale(image, (32, 32)), 90), (card.previewXPos*blockSize + yOffset + yImageOffset , card.previewYPos*blockSize + xOffset + xImageOffset))
			if(card.owner == "Red"):
				if(card.mode == "ATK"):
					if(card.previewFace == "DOWN"):
						back = pygame.image.load("redCardBackL.png").convert()
						screen.blit(pygame.transform.scale(back, (40, 60)), (card.previewXPos*blockSize + xOffset, card.previewYPos*blockSize + yOffset))
					else:
						front = pygame.image.load("redCardFrontMag.png").convert()
						image = pygame.image.load(str(card.idNum) + ".png").convert()
						screen.blit(pygame.transform.scale(front, (40, 60)), (card.previewXPos*blockSize + xOffset, card.previewYPos*blockSize + yOffset))
						screen.blit(pygame.transform.scale(image, (32, 32)), (card.previewXPos*blockSize + xOffset + xImageOffset , card.previewYPos*blockSize + yOffset + yImageOffset))
				else:
					if(card.previewFace == "DOWN"):
						back = pygame.image.load("redCardBackL.png").convert()
						screen.blit(rotImage(pygame.transform.scale(back, (40, 60)), 90), (card.previewXPos*blockSize + yOffset, card.previewYPos*blockSize + xOffset))
					else:
						front = pygame.image.load("redCardFrontMag.png").convert()
						image = pygame.image.load(str(card.idNum) + ".png").convert()
						screen.blit(rotImage(pygame.transform.scale(front, (40, 60)), 90), (card.previewXPos*blockSize + yOffset, card.previewYPos*blockSize + xOffset))
						screen.blit(rotImage(pygame.transform.scale(image, (32, 32)), 90), (card.previewXPos*blockSize + yOffset + yImageOffset , card.previewYPos*blockSize + xOffset + xImageOffset))

		
		cardCoords.append(str(card.previewXPos) + "," + str(card.previewYPos))
	
	dIndex = findDuplicateIndex(cardCoords)
	
	if( not(dIndex == -1)):
		x = int(cardCoords[dIndex][0])
		y = int(cardCoords[dIndex][2])
		drawBoardSpot(x, y, board)
		screen.blit(pygame.image.load("fighting.png"), ((110*x)+32, (110*y) + 32))

def drawBoard(board):
	count = 0
	for i in range(7):
		for j in range(7):
			screen.blit(pygame.image.load(board[i][j]+".png").convert(), ((110*i)+32, (110*j) + 32))

def drawBoardSpot(x, y, board):
	screen.blit(pygame.image.load(board[x][y]+".png").convert(), ((110*x)+32, (110*y) + 32))

def cardInRange(card, board):
	distance = abs(card.activeYPos - card.previewYPos) + abs(card.activeXPos - card.previewXPos)
	Range = 1
	if(card.search() == "Leader"):
		Range == 1
	elif(cardHasFieldBonus(board[card.activeXPos][card.activeYPos], card) and card.previewFace == "UP"):
		Range = 2
	else:
		Range = 1
	
	if( distance <= Range):
		return True
	else:
		return False

def drawBoardRange(card, board):
	if(("Leader" in card.search()) or ("Magic" in card.search())):
		Range = 1
	elif(cardHasFieldBonus(board[card.activeXPos][card.activeYPos], card) and card.previewFace == "UP"):
		Range = 2
	else:
		Range = 1

	for i in range(7):
		for j in range(7):
			distance = abs(card.activeYPos - j) + abs(card.activeXPos - i)
			if(distance <= Range):
				outlineSpot(i, j,YELLOW)

def activateFieldCard(card, board):
	Range = 2
	for i in range(7):
		for j in range(7):
			distance = abs(card.activeYPos - j) + abs(card.activeXPos - i)
			if(distance <= Range):
				if(card.idNum == "689"):
					board[i][j] = "Forest"
				elif(card.idNum == "690"):
					board[i][j] = "Wasteland"
				elif(card.idNum == "691"):
					board[i][j] = "Mountain"
				elif(card.idNum == "692"):
					board[i][j] = "Meadow"
				elif(card.idNum == "693"):
					board[i][j] = "Umi"
				elif(card.idNum == "694"):
					board[i][j] = "Yami"
				elif(card.idNum == "695"):
					board[i][j] = "Toonworld"
				elif(card.idNum == "696"):
					board[i][j] = "Neutral"

def drawDisplayWindow(activeCards, pointer, board, activePlayer, grabbed, grabbedCard):
	window = pygame.Surface((340, 771))
	picFrame = pygame.Surface((280, 280))
	window.fill(GREY)
	picFrame.fill(SOFT_BLACK)
	cardInfoFrame = pygame.Surface((310, 80))
	cardInfoFrame.fill(SOFT_BLACK)
	screen.blit(window, (830, 30))
	screen.blit(picFrame, (860, 140))
	screen.blit(cardInfoFrame, (845, 45))

	previewFrame = pygame.Surface((310, 285))
	previewFrame.fill(SOFT_BLACK)
	screen.blit(previewFrame, (845, 500))
	
	if(grabbed and not(grabbedCard.search() == "Leader")):
		nameText = FONT.render(grabbedCard.name, False, GREY)
		nameRect = nameText.get_rect()
		nameOffset = (310 - nameRect.width)/2
		if("Monster" in grabbedCard.search()):	
			if(grabbedCard.activeAtk > grabbedCard.baseAtk and grabbedCard.activeDef > grabbedCard.baseDef):
				atkText = FONT.render("ATK: " + str(grabbedCard.activeAtk), False, GREEN)
				defText = FONT.render("DEF: " + str(grabbedCard.activeDef), False, GREEN)
			if(grabbedCard.activeAtk < grabbedCard.baseAtk and grabbedCard.activeDef < grabbedCard.baseDef):
				atkText = FONT.render("ATK: " + str(grabbedCard.activeAtk), False, red)
				defText = FONT.render("DEF: " + str(grabbedCard.activeDef), False, red)
			if(grabbedCard.activeAtk == grabbedCard.baseAtk and grabbedCard.activeDef == grabbedCard.baseDef):
				atkText = FONT.render("ATK: " + str(grabbedCard.activeAtk), False, GREY)
				defText = FONT.render("DEF: " + str(grabbedCard.activeDef), False, GREY)
			atkRect = atkText.get_rect()
			atkOffset = (310 - atkRect.width)/4
			
			defRect = defText.get_rect()
			defOffset = (3*(310 - defRect.width))/4

			screen.blit(defText, (845 + int(defOffset), 90))
			screen.blit(atkText, (845 + int(atkOffset), 90))
		screen.blit(nameText, (845 + int(nameOffset), 50))
		screen.blit(pygame.image.load( grabbedCard.idNum + ".png"), (875, 155))
	else:
		for card in activeCards:
			if(card.previewXPos == pointer[0] and card.previewYPos == pointer[1]):
				if(card.owner == activePlayer.color or card.face == "UP"):
					nameText = FONT.render(card.name, False, GREY)
					nameRect = nameText.get_rect()
					nameOffset = (310 - nameRect.width)/2
					
					if("Monster" in card.search()):
						if(card.activeAtk > card.baseAtk and card.activeDef > card.baseDef):
							atkText = FONT.render("ATK: " + str(card.activeAtk), False, GREEN)
							defText = FONT.render("DEF: " + str(card.activeDef), False, GREEN)
						if(card.activeAtk < card.baseAtk and card.activeDef < card.baseDef):
							atkText = FONT.render("ATK: " + str(card.activeAtk), False, red)
							defText = FONT.render("DEF: " + str(card.activeDef), False, red)
						if(card.activeAtk == card.baseAtk and card.activeDef == card.baseDef):
							atkText = FONT.render("ATK: " + str(card.activeAtk), False, GREY)
							defText = FONT.render("DEF: " + str(card.activeDef), False, GREY)

						atkRect = atkText.get_rect()
						atkOffset = (310 - atkRect.width)/4
						defRect = defText.get_rect()
						defOffset = (3*(310 - defRect.width))/4

						screen.blit(defText, (845 + int(defOffset), 90))
						screen.blit(atkText, (845 + int(atkOffset), 90))
					screen.blit(nameText, (845 + int(nameOffset), 50))
					screen.blit(pygame.image.load( card.idNum + ".png"), (875, 155))
				else:
					nameText = FONT.render("???", False, GREY)
					nameRect = nameText.get_rect()
					nameOffset = (310 - nameRect.width)/2
					atkText = FONT.render("ATK: ???", False, GREY)
					atkRect = atkText.get_rect()
					atkOffset = (310 - atkRect.width)/4
					defText = FONT.render("DEF: ???", False, GREY)
					defRect = defText.get_rect()
					defOffset = (3*(310 - defRect.width))/4

					screen.blit(defText, (845 + int(defOffset), 90))
					screen.blit(atkText, (845 + int(atkOffset), 90))
					screen.blit(nameText, (845 + int(nameOffset), 50))
					
def cardHasFieldWeakness(fieldType, card):

	if("Monster" in card.search()):	
		if(fieldType == "Wasteland"):
			if(card.species == "Aqua" or card.species == "Fish" or card.species == "Plant"):
				return True
			else:
				return False

		if(fieldType == "Meadow"):
			if(card.species == "Spellcaster"):
				return True
			else:
				return False

		if(fieldType == "Mountain"):
			if(card.species == "Zombie"):
				return True
			else:
				return False

		if(fieldType == "Umi"):
			if(card.species == "Pyro" or card.species == "Machine"):
				return True
			else:
				return False

		if(fieldType == "Yami"):
			if(card.species == "Fairy"):
				return True
			else:
				return False

		if(fieldType == "Toonworld"):
			if(card.species == "Toon"):
				return False
			else:
				return True

		if(fieldType == "Forest"):
			if(card.species == "Fiend"):
				return True
			else:
				return False

		if(fieldType == "Neutral"):
			return False

		if(fieldType == "Crush"):
			return False
	else:
		return False

def cardHasFieldBonus(fieldType, card):
	
	if("Monster" in card.search()):
		if(fieldType == "Wasteland"):
			if(card.species == "Zombie" or card.species == "Rock" or card.species == "Machine"):
				return True
			else:
				return False
		
		if(fieldType == "Umi"):
			if(card.species == "Fish" or card.species == "Aqua" or card.species == "Thunder"):
				return True
			else:
				return False

		if(fieldType == "Yami"):
			if(card.species == "Fiend" or card.species == "Spellcaster" or card.species == "Zombie"):
				return True
			else:
				return False

		if(fieldType == "Meadow"):
			if(card.species == "Warrior" or card.species == "Beast-Warrior"):
				return True
			else:
				return False

		if(fieldType == "Toonworld"):
			if(card.species == "Toon"):
				return True
			else:
				return False

		if(fieldType == "Mountain"):
			if(card.species == "Dragon" or card.species == "Winged-Beast" or card.species == "Fairy"):
				return True
			else:
				return False

		if(fieldType == "Forest"):
			if(card.species == "Insect" or card.species == "Grass" or card.species == "Pyro" or card.species == "Beast-Warrior" or card.species == "Beast"):
				return True
			else:
				return False

		if(fieldType == "Neutral"):
			return False

		if(fieldType == "Crush"):
			if(card.species == "Immoral"):
				return True
			else:
				return False
	else:
		return False

def drawLifeBar(bluePlayer, redPlayer, activePlayer, turnCounter):
	#draw grey rectangle and black frames
	lifeBar = pygame.Surface((1139, 39))
	lifeBar.fill(GREY)
	screen.blit(lifeBar, (31, 831))
	blueFrame = pygame.Surface((500, 35))
	blueFrame.fill(SOFT_BLACK)
	screen.blit(blueFrame, (33, 833))
	redFrame = pygame.Surface((500, 35))
	redFrame.fill(SOFT_BLACK)
	screen.blit(redFrame, (668, 833))

	#format and draw blue player info
	blueNameText = FONT.render(bluePlayer.name, False, Blue)
	blueLifeText = FONT.render(str(bluePlayer.lifePoints), False, Blue)
	blueLifeRect = blueLifeText.get_rect()
	blueLifeRect.right = 527
	blueLifeRect.top = 835
	screen.blit(blueNameText, (37, 835))
	screen.blit(blueLifeText, blueLifeRect)

	#format and draw red player info
	redNameText = FONT.render(redPlayer.name, False, Red)
	redLifeText = FONT.render(str(redPlayer.lifePoints), False, Red)
	redNameRect = redNameText.get_rect()
	redNameRect.right = 1164
	redNameRect.top = 835
	screen.blit(redNameText, redNameRect)
	screen.blit(redLifeText, (674, 835))

	arrowBox = pygame.Surface((131, 35))
	arrowBox.fill(SOFT_BLACK)
	screen.blit(arrowBox, (535, 833))
	blueArrowText = FONT.render(u'\u2190', False, Blue)
	redArrowText = FONT.render(u'\u2192', False, Red)

	#draw turn number
	if(activePlayer == bluePlayer):
		pygame.draw.polygon(screen, Blue, ((540, 850), (580, 840), (580, 860)))
		turnText = FONT.render(str(turnCounter), False, Blue)
		if(turnCounter > 9):
			screen.blit(turnText, (593, 835))
		else:
			screen.blit(turnText, (600, 835))
	else:
		pygame.draw.polygon(screen, Red, ((662, 850), (624, 840), (624, 860)))
		turnText = FONT.render(str(turnCounter), False, Red)
		if(turnCounter > 9):
			screen.blit(turnText, (593, 835))
		else:
			screen.blit(turnText, (600, 835))

def rotImage(image, angle):

    loc = image.get_rect().center
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite

def drawPointerFrame(pointer, board):
	pointFrame = pygame.Surface((310, 50))
	pointFrame.fill(SOFT_BLACK)
	screen.blit(pointFrame, (845, 435))

	pointerText = FONT.render( "(" + str(pointer[0]+1) + ", " + str(pointer[1]+1) + ") "+ board[pointer[0]][pointer[1]], False, GREY)
	textRect = pointerText.get_rect()

	placeX = (310 - textRect.width)/2
	placeY = (50 - textRect.height)/2
	screen.blit(pointerText, (845 + int(placeX), 435 + int(placeY)))

def drawPreviewFrame(activeCards, board, grabbedCard):
	attackedCard = None
	cardCoords = []

	for card in activeCards:
		cardCoords.append(str(card.previewXPos) + "," + str(card.previewYPos))
		if(card.activeXPos == grabbedCard.previewXPos and card.activeYPos == grabbedCard.previewYPos and not(card == grabbedCard)):
			attackedCard = card

	dIndex = findDuplicateIndex(cardCoords)
	if(not(dIndex == -1)):
		if(attackedCard.owner == grabbedCard.owner):
			#display a preview of the interaction if both cards are owned by the same user
			interactionText = FONT.render("FUSION", False, GREY)
			textRect = interactionText.get_rect()
			placeX = (310 - textRect.width)/2
			screen.blit(interactionText, (845 + int(placeX), 510))

			vsText = FONT.render("+", False, GREY)
			vsTextRect = vsText.get_rect()
			vsOffset = (310 - vsTextRect.width)/2
			screen.blit(vsText, (845 + int(vsOffset), 712))

			if(grabbedCard.owner == "Blue"):
				image = pygame.image.load(str(grabbedCard.idNum) + ".png").convert()
				screen.blit(pygame.image.load("blueCardFrontL.png").convert(), (870, 555))	
				screen.blit(pygame.transform.scale(image, (64, 64)), (878, 563))
			else:
				image = pygame.image.load(str(grabbedCard.idNum) + ".png").convert()
				screen.blit(pygame.image.load("redCardFrontL.png").convert(), (870, 555))	
				screen.blit(pygame.transform.scale(image, (64, 64)), (878, 563))
			
			if("Monster" in grabbedCard.search()):
				if(grabbedCard.activeAtk > grabbedCard.baseAtk and grabbedCard.activeDef > grabbedCard.baseDef):
					infoText = FONT.render("ATK: " + str(grabbedCard.activeAtk), False, GREEN)
					infoTextD = FONT.render("DEF: " + str(grabbedCard.activeDef), False, GREEN)
				if(grabbedCard.activeAtk < grabbedCard.baseAtk and grabbedCard.activeDef < grabbedCard.baseDef):
					infoText = FONT.render("ATK: " + str(grabbedCard.activeAtk), False, red)
					infoTextD = FONT.render("DEF: " + str(grabbedCard.activeDef), False, red)
				if(grabbedCard.activeAtk == grabbedCard.baseAtk and grabbedCard.activeDef == grabbedCard.baseDef):
					infoText = FONT.render("ATK: " + str(grabbedCard.activeAtk), False, GREY)
					infoTextD = FONT.render("DEF: " + str(grabbedCard.activeDef), False, GREY)

				infoRect = infoText.get_rect()
				infoRectD = infoTextD.get_rect()
				xOffset = (80 - infoRect.width)/2
				xOffsetD = (80 - infoRectD.width)/2
				screen.blit(infoText, (870+ int(xOffset), 700))
				screen.blit(infoTextD, (870+ int(xOffsetD), 725))




			

			if(attackedCard.owner == "Blue"):
				image = pygame.image.load(str(attackedCard.idNum) + ".png").convert()
				screen.blit(pygame.image.load("blueCardFrontL.png").convert(), (1055, 555))	
				screen.blit(pygame.transform.scale(image, (64, 64)), (1063, 563))
			else:
				image = pygame.image.load(str(grabbedCard.idNum) + ".png").convert()
				screen.blit(pygame.image.load("redCardFrontL.png").convert(), (1055, 555))	
				screen.blit(pygame.transform.scale(image, (64, 64)), (1063, 563))

			if("Monster" in attackedCard.search()):
				if(attackedCard.activeAtk > attackedCard.baseAtk and attackedCard.activeDef > attackedCard.baseDef):
					atkdInfoText = FONT.render("ATK: " + str(attackedCard.activeAtk), False, GREEN)
					atkdInfoTextD = FONT.render("DEF: " + str(attackedCard.activeDef), False, GREEN)
				if(attackedCard.activeAtk < attackedCard.baseAtk and attackedCard.activeDef < attackedCard.baseDef):
					atkdInfoText = FONT.render("ATK: " + str(attackedCard.activeAtk), False, red)
					atkdInfoTextD = FONT.render("DEF: " + str(attackedCard.activeDef), False, red)
				if(attackedCard.activeAtk == attackedCard.baseAtk and attackedCard.activeDef == attackedCard.baseDef):
					atkdInfoText = FONT.render("ATK: " + str(attackedCard.activeAtk), False, GREY)
					atkdInfoTextD = FONT.render("DEF: " + str(attackedCard.activeDef), False, GREY)

				infoRect = atkdInfoText.get_rect()
				infoRectD = atkdInfoText.get_rect()
				atkdOffset = (80 - infoRect.width)/2
				atkdOffsetD = (80 - infoRectD.width)/2
				screen.blit(atkdInfoText, (1055 + int(atkdOffset), 700))
				screen.blit(atkdInfoTextD, (1055 + int(atkdOffsetD), 725))

		else:
			#draw battle info if the cards are owned by different users
			interactionText = FONT.render("BATTLE", False, GREY)
			textRect = interactionText.get_rect()
			placeX = (310 - textRect.width)/2
			screen.blit(interactionText, (845 + int(placeX), 510))

			vsText = FONT.render("VS", False, GREY)
			vsTextRect = vsText.get_rect()
			vsOffset = (310 - vsTextRect.width)/2
			screen.blit(vsText, (845 + int(vsOffset), 712))


			if(grabbedCard.owner == "Blue"):
				image = pygame.image.load(str(grabbedCard.idNum) + ".png").convert()
				screen.blit(pygame.image.load("blueCardFrontL.png").convert(), (870, 555))	
				screen.blit(pygame.transform.scale(image, (64, 64)), (878, 563))

			if(grabbedCard.owner == "Red"):
				image = pygame.image.load(str(grabbedCard.idNum) + ".png").convert()
				screen.blit(pygame.image.load("redCardFrontL.png").convert(), (870, 555))	
				screen.blit(pygame.transform.scale(image, (64, 64)), (878, 563))

			if("Monster" in grabbedCard.search()):
				if(grabbedCard.activeAtk > grabbedCard.baseAtk and grabbedCard.activeDef > grabbedCard.baseDef):
					infoText = FONT.render("ATK: " + str(grabbedCard.activeAtk), False, GREEN)
					infoTextD = FONT.render("DEF: " + str(grabbedCard.activeDef), False, GREEN)
				if(grabbedCard.activeAtk < grabbedCard.baseAtk and grabbedCard.activeDef < grabbedCard.baseDef):
					infoText = FONT.render("ATK: " + str(grabbedCard.activeAtk), False, red)
					infoTextD = FONT.render("DEF: " + str(grabbedCard.activeDef), False, red)
				if(grabbedCard.activeAtk == grabbedCard.baseAtk and grabbedCard.activeDef == grabbedCard.baseDef):
					infoText = FONT.render("ATK: " + str(grabbedCard.activeAtk), False, GREY)
					infoTextD = FONT.render("DEF: " + str(grabbedCard.activeDef), False, GREY)
				
				infoRect = infoText.get_rect()
				infoRectD = infoTextD.get_rect()
				xOffset = (80 - infoRect.width)/2
				xOffsetD = (80 - infoRectD.width)/2
				screen.blit(infoText, (870+ int(xOffset), 700))
				screen.blit(infoTextD, (870+ int(xOffsetD), 725))

			if("Monster" in attackedCard.search()):
				if(attackedCard.activeAtk > attackedCard.baseAtk and attackedCard.activeDef > attackedCard.baseDef):
					atkdInfoText = FONT.render("ATK: " + str(attackedCard.activeAtk), False, GREEN)
					atkdInfoTextD = FONT.render("DEF: " + str(attackedCard.activeDef), False, GREEN)
				if(attackedCard.activeAtk < attackedCard.baseAtk and attackedCard.activeDef < attackedCard.baseDef):
					atkdInfoText = FONT.render("ATK: " + str(attackedCard.activeAtk), False, red)
					atkdInfoTextD = FONT.render("DEF: " + str(attackedCard.activeDef), False, red)
				if(attackedCard.activeAtk == attackedCard.baseAtk and attackedCard.activeDef == attackedCard.baseDef):
					atkdInfoText = FONT.render("ATK: " + str(attackedCard.activeAtk), False, GREY)
					atkdInfoTextD = FONT.render("DEF: " + str(attackedCard.activeDef), False, GREY)

				infoRect = atkdInfoText.get_rect()
				infoRectD = atkdInfoText.get_rect()
				
				
				atkdOffset = (80 - infoRect.width)/2
				atkdOffsetD = (80 - infoRectD.width)/2
				
				
			
			atkdInfoTextQ = FONT.render("ATK: ???", False, GREY)
			atkdInfoTextDQ = FONT.render("DEF: ???", False, GREY)
			infoRectQ = atkdInfoTextQ.get_rect()
			infoRectDQ = atkdInfoTextDQ.get_rect()
			atkdOffsetDQ = (80 - infoRectDQ.width)/2
			atkdOffsetQ = (80 - infoRectQ.width)/2
			if(attackedCard.owner == "Blue"):
				if(attackedCard.mode == "ATK"):
					if(attackedCard.previewFace == "DOWN"):
						screen.blit(pygame.image.load("blueCardBackL.png").convert(), (1055, 555))
						screen.blit(atkdInfoTextQ, (1055 + int(atkdOffsetQ), 700))
						screen.blit(atkdInfoTextDQ, (1055 + int(atkdOffsetDQ), 725))

					else:
						image = pygame.image.load(str(attackedCard.idNum) + ".png").convert()
						screen.blit(pygame.image.load("blueCardFrontL.png").convert(), (1055, 555))
						screen.blit(pygame.transform.scale(image, (64, 64)), (1063, 563))
						if("Monster" in attackedCard.search()):
							screen.blit(atkdInfoText, (1055 + int(atkdOffset), 700))
							screen.blit(atkdInfoTextD, (1055 + int(atkdOffsetD), 725))

				else:
					if(attackedCard.previewFace == "DOWN"):
						back = pygame.image.load("blueCardBackL.png").convert()
						screen.blit(rotImage(back, 90), (1015, 575))
						screen.blit(atkdInfoTextQ, (1035 + int(atkdOffsetQ), 700))
						screen.blit(atkdInfoTextDQ, (1035 + int(atkdOffsetDQ), 725))
					else:
						image = pygame.image.load(str(attackedCard.idNum) + ".png").convert()
						front = pygame.image.load("blueCardFrontL.png").convert()
						screen.blit(rotImage(front, 90), (1015, 575))	
						screen.blit(rotImage(pygame.transform.scale(image, (64, 64)), 90), ( 1023, 583))
						if("Monster" in attackedCard.search()):
							screen.blit(atkdInfoText, (1035 + int(atkdOffset), 700))
							screen.blit(atkdInfoTextD, (1035 + int(atkdOffsetD), 725))
			if(attackedCard.owner == "Red"):
				if(attackedCard.mode == "ATK"):
					if(attackedCard.previewFace == "DOWN"):
						screen.blit(pygame.image.load("redCardBackL.png").convert(), (1055, 555))
						screen.blit(atkdInfoTextQ, (1055 + int(atkdOffsetQ), 700))
						screen.blit(atkdInfoTextDQ, (1055 + int(atkdOffsetDQ), 725))
					else:
						image = pygame.image.load(str(attackedCard.idNum) + ".png").convert()
						screen.blit(pygame.image.load("redCardFrontL.png").convert(), (1055, 555))
						screen.blit(pygame.transform.scale(image, (64, 64)), (1063, 563))
						if("Monster" in attackedCard.search()):
							screen.blit(atkdInfoText, (1055 + int(atkdOffset), 700))
							screen.blit(atkdInfoTextD, (1055 + int(atkdOffsetD), 725))
				else:
					if(attackedCard.previewFace == "DOWN"):
						back = pygame.image.load("redCardBackL.png").convert()
						screen.blit(rotImage(back, 90), (1015, 575))
						screen.blit(atkdInfoTextQ, (1035 + int(atkdOffsetQ), 700))
						screen.blit(atkdInfoTextDQ, (1035 + int(atkdOffsetDQ), 725))
					else:
						image = pygame.image.load(str(attackedCard.idNum) + ".png").convert()
						front = pygame.image.load("redCardFrontL.png").convert()
						screen.blit(rotImage(front, 90), (1015, 575))
						screen.blit(rotImage(pygame.transform.scale(image, (64, 64)), 90), (1023, 583))
						if("Monster" in attackedCard.search()):
							screen.blit(atkdInfoText, (1035 + int(atkdOffset), 700))
							screen.blit(atkdInfoTextD, (1035 + int(atkdOffsetD), 725))

def idToCard(idNum, owner):
	file = open("cardInfo.txt", "r")
	idString = "id" + str(idNum)
	for line in file:
		if idString in line:
			info = line.split()
			if(info[1] == "Monster"):
				card = Monster(info[2], -1, -1, -1, -1, -1, -1, True, owner, "DOWN", "DOWN", "ATK", idNum, int(info[3]), int(info[3]), int(info[4]), int(info[4]), info[5], None, info[6])
				return card
			elif(info[1] == "Magic"):
				if(info[3] == "False"):
					fuseBool = False
				else:
					fuseBool = True
				card = Magic(info[2], -1, -1, -1, -1, -1, -1, True, owner, "DOWN", "DOWN", "ATK", idNum, fuseBool)
				return card

def invertBoard(board):
	oldBoard = deepcopy(board)

	for i in range(7):
		for j in range(7):
			board[i][j] = oldBoard[6-i][6-j]

def drawSummoningRange(leader):
	for x in range(7):
		for y in range(7):
			if( abs(leader.activeXPos - x) <= 1 and abs(leader.activeYPos - y) <= 1 and not(leader.activeXPos == x and leader.activeYPos == y)):
				outlineSpot(x, y, DARK_BLUE)

def inSummoningRange(leader, pointer):
	if(abs(leader.activeXPos - pointer[0]) <= 1 and abs(leader.activeYPos - pointer[1]) <= 1):
		return True
	else:
		return False

def invertCards(activeCards):
	for card in activeCards:
		card.activeYPos = 6 - card.activeYPos
		card.previewYPos = card.activeYPos
		card.activeXPos = 6 - card.activeXPos
		card.previewXPos = card.activeXPos

def invertLeaders(activeLeaders):
	for leader in activeLeaders:
		leader.activeYPos = 6 - leader.activeYPos
		leader.previewYPos = leader.activeYPos
		leader.activeXPos = 6 - leader.activeXPos
		leader.previewXPos = leader.activeXPos

def applyFieldEffect(activeCards, board):
	for card in activeCards:
		if("Monster" in card.search()):
			if(cardHasFieldBonus(board[card.previewXPos][card.previewYPos], card)):
				card.activeAtk = card.baseAtk + 500
				card.activeDef = card.baseDef + 500
			elif(cardHasFieldWeakness(board[card.previewXPos][card.previewYPos], card)):
				card.activeAtk = card.baseAtk - 500
				card.activeDef = card.baseDef - 500
				if(card.activeAtk < 0):
					card.activeAtk = 0
				if(card.activeDef < 0):
					card.activeDef = 0
			else:
				card.activeAtk = card.baseAtk
				card.activeDef = card.baseDef

def executeBattles(board, activeCards, bluePlayer, redPlayer):
	count = 0
	cardCoords = []
	battlingCards = []
	stat0 = -1
	stat1 = -1

	for card in activeCards:
		cardCoords.append(str(card.activeXPos) + "," + str(card.activeYPos))
	dIndex = findDuplicateIndex(cardCoords)
	if(not(dIndex == -1)):
		x = int(cardCoords[dIndex][0])
		y = int(cardCoords[dIndex][2])
		for card in activeCards:
			if(card.activeXPos == x and card.activeYPos == y):
				battlingCards.append(card)

		if(battlingCards[0].owner == battlingCards[1].owner):
			print("fusion")
		elif(("Monster" in battlingCards[0].search()) and ("Monster" in battlingCards[1].search())):
			if(battlingCards[0].mode == "ATK"):
				stat0  = battlingCards[0].activeAtk
			else:
				stat0 = battlingCards[0].activeDef
			if(battlingCards[1].mode == "ATK"):
				stat1  = battlingCards[1].activeAtk
			else:
				stat1 = battlingCards[1].activeDef

			battlingCards[0].face = "UP"
			battlingCards[1].face = "UP"
			battlingCards[0].previewFace = "UP"
			battlingCards[1].previewFace = "UP"
			
			#if monster "0" wins
			if(stat0 > stat1):
				
				#assess life point damages if losing card was in attack mode
				if(battlingCards[1].mode == "ATK" and battlingCards[1].owner == "Red"):
					redPlayer.lifePoints = redPlayer.lifePoints - (stat0 - stat1)
				if(battlingCards[1].mode == "ATK" and battlingCards[1].owner == "Blue"):
					bluePlayer.lifePoints = bluePlayer.lifePoints - (stat0 - stat1)
				

				#if the winning card was in attack mode, destroy the other card
				if(battlingCards[0].mode == "ATK"):
					for card in activeCards:
						if(card == battlingCards[1]):
							activeCards.pop(count)
						count +=1
				else:
					#if the winning card was in defense mode, move the other card back to its old position
					battlingCards[1].activeXPos = battlingCards[1].previousXPos
					battlingCards[1].activeYPos = battlingCards[1].previousYPos
					battlingCards[1].previewXPos = battlingCards[1].previousXPos
					battlingCards[1].previewYPos = battlingCards[1].previousYPos
			
			#if monster "1" wins
			if(stat1 > stat0):
				
				#assess life point damages if losing card was in attack mode
				if(battlingCards[0].mode == "ATK" and battlingCards[0].owner == "Red"):
					redPlayer.lifePoints = redPlayer.lifePoints - (stat1 - stat0)
				if(battlingCards[0].mode == "ATK" and battlingCards[0].owner == "Blue"):
					bluePlayer.lifePoints = bluePlayer.lifePoints - (stat1 - stat0)

				#if the winning card was in attack mode, destroy the other card
				if(battlingCards[1].mode == "ATK"):
					for card in activeCards:
						if(card == battlingCards[0]):
							activeCards.pop(count)
						count +=1
				else:
					#if the winning card was in defense mode, move the other card back to its old position
					battlingCards[0].activeXPos = battlingCards[0].previousXPos
					battlingCards[0].activeYPos = battlingCards[0].previousYPos
					battlingCards[0].previewXPos = battlingCards[0].previousXPos
					battlingCards[0].previewYPos = battlingCards[0].previousYPos

			#if the monsters tie
			if(stat1 == stat0):

				#if both monsters are in attack mode, destroy them both
				if(battlingCards[0].mode == "ATK" and battlingCards[1].mode == "ATK"):
					for card in activeCards:
						if(card == battlingCards[0]):
							activeCards.pop(count)
						count +=1
					count = 0
					for card in activeCards:
						if(card == battlingCards[1]):
							activeCards.pop(count)
						count +=1
					print("tie")
				elif(battlingCards[1].mode == "DEF"):
					#if card 1 was in defensive mode, move card 0 back
					battlingCards[0].activeXPos = battlingCards[0].previousXPos
					battlingCards[0].activeYPos = battlingCards[0].previousYPos
					battlingCards[0].previewXPos = battlingCards[0].previousXPos
					battlingCards[0].previewYPos = battlingCards[0].previousYPos
				elif(battlingCards[0].mode == "DEF"):
					#if card 0 was in defensive mode, move card 1 back
					battlingCards[1].activeXPos = battlingCards[1].previousXPos
					battlingCards[1].activeYPos = battlingCards[1].previousYPos
					battlingCards[1].previewXPos = battlingCards[1].previousXPos
					battlingCards[1].previewYPos = battlingCards[1].previousYPos
		elif("Magic" in battlingCards[0].search() or "Magic" in battlingCards[1].search()):
			count = 0
			if("Magic" in battlingCards[0].search()):
				for card in activeCards:
					if (card == battlingCards[0]):
						activeCards.pop(count)
					count += 1
			if("Magic" in battlingCards[1].search()):
				for card in activeCards:
					if (card == battlingCards[1]):
						activeCards.pop(count)
					count += 1

def executeDirectDamage(board, activeCards, activeLeaders, bluePlayer, redPlayer):
	for leader in activeLeaders:
		for card in activeCards:
			if(card.activeXPos == leader.activeXPos and card.activeYPos == leader.activeYPos and not(card.owner == leader.owner)):
				if(leader.owner == "Red"):
					redPlayer.lifePoints = redPlayer.lifePoints - card.activeAtk
				if(leader.owner == "Blue"):
					bluePlayer.lifePoints = bluePlayer.lifePoints - card.activeAtk
				card.activeXPos = card.previousXPos
				card.activeYPos = card.previousYPos
				card.previewXPos = card.previousXPos
				card.previewYPos = card.previousYPos
				card.previewFace = "UP"
				card.face = "UP"

def drawHandFrame(summoningLeader, RedHand, BlueHand):
	borderFrame = pygame.Surface((708, 508))
	frame = pygame.Surface((700, 500))
	frame.fill(SOFT_BLACK)
	borderFrame.fill(GREY)
	screen.blit(borderFrame, (246, 196))
	screen.blit(frame, (250, 200))

	count = 0
	if(summoningLeader.owner == "Blue"):
			for card in BlueHand:
				if("Monster" in card.search()):	
					image = pygame.image.load(str(card.idNum) + ".png").convert()
					screen.blit(pygame.image.load("blueCardFrontL.png").convert(), (300 + (130*count), 250))
					screen.blit(pygame.transform.scale(image, (64, 64)), (308 + (130*count), 258))
					count += 1
				elif("Magic" in card.search()):	
					image = pygame.image.load(str(card.idNum) + ".png").convert()
					screen.blit(pygame.image.load("blueCardFrontMag.png").convert(), (300 + (130*count), 250))
					screen.blit(pygame.transform.scale(image, (64, 64)), (308 + (130*count), 258))
					count += 1
	else:
			for card in RedHand:
				if("Monster" in card.search()):
					image = pygame.image.load(str(card.idNum) + ".png").convert()
					screen.blit(pygame.image.load("redCardFrontL.png").convert(), (300 + (130*count), 250))
					screen.blit(pygame.transform.scale(image, (64, 64)), (308 + (130*count), 258))
					count += 1
				elif("Magic" in card.search()):	
					image = pygame.image.load(str(card.idNum) + ".png").convert()
					screen.blit(pygame.image.load("redCardFrontMag.png").convert(), (300 + (130*count), 250))
					screen.blit(pygame.transform.scale(image, (64, 64)), (308 + (130*count), 258))
					count += 1

def activateMagic(activeCards, board):
	count = -1
	for card in activeCards:
		activated = False
		count += 1
		
		if(card.face == "UP"):
			if(card.idNum == "689" or card.idNum == "690" or card.idNum == "691" or card.idNum == "692" or card.idNum == "693" or card.idNum == "694" or card.idNum == "695" or card.idNum == "696"):
				activateFieldCard(card, board)
				activated = True

		if(activated):
			activeCards.pop(count)

def drawSummonPointer(summoningLeader, pointerIndex):
	if(summoningLeader.owner == "Blue"):
		pointer = pygame.Rect(280 + (130*pointerIndex), 230, 120, 160)
		pygame.draw.rect(screen, Blue, pointer, 2)
	else:
		pointer = pygame.Rect(280 + (130*pointerIndex), 230, 120, 160)
		pygame.draw.rect(screen, Red, pointer, 2)

def validPlacement(grabbedCard, activeCards):
	if("Leader" in str(grabbedCard.search)):
		for card in activeCards:
			if(card.activeXPos == grabbedCard.previewXPos and card.activeYPos == grabbedCard.previewYPos):
				if( not (card.owner == grabbedCard.owner) or card.search == "Leader"):
					print("flag")
					return False
	else:
		for card in activeCards:
			if(card.activeXPos == grabbedCard.previewXPos and card.activeYPos == grabbedCard.previewYPos):
				if((card.owner == grabbedCard.owner) and (card.search == "Leader")):
					return False
	return True

def summoningWindow(summoningLeader, RedHand, BlueHand):
	looping = True
	pointerIndex = 0

	
	while(looping):
		drawHandFrame(summoningLeader, RedHand, BlueHand)
		drawSummonPointer(summoningLeader, pointerIndex)
		for event in pygame.event.get():
			if (event.type == pygame.KEYDOWN):
				if(event.key == pygame.K_BACKSPACE):
					looping = False
					return None
				if(event.key == pygame.K_LEFT):
					if(pointerIndex > 0):
						pointerIndex -= 1
				if(event.key == pygame.K_RIGHT):
					if(pointerIndex < 4):
						pointerIndex += 1
				if(event.key == pygame.K_SPACE and summoningLeader.canSummon):
					if(activePlayer.color == "Blue"):
						summonCard = BlueHand[pointerIndex]
						BlueHand.pop(pointerIndex)
						return summonCard
					else:
						summonCard = RedHand[pointerIndex]
						RedHand.pop(pointerIndex)
						return summonCard


		pygame.display.flip()

def fillHand(hand, deck):
	while(len(hand) < 5):
		randIndex = randint(0, (len(deck) - 1))
		hand.append(deck[randIndex])
		deck.pop(randIndex)

activeCards = []
activeLeaders = []

BlueLeader = Leader("Kaiba", 3, 6, 3, 6, 3, 6, True, "Blue", None, None, None, "BDL", True)
RedLeader = Leader("Yugi", 3, 0, 3, 0, 3, 0, True, "Red", None, None, None, "RDL", True)

BlueHand = []
BlueDeck = []
BlueHand.append(idToCard("694", "Blue"))
BlueHand.append(idToCard("696", "Blue"))


for x in range(40):
	randId = randint(0, 25)
	BlueDeck.append(idToCard(str(randId), "Blue"))
RedHand = []
RedDeck = []
for x in range(40):
	randId = randint(0, 25)
	RedDeck.append(idToCard(str(randId), "Red"))

activeLeaders.append(BlueLeader)
activeLeaders.append(RedLeader)

pygame.init()

pointer = [3, 3]
grabbedCard = None
summoning = False
summoningLeader = None
grabbed = False
darkBool = False
turnCounter = 1
screen = pygame.display.set_mode([1200, 900])


board = [["Crush"]*7 for i in range(7)]
board[0] = ["Yami"] *7 
board[1] = ["Umi"] *7 
board[2] = ["Wasteland"] *7 
board[3] = ["Neutral"] *7
board[4] = ["Mountain"] *7
board[5] = ["Forest"] *7
board[6] = ["Meadow"] *7 

clock = pygame.time.Clock()
bluePlayer = Player("Kaiba", "Blue", 4000)
redPlayer = Player("Yugi", "Red", 4000)
activePlayer = bluePlayer
activeColor = Blue
alpha_surf = pygame.Surface((1200, 900))
alpha_surf.fill(SOFT_BLACK)
alpha = 0
# Run until the user asks to quit
running = True
fillHand(BlueHand, BlueDeck)
fillHand(RedHand, RedDeck)

while running:
		
	executeBattles(board, activeCards, bluePlayer, redPlayer)
	executeDirectDamage(board, activeCards, activeLeaders, bluePlayer, redPlayer)
	activateMagic(activeCards, board)

	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			running = False
		if (event.type == pygame.KEYDOWN):
			if ((event.key == pygame.K_DOWN or event.key == pygame.K_s) and pointer[1] < 6):
				if(not grabbed and not summoning):
					pointer[1] += 1
				if(grabbed):	
					grabbedCard.previewYPos += 1
					if(cardInRange(grabbedCard, board) and validPlacement(grabbedCard, activeCards)):
						pointer[1] += 1
						grabbedCard.mode = "ATK"
					else:
						grabbedCard.previewYPos -= 1
				if(summoning):
					pointer[1] += 1
					if(not inSummoningRange(summoningLeader, pointer)):
						pointer[1] -= 1
			if ((event.key == pygame.K_UP or event.key == pygame.K_w) and pointer[1] > 0):
				if(not grabbed and not summoning):
					pointer[1] -= 1
				if(grabbed):	
					grabbedCard.previewYPos -= 1
					if(cardInRange(grabbedCard, board) and validPlacement(grabbedCard, activeCards)):
						pointer[1] -= 1
						grabbedCard.mode = "ATK"
					else:
						grabbedCard.previewYPos += 1
				if(summoning):
					pointer[1] -= 1
					if(not inSummoningRange(summoningLeader, pointer)):
						pointer[1] += 1
			if ((event.key == pygame.K_RIGHT or event.key == pygame.K_d) and pointer[0] < 6):
				if(not grabbed and not summoning):
					pointer[0] += 1
				if(grabbed):	
					grabbedCard.previewXPos += 1
					if(cardInRange(grabbedCard, board) and validPlacement(grabbedCard, activeCards)):
						pointer[0] += 1
						grabbedCard.mode = "ATK"
					else:
						grabbedCard.previewXPos -= 1
				if(summoning):
					pointer[0] += 1
					if(not inSummoningRange(summoningLeader, pointer)):
						pointer[0] -= 1
			if ((event.key == pygame.K_LEFT or event.key == pygame.K_a) and pointer[0] > 0):
				if(not grabbed and not summoning):
					pointer[0] -= 1
				if(grabbed):	
					grabbedCard.previewXPos -= 1
					if(cardInRange(grabbedCard, board) and validPlacement(grabbedCard, activeCards)):
						pointer[0] -= 1
						grabbedCard.mode = "ATK"
					else:
						grabbedCard.previewXPos += 1
				if(summoning):
					pointer[0] -= 1
					if(not inSummoningRange(summoningLeader, pointer)):
						pointer[0] += 1
			if (event.key == pygame.K_SPACE):
				if(grabbed):
					grabbed = False
					grabbedCard.canMove = False
					grabbedCard.previousXPos = grabbedCard.activeXPos
					grabbedCard.previousYPos = grabbedCard.activeYPos
					grabbedCard.activeXPos = grabbedCard.previewXPos
					grabbedCard.activeYPos = grabbedCard.previewYPos
					grabbedCard.face = grabbedCard.previewFace
					grabbedCard = None
				elif(summoning and  (not (pointer[0] == summoningLeader.activeXPos and pointer[1] == summoningLeader.activeYPos))):
					summonCard = summoningWindow(summoningLeader, RedHand, BlueHand)
					if(not(summonCard == None)):
						summonCard.previewXPos = pointer[0]
						summonCard.previewYPos = pointer[1]
						summonCard.previousXPos = pointer[0]
						summonCard.previousYPos = pointer[1]
						summonCard.activeXPos = pointer[0]
						summonCard.activeYPos = pointer[1]
						summoningLeader.canSummon = False
						summoning = False
						activeCards.append(summonCard)
				else:
					for card in activeCards:
						if(pointer[0] == card.previewXPos and pointer[1] == card.previewYPos):
							if((not grabbed) and card.canMove and (card.owner == activePlayer.color) and not(summoning)):
								grabbedCard = card
								grabbed = True
							elif((not grabbed) and (not card.canMove) or (not(card.owner == activePlayer.color)) or summoning):
								outlineSpot(pointer[0], pointer[1], red)
								drawCards(activeCards)
								pygame.display.flip()
								pygame.time.delay(200)
					for leader in activeLeaders:
						if(pointer[0] == leader.previewXPos and pointer[1] == leader.previewYPos):
							if((not grabbed) and leader.canMove and (leader.owner == activePlayer.color)):
								grabbedCard = leader
								grabbed = True
							elif((not grabbed) and (not leader.canMove) or (not(leader.owner == activePlayer.color))):
								outlineSpot(pointer[0], pointer[1], red)
								drawCards(activeCards)
								pygame.display.flip()
								pygame.time.delay(200)
			if(event.key == pygame.K_BACKSPACE):
				if(grabbed):
					grabbedCard.previewXPos = grabbedCard.activeXPos
					grabbedCard.previewYPos = grabbedCard.activeYPos
					grabbedCard.previewFace = grabbedCard.face
					grabbed = False
					grabbedCard = None
				if(summoning):
					summoning = False
					summoningLeader = None
			if(event.key == pygame.K_e and grabbed):
				if(not(grabbedCard.previewXPos == grabbedCard.activeXPos) or not(grabbedCard.previewYPos == grabbedCard.activeYPos) or (grabbedCard.search() == "Leader")):
						outlineSpot(pointer[0], pointer[1], red)
						drawCards(activeCards)
						pygame.display.flip()
						pygame.time.delay(200)
				if(grabbed):
					if(grabbedCard.previewYPos == grabbedCard.activeYPos and grabbedCard.previewXPos == grabbedCard.activeXPos):
						if(grabbedCard.mode == "ATK"):
							grabbedCard.mode = "DEF"
						else:
							grabbedCard.mode = "ATK"
			if(event.key == pygame.K_RETURN):
				if(grabbed or summoning):
					outlineSpot(pointer[0], pointer[1], red)
					drawCards(activeCards)
					pygame.display.flip()
					pygame.time.delay(200)
				else:
					if(activePlayer == bluePlayer):
						activePlayer = redPlayer
						activeColor = Red
						fillHand(RedHand, RedDeck)
					else:
						activePlayer = bluePlayer
						activeColor = Blue
						fillHand(BlueHand, BlueDeck)
					for card in activeCards:
						card.canMove = True
					for leader in activeLeaders:
						leader.canMove = True
						leader.canSummon = True
					for i in range(15):
						alpha_surf.set_alpha(alpha)
						alpha += 8
						screen.blit(alpha_surf, (0,0))
						pygame.display.flip()
						clock.tick(40)
					turnCounter += 1
					darkBool = True
					invertBoard(board)
					invertCards(activeCards)
					invertLeaders(activeLeaders)
			if(event.key == pygame.K_q):
				if(grabbed):
					if(grabbedCard.face == "UP" or  not(grabbedCard.previewXPos == grabbedCard.activeXPos) or not(grabbedCard.previewYPos == grabbedCard.activeYPos) or (grabbedCard.search() == "Leader")):
						outlineSpot(pointer[0], pointer[1], red)
						drawCards(activeCards)
						pygame.display.flip()
						pygame.time.delay(200)
					else:
						if(grabbedCard.previewFace == "DOWN"):
							grabbedCard.previewFace = "UP"
						else:
							grabbedCard.previewFace = "DOWN"
			if(event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
				if(not summoning):
					for leader in activeLeaders:
						if (leader.activeXPos == pointer[0] and leader.activeYPos == pointer[1] and not(grabbed) and (activePlayer.color == leader.owner)):
							summoningLeader = leader
					if( not (summoningLeader == None) and summoningLeader.canSummon):
						summoning = True
						if(summoningLeader.activeYPos == 0):
							pointer[1]  += 1
						else:
							pointer[1] -=1
					elif(not(summoningLeader == None)):
						summoningWindow(summoningLeader, RedHand, BlueHand)
				else:
					summoning = False
					summoningLeader = None
	
	applyFieldEffect(activeCards, board)
	screen.fill(SOFT_BLACK)
	drawDisplayWindow(activeCards, pointer, board, activePlayer, grabbed, grabbedCard)
	drawLifeBar(bluePlayer, redPlayer, activePlayer, turnCounter)
	drawGrid()
	drawBoard(board)
	drawPointerFrame(pointer, board)
	
	if(grabbed):
		drawBoardRange(grabbedCard, board)
		if(not(grabbedCard.search() == "Leader")):	
			drawPreviewFrame(activeCards, board, grabbedCard)
	
	if(summoning):
		drawSummoningRange(summoningLeader)
	outlineSpot(pointer[0], pointer[1], activeColor)
	drawLeaders(activeLeaders)
	drawCards(activeCards)
	if(darkBool):
		alpha_surf.set_alpha(alpha)
		screen.blit(alpha_surf, (0,0))
		alpha -= 8
		if(alpha == 0):
			darkBool = False

	pygame.display.flip()
	clock.tick(40)	
pygame.quit()