# Fighting Fantasy Pygame
This project is intended to demonstrate a simple dungeon crawl adventure game set up using a Pygame interface

## Run ff_pygame_interface to start the game
* Use arrow keys to move a player character
* Use "n" to move onto the next player character
* Use "o" to open doors and "c" to close doors

## Features
* Game and game objects are kept separate from the pygame interface
* Changes in the game object, such as changing position or name triggers on-screen changes using the observer model
** Pygame sprites are attached as observers to the GameObj
** The GameObj objects include "setter" functions for pos (position) and "name" (using the @name.setter decorator)
** When the attribute is changed, the _update_observers method is run in order to update the attached sprites
* Pygame interface includes background 32*32 bit sprites and character sprites, which are displayed in a 16 * 16 grid
* Pygame loop checks for key presses and redraws the sprites if any have been updateds

## TODO
Currently characters can move and open doors
* Add Fighting Fantasy fighting when player characters meet NPCs
* Add movement for NPCs
* Add treasure objects that characters can possess
