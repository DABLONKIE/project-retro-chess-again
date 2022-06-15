//  ---------------------------------------------------------------------------------------- Variable Setups
// Sprite Arrays
let piecesSprites : Sprite[] = []
let pieceValidSprites : Sprite[] = []
let pieceValidKillSprites : Sprite[] = []
let pieceValidKillSpritesCheckAll : Sprite[] = []
let pieceValidCastleSprites : Sprite[] = []
let tempSprites : Sprite[] = []
// Num Arrays
let selectorData : number[] = []
// 0,1=x,y 2=piece index 3,4 = original x,y
let pieces : number[][] = []
let pieceValidSpaces : number[][] = []
let pieceValidSpacesCheckMate : number[][] = []
let pieceValidKillSpaces : number[][] = []
let pieceValidKillSpacesCheckMate : number[][] = []
let pieceValidKillSpacesCheckAll : number[][] = []
let pieceValidCastleSpaces : number[][] = []
// Normal Variables
let whoseTurn = 0
let whoseTurnInvert = 1
let pieceFound = false
let volume = 0
let turnPawn : Sprite = null
let selector : Sprite = null
let checkmateBar : Sprite = null
let tempSpriteNum = 0
let placeFound = false
selectorData = [4, 4, null]
let pawnFirstMove = false
selector = null
turnPawn = null
let colorPalletteSwitched = true
let gamma = 0
let chosen = 0
let check = 0
let swapType = 0
let checked = 2
// 0 = white | 1 = black | 2 = none
let pieceAssetReference = [assets.image`whitePawn`, assets.image`whiteBishop`, assets.image`whiteRook`, assets.image`whiteKnight`, assets.image`whiteQueen`, assets.image`whiteKing`, assets.image`blackPawn`, assets.image`blackBishop`, assets.image`blackRook`, assets.image`blackKnight`, assets.image`blackQueen`, assets.image`blackKing`]
let killSpaceAssetRefernce = [assets.image`killSpace`, assets.image`debug`, assets.image`emptySpace`]
let deadPiecesOffsetWhite = 0
let deadPiecesOffsetBlack = 0
//  Original Chess Positions
//  0: 1=pawn  2=bishop  3=rook 4=knight 5=queen 6=king
//  1: 0=white 1=black
//  2 & 3: numbers are coordinates. Letters and numbers respectively.
//  4: special tag, for example, pawn not moved, king castlin
pieces = [[1, 0, 1, 2, 1], [1, 0, 2, 2, 1], [1, 0, 3, 2, 1], [1, 0, 4, 2, 1], [1, 0, 5, 2, 1], [1, 0, 6, 2, 1], [1, 0, 7, 2, 1], [1, 0, 8, 2, 1], [3, 0, 1, 1], [3, 0, 8, 1], [4, 0, 2, 1], [4, 0, 7, 1], [2, 0, 3, 1], [2, 0, 6, 1], [6, 0, 4, 1, 1], [5, 0, 5, 1], [1, 1, 1, 7, 1], [1, 1, 2, 7, 1], [1, 1, 3, 7, 1], [1, 1, 4, 7, 1], [1, 1, 5, 7, 1], [1, 1, 6, 7, 1], [1, 1, 7, 7, 1], [1, 1, 8, 7, 1], [3, 1, 1, 8], [3, 1, 8, 8], [4, 1, 2, 8], [4, 1, 7, 8], [2, 1, 3, 8], [2, 1, 6, 8], [6, 1, 4, 8, 1], [5, 1, 5, 8]]
// pieces = [[1,0,6,6,1],[6,1,4,6]]  #Check testing
// pieces = [[6,0,4,1,1],[3,0,1,1],[3,0,8,1], [2,1,1,7], [2,1,3,7], [1,0,2,6,1]]  #Castle testing
//  ---------------------------------------------------------------------------------------- Board Funcs
function DrawPiecesProportionally() {
    // Takes the pieces array and creates pieces accordingly.
    
    scene.setBackgroundImage(assets.image`chessBoard`)
    for (let i = 0; i < pieces.length; i++) {
        piecesSprites.push(sprites.create(CalPieceSprite(pieces[i][0], pieces[i][1])))
        SetPositionOnBoard(piecesSprites[i], pieces[i][2], pieces[i][3])
    }
}

function SetPositionOnBoard(sprite: Sprite, toX: number, toY: number, selected: boolean = false, OffX: number = 0, OffY: number = 0): number[] {
    // Handy function for setting pieces into position.
    // thank god i made this btw
    let goX = 6 + 12 * toX + OffX
    let goY = 117 - 12 * toY + OffY
    if (selected) {
        goY -= 10
    }
    
    if (!(sprite == null)) {
        sprite.setPosition(goX, goY)
    }
    
    return [goX, goY]
}

