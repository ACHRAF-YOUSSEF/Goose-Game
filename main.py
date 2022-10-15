import pygame
import engine
import os
from random import randint

WIDTH, HEIGHT = 800, 800
DIMENSION_Y = 6
DIMENSION_X = 8
SQ_SIZE_Y = HEIGHT // DIMENSION_Y
SQ_SIZE_X = WIDTH // DIMENSION_X
MAX_FPS = 10

# colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

play = False
start = False
options = False
moveMade = False
over_screen = False

colors = {"white":WHITE, "red":RED, "green":GREEN, "grey":GREY, "blue":BLUE, "black":BLACK, "1":(120, 100, 100), "2":(150, 80, 50), "3":(200, 50, 50), "4":(20, 120, 255)}
IMAGES = {}

musicList = [f"./music/{song}" for song in os.listdir("./music")]
music_index = 0

gs = engine.GameState()

# functions
def getSongName(song):
    pos = song.find("/")
    while (pos != -1) :
        song = song[pos+1::]
        pos = song.find("/")
        
    return song

def loadImages():
    pieces = ["red", "green"]

    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load(f"./images/{piece}.png"), (SQ_SIZE_X - 50, SQ_SIZE_Y - 50))

def draw_text(screen, txt, x, y, police, color):
    texte_font = pygame.font.Font(None,police)
    texte = texte_font.render(txt,True,color)
    txt_rect = texte.get_rect()
    txt_rect.center =  (x,y)
    screen.blit(texte,txt_rect)

def menu(screen, clock):
    screen.fill(BLACK)
    pygame.display.set_caption("main menu")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    startButton.draw(screen, "start")
    optionsButton.draw(screen, "options")
    quitButton.draw(screen, "exit")
    
    clock.tick(MAX_FPS)
    pygame.display.flip()

def optionsMenu(screen, clock):
    screen.fill(BLACK)
    pygame.display.set_caption("options menu")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    txt = f"{getSongName(musicList[music_index])}"
    
    draw_text(screen, txt, 400, 315, 50, colors["white"])
    musicSelector.draw(screen, "music")

    optionsBackButton.draw(screen, "backFromOptions")
    
    clock.tick(MAX_FPS)
    pygame.display.flip()

def playMenu(screen, gs, clock):
    screen.fill(BLACK)
    pygame.display.set_caption("play menu")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    playButton.draw(screen, "play")
    
    txt = "red" if gs.player_1 else "green"
    texte = "play as "+txt+" color"

    if len(texte) == 17:
        x, y = 300, 370
    else:
        x, y = 280, 370
    
    draw_text(screen, texte, x, y, 50, colors[txt])
    playerSelector.draw(screen, "player")
    
    backButton.draw(screen, "back")
    
    clock.tick(MAX_FPS)
    pygame.display.flip()
    
def getRightVariables(gs):
    if gs.player_1:
        gs.wasInJail = gs.wasInJail_1
        gs.inJail = gs.inJail_1
        gs.hasWaited = gs.hasWaited_1
        gs.startIndex = gs.startIndex_1
        gs.index = gs.index_1
        gs.moveLog = gs.moveLog_1
    
    else:
        gs.wasInJail = gs.wasInJail_2
        gs.inJail = gs.inJail_2
        gs.hasWaited = gs.hasWaited_2
        gs.startIndex = gs.startIndex_2
        gs.index = gs.index_2
        gs.moveLog = gs.moveLog_2
        
def ReturnRightVariables(gs):
    if gs.player_1:
        gs.wasInJail_1 = gs.wasInJail
        gs.inJail_1 = gs.inJail
        gs.hasWaited_1 = gs.hasWaited
        gs.startIndex_1 = gs.startIndex
        gs.index_1 = gs.index
        gs.moveLog_1 = gs.moveLog
    
    else:
        gs.wasInJail_2 = gs.wasInJail
        gs.inJail_2 = gs.inJail
        gs.hasWaited_2 = gs.hasWaited
        gs.startIndex_2 = gs.startIndex
        gs.index_2 = gs.index
        gs.moveLog_2 = gs.moveLog

