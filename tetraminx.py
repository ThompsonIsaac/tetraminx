# Isaac Thompson 2018 - Tic Tac Toe Tetraminx

import time

playerSymbol = 1 # 1 for X, 2 for O

evaluationDepth = 2 # The higher this is the more powerful the computer, but the slower.

expFactor = 10

moveNumbers = {"a4": 0, "b4": 1, "c4": 2, "d4": 3, "a3": 4, "b3": 5, "c3": 6, "d3": 7,
         "a2": 8, "b2": 9, "c2": 10, "d2": 11, "a1": 12, "b1": 13, "c1": 14, "d1": 15}

def newBoard():
    global data
    data = {}
    # Starts at top left, moves right then descends to next row.
    for i in range(16):
        data[i] = 0 # 4x4 empty cell
    

def printGame():
    for y in range(4):
        rowString = ""
        for x in range(4):
            cellData = data[x + y * 4]
            if cellData == 0:
                rowString += " "
            elif cellData == 1:
                rowString += "X"
            else:
                rowString += "O"
            if x < 3:
                rowString += " | "
        print(rowString)
        if y < 3:
            print("-- --- --- --")
        else:
            print("")

def validMove(str):
    if not str in moveNumbers:
        return "invalid"
    elif data[moveNumbers[str]] > 0:
        return "taken"
    return "yes"

def oppPlayer(no):
    if no == 1:
        return 2
    return 1

def cannedMove(gameData):
    squareOccupied = None
    for i in gameData:
        if gameData[i] > 0:
            if squareOccupied == None and squareOccupied != "Over":
                squareOccupied = i
            else:
                squareOccupied = "Over"
    if squareOccupied == 5:
        return 1
    elif squareOccupied == 6:
        return 7
    elif squareOccupied == 9:
        return 8
    elif squareOccupied == 10:
        return 14
    return None

def possibleMoves(player, remainingDepth, iterationData):
    foundMoves = []
    tempData = iterationData
    for i in range(16):
        if iterationData[i] == 0:
            newData = tempData.copy()
            newData[i] = player
            if remainingDepth == 0 or findWin(player, newData):
                foundMoves.append({"data": newData, "favorability": favorability(newData), "move": i})
            else:
                futureMoves = possibleMoves(oppPlayer(player), remainingDepth - 1, newData)
                newFavorability = favorability(newData)
                if playerSymbol == 1: # Use most positive favorability.
                    if futureMoves["worstFavorability"] > newFavorability:
                        newFavorability = futureMoves["worstFavorability"]
                elif playerSymbol == 2: # Use most negative favorability.
                    if futureMoves["worstFavorability"] < newFavorability:
                        newFavorability = futureMoves["worstFavorability"]
                    
                foundMoves.append({"data": newData, "favorability": newFavorability, "move": i, "responses": futureMoves["foundMoves"]})

    worstFavorability = None # Find the WORST CASE SCENARIO.
    for move in foundMoves:
        if worstFavorability == None:
            worstFavorability = move["favorability"]
    
        if playerSymbol == 1: # Since CPU is O, search for MOST POSITIVE favorability
            if move["favorability"] > worstFavorability:
                worstFavorability = move["favorability"]

        elif playerSymbol == 2: # Since CPU is X, search for MOST NEGATIVE favorability.
            if move["favorability"] < worstFavorability:
                worstFavorability = move["favorability"]

    #if remainingDepth == evaluationDepth - 1:
        #print("One move complete")
    
    return {"foundMoves": foundMoves, "worstFavorability": worstFavorability}

def findWin(player, gameData):
    for y in range(4): # Rows
        won = True
        for x in range(4):
            if not gameData[x + y * 4] == player:
                won = False
        if won:
            return True
    
    for x in range(4): # Columns
        won = True
        for y in range(4):
            if not gameData[x + y * 4] == player:
                won = False
        if won:
            return True

    won = True # Diagonals
    for d in range(4):
        if not gameData[d * 5] == player:
            won = False
    if won:
        return True

    won = True
    for d in range(4):
        if not gameData[3 + d * 3] == player:
            won = False
    if won:
        return True

    for x in range(3): # Squares
        for y in range(3):
            won = True
            
            if not gameData[x + y * 4] == player:
                won = False
            if not gameData[(x + 1) + y * 4] == player:
                won = False
            if not gameData[x + ((y + 1) * 4)] == player:
                won = False
            if not gameData[(x + 1) + ((y + 1) * 4)] == player:
                won = False
                
            if won:
                return True

    return False

