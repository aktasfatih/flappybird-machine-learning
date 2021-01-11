import pygame
from pygame.locals import *
import random
import math
import neuralNetwork

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Definition of a Block class
class Block:
    # 640 is the height of the upper side
    gapDistance = 200
    def __init__(self, upper, downer):
        """
        The blocks have the following properties:
            xValue : The x value of the obstacle
            yValue : The y value of the obstacle
            upperPic : Top part of the obstacle
            downerPic : Bottom part of the obstacle

        The (x,y) coordinates points to the top left corner of the upper side. So, it starts as negative.
        """
        self.xValue = 1300
        # Min -560 Max -260
        self.yValue = -560 + random.randint(0, 300)
        self.upperPic = upper
        self.downerPic =  downer


    # Drawing funcion for pyGame
    def draw(self, screen):
        screen.blit(self.upperPic, [self.xValue, self.yValue])
        screen.blit(self.downerPic, [self.xValue, self.yValue + 640 + Block.gapDistance])

        # Drawing Rectangles
        # pygame.draw.rect(screen, BLACK, (self.xValue, self.yValue, 104, 640), 2)
        # pygame.draw.rect(screen, BLACK, (self.xValue, self.yValue + 640 + Block.gapDistance, 104, 640), 2)


    # Checking if the bird is touching the obstacle
    def check(self, bird):
        if bird.colliderect((self.xValue, self.yValue, 104, 640)) or bird.colliderect((self.xValue, self.yValue + 640 + Block.gapDistance, 104, 640)):
            return True
        return False

def printIns(screen):
    """
    Printing the instructions on the screen if the game hasn't started yet
    """
    menuFont = pygame.font.SysFont('Arial', 30, True, False)
    screen.blit(menuFont.render("Press SPACE to begin (Also to jump)", True, WHITE), [300, 600])
    menuFont = pygame.font.SysFont('Arial', 15, True, False)
    screen.blit(menuFont.render("Flappy Birdy By Fatih AKTAS", True, WHITE), [450, 640])

def printScore(screen, score):
    """
    This function prints the current score while playing.
    """
    menuFont = pygame.font.SysFont('Arial', 30, True, False)
    screen.blit(menuFont.render("Score: "+ str(score), True, WHITE), [880, 10])

