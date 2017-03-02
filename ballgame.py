import sys, pygame
from pygame.locals import *

class game():

    def __init__(self):

        pygame.init()
        pygame.font.init()

        # set key hold down repeat

        pygame.key.set_repeat(1,1)

        # Image Sizes and positions and movement speeds
        self.lives_size = 700, 200
        self.padle_size = [90,10]
        self.padle_pos  = [350, 685]
        self.game_size = self.width, self.height = 700,700

        # Balls Movement Speed
        # Note: this is confusing because its both speed AND direction
        self.speedX = -2     # X coordinate movement for ball
        self.speedY = 2      # Y coordinate movement for ball
        self.speed = [self.speedX, self.speedY]  # Total ball Movement speed


        # Number of lives
        self.num_lives = 5
        self.speedX = -2
        self.speedY = 2
        self.speed = [self.speedX, self.speedY]

        # Colors, RGB values
        self.white = 255, 255, 255
        self.black = 0, 0, 0

        # Font style and display
        self.font = pygame.font.SysFont("Verdona", 24)
        self.font_color = self.black
        self.font_background = self.white


        # Label area where lives are displayed
        # Game over display not currently working
        self.display_lives = pygame.display.set_mode(self.lives_size)
        self.game_over = pygame.display.set_mode(self.lives_size)

        # Main Window for game... Wierd spot for it
        self.main_window = pygame.display.set_mode((700,720))

        # Game play Window
        self.screen = pygame.Surface((self.game_size))
        self.screen_rect = self.screen.get_rect()

        # Importing ball Image
        self.ball = pygame.image.load("redball2.png")
        self.ballrect = self.ball.get_rect()



    def paddle(self):

        # make the padle
        # This is the pygame Drawing function
        paddle = pygame.draw.rect(self.screen, self.black,
                Rect(self.padle_pos, self.padle_size))
        return paddle



    def moveBall(self):
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
        self.screen.fill(self.white)

        #place the ball on the screen
        self.screen.blit(self.ball, self.ballrect)
        pygame.display.flip()

    def hitPadle(self):
        pass

    def gameOver(self):
        gameover = "GAME OVER"
        self.main_window.fill((self.black))
        label = self.font.render(
                gameover,      # The font to render
                1,             # With anti aliasing
                self.font_color,
                self.font_background)
        label_rect = label.get_rect()

        return self.game_over.blit(label, (300, 0),label_rect)



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

                    # If yes, paddle moving, change ball direction accordingly
                    if  event.key == pygame.K_RIGHT:
                        change_direction = True
                        # make variable for which way to change direction
                        direction_change = go_right
                        # This Condition keeps the paddle on screen
                        if self.padle_pos[0] > self.width-self.padle_size[0]:
                            self.padle_pos[0]+=0
                        else:
                            self.padle_pos[0] += 3

                    # Same as previous If nest, but opposit direction
                    if  event.key == pygame.K_LEFT:
                        change_direction = True
                        direction_change = go_left
                        if self.padle_pos[0] < 0:
                            self.padle_pos[0]+=0
                        else:
                            self.padle_pos[0] -= 3


            # Put the paddle on screen
            paddle = self.paddle()

            # Ignore
            #self.movePaddle()

            if  self.num_lives == 0:

                self.gameOver()
                break

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


            # Yay pygame collision testing
            # Test if ball collides with paddle
            if self.ballrect.colliderect(paddle):
                print('good hit')

                # Conditions for how to adjust ball speed `self.speed` var
                # Should adujust speed AND invert direction
                # Currently not working properly

                    # 1) When moving left, ball often is not inverted and life
                    #    is lost, Ball usually goes throug paddle and often
                    #    becomes stuck and game ends immediatly.

                    # 2) Occasionally ball inverts in wrong direction????
                    #    happened once. While moving left

                    # 3) Ball changes correctly on right movements, however
                    #    gains far too  much speed. Needs a way to make more
                    #    minute adjustments.

                if change_direction is True:
                    print('change direction', self.speed)
                    # Changes the X coordinate in speed to a negative (inverts)
                    # This is what creates the bounce effect
                    self.speed[1] = -self.speed[1]
                    print(self.speed)

                    if direction_change == go_right:
                        speedX += 1
                        speedY -= 1
                        self.speed = [speedX, speedY]
                        direction_change = 0
                    elif direction_change == go_left:
                        speedX -= 1
                        speedY += 1
                        self.speed = [speedX, speedY]
                        direction_change = 0
                    else: self.speed = self.speed

                else:
                    print('direction constant')
                    self.speed[1] = -self.speed[1]

            # Life lost if ball hits bottom of screen
            if self.ballrect.bottom > self.height:
                print('hit bottom',self.speed)
                self.num_lives-=1
                print(self.num_lives)


            self.moveBall()

game = game()
game.game_loop()