function CalculateValidSpaces(pieceNum: number, draw: boolean = false, arrayType: number = 0): boolean {
    let i: number;
    let OccupiedSpace: boolean;
    let g: number;
    let estimateX: number;
    let estimateY: number;
    let b: number;
    let a: number;
    let pieceValidKillSpacesCheckAll: number[][];
    // Calculates move spaces for the specified piece.
    
    let validSpacesFound = false
    let noSpaces = false
    let x = pieces[pieceNum][2]
    let y = pieces[pieceNum][3]
    console.log("CalculateValidSpaces-started")
    // Pawn - 1 - nonlinear
    if (pieces[pieceNum][0] == 1) {
        validSpacesFound = true
        if (pieces[pieceNum][1] == 0) {
            if (pieces[pieceNum][4] == 1) {
                pawnFirstMove = true
                pieceValidSpaces = [[x, y + 1], [x, y + 2]]
            } else if (pieces[pieceNum][4] == 0) {
                pieceValidSpaces = [[x, y + 1]]
            }
            
        } else if (pieces[pieceNum][1] == 1) {
            if (pieces[pieceNum][4] == 1) {
                pawnFirstMove = true
                pieceValidSpaces = [[x, y - 1], [x, y - 2]]
            } else if (pieces[pieceNum][4] == 0) {
                pieceValidSpaces = [[x, y - 1]]
            }
            
        }
        
        for (i = 0; i < pieces.length; i++) {
            if (pieces[i][2] == pieceValidSpaces[0][0] && pieces[i][3] == pieceValidSpaces[0][1]) {
                pieceValidSpaces.removeAt(1)
                pieceValidSpaces.removeAt(0)
                break
            }
            
        }
    } else if (pieces[pieceNum][0] == 2) {
        //  Bishop - 2 - linear
        validSpacesFound = true
        OccupiedSpace = false
        for (i = 0; i < 8; i++) {
            // right up
            OccupiedSpace = false
            g = i + 1
            estimateX = x + g
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left up
            OccupiedSpace = false
            g = i + 1
            estimateX = x - g
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // right down
            OccupiedSpace = false
            g = i + 1
            estimateX = x + g
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left down
            OccupiedSpace = false
            g = i + 1
            estimateX = x - g
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
    } else if (pieces[pieceNum][0] == 3) {
        //  Rook - 3 - linear
        validSpacesFound = true
        OccupiedSpace = false
        for (i = 0; i < 8; i++) {
            // right
            OccupiedSpace = false
            g = i + 1
            estimateX = x + g
            estimateY = y
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left
            OccupiedSpace = false
            g = i + 1
            estimateX = x - g
            estimateY = y
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            //  down
            OccupiedSpace = false
            g = i + 1
            estimateX = x
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // up
            OccupiedSpace = false
            g = i + 1
            estimateX = x
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
    } else if (pieces[pieceNum][0] == 4) {
        // Knight - 4 - nonlinear
        validSpacesFound = true
        pieceValidSpaces = [[x + 2, y + 1], [x + 1, y + 2], [x - 2, y + 1], [x - 1, y + 2], [x + 2, y - 1], [x + 1, y - 2], [x - 2, y - 1], [x - 1, y - 2]]
    } else if (pieces[pieceNum][0] == 5) {
        // Queen - 5 - linear
        validSpacesFound = true
        OccupiedSpace = false
        for (i = 0; i < 8; i++) {
            // right
            OccupiedSpace = false
            g = i + 1
            estimateX = x + g
            estimateY = y
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left
            OccupiedSpace = false
            g = i + 1
            estimateX = x - g
            estimateY = y
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // down
            OccupiedSpace = false
            g = i + 1
            estimateX = x
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // up
            OccupiedSpace = false
            g = i + 1
            estimateX = x
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // right up
            OccupiedSpace = false
            g = i + 1
            estimateX = x + g
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left up
            OccupiedSpace = false
            g = i + 1
            estimateX = x - g
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // right down
            OccupiedSpace = false
            g = i + 1
            estimateX = x + g
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left down
            OccupiedSpace = false
            g = i + 1
            estimateX = x - g
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3] || IsNumOutOfBounds(estimateX) || IsNumOutOfBounds(estimateY)) {
                    OccupiedSpace = true
                }
                
            }
            if (!OccupiedSpace) {
                pieceValidSpaces.push([estimateX, estimateY])
            } else {
                break
            }
            
        }
    } else if (pieces[pieceNum][0] == 6) {
        // King - 6 - nonlinear
        validSpacesFound = true
        pieceValidSpaces = [[x, y + 1], [x + 1, y + 1], [x + 1, y], [x + 1, y - 1], [x, y - 1], [x - 1, y - 1], [x - 1, y], [x - 1, y + 1]]
        GetAllAttacksOfEnemies(whoseTurn)
        for (a = 0; a < pieceValidKillSpacesCheckAll.length; a++) {
            for (b = 0; b < pieceValidSpaces.length; b++) {
                if (pieceValidKillSpacesCheckAll[a][0] == pieceValidSpaces[b][0] && pieceValidKillSpacesCheckAll[a][1] == pieceValidSpaces[b][1]) {
                    if (draw) {
                        CreateTempSprite(600, assets.animation`invalidSpaceAnim`, pieceValidKillSpacesCheckAll[a][0], pieceValidKillSpacesCheckAll[a][1], 40, 0, 0, 10, true)
                    }
                    
                    pieceValidSpaces.removeAt(b)
                }
                
            }
        }
        pieceValidKillSpacesCheckAll = []
    }
    
    //  Checking for invalid spaces (nonlinear = base check, linear = failsafe )
    let piecesToCheck = pieces.length
    let piecesChecked = 0
    if (noSpaces || pieceValidSpaces.length == 0) {
        // Check 1
        return false
    }
    
    for (a = 0; a < pieces.length; a++) {
        for (b = 0; b < pieceValidSpaces.length; b++) {
            if (pieces[a][2] == pieceValidSpaces[b][0] && pieces[a][3] == pieceValidSpaces[b][1] || IsNumOutOfBounds(pieceValidSpaces[b][0]) || IsNumOutOfBounds(pieceValidSpaces[b][1])) {
                pieceValidSpaces.removeAt(b)
            }
            
        }
    }
    if (noSpaces || pieceValidSpaces.length == 0) {
        // Check 2
        return false
    }
    
    //  Drawing starts HERE-----
    if (!draw) {
        return validSpacesFound
    }
    
    for (i = 0; i < pieceValidSpaces.length; i++) {
        pieceValidSprites.push(sprites.create(assets.image`
            validSpace
        `))
        SetPositionOnBoard(pieceValidSprites[i], pieceValidSpaces[i][0], pieceValidSpaces[i][1], false, 0, 0)
        pieceValidSprites[i].z = -1
        animation.runImageAnimation(pieceValidSprites[i], assets.animation`validAnim`, 400, true)
    }
    return validSpacesFound
}