# The main game function
def Flappy_Bird_Game():
    # Global Game Variables
    scoreTime = 0
    gameStarted = False
    score = 0
    jumpSpeed = -10
    fallingConst = 0.4

    # How fast does the user get points
    scoreRate = 20

    # The x position of the background
    speedOfBg = 3
    xOfBg = 0

    # Position of our first bird
    gameOver = False
    xOfBird = 130
    yOfBird = 400
    vertSpeed = 0

    # Position of the blue bird
    gameOver2 = False
    xOfBird2 = 250
    yOfBird2 = 400
    vertSpeed2 = 0

    # The distance between the blocks
    difference = 400

    # True: Logs everything for the machine learning algoritm
    logger = False
    logFile = open("trainingData.txt", "a")

    # Obstacles list
    blockList = []
    def initBlocks():
        # Setting the x values of the blocks
        for i in range(len(blockList)):
            blockList[i].xValue = 1300 + difference * i

    # There will be 5 obstacles in total
    blockSpeed = 5

    # Our window seetings
    size = [1024, 718]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Flappy Bird")

    # Starting the pygame module
    pygame.init()

    # Loading assets and convering them for faster results
    bgPic = pygame.image.load("bg.png").convert()
    birdPic = pygame.image.load("birdy.png").convert_alpha()
    birdBluePic = pygame.image.load("birdy_blue.png").convert_alpha()
    upperPic = pygame.image.load("upper.png").convert_alpha()
    downerPic = pygame.image.load("downer.png").convert_alpha()
    gameOverPic = pygame.image.load("gameOver.png").convert_alpha()

    # Scaling up the images loaded
    birdPic = pygame.transform.scale2x(birdPic)
    birdBluePic = pygame.transform.scale2x(birdBluePic)
    upperPic =  pygame.transform.scale2x(upperPic)
    downerPic =  pygame.transform.scale2x(downerPic)
    gameOverPic = pygame.transform.scale2x(gameOverPic)
    orjBird = birdPic
    orjBirdBlue = birdBluePic

    # Appending blocks to blockList to access them easily
    blockList.append(Block(upperPic, downerPic))
    blockList.append(Block(upperPic, downerPic))
    blockList.append(Block(upperPic, downerPic))
    blockList.append(Block(upperPic, downerPic))

    initBlocks()
    # Is the game finished
    done = False

    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT + 1, 1500)

    # initialize the neural network and load a pre-trained network from a file
    nn = neuralNetwork.NeuralNetwork("trainingData.txt", [4, 3, 1])
    nn.loadNetwork("network.txt")

    # Main game loop
    while not done:
        isButtonPressed = False
        # Checking the events in pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Checking for keyboard inputs
            if event.type == pygame.KEYDOWN:
                # Press 'q' for quiting the game.
                if event.key == pygame.K_q:
                    pygame.quit()
                # Press 'Space' for jumping in the game.
                # IF the game hasn't started, it will start the game
                if event.key == pygame.K_SPACE:
                    isButtonPressed = True
                    if gameStarted == False and not gameOver:
                        # Starting the game

                        gameStarted = True
                        vertSpeed = jumpSpeed
                    elif gameStarted and gameOver == False:
                        # If the game has already started, just jump.
                        vertSpeed = jumpSpeed
                else:
                    isButtonPressed = False
                # Press x for the second player
                if event.key == pygame.K_x:
                    if gameStarted == False and not gameOver:
                        # Starting the game
                        gameStarted = True
                        vertSpeed2 = jumpSpeed
                    elif gameStarted and not gameOver2:
                        # If the game has already started, just jump.
                        vertSpeed2 = jumpSpeed
        # Logging variables for machine learning
        # Finding the distance of the next obstacle
        nextBlock = None
        nextObDistance = float('inf')
        for block in blockList:
            if block.xValue + 104 > xOfBird:
                if block.xValue + 104 < nextObDistance:
                    nextObDistance = block.xValue + 104
                    nextBlock = block

        if logger:
            if isButtonPressed:
                logFile.write("{} {} {} {} {}\n".format(yOfBird, vertSpeed, nextObDistance, nextBlock.yValue, "1"))
            else:
                logFile.write("{} {} {} {} {}\n".format(yOfBird, vertSpeed, nextObDistance, nextBlock.yValue, "0"))
            # print("{} {} {} {} {}\n".format(yOfBird, vertSpeed, nextObDistance, block.yValue, isButtonPressed))

        # ask the neural network if the bird should jump based on the bird's height and speed, and the next obstacle's distance and height
        if gameStarted and not gameOver and round(nn.singleForwardPropogation([yOfBird, vertSpeed, nextObDistance, 770 + nextBlock.yValue, 1])[0]) == 1:
            vertSpeed = jumpSpeed

        # Printing the background images
        screen.blit(bgPic, [xOfBg,0])
        screen.blit(bgPic, [xOfBg+401,0])
        screen.blit(bgPic, [xOfBg+802,0])
        screen.blit(bgPic, [xOfBg+1203,0])

        # Moving the background image
        xOfBg -= speedOfBg
        #  Checking if the background is out of screen
        if(xOfBg < -401):
            # We move the background back to the right
            xOfBg = 0

        # Rotating the bird according to its velocity
        birdPic = pygame.transform.rotate(orjBird, math.degrees(math.atan(-vertSpeed/20)))
        birdBluePic =pygame.transform.rotate(orjBirdBlue,math.degrees(math.atan(-vertSpeed2/20)))

        # Updating our bird picture on pyGame
        screen.blit(birdPic, [xOfBird, yOfBird])
        screen.blit(birdBluePic, [xOfBird2, yOfBird2])

        # Drawing the rectangle of the bird
        # pygame.draw.rect(screen, BLACK, (xOfBird, yOfBird, 64, 48), 1)
        # pygame.draw.rect(screen, RED, (xOfBird2, yOfBird2, 64, 48), 1)

        # Handling all the blocks in the game.
        for block in blockList:
            # Moving the blocks
            if gameStarted:
                block.xValue -= blockSpeed
            # Drawing the block
            block.draw(screen)
            # If the blick has passed the left side of the screen by 300
            # We send it to the right side of the screen
            if block.xValue < -300:
                block.xValue = 1300
            # Checking if the bird is touching the obstacle

            if block.check(pygame.Rect(xOfBird, yOfBird, 64, 48)):
                gameOver = True
            if block.check(pygame.Rect(xOfBird2, yOfBird2, 64, 48)):
                gameOver2 = True
            if yOfBird < -100:
                gameOver = True
            if yOfBird2 < -100:
                gameOver = True

        # Increasing points if bird is still alive
        if(scoreTime >= scoreRate) and gameStarted == True and (gameOver == False or gameOver2 == False):
            score += 1
            scoreTime = 0

        # Increasing the scoreTime to give points while flying
        scoreTime += 1

        # Checking if bird has fallen
        if yOfBird > 725:
            gameOver = True

        if yOfBird2 > 725:
            gameOver2 = True

        if gameOver and gameOver2:
            # Applying the settings for game over.
            gameStarted = False
            # Printing out the score and the gameover text.
            menuFont = pygame.font.SysFont('Arial', 60, True, False)
            screen.blit(menuFont.render("Score: " + str(score), True, WHITE), [400, 350])
            screen.blit(gameOverPic, [340,250])
            pygame.display.flip()
            # Waiting for 5 seconds
            pygame.time.delay(4000)

            # Moving the bird back to its initial postion.
            yOfBird = 400
            xOfBird = 130
            gameOver = False
            score = 0

            # Moving the bird back to its initial postion.
            yOfBird2 = 400
            xOfBird2 = 250
            gameOver = False
            gameOver2 = False
            score = 0
            # Resetting the obstacles
            initBlocks()

        # If the game is over, send the bird back
        if gameOver:
            xOfBird -= blockSpeed
        if gameOver2:
            xOfBird2 -= blockSpeed

        # If the game has started, we print the ingame score
        if gameStarted and (not gameOver or not gameOver2) :
            printScore(screen, score)

        # If the game hasn't started, we show instructions
        elif not gameStarted and not gameOver:
            printIns(screen)

        pygame.display.flip()

        # Moving the second bird
        yOfBird2 += vertSpeed2
        vertSpeed2 += fallingConst

        # Moving the first bird
        yOfBird += vertSpeed
        vertSpeed += fallingConst

        if not gameStarted and not gameOver:
            if yOfBird >= 400:
                vertSpeed = jumpSpeed
            if yOfBird2 >= 400:
                vertSpeed2 = jumpSpeed

        # FPS of the game
        clock.tick(99990)
        # print(score)
    pygame.quit()

# Main if for starting the game
if __name__ == "__main__":
    Flappy_Bird_Game()
