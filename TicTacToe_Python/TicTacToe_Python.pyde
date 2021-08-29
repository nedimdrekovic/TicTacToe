import math

'''
Main method.
'''
if __name__ == '__main__':
    board = [
             ['', '', ''],
             ['', '', ''],
             ['', '', '']
             ]

    available = []
    gameIsOver = False
    currentPlayer = 'X'

    canvasWidth = 1000
    canvasHeight = 800
    
    boardWidth = 500
    boardHeight = boardWidth
    circleRadiusWidth = (1.0/3)*boardWidth * 0.7    # 0.7, da Kreis knapp kleiner sein soll wie das Kästchen
    circleRadiusHeight = (1.0/3)*boardHeight * 0.7    # 0.7, da Kreis knapp kleiner sein soll wie das Kästchen
        
    backgroundColorValue = 100
    distance = (canvasWidth - boardWidth) / 2   # distance between border and left corner

'''
Function that defines initial environment properties.
'''
def setup():
    global available
    size(canvasWidth, canvasHeight)
    background(backgroundColorValue)

    if canvasHeight < 500 or canvasHeight > 800 or canvasWidth < 700 or canvasWidth > 1000:
        print("Canvas is too small.")
    if boardWidth > canvasWidth or boardHeight > canvasHeight:
        print("Board is too large.")
    
    # add indices for every cell
    for i in range(3):
        for j in range(3):
            available.append([i, j])

    stroke(255)
    # horizontal lines
    line((canvasWidth - boardWidth) / 2.0, 20 + (0.0/3)*boardHeight, ((canvasWidth - boardWidth) / 2.0) + boardWidth, 20 + (0.0/3)*boardHeight)
    line((canvasWidth - boardWidth) / 2.0, 20 + (1.0/3)*boardHeight, ((canvasWidth - boardWidth) / 2.0) + boardWidth, 20 + (1.0/3)*boardHeight)
    line((canvasWidth - boardWidth) / 2.0, 20 + (2.0/3)*boardHeight, ((canvasWidth - boardWidth) / 2.0) + boardWidth, 20 + (2.0/3)*boardHeight)
    line((canvasWidth - boardWidth) / 2.0, 20 + (3.0/3)*boardHeight, ((canvasWidth - boardWidth) / 2.0) + boardWidth, 20 + (3.0/3)*boardHeight)
    
    # vertical lines
    line((canvasWidth - boardWidth) / 2.0 + (0.0/3)*boardWidth, 20, (canvasWidth - boardWidth) / 2.0 + (0.0/3)*boardWidth, 20 + boardHeight)
    line((canvasWidth - boardWidth) / 2.0 + (1.0/3)*boardWidth, 20, (canvasWidth - boardWidth) / 2.0 + (1.0/3)*boardWidth, 20 + boardHeight)
    line((canvasWidth - boardWidth) / 2.0 + (2.0/3)*boardWidth, 20, (canvasWidth - boardWidth) / 2.0 + (2.0/3)*boardWidth, 20 + boardHeight)
    line((canvasWidth - boardWidth) / 2.0 + (3.0/3)*boardWidth, 20, (canvasWidth - boardWidth) / 2.0 + (3.0/3)*boardWidth, 20 + boardHeight)

    # show message who's next
    updateTurnMessage()

'''
Loops forever until it stops.
'''
def draw():
    pass

'''
Shows who's next.
'''
def updateTurnMessage():
    # now it's the opponent's turn
    fill(100)
    noStroke()
    rect(25, boardHeight + (1.0/5)*(canvasHeight-20-boardHeight), 200, 25)    # remove previous text (easier than using draw method just for this detail)
    
    # show new text
    textSize(25)
    fill(250)
    text("Player's turn:  " + currentPlayer, 30, 20 + boardHeight + (1.0/5) * (canvasHeight - (20 + boardHeight)))    # update text

'''
Returns defined value of clicked cell.
'''
def getCellValues(x, y):
    # set mouseclick coordinates
    temp1, temp2 = -1, -1
    if distance <= x <= distance + (1.0/3)*boardWidth:
        temp1 = 0
    elif distance + (1.0/3)*boardWidth <= x <= distance + (2.0/3)*boardWidth:
        temp1 = 1
    elif distance + (2.0/3)*boardWidth <= x <= distance + (3.0/3)*boardWidth:
        temp1 = 2
    if 20 <= y <= 20 + (1.0/3)*boardHeight:
        temp2 = 0
    elif 20 + (1.0/3)*boardHeight <= y <= 20 + (2.0/3)*boardHeight:
        temp2 = 1
    elif 20 + (2.0/3)*boardHeight <= y <= 20 + (3.0/3)*boardHeight:
        temp2 = 2
    return temp1, temp2

