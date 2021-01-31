import pygame
import random
from pygame import mixer # music/sounds
import math

HEIGHT = 800
WIDTH = 800
DIMENSION = 8
IMAGES = {}

playerTurn = 1 # white -> 1, black -> 0
whiteInCheck = False
blackInCheck = False
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

#Initialize pygame
pygame.init()

# #Background Sound
# mixer.music.load("background.wav")
# mixer.music.play(-1) # em loop

#Create the screen (width and height)
screen = pygame.display.set_mode((HEIGHT,WIDTH))

#Title and icon
pygame.display.set_caption("Chess")

def loadImages():
    pieces = ['bR', 'bN', 'bB', 'bQ', 'bK','bP','wR', 'wN', 'wB', 'wQ', 'wK', 'wP']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (squareSize, squareSize))


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

def canMove(pieceC, coords):

    global whiteInCheck
    global blackInCheck

    fst = coords[0]
    snd = coords[1]
    a = snd[0] - fst[0]
    b = snd[1] - fst[1]
    placeToCheck = []
    collided = True
    #print(a,b)
    pieceSnd = getPieceAtLocation(snd)
    piece = pieceC[-1].lower()

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

    print("toCheck:",placeToCheck)
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

    # I don't know what to do with these 2...
    if whiteInCheck:
        pass

    if blackInCheck:
        pass

    #Movement of the pieces:
    if not collided or piece == "n":
        #Pawns
        if piece == "p":
            if pieceC == "bP":
                if ((snd[0] - fst[0] == 1 and snd[1] == fst[1]) or (snd[0] == 3 and fst[0] == 1)) and pieceSnd == "--":
                    return True
                elif (snd[0] - fst[0] == 1 and abs(snd[1] - fst[1]) == 1) and pieceSnd != "--" and pieceSnd[0] != "b":
                    return True
            elif pieceC == "wP":
                if ((snd[0] - fst[0] == -1 and snd[1] == fst[1]) or (snd[0] == 4 and fst[0] == 6)) and pieceSnd == "--":
                    return True
                elif (snd[0] - fst[0] == -1 and abs(snd[1] - fst[1]) == 1) and pieceSnd != "--" and pieceSnd[0] != "w":
                    return True
                
        #Knights
        if piece == "n":
            if ((abs(snd[1] - fst[1]) == 2 and abs(snd[0] - fst[0]) == 1) or (abs(snd[0] - fst[0]) == 2 and abs(snd[1] - fst[1]) == 1)) and pieceC[0] != pieceSnd[0]:
                return True
        
        #Bishops
        if piece == "b":
            if (abs(snd[1] - fst[1]) == abs(snd[0] - fst[0])) and pieceC[0] != pieceSnd[0]:
                return True
        
        #Rooks
        if piece == "r":
            if ((snd[0] == fst[0]) or (snd[1] == fst[1])) and pieceC[0] != pieceSnd[0]:
                return True
        
        #Queens
        if piece == "q":
            if (((snd[0] == fst[0]) or (snd[1] == fst[1])) or (abs(snd[1] - fst[1]) == abs(snd[0] - fst[0]))) and pieceC[0] != pieceSnd[0]:
                return True

        #Kings
        if piece == "k":
            if pieceC[0] != pieceSnd[0] and ((abs(snd[0] - fst[0]) == 1 and snd[1] == fst[1]) or (snd[0] == fst[0] and abs(snd[1] - fst[1]) == 1) or (abs(snd[1] - fst[1]) == 1 and abs(snd[0] - fst[0]) == 1)):
                    return True
    return False

def movePiece(clicks):
    global playerTurn

    fstLocation = clicks[0]
    sndLocation = clicks[1]
    
    piece = getPieceAtLocation(clicks[0])
    if not ((piece[0] == "w" and playerTurn == 1) or (piece[0] == "b" and playerTurn == -1)):
        return False

    if not canMove(piece, (fstLocation, sndLocation)):
        return False

    # I want to make something that records moves in chess notation
    #moveLog.append(getChessNotation(clicks[1]))
    
    changePieceAtLocation(sndLocation, piece)
    changePieceAtLocation(fstLocation, "--")

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
                if len(playerClicks) == 2: # after 2nd click
                    print("\nPlayer:", playerTurn)
                    print("Clicks:",playerClicks)
                    if not movePiece(playerClicks): # if the piece cant move, then reset
                        squareSelected = ()
                        playerClicks = []
                    else:
                        print("Jogou")
                        playerTurn = -playerTurn
                        playerClicks = []

        drawBoard()
        drawPieces()

        #update the display
        #pygame.display.update()
        pygame.display.flip() # não sei qual é a diferença

if __name__ == "__main__":
    main()