def checkIfIsInList(checkList_1, checkList_2):
    for item in checkList_2:
        for _ in checkList_1:
            if item == _:
                return True
            
    return False

def updateCheckList(gs):
    return [gs.boardDescription[gs.coords[gs.l_1[gs.startIndex]][0]][gs.coords[gs.l_1[gs.startIndex]][1]], gs.boardDescription[gs.coords[gs.l_1[gs.index]][0]][gs.coords[gs.l_1[gs.index]][1]]]
    
def game(screen, gs, clock):
    global moveMade
    
    pygame.display.set_caption("goose game")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            
        color = "red" if gs.player_1 else "green"
        i = 0 if gs.player_1 else 1 
        
        getRightVariables(gs)
        
        if gs.count != 0:
            gs.startIndex = gs.index
            gs.index += gs.count
            
            gs.throwLog.append(gs.count)
            
            if gs.index >= len(gs.l_1):
                gs.index -= gs.count
                gs.throwLog.pop()
                gs.moveLog.pop()
                
            else:   
                print(gs.count)
                
                if gs.inJail_1 and gs.inJail_2:
                    gs.inJail_1 = False
                    gs.inJail_2 = False
                    
                if gs.player_1:
                    gs.inJail = gs.inJail_1
                else:
                    gs.inJail = gs.inJail_2
            
                if len(gs.moveLog) != 0:
                    startrow = gs.coords[gs.moveLog[gs.startIndex]][0]
                    startcol = gs.coords[gs.moveLog[gs.startIndex]][1]
                    endrow = startrow
                    endcol = startcol
                else:
                    startrow = gs.coords["start"][0]
                    startcol = gs.coords["start"][1]
                    endrow = startrow
                    endcol = startcol
                    
                checkList_1 = ["jail", "rewind same moves", "start over!", "move forward by 1", "move back by 1", "replay same moves", "move forward by 4", "move back by 6"]
                
                txt = "red" if gs.player_1 else "green"
                
                if gs.inJail:
                    gs.hasWaited += 1
                    gs.index -= gs.count
                
                if gs.hasWaited >= 2:
                    gs.inJail = False
                    gs.wasInJail = True
                    gs.index += gs.count
                    gs.hasWaited = 0
                    
                if not gs.inJail:
                    print("moving...!")
                    
                    for k in range(gs.startIndex, gs.index + 1):
                        endrow = gs.l_2[k][0]
                        endcol = gs.l_2[k][1]
                                        
                        move = engine.Move(startrow, startcol, endrow, endcol, i, color) 

                        gs.makeMove(move)
                        drawGameState(screen, gs)
                        clock.tick(MAX_FPS)
                        pygame.display.flip()
                                        
                        startrow = endrow
                        startcol = endcol
                                
                        gs.moveLog.append(gs.l_1[k])
                        
                        jump_sound.play()
                    
                    gs.wasInJail = False
                        
                checkList_2 = updateCheckList(gs)

                while checkList_2 != ["", ""] and (not gs.inJail and not gs.wasInJail):
                    for checkEvent in checkList_1:
                        if checkEvent in checkList_2:
                            if "jail" == checkEvent:
                                print(f" {txt} in jail!")
                                
                                gs.inJail = True
                                
                                checkList_2 = updateCheckList(gs)
                                
                                break
                                            
                            if checkEvent in checkList_1[1::]:
                                checkEvent_new = checkEvent.split(" ")
                                if checkEvent == "start over!":
                                    gs.count = gs.index
                                    direction = -1
                                    over_sound.play()
                                
                                elif checkEvent_new[1] == "forward":
                                    txt = "forward"
                                    gs.count = int(checkEvent.split(" ")[-1])
                                    direction = 1
                                
                                elif checkEvent_new[1] == "back":
                                    txt = "back"
                                    gs.count = int(checkEvent.split(" ")[-1])
                                    direction = -1
                                
                                elif checkEvent_new[0] == "replay":
                                    txt = "replay"
                                    direction = 1
                                
                                elif checkEvent_new[0] == "rewind":
                                    txt = "rewind"
                                    direction = -1
                                    
                                j = gs.count
                                k = gs.index
                                
                                while (j >= 0):
                                    endrow = gs.l_2[k][0]
                                    endcol = gs.l_2[k][1]
                                    
                                    move = engine.Move(startrow, startcol, endrow, endcol, i, color) 

                                    gs.makeMove(move)
                                    drawGameState(screen, gs)
                                    clock.tick(MAX_FPS)
                                    pygame.display.flip()
                                    
                                    gs.moveLog.append(gs.l_1[k])
                                    
                                    startrow = endrow
                                    startcol = endcol
                                    
                                    k += direction
                                    j -= 1
                                    
                                    jump_sound.play()
                                    
                                gs.index += gs.count * direction
                                gs.startIndex = gs.index
                                
                                checkList_2 = updateCheckList(gs)
                        
                        drawGameState(screen, gs)
                        ReturnRightVariables(gs)
                        clock.tick(MAX_FPS)
                        pygame.display.flip()
                
                ReturnRightVariables(gs)
                
            gs.player_1 = not gs.player_1
        
        gs.count = 0
        
        moveMade = True
        
    if moveMade:
        moveMade = False
        
    drawGameState(screen, gs)
    throwDiceButton.draw(screen, "throw")
    
    clock.tick(MAX_FPS)
    pygame.display.flip()