function CalculateKillSpaces(pieceNum: number, draw: boolean = false, arrayType: number = 0, bypassCheck: boolean = false, forCheck: boolean = false): boolean {
    let noSpaceNum: number;
    let i: number;
    let OccupiedSpace: boolean;
    let g: number;
    let estimateX: number;
    let estimateY: number;
    let b: number;
    // Calculates the available kills for the specified piece.
    
    // eliminar
    let pieceValidKillSpacesToCheck : number[][] = []
    let pieceValidKillSpacesChecked : number[][] = []
    let killSpacesFound = false
    let x = pieces[pieceNum][2]
    let y = pieces[pieceNum][3]
    // Pawn - 1 - nonlinear
    if (pieces[pieceNum][0] == 1) {
        noSpaceNum = 0
        if (pieces[pieceNum][1] == 0) {
            pieceValidKillSpacesToCheck = [[x + 1, y + 1], [x - 1, y + 1]]
            killSpacesFound = true
        } else if (pieces[pieceNum][1] == 1) {
            pieceValidKillSpacesToCheck = [[x + 1, y - 1], [x - 1, y - 1]]
            killSpacesFound = true
        }
        
    } else if (pieces[pieceNum][0] == 2) {
        // Bishop - 2 - linear
        killSpacesFound = true
        for (i = 0; i < 8; i++) {
            // right up
            OccupiedSpace = false
            if (bypassCheck) {
                OccupiedSpace = true
            }
            
            g = i + 1
            estimateX = x + g
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                if (!bypassCheck) {
                    break
                }
                
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left up
            OccupiedSpace = false
            if (bypassCheck) {
                OccupiedSpace = true
            }
            
            g = i + 1
            estimateX = x - g
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                if (!bypassCheck) {
                    break
                }
                
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // right down
            OccupiedSpace = false
            if (bypassCheck) {
                OccupiedSpace = true
            }
            
            g = i + 1
            estimateX = x + g
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                if (!bypassCheck) {
                    break
                }
                
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left down
            OccupiedSpace = false
            if (bypassCheck) {
                OccupiedSpace = true
            }
            
            g = i + 1
            estimateX = x - g
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                if (!bypassCheck) {
                    break
                }
                
            } else {
                
            }
            
        }
    } else if (pieces[pieceNum][0] == 3) {
        // Rook - 3 - linear
        killSpacesFound = true
        for (i = 0; i < 8; i++) {
            // right
            OccupiedSpace = false
            if (bypassCheck) {
                OccupiedSpace = true
            }
            
            g = i + 1
            estimateX = x + g
            estimateY = y
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                if (!bypassCheck) {
                    break
                }
                
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left
            OccupiedSpace = false
            if (bypassCheck) {
                OccupiedSpace = true
            }
            
            g = i + 1
            estimateX = x - g
            estimateY = y
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                if (!bypassCheck) {
                    break
                }
                
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // down
            OccupiedSpace = false
            if (bypassCheck) {
                OccupiedSpace = true
            }
            
            g = i + 1
            estimateX = x
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                if (!bypassCheck) {
                    break
                }
                
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // up
            OccupiedSpace = false
            if (bypassCheck) {
                OccupiedSpace = true
            }
            
            g = i + 1
            estimateX = x
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                if (!bypassCheck) {
                    break
                }
                
            } else {
                
            }
            
        }
    } else if (pieces[pieceNum][0] == 4) {
        // Knight - 4 - nonlinear
        killSpacesFound = true
        pieceValidKillSpacesToCheck = [[x + 2, y + 1], [x + 1, y + 2], [x - 2, y + 1], [x - 1, y + 2], [x + 2, y - 1], [x + 1, y - 2], [x - 2, y - 1], [x - 1, y - 2]]
    } else if (pieces[pieceNum][0] == 5) {
        // Queen - 5 - linear
        killSpacesFound = true
        for (i = 0; i < 8; i++) {
            // right
            OccupiedSpace = false
            g = i + 1
            estimateX = x + g
            estimateY = y
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (bypassCheck) {
                    pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                }
                
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                break
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left
            OccupiedSpace = false
            g = i + 1
            estimateX = x - g
            estimateY = y
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (bypassCheck) {
                    pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                }
                
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                break
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // down
            OccupiedSpace = false
            g = i + 1
            estimateX = x
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (bypassCheck) {
                    pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                }
                
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                break
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // up
            OccupiedSpace = false
            g = i + 1
            estimateX = x
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (bypassCheck) {
                    pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                }
                
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                break
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // right up
            OccupiedSpace = false
            g = i + 1
            estimateX = x + g
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (bypassCheck) {
                    pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                }
                
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                break
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left up
            OccupiedSpace = false
            g = i + 1
            estimateX = x - g
            estimateY = y + g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (bypassCheck) {
                    pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                }
                
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                break
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // right down
            OccupiedSpace = false
            g = i + 1
            estimateX = x + g
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (bypassCheck) {
                    pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                }
                
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                break
            } else {
                
            }
            
        }
        for (i = 0; i < 8; i++) {
            // left down
            OccupiedSpace = false
            g = i + 1
            estimateX = x - g
            estimateY = y - g
            for (b = 0; b < pieces.length; b++) {
                // occupancy check
                if (bypassCheck) {
                    pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                }
                
                if (estimateX == pieces[b][2] && estimateY == pieces[b][3]) {
                    OccupiedSpace = true
                }
                
            }
            if (OccupiedSpace) {
                killSpacesFound = true
                pieceValidKillSpacesToCheck.push([estimateX, estimateY])
                break
            } else {
                
            }
            
        }
    } else if (pieces[pieceNum][0] == 6) {
        // King - 6 - nonlinear
        killSpacesFound = true
        pieceValidKillSpacesToCheck = [[x, y + 1], [x + 1, y + 1], [x + 1, y], [x + 1, y - 1], [x, y - 1], [x - 1, y - 1], [x - 1, y], [x - 1, y + 1]]
        if (!forCheck) {
            GetAllAttacksOfEnemies(whoseTurn)
            for (let a = 0; a < pieceValidKillSpacesCheckAll.length; a++) {
                for (b = 0; b < pieceValidKillSpacesToCheck.length; b++) {
                    if (pieceValidKillSpacesCheckAll[a][0] == pieceValidKillSpacesToCheck[b][0] && pieceValidKillSpacesCheckAll[a][1] == pieceValidKillSpacesToCheck[b][1]) {
                        if (draw) {
                            CreateTempSprite(600, assets.animation`invalidSpaceAnim`, pieceValidKillSpacesCheckAll[a][0], pieceValidKillSpacesCheckAll[a][1], 40, 0, 0, 10, true)
                        }
                        
                        pieceValidKillSpacesToCheck.removeAt(b)
                    }
                    
                }
            }
        }
        
        pieceValidKillSpacesCheckAll = []
    }
    
    // ---
    if (killSpacesFound) {
        
    } else {
        return false
    }
    
    // ---
    if (!bypassCheck) {
        for (i = 0; i < pieces.length; i++) {
            for (let c = 0; c < pieceValidKillSpacesToCheck.length; c++) {
                if (pieceValidKillSpacesToCheck[c][0] == pieces[i][2] && pieceValidKillSpacesToCheck[c][1] == pieces[i][3] && pieces[i][1] != whoseTurn) {
                    pieceValidKillSpacesChecked.push([pieces[i][2], pieces[i][3]])
                }
                
            }
        }
    } else {
        pieceValidKillSpacesChecked = pieceValidKillSpacesToCheck
    }
    
    if (arrayType == 0) {
        pieceValidKillSpaces = pieceValidKillSpacesChecked
        pieceValidKillSpacesChecked = []
    } else if (arrayType == 1) {
        pieceValidKillSpacesChecked = []
    } else if (arrayType == 2) {
        pieceValidKillSpacesCheckAll = pieceValidKillSpacesCheckAll.concat(pieceValidKillSpacesChecked)
        pieceValidKillSpacesChecked = []
    }
    
    if (pieceValidKillSpaces.length == 0) {
        return false
    }
    
    if (!draw) {
        return killSpacesFound
    } else if (arrayType == 0) {
        for (i = 0; i < pieceValidKillSpaces.length; i++) {
            pieceValidKillSprites.push(sprites.create(killSpaceAssetRefernce[arrayType]))
            SetPositionOnBoard(pieceValidKillSprites[i], pieceValidKillSpaces[i][0], pieceValidKillSpaces[i][1])
            pieceValidKillSprites[i].z = 3
            if (arrayType == 0) {
                animation.runImageAnimation(pieceValidKillSprites[i], assets.animation`killSpaceAppear`, 100, false)
            }
            
        }
    }
    
    return killSpacesFound
}