def winFactor(player, gameData):
    factor = 0
    
    for y in range(4): # Rows
        localFactor = 3
        for x in range(4):
            if not gameData[x + y * 4] == player:
                localFactor -= 1
                if gameData[x + y * 4] == oppPlayer(player):
                    localFactor = -1
        if localFactor >= 0:
            factor += expFactor**localFactor
    
    for x in range(4): # Columns
        localFactor = 3
        for y in range(4):
            if not gameData[x + y * 4] == player:
                localFactor -= 1
                if gameData[x + y * 4] == oppPlayer(player):
                    localFactor = -1
        if localFactor >= 0:
            factor += expFactor**localFactor

    won = True # Diagonals
    localFactor = 3
    for d in range(4):
        if not gameData[d * 5] == player:
            localFactor -= 1
            if gameData[d * 5] == oppPlayer(player):
                localFactor = -1
    if localFactor >= 0:
        factor += expFactor**localFactor

    won = True
    localFactor = 3
    for d in range(4):
        if not gameData[3 + d * 3] == player:
            localFactor -= 1
            if gameData[d * 5] == oppPlayer(player):
                localFactor = -1
    if localFactor >= 0:
        factor += expFactor**localFactor

    for x in range(3): # Squares
        for y in range(3):
            localFactor = 3
            won = True
            
            if not gameData[x + y * 4] == player:
                localFactor -= 1
                if gameData[x + y * 4] == oppPlayer(player):
                    localFactor = -1
            if not gameData[(x + 1) + y * 4] == player:
                localFactor -= 1
                if gameData[(x + 1) + y * 4] == oppPlayer(player):
                    localFactor = -1
            if not gameData[x + ((y + 1) * 4)] == player:
                localFactor -= 1
                if gameData[x + ((y + 1) * 4)] == oppPlayer(player):
                    localFactor = -1
            if not gameData[(x + 1) + ((y + 1) * 4)] == player:
                localFactor -= 1
                if gameData[(x + 1) + ((y + 1) * 4)] == oppPlayer(player):
                    localFactor = -1
                
            if localFactor >= 0:
                factor += expFactor**localFactor

    return factor

def favorability(gameData):
    k = 0 # Positive indicates X favorability, negative indicates O favorability

    k += winFactor(1, gameData)
    k -= winFactor(2, gameData)

    return k

def cpuTurn():
    print("Computer is thinking.")

    cannedResponse = cannedMove(data)
    if cannedResponse != None:
        data[cannedResponse] = oppPlayer(playerSymbol)
    else:
        
        newEvaluationDepth = evaluationDepth
        if newEvaluationDepth >= remainingSquares:
            newEvaluationDepth = remainingSquares - 1
        evaluation = possibleMoves(oppPlayer(playerSymbol), newEvaluationDepth, data)["foundMoves"]

        bestFavorability = None # Find the BEST MOVE.
        bestMove = None
        for move in evaluation:
            #print(move["move"])
            #print(move["favorability"])
            if bestFavorability == None:
                bestFavorability = move["favorability"]
                bestMove = move["move"]
        
            if playerSymbol == 1: # Since CPU is O, search for MOST NEGATIVE favorability
                if move["favorability"] < bestFavorability:
                    bestFavorability = move["favorability"]
                    bestMove = move["move"]

            if playerSymbol == 2: # Since CPU is X, search for MOST POSITIVE favorability.
                if move["favorability"] > bestFavorability:
                    bestFavorability = move["favorability"]
                    bestMove = move["move"]

        data[bestMove] = oppPlayer(playerSymbol)

while True:
    newBoard()
    remainingSquares = 16
    allowPlayerToGo = False

    symbol = input("X or O? ")
    if symbol.lower() == "x":
        playerSymbol = 1
    else:
        playerSymbol = 2

    start = input("Who goes first? ")
    if start.lower() == "c" or start.lower() == "cpu" or start.lower() == "computer" or start.lower() == "you" or start.lower() == "u":
        playerStarts = False
    else:
        playerStarts = True
        printGame()
    
    while True:
        if playerStarts or allowPlayerToGo:
            move = input("Your move: ")
            while not validMove(move) == "yes":
                if validMove(move) == "invalid":
                    move = input("Not a valid move, valid moves include a1, d4, etc: ")
                elif validMove(move) == "taken":
                    move = input("Square taken, try again: ")

            data[moveNumbers[move]] = playerSymbol
            remainingSquares -= 1
            printGame()

            if findWin(playerSymbol, data):
                print("You win!")
                break

            if remainingSquares == 0:
                print("Tie game!")
                break

        cpuTurn()
        remainingSquares -= 1
        printGame()

        if findWin(oppPlayer(playerSymbol), data):
            print("You lose!")
            break

        if remainingSquares == 0:
            print("Tie game!")
            break

        allowPlayerToGo = True
        
    time.sleep(3)
