import sys, pygame
from pygame.locals import *

class game():

    def __init__(self):

        pygame.init()
        pygame.font.init()

        # set key hold down repeat

        pygame.key.set_repeat(2,2)

        # Image Sizes and positions and movement speeds
        self.lives_size = 700, 200
        self.padle_size = [50,10]
        self.padle_pos  = [350, 685]
        self.game_size = self.width, self.height = 700,700
        self.gButton_pos = [150, 300 ]
        self.gButton_size = [100, 50]
        self.rButton_pos = [450, 300]
        self.rButton_size = [100, 50]

        # Balls Movement Speed
        # Note: this is confusing because its both speed AND direction
        self.speedX = -2     # X coordinate movement for ball
        self.speedY = 1      # Y coordinate movement for ball
        self.speed = [self.speedX, self.speedY]  # Total ball Movement speed


        # Number of lives
        self.num_lives = 1

        # Colors, RGB values
        self.white = 255, 255, 255
        self.black = 0, 0, 0
        self.red = 200,0,0
        self.green = 0,200,0
        self.b_red = 255,0,0
        self.b_green = 0,255,0

        # Font style and display
        self.font = pygame.font.SysFont("Verdona", 24)
        self.font_color = self.black
        self.font_background = self.white

        # game state
        self.pause = False



        # Label area where lives are displayed
        # Game over display not currently working
        self.display_lives = pygame.display.set_mode(self.lives_size)


        # Main Window for game... Wierd spot for it
        self.main_window = pygame.display.set_mode((700,720))

        # Game play Window
        self.screen = pygame.Surface((self.game_size))
        self.screen_rect = self.screen.get_rect()

        # Make game oover window image
        #game_over = pygame.display.set_mode((200,200))
        #gameover_rect = self.game_over.get_rect()

        # Importing ball Image
        self.ball = pygame.image.load("redball2.png")
        self.ballrect = self.ball.get_rect()


    def textObjects(self, text, font):
        textSurface = font.render(text, True, self.black)
        return  textSurface, textSurface.get_rect()

    def Button(self, msg, color, b_color, x,y, w,h, action = None):

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        print(mouse)


       # identify button boundry

        boundry = x + w > mouse[0] > x and y + h > mouse[1] > y

        # button image / active vs inactives

        if boundry is True:

            pygame.draw.rect(self.main_window, b_color, Rect((x,y), (w,h)))

            if click[0] == 1 and action != None:

                if action == "start":
                    self.num_lives = 5
                    self.game_loop()

                elif action == "quit":
                    pygame.quit()


        else:

            pygame.draw.rect(self.main_window, color, Rect((x,y), (w,h)))

        text = pygame.font.SysFont("Verdona", 40)
        textSurface, textRect = self.textObjects(msg, text)
        self.main_window.blit(textSurface, (x, y),textRect)




    def paddle(self):

        # make the padle
        # This is the pygame Drawing function
        paddle = pygame.draw.rect(self.screen, self.black,
                Rect(self.padle_pos, self.padle_size))
        return paddle


    def moveBall(self):
        # Doesn't only move ball
        # updates lives
        # places windows

        # Fill main window color Black
        self.main_window.fill((self.black))

        # place the game play window on main window
        self.main_window.blit(self.screen, (0,20), self.screen_rect)

        # Show Lives
        lives = "lives left: {}".format(self.num_lives)
        label = self.font.render(
                lives,         # The string to render
                1,             # With anti aliasing
                self.font_color,
                self.font_background)

        # Make lives display an image object
        label_rect = label.get_rect()

        # place the lives display on the window made for it
        self.display_lives.blit(label, (300, 0),label_rect)


        # place the game play window on main window
        self.main_window.blit(self.screen, (0,20), self.screen_rect)
        # place the lives display on the window made for it
        self.screen.fill(self.white)

        #place the ball on the screen
        self.screen.blit(self.ball, self.ballrect)
        pygame.display.flip()

    def hitPadle(self):
        pass

    def gameOver(self):

        self.screen.fill((self.white))
        self.main_window.blit(self.screen, (0,20), self.screen_rect)


        while True:

            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    #quit()

            self.Button("AGAIN!",self.green, self.b_green, 150,300, 100,50, "start")
            self.Button("QUIT",self.red, self.b_red, 450,300, 100,50, "quit")


            pygame.display.flip()


    def paused(self):

            #largeText = pygame.font.SysFont("comicsansms",115)
            #TextSurf, TextRect = text_objects("Paused", largeText)
            #TextRect.center = ((display_width/2),(display_height/2))
            #gameDisplay.blit(TextSurf, TextRect)

            while self.pause:

                for event in pygame.event.get():

                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    if event.type == KEYDOWN:
                        if event.key == K_c:
                            self.pause = False
                            break



    def game_loop(self):

        # OK here we go
        # Ignore ALL  print statements, they are there for debug

        # make some variables to help direction changes
        change_direction = False
        speedX = 2
        speedY = 2
        go_right = 1
        go_left = 2
        direction_change = 0

        # MAIN EVENT LOOP
        while True:

            # Event testing loop

            for event in pygame.event.get():
                #print(event)

                #condition to exit
                if event.type == pygame.QUIT: sys.exit()

                # Conditions for handling the paddle

                # Test if a key is pressed
                if event.type == KEYUP:
                    # If not, paddle not moving, ball direction uneffected
                    change_direction = False
                if event.type == pygame.KEYDOWN:

                    # See which key is pressed
                    # If yes, paddle moving, change ball direction accordingly
                    if  event.key == pygame.K_RIGHT:
                        change_direction = True
                        # make variable for which way to change direction
                        direction_change = go_right
                        # This Condition keeps the paddle on screen
                        if self.padle_pos[0] > self.width-self.padle_size[0]:
                            self.padle_pos[0]+=0
                        else:
                            self.padle_pos[0] += 5

                    # Same as previous If nest, but opposit direction
                    if  event.key == pygame.K_LEFT:
                        change_direction = True
                        direction_change = go_left
                        if self.padle_pos[0] < 0:
                            self.padle_pos[0]+=0
                        else:
                            self.padle_pos[0] -= 5

                    # Pause game key (p), press (c) to continue. 
                    #    see paused() method
                    if event.key == K_p:
                        self.pause = True
                        self.paused()


            # Put the paddle on screen
            paddle = self.paddle()

            # Ignore
            #self.movePaddle()

            if  self.num_lives == 0:

                print('='*30,'\n','='*30)
                #self.pause = True
                #self.paused()
                self.gameOver()

            # Move Ball

            #print (self.speed)
            # This is the Pygame function that makes the ball move
            self.ballrect = self.ballrect.move(self.speed)

            # Test if ball hits wall, cieling or floor and inverts direction
            if self.ballrect.left < 0 or self.ballrect.right > self.width:
                self.speed[0] = -self.speed[0]
                print("hit side",self.speed)

            if self.ballrect.top < 0 or self.ballrect.bottom > self.height:
                self.speed[1] = -self.speed[1]

            # Print speed at top screen bounce for debugging
            if self.ballrect.top < 0:
                print('hit top ', self.speed)


            # Yay pygame collision testing
            # Test if ball collides with paddle
            if self.ballrect.colliderect(paddle):
                print('good hit')

                # Conditions for how to adjust ball speed `self.speed` var
                # Should adujust speed AND invert direction
                # Currently not working properly, However I do have it working
                # much better now and not quite as worried.

                    # 1) When moving left, ball sometimes is not inverted (bounced
                    #    up) and life is lost, Ball usually goes throug paddle and often
                    #    becomes stuck and game ends immediatly.

                    # 2) Occasionally ball inverts in wrong direction????
                    #    switch from -1>>0>>1 and visa versa is probably
                    #    creating something wierd here.

                    # 3) Speed Fluctuates seemingly at random, could be lag
                    #
                    #

                if change_direction is True:
                    print('change direction', self.speed)
                    # Changes the X coordinate in speed to a negative (inverts)
                    #print(self.speed)

                    if direction_change == go_right:
                        speedX += 1
                        speedY -= 1
                        self.speed = [speedX, speedY]
                        direction_change = 0
                        print('change right', self.speed)

                    elif direction_change == go_left:
                        speedX -= 1
                        speedY += 1
                        self.speed = [speedX, speedY]
                        direction_change = 0
                        print('change left', self.speed)

                    else: self.speed = self.speed
                    # This is what creates the bounce effect
                    self.speed[1] = -self.speed[1]
                    print('after bounce', self.speed)
 
                else:
                    self.speed[1] = -self.speed[1]
                    print('direction constant', self.speed)

            # Life lost if ball hits bottom of screen
            if self.ballrect.bottom > self.height:
                print('hit bottom',self.speed)
                self.num_lives-=1
                print(self.num_lives)


            self.moveBall()

game = game()
game.game_loop()
