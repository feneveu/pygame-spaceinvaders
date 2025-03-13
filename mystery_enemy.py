import pygame as pg
from bullet import EnemyLaser
import random


class MysteryEnemy(pg.sprite.Sprite):

    def __init__(self, posx, posy):
        super(MysteryEnemy, self).__init__()

        # sets up the images for the mystery enemy
        em = pg.image.load("images/mystery.png").convert_alpha()

        # changes the size of the image
        new_size = (em.get_width() // 5, em.get_height() // 5)  # Shrinks by 50%

        # starts at the first image
        self.image = pg.transform.scale(em, new_size)

        # creates a mask
        self.mask = pg.mask.from_surface(self.image)
        # sets a rectangle
        self.rect = pg.Rect(posx, posy, self.image.get_width(), self.image.get_height())

        # there have been 0 animation counts
        self.anim_counter = 0

        # the speed that they move at side to side
        self.speed = 160

        # will switch to number 1 as the other animation
        self.image_switch = 1

        # the x position of this specific alien
        self.xpos = posx
        # the y position of this specific alien
        self.ypos = posy

        # the mystery aliens are worth 10 points
        self.worth = self.randscore()

    def randscore(self):
        """creates a randomscore"""
        scoreval = random.choice([50, 100, 150, 200, 300])
        return scoreval

    def toggle_image(self):
        """switches the image in animation"""
        if self.image_switch == 0:
            self.image_switch = 1
        else:
            self.image_switch = 0

    def die(self):
        """kills the alien"""
        self.kill()
        del self
