# ---------------------------------------------------------------------------------------- Variable Setups

#Sprite Arrays
piecesSprites: List[Sprite] = []
pieceValidSprites: List[Sprite] = []
pieceValidKillSprites: List[Sprite] = []
pieceValidKillSpritesCheckAll: List[Sprite] = []
pieceValidCastleSprites: List[Sprite] = []
tempSprites: List[Sprite] = []
#Num Arrays
selectorData: List[number] = [] #0,1=x,y 2=piece index 3,4 = original x,y
pieces: List[List[number]] = []
pieceValidSpaces: List[List[number]] = []
pieceValidSpacesCheckMate: List[List[number]] = []
pieceValidKillSpaces: List[List[number]] = []
pieceValidKillSpacesCheckMate: List[List[number]] = []
pieceValidKillSpacesCheckAll: List[List[number]] = []
pieceValidCastleSpaces: List[List[number]] = []


#Normal Variables
whoseTurn = 0
whoseTurnInvert = 1
pieceFound = False
volume = 0
sequence = 0
turnPawn: Sprite = None
selector: Sprite = None
checkmateBar: Sprite = None
tempSpriteNum = 0
placeFound = False
selectorData = [4, 4, None]
pawnFirstMove = False
selector = None
turnPawn = None
title: Sprite = None
buttonPlay: Sprite = None
dialogue: Sprite = None
buttonSettings: Sprite = None
colorPalletteSwitched = True
if blockSettings.read_number("Gamma") == None:
    blockSettings.write_number("Gamma", 0)
gamma = blockSettings.read_number("Gamma")
chosen = 0
check = 0
dialogueOpen = False
buttonSelected = 0
buttonSelectedMax = 2
swapType = 0
checked = 2 #0 = white | 1 = black | 2 = none
pieceAssetReference = [
    assets.image("""whitePawn"""),
    assets.image("""whiteBishop"""),
    assets.image("""whiteRook"""),
    assets.image("""whiteKnight"""),
    assets.image("""whiteQueen"""),
    assets.image("""whiteKing"""),
    assets.image("""blackPawn"""),
    assets.image("""blackBishop"""),
    assets.image("""blackRook"""),
    assets.image("""blackKnight"""),
    assets.image("""blackQueen"""),
    assets.image("""blackKing""")]
killSpaceAssetRefernce = [
    assets.image("""killSpace"""),
    assets.image("""debug"""),
    assets.image("""emptySpace""")]

deadPiecesOffsetWhite = 0
deadPiecesOffsetBlack = 0
# Original Chess Positions
# 0: 1=pawn  2=bishop  3=rook 4=knight 5=queen 6=king
# 1: 0=white 1=black
# 2,3: numbers are coordinates. Letters and numbers respectively.
# 4: if disabled (1), it will not be considered. 
# 5: special tag, for example, pawn not moved, king castling...
pieces = [
    [1, 0, 1, 2, 0, 1],
    [1, 0, 2, 2, 0, 1],
    [1, 0, 3, 2, 0, 1],
    [1, 0, 4, 2, 0, 1],
    [1, 0, 5, 2, 0, 1],
    [1, 0, 6, 2, 0, 1],
    [1, 0, 7, 2, 0, 1],
    [1, 0, 8, 2, 0, 1],
    [3, 0, 1, 1, 0],
    [3, 0, 8, 1, 0],
    [4, 0, 2, 1, 0],
    [4, 0, 7, 1, 0],
    [2, 0, 3, 1, 0],
    [2, 0, 6, 1, 0],
    [6, 0, 4, 1, 0, 1],
    [5, 0, 5, 1, 0],
    [1, 1, 1, 7, 0, 1],
    [1, 1, 2, 7, 0, 1],
    [1, 1, 3, 7, 0, 1],
    [1, 1, 4, 7, 0, 1],
    [1, 1, 5, 7, 0, 1],
    [1, 1, 6, 7, 0, 1],
    [1, 1, 7, 7, 0, 1],
    [1, 1, 8, 7, 0, 1],
    [3, 1, 1, 8, 0],
    [3, 1, 8, 8, 0],
    [4, 1, 2, 8, 0],
    [4, 1, 7, 8, 0],
    [2, 1, 3, 8, 0],
    [2, 1, 6, 8, 0],
    [6, 1, 4, 8, 0, 1],
    [5, 1, 5, 8, 0]]

pieces = [[5,0,4,4,0],[6,1,2,6,0,1],[3,1,1,5,0],[1,0,4,5,0,1],[1,0,8,1,0,1],[6,0,2,2,0,1]]  #Check testing
#pieces = [[6,0,4,1,1],[3,0,1,1],[3,0,8,1], [2,1,1,7], [2,1,3,7], [1,0,2,6,1]]  #Castle testing
#pieces = [[1,0,8,1,0,1]]
# ---------------------------------------------------------------------------------------- Board Funcs
def DrawPiecesProportionally(): #Takes the pieces array and creates pieces accordingly.
    global pieceAssetReference, piecesSprites
    scene.set_background_image(assets.image("""chessBoard"""))
    for i in range(len(pieces)):
        piecesSprites.append(sprites.create(CalPieceSprite(pieces[i][0],pieces[i][1])))
        SetPositionOnBoard(piecesSprites[i], pieces[i][2], pieces[i][3])
def SetPositionOnBoard(sprite: Sprite, toX, toY, selected = False, OffX = 0, OffY = 0): #Handy function for setting pieces into position.
    #thank god i made this btw
    goX = (6 + 12 * toX) + OffX
    goY = (117 - 12 * toY) + OffY
    if selected:
        goY -= 10
    if not sprite == None: sprite.set_position(goX, goY)
    return goX, goY