function CalculateCastleSpaces(pieceNum: number, draw: boolean = false): boolean {
    let i: number;
    let b: number;
    
    let castleSpaceFound = false
    let leftEmpty = true
    let rightEmpty = true
    console.log("CalculateCastleSpaces-Initialized")
    for (i = 0; i < 2; i++) {
        console.log("CalculateCastleSpaces-RunningLeft-" + (i + 1) + ", 1")
        for (b = 0; b < pieces.length; b++) {
            if (pieces[b][2] == i + 2 && pieces[b][3] == 1) {
                leftEmpty = false
            }
            
        }
    }
    for (i = 0; i < 3; i++) {
        console.log("CalculateCastleSpaces-RunningLeft-" + (i + 5) + ", 1")
        for (b = 0; b < pieces.length; b++) {
            if (pieces[b][2] == i + 5 && pieces[b][3] == 1) {
                rightEmpty = false
            }
            
        }
    }
    if (pieces[pieceNum][0] != 6) {
        console.log("CalculateCastleSpaces-Cancelled-WrongPiece")
        return false
    }
    
    if (pieces[pieceNum][1] == 0 && pieces[pieceNum][4] == 1) {
        for (i = 0; i < pieces.length; i++) {
            if (pieces[i][1] == 0) {
                if (pieces[i][0] == 3) {
                    if (pieces[i][2] == 1 && pieces[i][3] == 1 && leftEmpty) {
                        pieceValidCastleSpaces.push([1, 1])
                        castleSpaceFound = true
                    } else if (pieces[i][2] == 8 && pieces[i][3] == 1 && rightEmpty) {
                        pieceValidCastleSpaces.push([8, 1])
                        castleSpaceFound = true
                    }
                    
                }
                
            }
            
        }
    }
    
    if (castleSpaceFound && draw) {
        for (i = 0; i < pieceValidCastleSpaces.length; i++) {
            pieceValidCastleSprites.push(sprites.create(assets.image`castleSpace`))
            SetPositionOnBoard(pieceValidCastleSprites[i], pieceValidCastleSpaces[i][0], pieceValidCastleSpaces[i][1])
            pieceValidCastleSprites[i].z = 3
            animation.runImageAnimation(pieceValidCastleSprites[i], assets.animation`castleSpaceAnim`, 100, true)
        }
    }
    
    if (castleSpaceFound) {
        return true
    }
    
    return false
}

