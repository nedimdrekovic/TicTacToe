import math
import sys

'''
Main method.
'''
if __name__ == '__main__':
    board = [
             ['', '', ''],
             ['', '', ''],
             ['', '', '']
             ]

    human = 'O'  # player
    machine = 'O' if human == 'X' else 'X' # depends on what human is
    currentPlayer = human
    
    if human == machine:
        print("Human and Computer need to be different players. Choose 'X' or 'O' for the player and the computer")
        sys.exit()
        
    # first move of computer is totally random
    #board[int(random(3))][int(random(3))] = machine

    canvasWidth, canvasHeight = 1000, 800
    
    boardWidth = 500
    boardHeight = boardWidth
    circleRadiusWidth = (1.0/3)*boardWidth * 0.7    # 0.7, da Kreis knapp kleiner sein soll wie das Kästchen
    circleRadiusHeight = (1.0/3)*boardHeight * 0.7    # 0.7, da Kreis knapp kleiner sein soll wie das Kästchen
        
    backgroundColorValue = 100
    distance = (canvasWidth - boardWidth) / 2.0   # distance between border and left corner

'''
Function that defines initial environment properties.
'''
def setup():
    size(canvasWidth, canvasHeight)
    background(backgroundColorValue)

    stroke(0, 0, 255)   # set color of 'X'
    strokeWeight(6)
    
    # only there to draw user-defined beginning situation (depends on what is in the board)
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                line(distance + (1.0/15)*boardWidth+(boardWidth/3.0)*j, 20 + (1.0/15)*boardHeight+(boardHeight/3.0)*i, distance + (4.0/15)*boardWidth+(boardWidth/3.0)*j, 20 + (4.0/15)*boardHeight+(boardHeight/3.0)*i) # '\'
                line(distance + (4.0/15)*boardWidth+(boardWidth/3.0)*j, 20 + (1.0/15)*boardHeight+(boardHeight/3.0)*i, distance + (1.0/15)*boardWidth+(boardWidth/3.0)*j, 20 + (4.0/15)*boardHeight+(boardHeight/3.0)*i) # '/'
            elif board[i][j] == 'O':
                stroke(255, 0, 0)   # set color of 'O'
                fill(backgroundColorValue)   # fill ellipse
                ellipse(distance + (1.0/6)*boardWidth+(1/3.0)*boardWidth*j, 20 + (1/6.0)*boardHeight+(1/3.0)*boardHeight*i, circleRadiusWidth, circleRadiusHeight)                        
                
    # conditions for height of board and canvas
    if canvasHeight < 500 or canvasHeight > 800 or canvasWidth < 700 or canvasWidth > 1000:
        print("Canvas is too small.")
    if boardWidth > canvasWidth or boardHeight > canvasHeight:
        print("Board is too large.")

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
Shows who's next.
'''
def updateTurnMessage():
    # now it's the opponent's turn
    fill(100)
    noStroke()
    rect(25, boardHeight + (1.0/5)*(canvasHeight-20-boardHeight), 200, 25)    # remove previous text (easier than using draw method just for this detail)
    
    # show who's next
    textSize(25)
    fill(250)
    text("Player: " + currentPlayer, 30, 20 + boardHeight + (1.0/5) * (canvasHeight - (20 + boardHeight)))    # update text

'''
Returns defined value of clicked cell.
'''
def getCellCoords(x, y):
    # set mouseclick coordinates
    tempX, tempY = -1, -1
    if distance <= x <= distance + (1.0/3)*boardWidth:
        tempX = 0
    elif distance + (1.0/3)*boardWidth <= x <= distance + (2.0/3)*boardWidth:
        tempX = 1
    elif distance + (2.0/3)*boardWidth <= x <= distance + (3.0/3)*boardWidth:
        tempX = 2
    if 20 <= y <= 20 + (1.0/3)*boardHeight:
        tempY = 0
    elif 20 + (1.0/3)*boardHeight <= y <= 20 + (2.0/3)*boardHeight:
        tempY = 1
    elif 20 + (2.0/3)*boardHeight <= y <= 20 + (3.0/3)*boardHeight:
        tempY = 2
    return tempX, tempY

def bestMove():
    # folgenden Code lieber in eine Methode schreiben um Überblick zu erhalten
    # computer
    bestScore = -1 * float('inf')
    bestMove = [0, 0]
    for i in range(3):
        for j in range(3):
            if board[j][i] == '':
                board[j][i] = machine
                score = minimax(board, 0, False)
                board[j][i] = '' # undo board
                if score > bestScore:
                    bestScore = score
                    bestMove = [j, i] # bzw. [j, i] vllt.??
    board[bestMove[0]][bestMove[1]] = machine
    currentPlayer = human    


'''
Computes best possible score for the computer to play.
'''
def minimax(board, depth, isMaximizing):
    winner = getWinner()
    if winner != None: # if there is a winners
        scores = {human:-1, machine:1, 'Draw':0}  # values for possible outcomes
        return scores[winner[0]]
    
    bestScore = -float('inf') if isMaximizing else float('inf')
    for i in range(3):
        for j in range(3):
            if board[j][i] == '':
                board[j][i] = machine if isMaximizing else human
                score = minimax(board, depth + 1, not isMaximizing)
                board[j][i] = '' # undo value of cell
                bestScore = max(score, bestScore) if isMaximizing else min(score, bestScore)
    return bestScore

'''
Highlights winner of the game when there is one.
'''
def highlightWinner(gw1, gw2, direction):
    # draw line for highlighting the winner
    strokeWeight(2.5)
    stroke(220)
    if direction == "dv":
        line(distance + 20, 40, distance + boardWidth - 20, boardHeight)
    elif direction == "dr":
        line(distance + boardWidth - 20, 40, distance + 20, boardHeight)
    elif direction == "h":  # horizontal
        line(distance + 20, 20 + (1.0/6) * boardHeight + (1.0/3) * gw1 * boardHeight, distance + (boardWidth-20), 20 + (1.0/6)*boardHeight+(1.0/3)*gw1*boardHeight)
    elif direction == "v":  # vertical
        line(distance + (1.0/6) * boardWidth + (1.0/3) * boardWidth * gw2, 40, distance + (1.0/6) * boardWidth + (1.0/3) * boardWidth * gw2, boardHeight)

'''
Loops forever until it stops.
'''
def draw():
    pass

'''
Check if a winner exists
Draw winner message when game is finished.
'''
def checkWinner(winner):
    global currentPlayer
    fill(255)
    textSize(50)
    if winner[0] == 'Draw':
        text("Draw", 0.425 * canvasWidth, 20 + boardHeight + 0.5 * (canvasHeight - boardHeight))
    else:
        text("Winner:"+winner[0], 0.425 * canvasWidth, 20 + boardHeight + 0.5 * (canvasHeight - (20 + boardHeight)))
        highlightWinner(winner[1], winner[2], winner[3])
    currentPlayer = "-"
    print("Game is over")


'''
Method is called when mouse is pressed somewhere in the canvas.
'''
def mousePressed():
    global currentPlayer, board

    x, y = getCellCoords(mouseX, mouseY)

    if (x == -1) or (y == -1):
        print("Bitte ein noch nicht belegtes Feld anklicken.")
        return
    if board[y][x] == '': # if field is available
        board[y][x] = human # human
        currentPlayer = machine  # now its 'O''s turn

        # draw 'X'
        stroke(0, 0, 255)   # set color of 'X'
        strokeWeight(6)
        line(distance + (1.0/15)*boardWidth+(boardWidth/3.0)*x, 20 + (1.0/15)*boardHeight+(boardHeight/3.0)*y, distance + (4.0/15)*boardWidth+(boardWidth/3.0)*x, 20 + (4.0/15)*boardHeight+(boardHeight/3.0)*y) # '\'
        line(distance + (4.0/15)*boardWidth+(boardWidth/3.0)*x, 20 + (1.0/15)*boardHeight+(boardHeight/3.0)*y, distance + (1.0/15)*boardWidth+(boardWidth/3.0)*x, 20 + (4.0/15)*boardHeight+(boardHeight/3.0)*y) # '/'

        # check if there is a winner and draw winner message
        winner = getWinner()
        if winner != None: # if there is a winner
            checkWinner(winner)        
            updateTurnMessage()
            return
            
        # insert machine in the spot where the it has the highest winning chance
        bestScore = -1 * float('inf')
        bestMove = [0, 0]
        for i in range(3):
            for j in range(3):
                if board[j][i] == '':
                    board[j][i] = machine
                    score = minimax(board, 0, False) # compute minimax algorithm
                    board[j][i] = '' # undo board
                    if score > bestScore:
                        bestScore = score
                        bestMove = [j, i] # bzw. [j, i] vllt.??
        board[bestMove[0]][bestMove[1]] = machine
        currentPlayer = human

        # draw 'O'
        stroke(255, 0, 0)   # set color of 'O'
        fill(backgroundColorValue)   # fill ellipse
        ellipse(distance + (1.0/6)*boardWidth+(1/3.0)*boardWidth*bestMove[1], 20 + (1/6.0)*boardHeight+(1/3.0)*boardHeight*bestMove[0], circleRadiusWidth, circleRadiusHeight)                        
                    
        # check if there is a winner and draw winner message
        winner = getWinner()
        if winner != None: # if there is a winner
            checkWinner(winner)        
            updateTurnMessage()
            return
    
        # udpate message
        updateTurnMessage()

'''
Returns Winner about the end of game if there is one
'''
def getWinner():
    winner = None
    emptyCells = 0
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
            if board[i][j] == '':
                emptyCells += 1
            
    if emptyCells == 0: # check if game has ended and number of empty cells are 0 then it's a tie
        return ['Draw', None, None, None]
    return winner

'''
Returns True if the arguments are equal.
'''
def equals3(a, b, c) :
    return (a == b) & (b == c) & (a == c) & (str(a) != "")