def CalculateValidSpaces(pieceNum, draw = False, arrayType = 0): #Calculates move spaces for the specified piece.
    global pieceValidSpaces, pieceValidSprites, pawnFirstMove, pieces, whoseTurn
    validSpacesFound = False
    noSpaces = False
    x = pieces[pieceNum][2]
    y = pieces[pieceNum][3]
    if pieces[pieceNum][4] == 1:
        print("CalculateValidSpaces-Piece is disabled, skipping.")
        return False
    #Pawn - 1 - nonlinear
    if pieces[pieceNum][0] == 1:
        validSpacesFound = True
        if pieces[pieceNum][1] == 0:
            if pieces[pieceNum][5] == 1:
                pawnFirstMove = True
                pieceValidSpaces = [[x, y + 1], [x, y + 2]]
            elif pieces[pieceNum][5] == 0:
                pieceValidSpaces = [[x, y + 1]]
        elif pieces[pieceNum][1] == 1:
            if pieces[pieceNum][5] == 1:
                pawnFirstMove = True
                pieceValidSpaces = [[x, y - 1], [x, y - 2]]
            elif pieces[pieceNum][5] == 0:
                pieceValidSpaces = [[x, y - 1]]
        for i in range(len(pieces)):
            if pieces[i][2] == pieceValidSpaces[0][0] and pieces[i][3] == pieceValidSpaces[0][1]:
                pieceValidSpaces.remove_at(1)
                pieceValidSpaces.remove_at(0)
                break

    # Bishop - 2 - linear
    elif pieces[pieceNum][0] == 2:
        validSpacesFound = True
        OccupiedSpace = False
        for i in range(8): #right up
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #left up
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #right down
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #left down
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
    # Rook - 3 - linear
    elif pieces[pieceNum][0] == 3:
        validSpacesFound = True
        OccupiedSpace = False
        for i in range(8): #right
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y
            for b in range(len(pieces)): #occupancy check
                if (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #left
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): # down
            OccupiedSpace = False
            g = i + 1
            estimateX = x
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #up
            OccupiedSpace = False
            g = i + 1
            estimateX = x
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
    #Knight - 4 - nonlinear
    elif pieces[pieceNum][0] == 4:
        validSpacesFound = True
        pieceValidSpaces = [[x + 2, y + 1], [x + 1, y + 2], [x - 2, y + 1], [x - 1, y + 2], [x + 2, y - 1], [x + 1, y - 2], [x - 2, y - 1], [x - 1, y - 2]]
    #Queen - 5 - linear
    elif pieces[pieceNum][0] == 5:
        validSpacesFound = True
        OccupiedSpace = False
        for i in range(8): #right
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y
            for b in range(len(pieces)): #occupancy check
                if (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #left
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #down
            OccupiedSpace = False
            g = i + 1
            estimateX = x
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #up
            OccupiedSpace = False
            g = i + 1
            estimateX = x
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #right up
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #left up
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #right down
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
        for i in range(8): #left down
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if  (estimateX == pieces[b][2] and estimateY == pieces[b][3]) or IsNumOutOfBounds(estimateX) or IsNumOutOfBounds(estimateY):
                    OccupiedSpace = True
            if not OccupiedSpace:
                pieceValidSpaces.append([estimateX, estimateY])
            else:
                break
    #King - 6 - nonlinear
    elif pieces[pieceNum][0] == 6:
        validSpacesFound = True
        pieceValidSpaces = [[x, y + 1], [x + 1, y + 1], [x + 1, y], [x + 1, y - 1], [x, y - 1], [x - 1, y - 1], [x - 1, y], [x - 1, y + 1]]
        
    # Checking for invalid spaces (nonlinear = base check, linear = failsafe )

    if noSpaces or len(pieceValidSpaces) == 0: #Check 1
        return False

    for a in range(len(pieces)):
        for b in range(len(pieceValidSpaces)):
            if(pieces[a][2] == pieceValidSpaces[b][0] and pieces[a][3] == pieceValidSpaces[b][1]) or IsNumOutOfBounds(pieceValidSpaces[b][0]) or IsNumOutOfBounds(pieceValidSpaces[b][1]):
                pieceValidSpaces.remove_at(b)
    
    if pieces[pieceNum][0] == 6:
        GetAllAttacksOfEnemies(whoseTurn)
        for a in range(len(pieceValidKillSpacesCheckAll)):
            for b in range(len(pieceValidSpaces)):
                if(pieceValidKillSpacesCheckAll[a][0] == pieceValidSpaces[b][0] and pieceValidKillSpacesCheckAll[a][1] == pieceValidSpaces[b][1]):
                    if draw: CreateTempSprite(600, assets.animation("""invalidSpaceAnim"""), pieceValidKillSpacesCheckAll[a][0], pieceValidKillSpacesCheckAll[a][1], 40, 0, 0, 10, True)
                    pieceValidSpaces.remove_at(b)
    
    if noSpaces or len(pieceValidSpaces) == 0: #Check 2
        return False

    if arrayType == 1:
        pieceValidSpaces = []

    # Drawing starts HERE-----
    if not draw:
        return validSpacesFound
    for i in range(len(pieceValidSpaces)):
        pieceValidSprites.append(sprites.create(assets.image("""
            validSpace
        """)))
        SetPositionOnBoard(pieceValidSprites[i],
            pieceValidSpaces[i][0],
            pieceValidSpaces[i][1],
            False,
            0,0)
        pieceValidSprites[i].z = -1
        animation.run_image_animation(pieceValidSprites[i], assets.animation("""validAnim"""), 400, True)
    return validSpacesFound
def CalculateKillSpaces(pieceNum, draw = False, arrayType = 0, bypassCheck = False, forCheck = False): #Calculates the available kills for the specified piece.
    global pieces, pieceValidKillSpaces, pieceValidKillSprites, whoseTurn, pieceValidKillSpacesCheckMate, pieceValidKillSpacesCheckAll,killSpaceAssetRefernce
    #print("CalculateKillSpaces-Initialized")
    if arrayType != 0:
        print("CalculateKillSpaces-arrayType-"+arrayType)
    if pieces[pieceNum][4] == 1:
        print("CalculateKillSpaces-Piece is disabled, skipping.")
        return False
    #eliminar
    pieceValidKillSpacesToCheck: List[List[number]] = []
    pieceValidKillSpacesChecked: List[List[number]] = []
    killSpacesFound = False
    x = pieces[pieceNum][2]
    y = pieces[pieceNum][3]
    #Pawn - 1 - nonlinear
    if pieces[pieceNum][0] == 1:
        noSpaceNum = 0;
        if pieces[pieceNum][1] == 0:
            pieceValidKillSpacesToCheck = [[x + 1, y + 1], [x - 1, y + 1]]
            killSpacesFound = True
        elif pieces[pieceNum][1] == 1:
            pieceValidKillSpacesToCheck = [[x + 1, y - 1], [x - 1, y - 1]]
            killSpacesFound = True
    #Bishop - 2 - linear
    elif pieces[pieceNum][0] == 2:
        killSpacesFound = True
        for i in range(8): #right up
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #left up
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #right down
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #left down
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
    #Rook - 3 - linear
    elif pieces[pieceNum][0] == 3:
        killSpacesFound = True
        for i in range(8): #right
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #left
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #down
            OccupiedSpace = False
            g = i + 1
            estimateX = x
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #up
            OccupiedSpace = False
            g = i + 1
            estimateX = x
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
    #Knight - 4 - nonlinear
    elif pieces[pieceNum][0] == 4:
        killSpacesFound = True
        pieceValidKillSpacesToCheck = [[x + 2, y + 1], [x + 1, y + 2], [x - 2, y + 1], [x - 1, y + 2], [x + 2, y - 1], [x + 1, y - 2], [x - 2, y - 1], [x - 1, y - 2]]
    #Queen - 5 - linear
    elif pieces[pieceNum][0] == 5:
        killSpacesFound = True
        for i in range(8): #right
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #left
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #down
            OccupiedSpace = False
            g = i + 1
            estimateX = x
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #up
            OccupiedSpace = False
            g = i + 1
            estimateX = x
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #right up
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #left up
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y + g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #right down
            OccupiedSpace = False
            g = i + 1
            estimateX = x + g
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
        for i in range(8): #left down
            OccupiedSpace = False
            g = i + 1
            estimateX = x - g
            estimateY = y - g
            for b in range(len(pieces)): #occupancy check
                if bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                if estimateX == pieces[b][2] and estimateY == pieces[b][3] and not (pieces[b][0]== 6 and pieces[b][1] == whoseTurn):
                    OccupiedSpace = True
            if OccupiedSpace:
                killSpacesFound = True
                if not bypassCheck: pieceValidKillSpacesToCheck.append([estimateX, estimateY])
                break
            else:
                pass
    #King - 6 - nonlinear
    elif pieces[pieceNum][0] == 6:
        killSpacesFound = True
        pieceValidKillSpacesToCheck = [[x, y + 1], [x + 1, y + 1], [x + 1, y], [x + 1, y - 1], [x, y - 1], [x - 1, y - 1], [x - 1, y], [x - 1, y + 1]]
    if killSpacesFound:
        pass
    else:
        return False

    if not bypassCheck:
        for i in range(len(pieces)):
            for c in range(len(pieceValidKillSpacesToCheck)):
                if (pieceValidKillSpacesToCheck[c][0] == pieces[i][2] and pieceValidKillSpacesToCheck[c][1] == pieces[i][3] and pieces[i][1] != whoseTurn):
                    pieceValidKillSpacesChecked.append([pieces[i][2], pieces[i][3]])
    else:
        pieceValidKillSpacesChecked = pieceValidKillSpacesToCheck

    if pieces[pieceNum][0] == 6 and not forCheck:
        GetAllAttacksOfEnemies(whoseTurn)
        for a in range(len(pieceValidKillSpacesCheckAll)):
            for b in range(len(pieceValidKillSpacesChecked)):
                if(pieceValidKillSpacesCheckAll[a][0] == pieceValidKillSpacesChecked[b][0] and pieceValidKillSpacesCheckAll[a][1] == pieceValidKillSpacesChecked[b][1]):
                    if draw: CreateTempSprite(600, assets.animation("""invalidSpaceAnim"""), pieceValidKillSpacesCheckAll[a][0], pieceValidKillSpacesCheckAll[a][1], 40, 0, 0, 10, True)
                    pieceValidKillSpacesChecked.remove_at(b)
    if arrayType == 0:
        pieceValidKillSpaces = pieceValidKillSpacesChecked
        pieceValidKillSpacesChecked = []
    elif arrayType == 1:
        pieceValidKillSpacesChecked = []
    elif arrayType == 2:
        pieceValidKillSpacesCheckAll = pieceValidKillSpacesCheckAll + pieceValidKillSpacesChecked
        pieceValidKillSpacesChecked = []
    if len(pieceValidKillSpaces) == 0:
        return False

    if not draw:
        return killSpacesFound;
    elif arrayType == 0:
        for i in range(len(pieceValidKillSpaces)):
            pieceValidKillSprites.append(sprites.create(killSpaceAssetRefernce[arrayType]))
            SetPositionOnBoard(pieceValidKillSprites[i],pieceValidKillSpaces[i][0],pieceValidKillSpaces[i][1])
            pieceValidKillSprites[i].z = 3
            if arrayType == 0: animation.run_image_animation(pieceValidKillSprites[i], assets.animation("""killSpaceAppear"""), 100, False)
    return killSpacesFound
def CalculateCastleSpaces(pieceNum, draw = False):
    global pieceValidCastleSpaces, pieceValidCastleSprites, pieces, piecesSprites, swapType
    castleSpaceFound = False
    leftEmpty = True
    rightEmpty = True
    print("CalculateCastleSpaces-Initialized")
    for i in range(2):
        print("CalculateCastleSpaces-RunningLeft-"+(i+1)+", 1")
        for b in range(len(pieces)):
            if pieces[b][2] == i + 2 and pieces[b][3] == 1:
                leftEmpty = False
    for i in range(3):
        print("CalculateCastleSpaces-RunningLeft-"+(i+5)+", 1")
        for b in range(len(pieces)):
            if pieces[b][2] == i + 5 and pieces[b][3] == 1:
                rightEmpty = False
    if pieces[pieceNum][0] != 6:
        print("CalculateCastleSpaces-Cancelled-WrongPiece")
        return False
    if pieces[pieceNum][1] == 0 and pieces[pieceNum][5] == 1:
        for i in range(len(pieces)):
            if pieces[i][1] == 0:
                if pieces[i][0] == 3:
                    if pieces[i][2] == 1 and pieces[i][3] == 1 and leftEmpty:
                        pieceValidCastleSpaces.append([1,1])
                        castleSpaceFound = True
                    elif pieces[i][2] == 8 and pieces[i][3] == 1 and rightEmpty:
                        pieceValidCastleSpaces.append([8,1])
                        castleSpaceFound = True
    if castleSpaceFound and draw:
        for i in range(len(pieceValidCastleSpaces)):
            pieceValidCastleSprites.append(sprites.create(assets.image("""castleSpace""")))
            SetPositionOnBoard(pieceValidCastleSprites[i],pieceValidCastleSpaces[i][0],pieceValidCastleSpaces[i][1])
            pieceValidCastleSprites[i].z = 3
            animation.run_image_animation(pieceValidCastleSprites[i], assets.animation("""castleSpaceAnim"""), 100, True)
    if castleSpaceFound:
        return True
    return False
def CheckForChecks(prediction = False): #Is the king in peril?
    global pieces, whoseTurn, whoseTurnInvert, checked, pieceValidKillSpacesCheckAll, checkmateBar, check
    print("CheckForChecks-Started")
    #here goes nothin!!!
    previousChecked = checked
    if not prediction: checked = 0
    kingID = 0
    actuallyChecked = False
    print("CheckForChecks-Chosen Ally:"+whoseTurn)
    for i in range(pieces.length):
        if pieces[i][0] == 6 and pieces[i][1] == whoseTurn:
            kingID = i
            print("CheckForChecks-KingFound")
    GetAllAttacksOfEnemies(whoseTurn)
    for i in range(len(pieceValidKillSpacesCheckAll)):
        #print("CheckForChecks-Running X "+pieceValidKillSpacesCheckAll[i][0])
        #print("CheckForChecks-Running Y "+pieceValidKillSpacesCheckAll[i][1])
        if pieces[kingID][2] == pieceValidKillSpacesCheckAll[i][0] and pieces[kingID][3] == pieceValidKillSpacesCheckAll[i][1]:
            print("CheckForChecks-King" + whoseTurn + " is in peril!")
            check = 1
            actuallyChecked = True
    if actuallyChecked and not prediction:
        checked = whoseTurn
        animation.run_image_animation(checkmateBar, assets.animation("""checkmateBarCheck"""), 50, False)
        if not CanKingMove():
            print("CheckForChecks-True Checkmate!")
            check = whoseTurn
            #animation.run_image_animation(checkmateBar, assets.animation("""checkmateBarCheckmate"""), 50, False)
    elif not prediction:
        print("checking if it's gone")
        if checked == 0 and previousChecked != checked: animation.run_image_animation(checkmateBar, assets.animation("""checkmateBarDecheck"""), 50, False)
    print("CheckForChecks-Complete-SpotsFound-"+len(pieceValidKillSpacesCheckAll))
    print("CheckForChecks-Complete-CheckValue-"+check)
    print("CheckForChecks-deletedAltArray")
    return(actuallyChecked)
def GetAllAttacksOfEnemies(recievingTeam): #Get ALL attack spaces of enemies for king movement
    global pieces, whoseTurn, pieceValidKillSpacesCheckAll
    pieceValidKillSpacesCheckAll = []
    for i in range(pieces.length):
        if pieces[i][1] != recievingTeam:
            #print("GetAllAttacksOfEnemies-RunningKillSpaceFor:"+pieces[i][0])
            CalculateKillSpaces(i, False, 2, True, True)
def CanKingMove(): #Returns a TRUE or FALSE depending if the king has valid moves/kills.
    global pieces, whoseTurn, whoseTurnInvert
    kingID = 0
    for i in range(pieces.length):
        if pieces[i][0] == 6 and pieces[i][1] == whoseTurn:
            kingID = i
    if CalculateValidSpaces(kingID, False, 1) or CalculateKillSpaces(kingID, False, 1):
        return True
    else:
        return False
def Setup(): #Initialize Commands, game is inert without them.
    global selector, turnPawn, checkmateBar
    selector = sprites.create(assets.image("""selector"""), 0)
    turnPawn = sprites.create(assets.image("""whitePawn"""), 0)
    checkmateBar  = sprites.create(assets.image("""checkmateBar"""), 0)
    checkmateBar.x = 138
    checkmateBar.y = 38
    selector.z = 4

    UpdateColors()
    DrawPiecesProportionally()
    SetPositionOnBoard(selector, selectorData[0], selectorData[1])
    SetPositionOnBoard(turnPawn, 12, 8, False, 1)

    controller.A.on_event(ControllerButtonEvent.PRESSED, selectorPickUp)
    controller.up.on_event(ControllerButtonEvent.PRESSED, SelectorGoUP)
    controller.down.on_event(ControllerButtonEvent.PRESSED, SelectorGoDOWN)
    controller.left.on_event(ControllerButtonEvent.PRESSED, SelectorGoLEFT)
    controller.right.on_event(ControllerButtonEvent.PRESSED, SelectorGoRIGHT)
def MainMenu(): #Draw menu and bind menu buttons. Also it looks cool :)
    global title, buttonSelected, sequence
    sequence = 1
    UpdateColors()
    buttonSelected = 0
    title = sprites.create(assets.image("""title"""))
    buttonPlay = sprites.create(assets.image("""buttonPlay"""))
    buttonPlay.x = 27
    buttonPlay.y = 50
    buttonSettings = sprites.create(assets.image("""buttonSettings"""))
    buttonSettings.x = 27
    buttonSettings.y = 65
    title.y = 20
    def BindMenuButtons():
        controller.up.on_event(ControllerButtonEvent.PRESSED, DecreaseSelection)
        controller.down.on_event(ControllerButtonEvent.PRESSED, IncreaseSelection)
        controller.A.on_event(ControllerButtonEvent.PRESSED, SelectSelection)
    def IncreaseSelection():
        global buttonSelected, buttonSelectedMax
        buttonSelected += 1
        if buttonSelected > buttonSelectedMax:
            buttonSelected = buttonSelectedMax
        buttonPlay.x = 27
        buttonSettings.x = 27
        if buttonSelected == 1:
            buttonPlay.x += 5
        elif buttonSelected == 2:
            buttonSettings.x += 5
    def DecreaseSelection():
        global buttonSelected, buttonSelectedMax
        buttonSelected -= 1
        if buttonSelected < 1:
            buttonSelected = 1
        buttonPlay.x = 27
        buttonSettings.x = 27
        if buttonSelected == 1:
            buttonPlay.x += 5
        elif buttonSelected == 2:
            buttonSettings.x += 5
    def SelectSelection():
        global gamma
        if buttonSelected == 1:
            title.destroy()
            buttonPlay.destroy()
            buttonSettings.destroy()
            for i in range(50):
                gamma -= 4
                UpdateColors()
                pause(1)
            Setup()
            UnbindAll()
            for i in range(50):
                gamma += 4
                UpdateColors()
                pause(1)
            BindAll()
        if buttonSelected == 2:
            OpenDialogue()
            if gamma > 50 or gamma < -30 or gamma == None or gamma != gamma:  game.splash("Invalid gamma number.")
            else: blockSettings.write_number("Gamma", gamma)
            gamma = blockSettings.read_number("Gamma")
            print(gamma)
            UpdateColors()
            controller.B.on_event(ControllerButtonEvent.PRESSED, CloseDialogue,)
    controller.up.on_event(ControllerButtonEvent.PRESSED, DecreaseSelection)
    controller.down.on_event(ControllerButtonEvent.PRESSED, IncreaseSelection)
    controller.A.on_event(ControllerButtonEvent.PRESSED, SelectSelection)
    animation.run_image_animation(title, assets.animation("""titleAnim"""), 1000, True)
    scene.set_background_image(assets.image("""mainMenu"""))
def PromotionSequence(pnum, team): #Sequence of promoting a pawn, mostly code about chosing the piece
    global piecesSprites, pieces
    selector.set_image(assets.image("""selectorPromotion"""))
    if team == 0: animation.run_image_animation(piecesSprites[pnum], assets.animation("promotionBegunWhite"), 50, False)
    if team == 1: animation.run_image_animation(piecesSprites[pnum], assets.animation("promotionBegunBlack"), 50, False)
    promotionRing = sprites.create(assets.image("""promotionChooser"""))
    animation.run_image_animation(promotionRing, assets.animation("""promotionChooserAppear"""), 100, False)
    promotionBishop = sprites.create(CalPieceSprite(2, team))
    promotionRook = sprites.create(CalPieceSprite(3, team))
    promotionKnight = sprites.create(CalPieceSprite(4, team))
    promotionQueen = sprites.create(CalPieceSprite(5, team))
    SetPositionOnBoard(selector, pieces[pnum][2], pieces[pnum][3])
    SetPositionOnBoard(promotionRing, pieces[pnum][2], pieces[pnum][3])
    SetPositionOnBoard(promotionBishop, pieces[pnum][2], pieces[pnum][3] + 1)
    SetPositionOnBoard(promotionRook, pieces[pnum][2], pieces[pnum][3] - 1)
    SetPositionOnBoard(promotionKnight, pieces[pnum][2] - 1, pieces[pnum][3])
    SetPositionOnBoard(promotionQueen, pieces[pnum][2] + 1, pieces[pnum][3])
    chosen = 0
    def GoUpBishop():
        global chosen
        chosen = 2
        SetPositionOnBoard(selector, pieces[pnum][2], pieces[pnum][3] + 1)
    def GoDownRook():
        global chosen
        chosen = 3
        SetPositionOnBoard(selector, pieces[pnum][2], pieces[pnum][3] - 1)
    def GoLeftKnight():
        global chosen
        chosen = 4
        SetPositionOnBoard(selector, pieces[pnum][2] - 1, pieces[pnum][3])
    def GoRightQueen():
        global chosen
        chosen = 5
        SetPositionOnBoard(selector, pieces[pnum][2] + 1, pieces[pnum][3])
    def SelectPromotion():
        global chosen,whoseTurn
        if chosen == 0:
            return None
        pieces[pnum][0] = chosen
        piecesSprites[pnum].set_image(CalPieceSprite(chosen, team))
        promotionBishop.destroy()
        promotionRook.destroy()
        promotionKnight.destroy()
        promotionQueen.destroy()
        promotionRing.destroy()
        selector.set_image(assets.image("""selector"""))
        SetPositionOnBoard(selector, pieces[pnum][2],pieces[pnum][3])
        CreateTempSprite(1000,assets.animation("""promotionChosen"""),pieces[pnum][2],pieces[pnum][3],100, 0, 0, 2, True)
        SafeAnimPause(1000)
        BindAll()
        CheckForChecks()
    SafePause(500)
    controller.up.on_event(ControllerButtonEvent.PRESSED, GoUpBishop)
    controller.down.on_event(ControllerButtonEvent.PRESSED, GoDownRook)
    controller.left.on_event(ControllerButtonEvent.PRESSED, GoLeftKnight)
    controller.right.on_event(ControllerButtonEvent.PRESSED, GoRightQueen)
    controller.A.on_event(ControllerButtonEvent.PRESSED, SelectPromotion)
def UpdateColors(): #Change color pallette, it would look dumb otherwise.
    global gamma
    color.set_color(1, color.rgb(CalGamma(255), CalGamma(255), CalGamma(255)))
    color.set_color(2, color.rgb(CalGamma(255), 0, 0))
    color.set_color(3, color.rgb(CalGamma(80), CalGamma(80), CalGamma(80)))
    color.set_color(4, color.rgb(CalGamma(180), CalGamma(180), CalGamma(180)))
    color.set_color(5, color.rgb(CalGamma(209), CalGamma(209), CalGamma(209)))
    color.set_color(6, color.rgb(CalGamma(90), CalGamma(90), CalGamma(90)))
    color.set_color(7, color.rgb(CalGamma(50), CalGamma(50), CalGamma(50)))
    color.set_color(8, color.rgb(CalGamma(60), CalGamma(60), CalGamma(60)))
    color.set_color(10, color.rgb(CalGamma(50), CalGamma(200), CalGamma(50)))
    color.set_color(9, color.rgb(CalGamma(255), CalGamma(159), 0))
    color.set_color(11, color.rgb(CalGamma(205), CalGamma(109), 0))
    color.set_color(14, color.rgb(CalGamma(50), CalGamma(150), CalGamma(50)))
    color.set_color(15, color.rgb(CalGamma(0), CalGamma(0), CalGamma(0)))
# ---------------------------------------------------------------------------------------- Selector Funcs
def SelectorGoRIGHT():
    if not (selectorData[0] == 8):
        selectorData[0] += 1
        SetPositionOnBoard(selector, selectorData[0], selectorData[1])
        if not (selectorData[2] == None):
            SetPositionOnBoard(piecesSprites[selectorData[2]],selectorData[0],selectorData[1],True)
    else:
        pass
def SelectorGoLEFT():
    if not (selectorData[0] == 1):
        selectorData[0] -= 1
        SetPositionOnBoard(selector, selectorData[0], selectorData[1])
        if not (selectorData[2] == None):
            SetPositionOnBoard(piecesSprites[selectorData[2]],
                selectorData[0],
                selectorData[1],
                True)
    else:
        pass
def SelectorGoUP():
    if not (selectorData[1] == 8):
        selectorData[1] += 1
        SetPositionOnBoard(selector, selectorData[0], selectorData[1])
        if not (selectorData[2] == None):
            SetPositionOnBoard(piecesSprites[selectorData[2]],
                selectorData[0],
                selectorData[1],
                True)
    else:
        pass
def SelectorGoDOWN():
    if not (selectorData[1] == 1):
        selectorData[1] -= 1
        SetPositionOnBoard(selector, selectorData[0], selectorData[1])
        if not (selectorData[2] == None):
            SetPositionOnBoard(piecesSprites[selectorData[2]],
                selectorData[0],
                selectorData[1],
                True)
    else:
        pass
def selectorPickUp():
    global pieceFound, whoseTurn
    somethingFound = False
    UnbindAll()
    for i in range(len(pieces)):
        if pieces[i][2] == selectorData[0] and pieces[i][3] == selectorData[1]:
            pieceFound = True
            selectorData[2] = i
            selectorData[3] = selectorData[0]
            selectorData[4] = selectorData[1]
            break
    if pieceFound and pieces[selectorData[2]][1] == whoseTurn:
        if pieces[selectorData[2]][1] == whoseTurn and (CalculateValidSpaces(selectorData[2]) or CalculateKillSpaces(selectorData[2])):
            print("SelectorPickUp-valid moves")
            if whoseTurn == 0: animation.run_image_animation(selector,assets.animation("""selectorPickupAnim"""), 30, False)
            elif whoseTurn == 1: animation.run_image_animation(selector,assets.animation("""selectorBlackPickupAnim"""), 30, False)
            #PickUpSoundEffect()
            controller.A.on_event(ControllerButtonEvent.PRESSED, ButtonBoundSelectorPutDown)
            controller.B.on_event(ControllerButtonEvent.PRESSED, selectorPutDownCancel)
            piecesSprites[selectorData[2]].set_position(piecesSprites[selectorData[2]].x,
                piecesSprites[selectorData[2]].y)
            piecesSprites[selectorData[2]].z = 3
            tempMemory = selectorData[2]
            SafeAnimPause(180, True)
            def frame1():
                piecesSprites[tempMemory].y += 1
            timer.after(60, frame1)
            def frame2():
                piecesSprites[tempMemory].y -= 1
            timer.after(90, frame2)
            def frame3():
                piecesSprites[tempMemory].y -= 3
            timer.after(120, frame3)
            def frame4():
                piecesSprites[tempMemory].y -= 5
            timer.after(150, frame4)
            def frame5():
                piecesSprites[tempMemory].y -= 1
            timer.after(180, frame5)
            CalculateValidSpaces(selectorData[2],True)
            CalculateKillSpaces(selectorData[2],True)
            if pieces[selectorData[2]][0] == 6: CalculateCastleSpaces(selectorData[2],True)
            pieceFound = False
            BindAll(True)
        else:
            print("SelectorPickUp-No valid spaces")
            selectorPutDown(True)
            pieceFound = False
            selectorData[2] = None
            #DenySoundEffect()
    else:
        print("SelectorPickUp-Piece was not found")
        selectorPutDown(True)
        pieceFound = False
        selectorData[2] = None
        #DenySoundEffect()
    BindAll(False)
def selectorPutDown(doNotSwitch = False, bypassCheck = False, noAnim = False):
    global placeFound, pieceValidSprites, pieceValidSpaces, pieceValidKillSprites, pieceValidKillSpaces, pieceValidCastleSpaces, pieceValidCastleSprites, pieces, pawnFirstMove
    global swapType, whoseTurnInvert, deadPiecesOffsetWhite, deadPiecesOffsetBlack, check, whoseTurn
    killingPlace = False
    swapPlace = False
    print("SelectorPutDown-Start")
    #UnbindAll()
    if check != 0 and not doNotSwitch:
        print("SelectorPutDown-Check Blockage start")
        piecesBuffer = pieces
        pieces[selectorData[2]][2] = selectorData[0]
        pieces[selectorData[2]][3] = selectorData[1]
        GetAllAttacksOfEnemies(whoseTurn)
        if CheckForChecks(True) and not bypassCheck:
            print("SelectorPutDown-Doesnt stop check")
            pieces = piecesBuffer
            for i in range(len(pieces)):
                if pieces[i][0] == 6 and pieces[i][1] == whoseTurn:
                    CreateTempSprite(800,assets.animation("attention"),pieces[i][2],pieces[i][3],200,0,0,-1,True)
            return
        else:
            print("SelectorPutDown-Does stop check")
            #check = 0
            #pieces = piecesBuffer
            pass
        print("SelectorPutDown-Check Blockage end")
    print("SelectorPutDown-Finding Spot")
    for i in range(len(pieceValidSpaces)):
        if selectorData[0] == pieceValidSpaces[i][0] and selectorData[1] == pieceValidSpaces[i][1]:
            placeFound = True
            print("SelectorPutDown-Found the spot")
            break
    print("SelectorPutDown-Finding kill spot")
    for i in range(len(pieceValidKillSpaces)):
        if selectorData[0] == pieceValidKillSpaces[i][0] and selectorData[1] == pieceValidKillSpaces[i][1]:
            killingPlace = True
            placeFound = True
            print("SelectorPutDown-Found the kill spot")
            #KillSoundEffect()
            #tempX, tempY = SetPositionOnBoard(None, selectorData[0],selectorData[1])
            #CreateTempSprite(300, assets.animation("""returnToDust"""), tempX, tempY, 60)
            break
    print("SelectorPutDown-Finding castle spot")
    for i in range(len(pieceValidCastleSpaces)):
        if selectorData[0] == pieceValidCastleSpaces[i][0] and selectorData[1] == pieceValidCastleSpaces[i][1]:
            swapPlace = True
            placeFound = True
            print("SelectorPutDown-Found castle spot")
            break
    if placeFound or bypassCheck:
        print("SelectorPutDown-Proceeding with placing")
        teamBuffer = whoseTurn
        if not doNotSwitch: SwitchingSides()
        promotion = False;
        #PutDownSoundEffect()
        controller.A.on_event(ControllerButtonEvent.PRESSED, selectorPickUp)
        controller.B.on_event(ControllerButtonEvent.PRESSED, None)
        piecesSprites[selectorData[2]].z = 0
        if pawnFirstMove and not bypassCheck:
            pieces[selectorData[2]][5] = 0
        if killingPlace:
            print("SelectorPutDown-Oh boy killing time")
            for i in range(len(pieces)):
                if pieces[i][2] == selectorData[0] and pieces[i][3] == selectorData[1]:
                    currentOffset = 0
                    if whoseTurn == 0: 
                        currentOffset = deadPiecesOffsetWhite
                        deadPiecesOffsetWhite += 2
                    elif whoseTurn == 1: 
                        currentOffset = deadPiecesOffsetBlack
                        deadPiecesOffsetBlack += 2
                    pieces[i][4] = 1 
                    pieces[i][2] = 10 + (whoseTurn * 2)
                    pieces[i][3] = 4
                    SetPositionOnBoard(piecesSprites[i], pieces[i][2], pieces[i][3], False, 0, currentOffset)
                    piecesSprites[i].z = currentOffset
                    break
        if swapPlace:
            for i in range(len(pieces)):
                if pieces[i][2] == selectorData[0] and pieces[i][3] == selectorData[1]:
                    SetPositionOnBoard(piecesSprites[i], pieces[i][2], pieces[i][3])
                    break
        pieces[selectorData[2]][2] = selectorData[0]
        pieces[selectorData[2]][3] = selectorData[1]
        if pieces[selectorData[2]][0] == 1:
            if pieces[selectorData[2]][1] == 0 and pieces[selectorData[2]][3] == 8:
                promotion = True
            if pieces[selectorData[2]][1] == 1 and pieces[selectorData[2]][3] == 1:
                promotion = True
        if pieces[selectorData[2]][5] == 1 and not bypassCheck:
            pieces[selectorData[2]][5] = 0
        SetPositionOnBoard(piecesSprites[selectorData[2]],
            pieces[selectorData[2]][2],
            pieces[selectorData[2]][3])
        for i in range(len(pieceValidSprites)):
            pieceValidSprites[i].destroy()
        for i in range(len(pieceValidKillSprites)):
            if pieceValidKillSpaces[i][0] == pieces[selectorData[2]][2] and pieceValidKillSpaces[i][1] == pieces[selectorData[2]][3]:
                CreateTempSprite(1000, assets.animation("""killSpaceKill"""), pieceValidKillSprites[i].x, pieceValidKillSprites[i].y, 80, 0, 0, 5)
            else:
                CreateTempSprite(300, assets.animation("""killSpaceDisappear"""), pieceValidKillSprites[i].x, pieceValidKillSprites[i].y, 100, 0, 0, 5)
            pieceValidKillSprites[i].destroy()
        for i in range(len(pieceValidCastleSprites)):
            pieceValidCastleSprites[i].destroy()
        if not noAnim and not promotion :
            if whoseTurn == 0: animation.run_image_animation(selector,assets.animation("""selectorPutdownAnim"""), 30, False)
            elif whoseTurn == 1: animation.run_image_animation(selector,assets.animation("""selectorBlackPutdownAnim"""), 30, False)
            tempMemory = selectorData[2]
            piecesSprites[tempMemory].y -= 9
            SafeAnimPause(250)
            def frame1():
                piecesSprites[tempMemory].y += 5
            timer.after(50, frame1)
            def frame2():
                piecesSprites[tempMemory].y += 4
            timer.after(100, frame2)
            def frame3():
                piecesSprites[tempMemory].y += 1
            timer.after(200, frame3)
            def frame4():
                piecesSprites[tempMemory].y -= 1
            timer.after(250, frame4)
        elif not promotion:
            #piecesSprites[selectorData[2]].y -= 1
            if whoseTurn == 0: selector.set_image(assets.image("""selector"""))
            else: selector.set_image(assets.image("""selectorBlack"""))
        elif promotion:
            PromotionSequence(selectorData[2], teamBuffer)
        selectorData[2] = None
        pieceValidSprites = []
        pieceValidSpaces = []
        pieceValidKillSpaces = []
        pieceValidKillSprites = []
        pieceValidCastleSpaces = []
        pieceValidCastleSprites = []
        placeFound = False
    if not (bypassCheck or doNotSwitch):
        CheckForChecks()
    #BindAll(False)
def selectorPutDownCancel():
    global pieceFound, selectorData, pawnFirstMove
    selectorData[0] = selectorData[3]
    selectorData[1] = selectorData[4]
    SetPositionOnBoard(piecesSprites[selectorData[2]],
    selectorData[0],
    selectorData[1],
    True)
    SetPositionOnBoard(selector, selectorData[0], selectorData[1])
    selectorPutDown(True, True, True)
    pieceFound = False
    selectorData[2] = None
    #CancelSoundEffect()
# ---------------------------------------------------------------------------------------- Misc/QOL Funcs
def SwitchingSides(): #Switches the sides, self-explanatory.
    global whoseTurn,whoseTurnInvert,check,checked
    bufferTurn = whoseTurn
    print("----------------------SIDES-SWITCHED")
    if whoseTurn == 0:
        animation.run_image_animation(turnPawn,
            assets.animation("""whiteTurnBlack"""),
            80,
            False)
        turnPawn.set_image(assets.image("""
            blackPawn
        """))
        whoseTurnInvert = 0
        whoseTurn = 1
    else:
        animation.run_image_animation(turnPawn,
            assets.animation("""blackTurnWhite"""),
            50,
            False)
        turnPawn.set_image(assets.image("""
            whitePawn
        """))
        whoseTurnInvert = 1
        whoseTurn = 0
    print("Check: "+check)
def SafePause(time, mode = False): #Stops the code for a second whilst unbinding the buttons to stop exploits.
    UnbindAll()
    pause(time)
    BindAll(mode)
def SafeAnimPause(time, mode = False): #Unbinds all buttons for set amount of time, to let animations play. WHILE letting the code run.
    def wait():
        UnbindAll()
        pause(time)
        BindAll(mode)
    timer.background(wait)
def ButtonBoundSelectorPutDown(): #A function with no inputs to be bound to the button.
    selectorPutDown()
def CreateTempSprite(delay, spriteAnimation, x, y, speed, ox = 0, oy = 0, z = 100, chessPositions = False): #Creates a temporary sprite to play an animation
    global tempSprites, tempSpriteNum
    tempSprites.append(sprites.create(assets.image("""emptySpace""")))
    tempSprites[len(tempSprites) - 1].x = x
    tempSprites[len(tempSprites) - 1].y = y
    if chessPositions: SetPositionOnBoard(tempSprites[len(tempSprites) - 1], x, y)
    tempSprites[len(tempSprites) - 1].x += ox
    tempSprites[len(tempSprites) - 1].y += oy
    tempSprites[len(tempSprites) - 1].z = z
    tempSpriteNum += 1
    animation.run_image_animation(tempSprites[len(tempSprites) - 1], spriteAnimation, speed, False)
    def on_debounce():
        tempSprites.shift().destroy()
    timer.debounce(str(tempSpriteNum), delay, on_debounce)
def IsNumOutOfBounds(numberGiven): #A compact version of checking if the coordinates are out of bounds
    if numberGiven > 8 or numberGiven < 1:
        return True
    else:
        return False
def UnbindAll(): #Unbinds all buttons.
    controller.A.on_event(ControllerButtonEvent.PRESSED, None)
    controller.up.on_event(ControllerButtonEvent.PRESSED, None)
    controller.down.on_event(ControllerButtonEvent.PRESSED, None)
    controller.left.on_event(ControllerButtonEvent.PRESSED, None)
    controller.right.on_event(ControllerButtonEvent.PRESSED, None)
def BindAll(mode = False): #Binds all buttons back.
    if mode:
        controller.A.on_event(ControllerButtonEvent.PRESSED, ButtonBoundSelectorPutDown)
        controller.B.on_event(ControllerButtonEvent.PRESSED, selectorPutDownCancel)
    else:
        controller.A.on_event(ControllerButtonEvent.PRESSED, selectorPickUp)
    controller.up.on_event(ControllerButtonEvent.PRESSED, SelectorGoUP)
    controller.down.on_event(ControllerButtonEvent.PRESSED, SelectorGoDOWN)
    controller.left.on_event(ControllerButtonEvent.PRESSED, SelectorGoLEFT)
    controller.right.on_event(ControllerButtonEvent.PRESSED, SelectorGoRIGHT)
def CalGamma(val):  #Caps out brightness values to stop looping and adds gamma.
    global gamma
    val += gamma
    if val > 255:
        return 255
    elif val < 0:
        return 0
    else:
        return val
def CalPieceSprite(pieceClass : number, team): #Get the sprite according to class type and team
    global pieceAssetReference
    offset = -1
    if team == 1:
        offset = 5
    spriteIndex = pieceClass + offset
    return pieceAssetReference[spriteIndex]
def OpenDialogue():
    global dialogueOpen,dialogue
    UnbindAll()
    dialogueOpen = True
    dialogue = sprites.create(assets.image("""dialogue"""))
    animation.run_image_animation(dialogue, assets.animation("dialogueOpen"), 100, False)
def CloseDialogue():
    global dialogueOpen,dialogue,sequence
    dialogueOpen = False
    CreateTempSprite(700, assets.animation("""dialogueClose"""),dialogue.x/2,dialogue.y/2,100,1,6)
    dialogue.destroy()
# ---------------------------------------------------------------------------------------- Starting Code
controller.menu.on_event(ControllerButtonEvent.PRESSED, None)
MainMenu()