function CheckForChecks() {
    let i: number;
    // Is the king in peril?
    
    console.log("CheckForChecks-Started")
    // here goes nothin!!!
    let kingID = 0
    let actuallyChecked = false
    console.log("CheckForChecks-ally:" + whoseTurn)
    console.log("CheckForChecks-foe:" + whoseTurnInvert)
    for (i = 0; i < pieces.length; i++) {
        if (pieces[i][0] == 6 && pieces[i][1] == whoseTurn) {
            kingID = i
            console.log("CheckForChecks-KingFound")
        }
        
    }
    GetAllAttacksOfEnemies(whoseTurn)
    for (i = 0; i < pieceValidKillSpacesCheckAll.length; i++) {
        console.log("CheckForChecks-Running X " + pieceValidKillSpacesCheckAll[i][0])
        console.log("CheckForChecks-Running Y " + pieceValidKillSpacesCheckAll[i][1])
        if (pieces[kingID][2] == pieceValidKillSpacesCheckAll[i][0] && pieces[kingID][3] == pieceValidKillSpacesCheckAll[i][1]) {
            console.log("CheckForChecks-King" + whoseTurn + " is in peril!")
            checked = whoseTurn
            actuallyChecked = true
        }
        
    }
    if (actuallyChecked) {
        check = 1
        animation.runImageAnimation(checkmateBar, assets.animation`checkmateBarCheck`, 50, false)
        if (!CanKingMove()) {
            check = 2
            animation.runImageAnimation(checkmateBar, assets.animation`checkmateBarCheckmate`, 50, false)
        }
        
    } else if (check == 1) {
        animation.runImageAnimation(checkmateBar, assets.animation`checkmateBarDecheck`, 50, false)
    }
    
    console.log("CheckForChecks-Complete-SpotsFound-" + pieceValidKillSpacesCheckAll.length)
    console.log("CheckForChecks-deletedAltArray")
    console.log("----------------------------NEW-TURN")
}

function GetAllAttacksOfEnemies(recievingTeam: number) {
    // Get ALL attack spaces of enemies for king movement
    
    pieceValidKillSpacesCheckAll = []
    for (let i = 0; i < pieces.length; i++) {
        if (pieces[i][1] != recievingTeam) {
            // print("GetAllAttacksOfEnemies-RunningKillSpaceFor:"+pieces[i][0])
            CalculateKillSpaces(i, false, 2, true, true)
        }
        
    }
}

function CanKingMove(): boolean {
    // Returns a TRUE or FALSE depending if the king has valid moves/kills.
    
    let kingID = 0
    for (let i = 0; i < pieces.length; i++) {
        if (pieces[i][0] == 6 && pieces[i][1] == whoseTurn) {
            kingID = i
        }
        
    }
    if (CalculateValidSpaces(kingID, false, 1) || CalculateKillSpaces(kingID, false, 1)) {
        return true
    } else {
        return false
    }
    
}

function Setup() {
    // Initialize Commands, game is inert without them.
    
    selector = sprites.create(assets.image`selector`, 0)
    turnPawn = sprites.create(assets.image`whitePawn`, 0)
    checkmateBar = sprites.create(assets.image`checkmateBar`, 0)
    checkmateBar.x = 138
    checkmateBar.y = 38
    selector.z = 4
    UpdateColors()
    DrawPiecesProportionally()
    SetPositionOnBoard(selector, selectorData[0], selectorData[1])
    SetPositionOnBoard(turnPawn, 12, 8, false, 1)
    controller.A.onEvent(ControllerButtonEvent.Pressed, selectorPickUp)
    controller.up.onEvent(ControllerButtonEvent.Pressed, SelectorGoUP)
    controller.down.onEvent(ControllerButtonEvent.Pressed, SelectorGoDOWN)
    controller.left.onEvent(ControllerButtonEvent.Pressed, SelectorGoLEFT)
    controller.right.onEvent(ControllerButtonEvent.Pressed, SelectorGoRIGHT)
}

function PromotionSequence(pnum: number, team: number) {
    // Sequence of promoting a pawn, mostly code about chosing the piece
    
    selector.setImage(assets.image`selectorPromotion`)
    if (team == 0) {
        animation.runImageAnimation(piecesSprites[pnum], assets.animation`promotionBegunWhite`, 100, false)
    }
    
    if (team == 1) {
        animation.runImageAnimation(piecesSprites[pnum], assets.animation`promotionBegunBlack`, 100, false)
    }
    
    let promotionRing = sprites.create(assets.image`promotionChooser`)
    animation.runImageAnimation(promotionRing, assets.animation`promotionChooserAppear`, 200, true)
    let promotionBishop = sprites.create(CalPieceSprite(2, team))
    let promotionRook = sprites.create(CalPieceSprite(3, team))
    let promotionKnight = sprites.create(CalPieceSprite(4, team))
    let promotionQueen = sprites.create(CalPieceSprite(5, team))
    SetPositionOnBoard(selector, pieces[pnum][2], pieces[pnum][3])
    SetPositionOnBoard(promotionRing, pieces[pnum][2], pieces[pnum][3])
    SetPositionOnBoard(promotionBishop, pieces[pnum][2], pieces[pnum][3] + 1)
    SetPositionOnBoard(promotionRook, pieces[pnum][2], pieces[pnum][3] - 1)
    SetPositionOnBoard(promotionKnight, pieces[pnum][2] - 1, pieces[pnum][3])
    SetPositionOnBoard(promotionQueen, pieces[pnum][2] + 1, pieces[pnum][3])
    let chosen = 0
    SafePause(700)
    controller.up.onEvent(ControllerButtonEvent.Pressed, function GoUpBishop() {
        
        chosen = 2
        SetPositionOnBoard(selector, pieces[pnum][2], pieces[pnum][3] + 1)
    })
    controller.down.onEvent(ControllerButtonEvent.Pressed, function GoDownRook() {
        
        chosen = 3
        SetPositionOnBoard(selector, pieces[pnum][2], pieces[pnum][3] - 1)
    })
    controller.left.onEvent(ControllerButtonEvent.Pressed, function GoLeftKnight() {
        
        chosen = 4
        SetPositionOnBoard(selector, pieces[pnum][2] - 1, pieces[pnum][3])
    })
    controller.right.onEvent(ControllerButtonEvent.Pressed, function GoRightQueen() {
        
        chosen = 5
        SetPositionOnBoard(selector, pieces[pnum][2] + 1, pieces[pnum][3])
    })
    controller.A.onEvent(ControllerButtonEvent.Pressed, function SelectPromotion() {
        
        if (chosen == 0) {
            return null
        }
        
        pieces[pnum][0] = chosen
        piecesSprites[pnum].setImage(CalPieceSprite(chosen, team))
        promotionBishop.destroy()
        promotionRook.destroy()
        promotionKnight.destroy()
        promotionQueen.destroy()
        promotionRing.destroy()
        selector.setImage(assets.image`selector`)
        SetPositionOnBoard(selector, pieces[pnum][2], pieces[pnum][3])
        CreateTempSprite(1000, assets.animation`promotionChosen`, pieces[pnum][2], pieces[pnum][3], 100, 0, 0, 2, true)
        SafeAnimPause(1000)
        BindAll()
        CheckForChecks()
    })
}

