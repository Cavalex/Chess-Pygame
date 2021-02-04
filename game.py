import pygame
import random
from pygame import mixer # music/sounds
import math

#Initialize pygame
pygame.init()

HEIGHT = 800
WIDTH = 800
DIMENSION = 8
IMAGES = {}

text0 = "You are in Check"
text1 = "This is a Chess Game!"
text2 = ("Player: white")
text3 = ""
text4 = "You are in Check"
font = pygame.font.Font("fonts/LEMONMILK-Regular.otf", 30)
textX = WIDTH + 30
textY0 = 100
textY1 = HEIGHT // 2 - 35
textY2 = HEIGHT // 2
textY3 = HEIGHT // 2 + 35
textY4 = HEIGHT - 100

playerTurn = 1 # white -> 1, black -> 0
hasBlackKingMoved = False # for the castle
hasWhiteKingMoved = False # for the castle
moveLog = []

squareSize = HEIGHT//DIMENSION

board = [
    ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
    ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["--", "--", "--", "--", "--", "--", "--", "--"],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
    ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]

# #Background Sound
# mixer.music.load("background.wav")
# mixer.music.play(-1) # em loop

#Create the screen (width and height)
screen = pygame.display.set_mode((WIDTH+450,HEIGHT))

#Title and icon
pygame.display.set_caption("Chess")

def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK','bP','wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (squareSize, squareSize))

def showText(text,x,y):
    text = font.render(text, True, (0, 0, 0))
    screen.blit(text, (x,y))

def drawBoard():
    colors = [pygame.Color((240,217,182)), pygame.Color((181,136,99))] #my chess.com colors :D
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            pygame.draw.rect(screen, color, pygame.Rect(c*squareSize, r*squareSize, squareSize, squareSize))

def drawPieces():
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(c*squareSize, r*squareSize, squareSize, squareSize))

def getPieceAtLocation(location):
    return board[location[0]][location[1]]

def changePieceAtLocation(location, piece):
    board[location[0]][location[1]] = piece

def getKingsPositions():
    bK = ""
    wK = ""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece == "bK":
                bK = (r,c)
            elif piece == "wK":
                wK = (r,c)
    return (bK, wK)

#detects collisions between pieces when moving
def willCollide(coords):
    
    fst = coords[0]
    snd = coords[1]

    #diference between both coordinates, basically how much the piece moved
    a = snd[0] - fst[0]
    b = snd[1] - fst[1]

    #coordinates to check for pieces there so pieces don't jump above other pieces
    placeToCheck = []
    collided = True

    #Checking collision with other pieces:
    if a == b and a < 0: # top left corner
        while a != 0 and b != 0:
            placeToCheck.append((fst[0]+a, fst[1]+b))
            a+=1
            b+=1
    elif a == b and a > 0: # bottom right corner
        while a != 0 and b != 0:
            placeToCheck.append((fst[0]+a, fst[1]+b))
            a-=1
            b-=1
    elif abs(a) == abs(b) and a < 0 and b > 0: #top right corner
        while a != 0 and b != 0:
            placeToCheck.append((fst[0]+a, fst[1]+b))
            a+=1
            b-=1
    elif abs(a) == abs(b) and a > 0 and b < 0: #bottom left corner
        while a != 0 and b != 0:
            placeToCheck.append((fst[0]+a, fst[1]+b))
            a-=1
            b+=1
    elif a == 0 and b < 0: #left
        while b != 0:
            placeToCheck.append((fst[0]+a, fst[1]+b))
            b+=1
    elif a == 0 and b > 0: #right
        while b != 0:
            placeToCheck.append((fst[0]+a, fst[1]+b))
            b-=1
    elif b == 0 and a < 0: #top
        while a != 0:
            placeToCheck.append((fst[0]+a, fst[1]+b))
            a+=1
    elif b == 0 and a > 0: #bottom
        while a != 0:
            placeToCheck.append((fst[0]+a, fst[1]+b))
            a-=1

    #print("toCheck:",placeToCheck)
    # by reversing the list and not checking the last element I avoid not being able to eat pieces
    # since the first element of placeToCheck was the target square
    placeToCheck.reverse()
    for i in range(len(placeToCheck)):
        if i != len(placeToCheck) - 1:
            if getPieceAtLocation(placeToCheck[i]) != "--":
                collided = True
                break
            else:
                collided = False
        else:
            collided = False

    return collided