'''
Method is called when mouse is pressed somewhere in the canvas.
'''
def mousePressed():
    global currentPlayer, available, board
    global gameIsOver
    global distance
    global boardWidth

    if not gameIsOver:
        if len(available) > 0:            
            x, y = getCellValues(mouseX, mouseY)

            if (x == -1) | (y == -1):
                print("Bitte ein noch nicht belegtes Feld anklicken.")
                return
            if board[y][x] == '':
                #mm_value = maxi('O', available.length)
                board[y][x] = currentPlayer  #  player
                currentPlayer = 'O' if currentPlayer == 'X' else 'X'
                
                #board[mm_value][x] = 'O'  #  KI
                available.remove([x,y])

    textSize(30)
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                # draw 'X'
                stroke(0, 0, 255)   # set color of 'X'
                strokeWeight(6)
                line(distance + (1.0/15)*boardWidth+(boardWidth/3.0)*j, 20 + (1.0/15)*boardHeight+(boardHeight/3.0)*i, distance + (4.0/15)*boardWidth+(boardWidth/3.0)*j, 20 + (4.0/15)*boardHeight+(boardHeight/3.0)*i) # '\'
                line(distance + (4.0/15)*boardWidth+(boardWidth/3.0)*j, 20 + (1.0/15)*boardHeight+(boardHeight/3.0)*i, distance + (1.0/15)*boardWidth+(boardWidth/3.0)*j, 20 + (4.0/15)*boardHeight+(boardHeight/3.0)*i) # '/'
            elif board[i][j] == 'O':
                # draw 'O'
                stroke(255, 0, 0)   # set color of 'O'
                fill(backgroundColorValue)   # fill ellipse
                ellipse(distance + (1.0/6)*boardWidth+(1/3.0)*boardWidth*j, 20 + (1/6.0)*boardHeight+(1/3.0)*boardHeight*i, circleRadiusWidth, circleRadiusHeight)

    # get winner of the game
    winner = getWinner()
    if winner != "Draw":
        # show winner of game
        fill(255)
        textSize(50)
        text("Winner: " + winner[0], 0.35 * canvasWidth, 20 + boardHeight + 0.5 * (canvasHeight - boardHeight))
        gw1 = winner[1]
        gw2 = winner[2]
        direction = winner[3]    

        # change state of game and player
        gameIsOver = True
        currentPlayer = "-"
        
        # draw line for highlighting the winner
        strokeWeight(2.5)
        stroke(0)
        if direction == "dv":
            line(distance + 20, 40, distance + boardWidth - 20, boardHeight)
        elif direction == "dr":
            line(distance + boardWidth - 20, 40, distance + 20, boardHeight)
        elif direction == "h":  # horizontal
            line(distance + 20, 20 + (1.0/6) * boardHeight + (1.0/3) * gw1 * boardHeight, distance + (boardWidth-20), 20 + (1.0/6)*boardHeight+(1.0/3)*gw1*boardHeight)
        elif direction == "v":  # vertical
            line(distance + (1.0/6) * boardWidth + (1.0/3) * boardWidth * gw2, 40, distance + (1.0/6) * boardWidth + (1.0/3) * boardWidth * gw2, boardHeight)
        
    elif isFullyOccupied(board):
        fill(255)
        textSize(50)
        text(winner, 0.425 * canvasWidth, 20 + boardHeight + 0.5 * (canvasHeight - (20 + boardHeight)))
        gameIsOver = True
        currentPlayer = "-"

    # udpate message
    updateTurnMessage()


def bewerten() :
  return 1  #  dummy

def maxi(spieler, tiefe) :
  if (tiefe == 0) :
    return bewerten()
  maxWert = -1 * math.inf
  return 1

def mini(spieler, tiefe) :
  if (tiefe == 0) :
    return bewerten()
  minWert = math.inf

'''
Returns Information about the end of game.
'''
def getWinner() :
    for i in range(3):
        for j in range(3):
            if equals3(board[i][j], board[i][(j + 1) % 3], board[i][(j + 2) % 3]):
                return [board[i][j], i, j, "h"]
            elif (equals3(board[i][j], board[(i + 1) % 3][j], board[(i + 2) % 3][j])) :
                return [board[i][j], i, j, "v"]
            elif (equals3(board[0][0], board[1][1], board[2][2])) :
                return [board[0][0], 0, 2, "dv"] #  diagonal vorwaerts
            elif (equals3(board[0][2], board[1][1], board[2][0])) :
                return [board[0][2], 0, 2, "dr"] #  diagonal rueckwarts
    return "Draw"

'''
Checks if every cell in the board is occupied.
Returns true if there are no available cells.
'''
def isFullyOccupied(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                return False
    return True


'''
Returns True if the arguments are equal.
'''
def equals3(a, b, c) :
    return (a == b) & (b == c) & (a == c) & (str(a) != "")