function UpdateColors() {
    // Change color pallette, it would look dumb otherwise.
    
    color.setColor(1, color.rgb(CalGamma(255), CalGamma(255), CalGamma(255)))
    color.setColor(2, color.rgb(CalGamma(255), 0, 0))
    color.setColor(3, color.rgb(CalGamma(80), CalGamma(80), CalGamma(80)))
    color.setColor(4, color.rgb(CalGamma(180), CalGamma(180), CalGamma(180)))
    color.setColor(5, color.rgb(CalGamma(209), CalGamma(209), CalGamma(209)))
    color.setColor(6, color.rgb(CalGamma(90), CalGamma(90), CalGamma(90)))
    color.setColor(7, color.rgb(CalGamma(50), CalGamma(50), CalGamma(50)))
    color.setColor(8, color.rgb(CalGamma(60), CalGamma(60), CalGamma(60)))
    color.setColor(10, color.rgb(CalGamma(50), CalGamma(200), CalGamma(50)))
    color.setColor(9, color.rgb(CalGamma(255), CalGamma(159), 0))
    color.setColor(11, color.rgb(CalGamma(205), CalGamma(109), 0))
    color.setColor(14, color.rgb(CalGamma(50), CalGamma(150), CalGamma(50)))
    color.setColor(15, color.rgb(CalGamma(0), CalGamma(0), CalGamma(0)))
}

//  ---------------------------------------------------------------------------------------- Selector Funcs
function SelectorGoRIGHT() {
    if (!(selectorData[0] == 8)) {
        selectorData[0] += 1
        SetPositionOnBoard(selector, selectorData[0], selectorData[1])
        if (!(selectorData[2] == null)) {
            SetPositionOnBoard(piecesSprites[selectorData[2]], selectorData[0], selectorData[1], true)
        }
        
    } else {
        
    }
    
}

function SelectorGoLEFT() {
    if (!(selectorData[0] == 1)) {
        selectorData[0] -= 1
        SetPositionOnBoard(selector, selectorData[0], selectorData[1])
        if (!(selectorData[2] == null)) {
            SetPositionOnBoard(piecesSprites[selectorData[2]], selectorData[0], selectorData[1], true)
        }
        
    } else {
        
    }
    
}

function SelectorGoUP() {
    if (!(selectorData[1] == 8)) {
        selectorData[1] += 1
        SetPositionOnBoard(selector, selectorData[0], selectorData[1])
        if (!(selectorData[2] == null)) {
            SetPositionOnBoard(piecesSprites[selectorData[2]], selectorData[0], selectorData[1], true)
        }
        
    } else {
        
    }
    
}

function SelectorGoDOWN() {
    if (!(selectorData[1] == 1)) {
        selectorData[1] -= 1
        SetPositionOnBoard(selector, selectorData[0], selectorData[1])
        if (!(selectorData[2] == null)) {
            SetPositionOnBoard(piecesSprites[selectorData[2]], selectorData[0], selectorData[1], true)
        }
        
    } else {
        
    }
    
}

function selectorPickUp() {
    let tempMemory: number;
    
    let somethingFound = false
    UnbindAll()
    for (let i = 0; i < pieces.length; i++) {
        if (pieces[i][2] == selectorData[0] && pieces[i][3] == selectorData[1]) {
            pieceFound = true
            selectorData[2] = i
            selectorData[3] = selectorData[0]
            selectorData[4] = selectorData[1]
            break
        }
        
    }
    if (pieceFound && pieces[selectorData[2]][1] == whoseTurn) {
        if (pieces[selectorData[2]][1] == whoseTurn && CalculateValidSpaces(selectorData[2])) {
            console.log("selectorPickUp-valid moves")
            animation.runImageAnimation(selector, assets.animation`selectorPickupAnim`, 30, false)
            // PickUpSoundEffect()
            controller.A.onEvent(ControllerButtonEvent.Pressed, ButtonBoundSelectorPutDown)
            controller.B.onEvent(ControllerButtonEvent.Pressed, selectorPutDownCancel)
            piecesSprites[selectorData[2]].setPosition(piecesSprites[selectorData[2]].x, piecesSprites[selectorData[2]].y)
            piecesSprites[selectorData[2]].z = 3
            tempMemory = selectorData[2]
            SafeAnimPause(180, true)
            timer.after(60, function frame1() {
                piecesSprites[tempMemory].y += 1
            })
            timer.after(90, function frame2() {
                piecesSprites[tempMemory].y -= 1
            })
            timer.after(120, function frame3() {
                piecesSprites[tempMemory].y -= 3
            })
            timer.after(150, function frame4() {
                piecesSprites[tempMemory].y -= 5
            })
            timer.after(180, function frame5() {
                piecesSprites[tempMemory].y -= 1
            })
            CalculateValidSpaces(selectorData[2], true)
            CalculateKillSpaces(selectorData[2], true)
            if (pieces[selectorData[2]][0] == 6) {
                CalculateCastleSpaces(selectorData[2], true)
            }
            
            pieceFound = false
            BindAll(true)
        } else if (CalculateKillSpaces(selectorData[2])) {
            console.log("PickUp-moves failed, kills valid")
            animation.runImageAnimation(selector, assets.animation`selectorPickupAnim`, 30, false)
            // PickUpSoundEffect()
            controller.A.onEvent(ControllerButtonEvent.Pressed, ButtonBoundSelectorPutDown)
            piecesSprites[selectorData[2]].setPosition(piecesSprites[selectorData[2]].x, piecesSprites[selectorData[2]].y - 10)
            piecesSprites[selectorData[2]].z = 3
            piecesSprites[selectorData[2]].y += 1
            CalculateValidSpaces(selectorData[2], true)
            CalculateKillSpaces(selectorData[2], true, 0, false)
            pieceFound = false
            piecesSprites[selectorData[2]].y -= 1
        } else {
            console.log("PickUp-No valid spaces")
            selectorPutDown(true)
            pieceFound = false
            selectorData[2] = null
        }
        
    } else {
        // DenySoundEffect()
        console.log("PickUp-Piece was not found")
        selectorPutDown(true)
        pieceFound = false
        selectorData[2] = null
    }
    
    // DenySoundEffect()
    BindAll(false)
}