def getAllMovesWithPiece(piece, pieceCoords):
    moves = []
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            coords = (r,c)
            if canMove(piece, (pieceCoords, (r,c)))[2]:
                moves.append(coords)
    return moves

def isKingUnderAttack():
    kingCoords = getKingsPositions()[0] if playerTurn == -1 else getKingsPositions()[1]
    print("\nPrints related to the king:")
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            coords = (r,c)
            pieceAtCoords = getPieceAtLocation(coords)
            if pieceAtCoords == "--":
                continue
            elif canMove(pieceAtCoords, (coords, kingCoords))[2]:
                return True
    return False

def movePiece(fst, snd, piece):
    changePieceAtLocation(snd, piece)
    changePieceAtLocation(fst, "--")

def canMove(pieceC, coords):
    blackKingPosition = getKingsPositions()[0]
    whiteKingPosition = getKingsPositions()[1]

    fst = coords[0]
    snd = coords[1]

    pieceSnd = getPieceAtLocation(snd)
    piece = pieceC[-1].lower()

    collided = willCollide(coords)
    ateBlackKing = True if not collided and pieceSnd.lower() == "bk" else False
    ateWhiteKing = True if not collided and pieceSnd.lower() == "wk" else False

    #print("black king was eaten, lol:", str(ateBlackKing) + "\n" + "white king was eaten, lol:", str(ateWhiteKing))

    #Movement of the pieces:
    if not collided or piece == "n":
        #Pawns
        if piece == "p":
            if pieceC == "bP":
                if ((snd[0] - fst[0] == 1 and snd[1] == fst[1]) or (snd[0] == 3 and fst[0] == 1) and snd[1] == fst[1]) and pieceSnd == "--":
                    return (ateBlackKing,ateWhiteKing ,True)
                elif (snd[0] - fst[0] == 1 and abs(snd[1] - fst[1]) == 1) and pieceSnd != "--" and pieceSnd[0] != "b":
                    return (ateBlackKing,ateWhiteKing ,True)
            elif pieceC == "wP":
                if ((snd[0] - fst[0] == -1 and snd[1] == fst[1]) or (snd[0] == 4 and fst[0] == 6) and snd[1] == fst[1]) and pieceSnd == "--":
                    return (ateBlackKing,ateWhiteKing ,True)
                elif (snd[0] - fst[0] == -1 and abs(snd[1] - fst[1]) == 1) and pieceSnd != "--" and pieceSnd[0] != "w":
                    return (ateBlackKing,ateWhiteKing ,True)
                
        #Knights
        if piece == "n":
            if ((abs(snd[1] - fst[1]) == 2 and abs(snd[0] - fst[0]) == 1) or (abs(snd[0] - fst[0]) == 2 and abs(snd[1] - fst[1]) == 1)) and pieceC[0] != pieceSnd[0]:
                return (ateBlackKing,ateWhiteKing ,True)
        
        #Bishops
        if piece == "b":
            if (abs(snd[1] - fst[1]) == abs(snd[0] - fst[0])) and pieceC[0] != pieceSnd[0]:
                return (ateBlackKing,ateWhiteKing ,True)
        
        #Rooks
        if piece == "r":
            if ((snd[0] == fst[0]) or (snd[1] == fst[1])) and pieceC[0] != pieceSnd[0]:
                return (ateBlackKing,ateWhiteKing ,True)
        
        #Queens
        if piece == "q":
            if (((snd[0] == fst[0]) or (snd[1] == fst[1])) or (abs(snd[1] - fst[1]) == abs(snd[0] - fst[0]))) and pieceC[0] != pieceSnd[0]:
                return (ateBlackKing,ateWhiteKing ,True)

        #Kings
        if piece == "k":
            if pieceC[0] != pieceSnd[0] and ((abs(snd[0] - fst[0]) == 1 and snd[1] == fst[1]) or (snd[0] == fst[0] and abs(snd[1] - fst[1]) == 1) or (abs(snd[1] - fst[1]) == 1 and abs(snd[0] - fst[0]) == 1)):
                    return (ateBlackKing,ateWhiteKing ,True)
    return (ateBlackKing,ateWhiteKing ,False)

