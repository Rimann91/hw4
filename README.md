# Project Overview

This README will be for keeping track of project goals and progress for the
developers rather than for assisting potential users.

## Game Play instructions

**objective**

Don't let the ball hit the floor!, you only get five lives.

- *MOVEMENT:* use LEFT and RIGHT arrow keys to move paddle

- *BALL DIRECTION:* the ball direction can be changed by hitting it with the
  paddle while the paddle is in motion

- *PAUSE GAME:* you can pause the game by pressing (p). Press (c) to continue


## Current Functionality and Future plans

**Current**

Game is very primitive, a ball bounces around screen in a predictable pattern,
when it hits the bottom a life is lost. When lives hit 0, the program closes.
The paddle is moveable with the arrow keys (LEFT and RIGHT). Currently working
on ball bounce pattern changes when ball hits a moving paddle.

**TODO:**

- Game Over screen and new game option

- Pause function

*[here](https://pythonprogramming.net/pause-game-pygame/) to short example of
`pause` and `game over` functions*

- Better ball physics

- Ball starts non moving on paddle until a specified key is pressed

- Ball explodes/ dissapears on life lost and new ball becomes available on
  paddle

- Point/scoring system

- Levels

- Objectives
    
    - Hit paddle `x` many times in a row

    - break blocks

    - make a basket

    - survive for `x` minutes

- Obstacles

  
## ballgame.py

*The main file script*

currently the only file script, it hosts the main game logic

## Other potential packages

1) Package for different kinds of obstacles

2) High score database (python dictionary file)  

3) package for different levels