function selectorPutDown(doNotSwitch: boolean = false, bypassCheck: boolean = false, noAnim: boolean = false) {
    let i: number;
    let teamBuffer: number;
    let promotion: boolean;
    let currentOffset: number;
    let tempMemory: number;
    
    
    let killingPlace = false
    let swapPlace = false
    // UnbindAll()
    for (i = 0; i < pieceValidSpaces.length; i++) {
        if (selectorData[0] == pieceValidSpaces[i][0] && selectorData[1] == pieceValidSpaces[i][1]) {
            placeFound = true
            break
        }
        
    }
    for (i = 0; i < pieceValidKillSpaces.length; i++) {
        if (selectorData[0] == pieceValidKillSpaces[i][0] && selectorData[1] == pieceValidKillSpaces[i][1]) {
            killingPlace = true
            placeFound = true
            // KillSoundEffect()
            // tempX, tempY = SetPositionOnBoard(None, selectorData[0],selectorData[1])
            // CreateTempSprite(300, assets.animation("""returnToDust"""), tempX, tempY, 60)
            break
        }
        
    }
    for (i = 0; i < pieceValidCastleSpaces.length; i++) {
        if (selectorData[0] == pieceValidCastleSpaces[i][0] && selectorData[1] == pieceValidCastleSpaces[i][1]) {
            swapPlace = true
            placeFound = true
            break
        }
        
    }
    if (placeFound || bypassCheck) {
        teamBuffer = whoseTurn
        if (!doNotSwitch) {
            SwitchingSides()
        }
        
        promotion = false
        // PutDownSoundEffect()
        controller.A.onEvent(ControllerButtonEvent.Pressed, selectorPickUp)
        controller.B.onEvent(ControllerButtonEvent.Pressed, null)
        piecesSprites[selectorData[2]].z = 0
        if (pawnFirstMove && !bypassCheck) {
            pieces[selectorData[2]][4] = 0
        }
        
        if (killingPlace) {
            for (i = 0; i < pieces.length; i++) {
                if (pieces[i][2] == selectorData[0] && pieces[i][3] == selectorData[1]) {
                    currentOffset = 0
                    if (whoseTurn == 0) {
                        currentOffset = deadPiecesOffsetWhite
                        deadPiecesOffsetWhite += 2
                    } else if (whoseTurn == 1) {
                        currentOffset = deadPiecesOffsetBlack
                        deadPiecesOffsetBlack += 2
                    }
                    
                    pieces[i][2] = 10 + whoseTurn * 2
                    pieces[i][3] = 4
                    SetPositionOnBoard(piecesSprites[i], pieces[i][2], pieces[i][3], false, 0, currentOffset)
                    break
                }
                
            }
        }
        
        if (swapPlace) {
            for (i = 0; i < pieces.length; i++) {
                if (pieces[i][2] == selectorData[0] && pieces[i][3] == selectorData[1]) {
                    SetPositionOnBoard(piecesSprites[i], pieces[i][2], pieces[i][3])
                    break
                }
                
            }
        }
        
        pieces[selectorData[2]][2] = selectorData[0]
        pieces[selectorData[2]][3] = selectorData[1]
        if (pieces[selectorData[2]][0] == 1) {
            if (pieces[selectorData[2]][1] == 0 && pieces[selectorData[2]][3] == 8) {
                promotion = true
            }
            
            if (pieces[selectorData[2]][1] == 1 && pieces[selectorData[2]][3] == 1) {
                promotion = true
            }
            
        }
        
        if (pieces[selectorData[2]][4] == 1 && !bypassCheck) {
            pieces[selectorData[2]][4] = 0
        }
        
        SetPositionOnBoard(piecesSprites[selectorData[2]], pieces[selectorData[2]][2], pieces[selectorData[2]][3])
        for (i = 0; i < pieceValidSprites.length; i++) {
            pieceValidSprites[i].destroy()
        }
        for (i = 0; i < pieceValidKillSprites.length; i++) {
            if (pieceValidKillSpaces[i][0] == pieces[selectorData[2]][2] && pieceValidKillSpaces[i][1] == pieces[selectorData[2]][3]) {
                CreateTempSprite(1000, assets.animation`killSpaceKill`, pieceValidKillSprites[i].x, pieceValidKillSprites[i].y, 80, 0, 0, 5)
            } else {
                CreateTempSprite(300, assets.animation`killSpaceDisappear`, pieceValidKillSprites[i].x, pieceValidKillSprites[i].y, 100, 0, 0, 5)
            }
            
            pieceValidKillSprites[i].destroy()
        }
        for (i = 0; i < pieceValidCastleSprites.length; i++) {
            pieceValidCastleSprites[i].destroy()
        }
        if (!noAnim && !promotion) {
            animation.runImageAnimation(selector, assets.animation`selectorPutdownAnim`, 50, false)
            tempMemory = selectorData[2]
            piecesSprites[tempMemory].y -= 9
            SafeAnimPause(250)
            timer.after(50, function frame1() {
                piecesSprites[tempMemory].y += 5
            })
            timer.after(100, function frame2() {
                piecesSprites[tempMemory].y += 4
            })
            timer.after(200, function frame3() {
                piecesSprites[tempMemory].y += 1
            })
            timer.after(250, function frame4() {
                piecesSprites[tempMemory].y -= 1
            })
        } else if (!promotion) {
            // piecesSprites[selectorData[2]].y -= 1
            selector.setImage(assets.image`selector`)
        } else if (promotion) {
            PromotionSequence(selectorData[2], teamBuffer)
        }
        
        selectorData[2] = null
        pieceValidSprites = []
        pieceValidSpaces = []
        pieceValidKillSpaces = []
        pieceValidKillSprites = []
        pieceValidCastleSpaces = []
        pieceValidCastleSprites = []
        placeFound = false
        if (!bypassCheck) {
            CheckForChecks()
        }
        
    }
    
}