def isLegalMove(pieceC, coords):
    
    fst = coords[0]
    snd = coords[1]

    pieceSnd = getPieceAtLocation(snd)
    piece = pieceC[-1].lower()
    
    #return canMove(pieceC, coords)[2]

    # make the new board and see if it is attacking the king
    movePiece(fst, snd, pieceC)
    if isKingUnderAttack():
        movePiece(snd, fst, pieceC)
        changePieceAtLocation(snd, pieceSnd)
        return False
    else:
        movePiece(snd, fst, pieceC)
        changePieceAtLocation(snd, pieceSnd)
        return canMove(pieceC, coords)[2]

def updateBoard(clicks):

    global text1
    global text2
    global text3

    fstLocation = clicks[0]
    sndLocation = clicks[1]
    
    piece = getPieceAtLocation(fstLocation)

    if not ((piece[0] == "w" and playerTurn == 1) or (piece[0] == "b" and playerTurn == -1)):
        text2 = "Not your turn!"
        text3 = "Try again!"
        return False

    #print("Is the king under attack?:", str(isKingUnderAttack()))
    #print("Is this move legal?:",str(isLegalMove(piece, (fstLocation, sndLocation))))

    if not isLegalMove(piece, (fstLocation, sndLocation)):
        text2 = "Illegal Move!"
        text3 = "Try again!"
        return False
    else:
        playerToPlay = "white" if playerTurn == -1 else "black" # must be reversed
        text2 = ("Player: %s" % playerToPlay)
        text3 = ""

    if not canMove(piece, (fstLocation, sndLocation))[2]:
        return False

    # I want to make something that records moves in chess notation
    #moveLog.append(getChessNotation(clicks[1]))
    
    movePiece(fstLocation, sndLocation, piece)

    return True

def main():
    global playerTurn
    # Game Loop
    running = True

    #screen.fill((255,0,0))

    screen.fill(pygame.Color("white"))

    loadImages()

    squareSelected = ()
    playerClicks = [] #keep track of player clicks: 2 tuples [(6,4),(4,4)]
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() #(x,y) do rato
                col = location[0] // squareSize
                row = location[1] // squareSize
                if squareSelected == (row,col): #clicked the same square twice
                    squareSelected = ()
                    playerClicks = [] # clear playerCLicks
                else:
                    squareSelected = (row,col)
                    playerClicks.append(squareSelected)
                if len(playerClicks) == 1 and getPieceAtLocation(playerClicks[0]) == "--":
                    squareSelected = ()
                    playerClicks = []
                if len(playerClicks) == 2: # after 2nd click

                    #print(getAllMovesWithPiece(getPieceAtLocation(playerClicks[0]), playerClicks[0]))
                    
                    print("\nPlayer:", playerTurn)
                    print("Clicks:",playerClicks)
                    if not updateBoard(playerClicks): # if the piece cant move, then reset
                        squareSelected = ()
                        playerClicks = []
                    else:
                        print("Jogou")
                        playerTurn = -playerTurn
                        playerClicks = []

        #screen.fill(pygame.Color("brown"))
        screen.fill((120,120,120))

        drawBoard()
        drawPieces()

        showText(text0, textX, textY0)
        showText(text1, textX, textY1)
        showText(text2, textX, textY2)
        showText(text3, textX, textY3)
        showText(text4, textX, textY4)

        #update the display
        #pygame.display.update()
        pygame.display.flip() # não sei qual é a diferença

if __name__ == "__main__":
    main()