def gameOverScreen(screen, gs, clock):
    global over_screen
    
    screen.fill(BLACK)
    pygame.display.set_caption("game over screen")
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            
    i = 0 if gs.board[2][2][0] != "-" else 1 if gs.board[2][2][1] != "-" else -1 
            
    if i != -1:
        draw_text(screen, gs.board[2][2][i]+" wins!", 400, 350, 50, colors[gs.board[2][2][i]])
        
    if not over_screen:
        victoy_sound.play()
        over_screen = True
    
    clock.tick(MAX_FPS)
    pygame.display.flip()

def main():
    global play, start, options, gs

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    screen.fill(WHITE)

    loadImages()

    while True:
        if start:
            if play:
                if not gs.end_game():
                    game(screen, gs, clock)
                else:
                    gameOverScreen(screen, gs, clock)
            else:
                playMenu(screen, gs, clock)
        elif options:
            optionsMenu(screen, clock)
        else:
            menu(screen, clock)

def drawGameState(screen, gs):
    screen.fill(WHITE)
    drawBoardColors(screen, gs.boardColors)
    drawBoard(screen)
    drawTxt(screen, gs.boardTxt)
    boardDescription(screen, gs.boardDescription)
    drawPiece(screen, gs.board)
    
def drawBoard(screen):
    for row in range(DIMENSION_Y):
        for col in range(DIMENSION_X):
            color = colors["grey"]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE_X, row * SQ_SIZE_Y, SQ_SIZE_X, SQ_SIZE_Y), 1)
            
def drawBoardColors(screen, board):
    for row in range(DIMENSION_Y):
        for col in range(DIMENSION_X):
            color = colors[board[row][col]]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE_X, row * SQ_SIZE_Y, SQ_SIZE_X, SQ_SIZE_Y))

def drawTxt(screen, board):
    for row in range(DIMENSION_Y):
        for col in range(DIMENSION_X):  
            draw_text(screen, board[row][col], col * SQ_SIZE_X + 50, row * SQ_SIZE_Y + 20, 40, WHITE)  
            
def boardDescription(screen, board):
    for row in range(DIMENSION_Y):
        for col in range(DIMENSION_X):  
            txt = board[row][col]
            
            j = 0
            words = txt.split()
            
            for word in words:
                j += 22
                draw_text(screen, word, col * SQ_SIZE_X + 50, row * SQ_SIZE_Y + j + 26, 35, WHITE) 