// BindAll(False)
function selectorPutDownCancel() {
    
    selectorData[0] = selectorData[3]
    selectorData[1] = selectorData[4]
    SetPositionOnBoard(piecesSprites[selectorData[2]], selectorData[0], selectorData[1], true)
    SetPositionOnBoard(selector, selectorData[0], selectorData[1])
    selectorPutDown(true, true, true)
    pieceFound = false
    selectorData[2] = null
}

// CancelSoundEffect()
//  ---------------------------------------------------------------------------------------- Misc/QOL Funcs
function SwitchingSides() {
    // Switches the sides, self-explanatory.
    
    let bufferTurn = whoseTurn
    console.log("----------------------SIDES-SWITCHED")
    if (whoseTurn == 0) {
        animation.runImageAnimation(turnPawn, assets.animation`whiteTurnBlack`, 80, false)
        turnPawn.setImage(assets.image`
            blackPawn
        `)
        whoseTurnInvert = 0
        whoseTurn = 1
    } else {
        animation.runImageAnimation(turnPawn, assets.animation`blackTurnWhite`, 50, false)
        turnPawn.setImage(assets.image`
            whitePawn
        `)
        whoseTurnInvert = 1
        whoseTurn = 0
    }
    
}

function SafePause(time: number, mode: boolean = false) {
    // Stops the code for a second whilst unbinding the buttons to stop exploits.
    UnbindAll()
    pause(time)
    BindAll(mode)
}

function SafeAnimPause(time: number, mode: boolean = false) {
    // Unbinds all buttons for set amount of time, to let animations play. WHILE letting the code run.
    timer.background(function wait() {
        UnbindAll()
        pause(time)
        BindAll(mode)
    })
}

function ButtonBoundSelectorPutDown() {
    // A function with no inputs to be bound to the button.
    selectorPutDown()
}

function CreateTempSprite(delay: number, spriteAnimation: any, x: number, y: number, speed: number, ox: number = 0, oy: number = 0, z: number = 100, chessPositions: boolean = false) {
    // Creates a temporary sprite to play an animation
    
    tempSprites.push(sprites.create(assets.image`emptySpace`))
    tempSprites[tempSprites.length - 1].x = x
    tempSprites[tempSprites.length - 1].y = y
    if (chessPositions) {
        SetPositionOnBoard(tempSprites[tempSprites.length - 1], x, y)
    }
    
    tempSprites[tempSprites.length - 1].x += ox
    tempSprites[tempSprites.length - 1].y += oy
    tempSprites[tempSprites.length - 1].z = z
    tempSpriteNum += 1
    animation.runImageAnimation(tempSprites[tempSprites.length - 1], spriteAnimation, speed, false)
    timer.debounce("" + tempSpriteNum, delay, function on_debounce() {
        tempSprites.shift().destroy()
    })
}

function IsNumOutOfBounds(numberGiven: number): boolean {
    // A compact version of checking if the coordinates are out of bounds
    if (numberGiven > 8 || numberGiven < 1) {
        return true
    } else {
        return false
    }
    
}

function UnbindAll() {
    // Unbinds all buttons.
    controller.A.onEvent(ControllerButtonEvent.Pressed, null)
    controller.up.onEvent(ControllerButtonEvent.Pressed, null)
    controller.down.onEvent(ControllerButtonEvent.Pressed, null)
    controller.left.onEvent(ControllerButtonEvent.Pressed, null)
    controller.right.onEvent(ControllerButtonEvent.Pressed, null)
}

function BindAll(mode: boolean = false) {
    // Binds all buttons back.
    if (mode) {
        controller.A.onEvent(ControllerButtonEvent.Pressed, ButtonBoundSelectorPutDown)
        controller.B.onEvent(ControllerButtonEvent.Pressed, selectorPutDownCancel)
    } else {
        controller.A.onEvent(ControllerButtonEvent.Pressed, selectorPickUp)
    }
    
    controller.up.onEvent(ControllerButtonEvent.Pressed, SelectorGoUP)
    controller.down.onEvent(ControllerButtonEvent.Pressed, SelectorGoDOWN)
    controller.left.onEvent(ControllerButtonEvent.Pressed, SelectorGoLEFT)
    controller.right.onEvent(ControllerButtonEvent.Pressed, SelectorGoRIGHT)
}

function CalGamma(val: number): number {
    // Caps out brightness values to stop looping and adds gamma.
    
    val += gamma
    if (val > 255) {
        return 255
    } else if (val < 0) {
        return 0
    } else {
        return val
    }
    
}

function CalPieceSprite(pieceClass: number, team: number): Image {
    // Get the sprite according to class type and team
    
    let offset = -1
    if (team == 1) {
        offset = 5
    }
    
    let spriteIndex = pieceClass + offset
    return pieceAssetReference[spriteIndex]
}

//  ---------------------------------------------------------------------------------------- Starting Code
controller.menu.onEvent(ControllerButtonEvent.Pressed, null)
Setup()
