# William Riley Hughes
# HW 4

"""Added functionality

- Intro, Pause, game_over screens
- Pause option with (p) key
- option to quit from pause
- option to play again or quit in gameover
- Ball changes direction depending on if, and which way the paddle is moving at
  collision
- Added sound effects

"""

import sys, pygame
from pygame.locals import *


class game():

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        # set key hold down repeat

        pygame.key.set_repeat(2,2)

        # Image Sizes and positions and movement speeds
        self.display_width = 700
        self.display_height = 720
        self.lives_size = 700, 200
        self.padle_size = [80,20]
        self.padle_pos  = [350, 675]
        self.game_size = self.width, self.height = 700,700
        self.gButton_pos = [150, 300 ]
        self.gButton_size = [100, 50]
        self.rButton_pos = [450, 300]
        self.rButton_size = [100, 50]

        # Balls Movement Speed
        self.speedX = -4     # X coordinate movement for ball
        self.speedY = 3      # Y coordinate movement for ball
        self.speed = [self.speedX, self.speedY]  # Total ball Movement speed

        # Sound effects
        self.pong = pygame.mixer.Sound("pingpong.ogg")
        self.dribble = pygame.mixer.Sound("dribble.ogg")
        self.crash = pygame.mixer.Sound("crash.ogg")

        # Number of lives
        self.num_lives = 5

        # Colors, RGB values
        self.white = 255, 255, 255
        self.black = 0, 0, 0
        self.red = 200,0,0
        self.green = 0,200,0
        self.b_red = 255,0,0
        self.b_green = 0,255,0

        # Font style and display
        self.font = pygame.font.SysFont("Verdona", 24)
        self.large_text = 115
        self.small_text = 30
        self.font_color = self.black
        self.font_background = self.white

        # game state
        self.pause = False

        # Label area where lives are displayed
        self.lives_label = pygame.Surface((700, 15))
        self.lives_rect = self.lives_label.get_rect()

        # Main Window for game
        self.main_window = pygame.display.set_mode((self.display_width, self.display_height))

        # Game play Window
        self.screen = pygame.Surface((self.game_size))
        self.screen_rect = self.screen.get_rect()

        # Importing ball Image
        self.ball = pygame.image.load("redball2.png")
        self.ballrect = self.ball.get_rect()


    def textObjects(self, text, font):
        """make text images"""

        textSurface = font.render(text, True, self.black)
        return  textSurface, textSurface.get_rect()

    def Button(self, msg, color, b_color, x,y, w,h, action = None):
        """Create buttons

        no built in button functions in pygame, create from scratch
        """

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

       # identify button boundry

        boundry = x + w > mouse[0] > x and y + h > mouse[1] > y

        # button image / active vs inactives
        # changes color of button if hovered over

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

        text = pygame.font.SysFont("Verdona", 30)
        textSurface, textRect = self.textObjects(msg, text)
        #textRect.center((x+(w/2)),(y+(h/2)))
        self.main_window.blit(textSurface,(x,y+15), textRect)


    def paddle(self):
        """ make the padle"""

        paddle = pygame.draw.rect(self.screen, self.black,
                Rect(self.padle_pos, self.padle_size))
        return paddle


    def update_screen(self):
        """what to update each frame/loop"""

        # updates lives

        # Fill main window color Black
        self.main_window.fill((self.black))

        # place the game play window on main window
        self.main_window.blit(self.screen, (0,20), self.screen_rect)
        self.main_window.blit(self.lives_label, (0,0), self.lives_rect)
        self.lives_label.fill((self.white))

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
        self.lives_label.blit(label, (300, 0),label_rect)


        # place the game play window on main window
        self.main_window.blit(self.screen, (0,20), self.screen_rect)
        self.screen.fill(self.white)

        #place the ball on the screen
        self.screen.blit(self.ball, self.ballrect)
        pygame.display.flip()


    def gameOver(self):
        """Create game over screen

        Note: does not restart ball position if you play again, just resets
        lives. There is a glitch if the ball goes under the paddle. Lives
        immediatly drop to 0, you wont be able to play again
        """

        self.screen.fill((self.white))
        self.main_window.blit(self.screen, (0,20), self.screen_rect)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = self.textObjects("Game Over", largeText)
        TextRect.center = ((self.display_width/2),(self.display_height/2))
        self.main_window.blit(TextSurf, TextRect)

        while True:

            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    #quit()

            self.Button("AGAIN!",self.green, self.b_green, 150,200, 100,50, "start")
            self.Button("QUIT",self.red, self.b_red, 450,200, 100,50, "quit")


            pygame.display.flip()


    def intro(self):
        """Create Intro screen"""

        self.main_window.fill((self.white))
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = self.textObjects("HW4", largeText)
        TextRect.center = ((self.display_width/2),(self.display_height/2))
        self.main_window.blit(TextSurf, TextRect)

        while True:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == KEYDOWN:
                    if event.key == K_c:
                        self.pause = False
                        break

            self.Button("START",self.green, self.b_green, 150,200, 100,50, "start")
            self.Button("QUIT",self.red, self.b_red, 450,200, 100,50, "quit")
            pygame.display.flip()


    def paused(self):
        """Create pause screen"""

        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf, TextRect = self.textObjects("Paused", largeText)
        TextRect.center = ((self.display_width/2),(self.display_height/2))
        self.main_window.blit(TextSurf, TextRect)

        while self.pause:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == KEYDOWN:
                    if event.key == K_c:
                        self.pause = False
                        break

            self.Button("Continue",self.green, self.b_green, 150,200, 100,50, "start")
            self.Button("QUIT",self.red, self.b_red, 450,200, 100,50, "quit")
            pygame.display.flip()


    def game_loop(self):

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
                        direction_change = go_right
                        # This Condition keeps the paddle on screen
                        if self.padle_pos[0] > self.width-self.padle_size[0]-10:
                            self.padle_pos[0]+=0
                        else:
                            self.padle_pos[0] += 5

                    if  event.key == pygame.K_LEFT:
                        change_direction = True
                        direction_change = go_left
                        if self.padle_pos[0] < 10:
                            self.padle_pos[0]+=0
                        else:
                            self.padle_pos[0] -= 5

                    # Pause game key (p), press (c) to continue.
                    if event.key == K_p:
                        self.pause = True
                        self.paused()

            paddle = self.paddle()

            if  self.num_lives == 0:

                self.gameOver()

            # This is the Pygame function that makes the ball move
            self.ballrect = self.ballrect.move(self.speed)

            # Test if ball hits wall, cieling or floor and inverts direction
            if self.ballrect.left < 0 or self.ballrect.right > self.width:
                pygame.mixer.Sound.play(self.dribble)
                self.speed[0] = -self.speed[0]

            if self.ballrect.top < 0 or self.ballrect.bottom > self.height:
                self.speed[1] = -self.speed[1]

            # Print speed at top screen bounce for debugging
            if self.ballrect.top < 0:
                pygame.mixer.Sound.play(self.dribble)

            # Test if ball collides with paddle

            if self.ballrect.colliderect(paddle):
                pygame.mixer.Sound.play(self.pong)

                """ Intednded to change the trajectory of the ball

                Although it does change the trajectory, due to the nature of
                how pygames `move()` function works, it also changes the speed
                of the ball. """

                if change_direction is True:

                    # Changes the X coordinate in speed to a negative (inverts)

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
                    self.speed[1] = -self.speed[1]

                else:
                    self.speed[1] = -self.speed[1]

            # Life lost if ball hits bottom of screen
            if self.ballrect.bottom > self.height:
                pygame.mixer.Sound.play(self.crash)
                self.num_lives-=1

            self.update_screen()


game = game()

def main():

    game.intro()
    game.game_loop()

main()