def drawPiece(screen, board):
    for row in range(DIMENSION_Y):
        for col in range(DIMENSION_X): 
            piece = board[row][col]
            
            if piece[0] == "red":
                screen.blit(IMAGES[piece[0]], pygame.Rect(col * SQ_SIZE_X + 40, row * SQ_SIZE_Y + 20, SQ_SIZE_X, SQ_SIZE_Y))
            
            if piece[1] == "green":
                screen.blit(IMAGES[piece[1]], pygame.Rect(col * SQ_SIZE_X + 5, row * SQ_SIZE_Y + 20, SQ_SIZE_X, SQ_SIZE_Y))

def do_function(x):
    global play, start, gs, options, moveMade, musicList, music_index

    if x == "play":
        play = True
        pygame.mixer.music.load(musicList[music_index])
        pygame.mixer.music.set_volume(.5)
        pygame.mixer.music.play(-1)
        
    if x == "start":
        start = True
        
    if x == "exit":
        quit()
        
    if x == "options":
        options = True
    
    if x == "backFromOptions":
        options = False
        
    if x == "back":
        start = False
    
    if x == "player":
        gs.player_1 = not gs.player_1  
        
    if x == "throw":
        number = randint(1, 6)
        
        gs.count = number
        
    if x == "music":
        music_index += 1
        
        if music_index >= len(musicList):
            music_index = 0
    
    
# classes
class Button:
    def __init__(gs, text, width, height, pos, elevation):
        # Core attributes
        gs.pressed = False
        gs.elevation = elevation
        gs.dynamic_elecation = elevation
        gs.original_y_pos = pos[1]

        # top rectangle
        gs.top_rect = pygame.Rect(pos, (width, height))
        gs.top_color = '#475F77'

        # bottom rectangle
        gs.bottom_rect = pygame.Rect(pos, (width, height))
        gs.bottom_color = '#354B5E'

        # text
        gs.text_surf = pygame.font.Font(None, 30).render(text, True, BLACK)
        gs.text_rect = gs.text_surf.get_rect(center=gs.top_rect.center)

    def draw(gs, screen, x):
        # elevation logic
        gs.top_rect.y = gs.original_y_pos - gs.dynamic_elecation
        gs.text_rect.center = gs.top_rect.center

        gs.bottom_rect.midtop = gs.top_rect.midtop
        gs.bottom_rect.height = gs.top_rect.height + gs.dynamic_elecation

        pygame.draw.rect(screen, gs.top_color, gs.top_rect, border_radius=12)
        screen.blit(gs.text_surf, gs.text_rect)
        gs.check_click(x)

    def check_click(gs,x):
        mouse_pos = pygame.mouse.get_pos()
        if gs.top_rect.collidepoint(mouse_pos):
            gs.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                gs.dynamic_elecation = 0
                gs.pressed = True
            else:
                gs.dynamic_elecation = gs.elevation
                if gs.pressed:
                    do_function(x)
                    gs.pressed = False
        else:
            gs.dynamic_elecation = gs.elevation
            gs.top_color = '#475F77'

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    
    icon = pygame.image.load("./icon/goose.png")
    pygame.display.set_icon(icon)
    
    # throw dice button
    throwDiceButton = Button("throw", 100, 40, (400, 760), 5)
    
    # play menu buttons
    playButton = Button("play", 200, 40, (300, 300), 5)
    playerSelector = Button("change", 100, 40, (450, 355), 5)
    backButton = Button("back", 200, 40, (300, 400), 5)
    
    # main menu buttons
    startButton = Button("start", 200, 40, (300, 300), 5)
    optionsButton = Button("options", 200, 40, (300, 350), 5)
    quitButton = Button("exit", 200, 40, (300, 400), 5)
    
    # options menu buttons
    over_sound = pygame.mixer.Sound("sfx/over.wav")
    victoy_sound = pygame.mixer.Sound("sfx/victory.wav")
    jump_sound = pygame.mixer.Sound("sfx/jump.wav")
    
    musicSelector = Button("change", 100, 40, (350, 350), 5)
    optionsBackButton = Button("back", 200, 40, (300, 400), 5)
    
    main()
