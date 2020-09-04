import pygame, random, sys ,os,time
from pynput.keyboard import Key, Controller
from pygame.locals import *
from PIL import ImageGrab
import cv2
import numpy as np
from matplotlib import pyplot as plt

X=0
Y=30
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (X,Y)
keyboard = Controller()

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 8
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 20
PLAYERMOVERATE = 8
count=3
global moveLeft 
global moveRight

STR=('image/car1.png','image/car3.png')
checkrangx = [149,172,195,218,241,264,287,310,333,356,379,402,425,448,471,494]#16
checkrangy = [50,100,150,200,250,300,350,400,450,500,550,600]#12
sbmt = np.zeros(shape=(12,16),dtype=np.int)


def screendetector():
    global moveLeft
    global moveRight
    img = ImageGrab.grab(bbox=(0,30,600,630)) #x, y, w, h
    sbmt = np.zeros(shape=(12,16),dtype=np.int)
    img_np = np.array(img)
    for x in STR:
        assign=-1

        if(x=='image/car1.png'):
            assign=1
    	
        img_rgb = img_np
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread(x,0)
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 1)
            xxpoint=-1
            yypoint=-1
            xpoint=0
            ypoint=0
            for xindex in range(len(checkrangx)):
                if(pt[0]<checkrangx[xindex]):
                    xpoint=xindex;
                    if(xindex<15 and pt[0]+23<checkrangx[xindex+1]):
                        xxpoint=xindex+1;
                    break;
            for xindex in range(len(checkrangy)):
                if(pt[1]<checkrangy[xindex]):
                    ypoint=xindex;
                    if(xindex<11 and pt[1]+50<checkrangy[xindex+1]):
                        yypoint=xindex+1;
                    break;
            sbmt[ypoint][xpoint]=assign;
            if(xxpoint!=-1 and yypoint!=-1):
                    sbmt[yypoint][xxpoint]=assign;
                    sbmt[ypoint][xxpoint]=assign;
                    sbmt[yypoint][xpoint]=assign;
    xx=list()
    filepath = 'syn0.txt'  
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            temp = line.strip().split(" ")
            result = list(map(float, temp))
            #xx = list(xx + result)
            xx.append(result)
            line = fp.readline()

    yy=list()
    filepath = 'syn1.txt'  
    with open(filepath) as fp:  
        line = fp.readline()
        while line:
            temp = line.strip().split(" ")
            result = list(map(float, temp))
            #xx = list(xx + result)
            yy.append(result)
            line = fp.readline()
    
    syn0 = np.asarray(xx)
    syn1 = np.asarray(yy)
    #print(sbmt.shape)
    #print(syn0.shape)
    #print(syn1.shape)
    l0 = sbmt.flatten() 
    l1 = nonlin(np.dot(l0,syn0))
    l2 = nonlin(np.dot(l1,syn1))

#keyboard.press('a')
#keyboard.release('a')
#print("a is pressed")
    
    if(int(round(l2[0]))==1):
        moveRight = False
        moveLeft = True
        pygame.display.set_caption('left')
    if(int(round(l2[0]))==0):
        moveRight = True
        moveLeft = False
        pygame.display.set_caption('right')
    ##left=1   right=0
    
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)

    return 1/(1+np.exp(-x))

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: #escape quits
                    terminate()
                return

def playerHasHitBaddie(playerRect, baddies):
    for b in baddies:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('car race')
pygame.mouse.set_visible(False)

# fonts
font = pygame.font.SysFont(None, 30)

# sounds
gameOverSound = pygame.mixer.Sound('music/crash.wav')
pygame.mixer.music.load('music/car.wav')
laugh = pygame.mixer.Sound('music/laugh.wav')


# images
playerImage = pygame.image.load('image/car1.png')
car3 = pygame.image.load('image/car3.png')
car4 = pygame.image.load('image/car4.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('image/car2.png')
sample = [car3]#[car3,car4,baddieImage] #edit this for variety of baddie cars
wallLeft = pygame.image.load('image/left.png')
wallRight = pygame.image.load('image/right.png')


# "Start" screen
drawText('Press any key to start the game.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3))
drawText('And Enjoy', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3)+30)
pygame.display.update()
waitForPlayerToPressKey()
zero=0
if not os.path.exists("data/save.dat"):
    f=open("data/save.dat",'w')
    f.write(str(zero))
    f.close()   
v=open("data/save.dat",'r')
topScore = int(v.readline())
v.close()

while (count>0):
    # start of the game
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)
    

    while True: # the game loop
        score += 1 # increase score
        ##changed   
        screendetector()
        for event in pygame.event.get():
            
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True
                
            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()
            

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            

        # Add new baddies at the top of the screen
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize =30 
            newBaddie = {'rect': pygame.Rect(random.randint(140, 485), 0 - baddieSize, 23, 50),
                        'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                        'surface':pygame.transform.scale(random.choice(sample), (23, 50)),##23 width 47
                        }
            baddies.append(newBaddie)
            sideLeft= {'rect': pygame.Rect(0,0,126,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallLeft, (126, 599)),
                       }
            baddies.append(sideLeft)
            sideRight= {'rect': pygame.Rect(494,0,310,600),
                       'speed': random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                       'surface':pygame.transform.scale(wallRight, (311, 599)),
                       }
            baddies.append(sideRight)
            
            

        # Move the player around.
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * PLAYERMOVERATE)
        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0, PLAYERMOVERATE)
        
        for b in baddies:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, b['speed'])
            elif reverseCheat:
                b['rect'].move_ip(0, -5)
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         
        for b in baddies[:]:
            if b['rect'].top > WINDOWHEIGHT:
                baddies.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 128, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface,128, 20)
        drawText('Rest Life: %s' % (count), font, windowSurface,128, 40)
        
        windowSurface.blit(playerImage, playerRect)

        
        for b in baddies:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the car have hit the player.
        if playerHasHitBaddie(playerRect, baddies):
            if score > topScore:
                g=open("data/save.dat",'w')
                g.write(str(score))
                g.close()
                topScore = score
            break

        mainClock.tick( )

    # "Game Over" screen.
    pygame.mixer.music.stop()
    count=count-1
    gameOverSound.play()
    time.sleep(1)
    if (count==0):
     laugh.play()
     drawText('Game over', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
     drawText('Press any key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 30)
     pygame.display.update()
     time.sleep(2)
     waitForPlayerToPressKey()
     count=3
     gameOverSound.stop()