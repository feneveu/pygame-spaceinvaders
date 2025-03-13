import pygame as pg
from bullet import Bullet
import time


class Ship(pg.sprite.Sprite):
    """creates the space ship"""

    def __init__(self, xpos, ypos):
        super(Ship, self).__init__()

        # loads the ship image
        ship = pg.image.load("images/ship.png").convert_alpha()

        # resizes the image
        new_size = (ship.get_width() // 1, ship.get_height() // 1)  # Shrinks by 50%
        self.image = pg.transform.scale(ship, new_size)

        # creates the mask
        self.mask = pg.mask.from_surface(self.image)
        # creates the rect
        self.rect = pg.Rect(xpos, ypos, self.image.get_width(), self.image.get_height())

        # sets the movement speed of the ship
        self.speed = 100

        # tracks the x and y pos of the ship
        self.xpos = xpos
        self.ypos = ypos

        # creates the bullets group for the ship bullets
        self.bullets = pg.sprite.Group()

        # sets the ship reload time to 1 second
        self.reload_time = 1
        self.last_shot_time = 0

    def shoot(self):
        """shoots a bullet from the ship"""
        # creates a reference to the current time
        current_time = time.time()
        # check if the bullet reload time has passed
        if current_time - self.last_shot_time >= self.reload_time:

            # create a bullet object
            b = Bullet(self.rect.centerx, self.rect.top)
            # add it to the sprite group
            self.bullets.add(b)
            # reset timer
            self.last_shot_time = current_time

    def update(self, dt):
        """updates the ship position"""
        self.rect.x -= dt * self.speed
        self.xpos -= dt * self.speed

    def die(self):
        """kills the ship"""
        self.kill()
        del self
