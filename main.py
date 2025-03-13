import pygame as pg
import time

from enemies import Enemies
from ship import Ship


# initializes the pygame
pg.init()


class Game:
    """creates the game"""
    def __init__(self):

        # sets the window sizing
        self.width = 600
        self.height = 600
        self.window = pg.display.set_mode((self.width, self.height))
        # creates the clock
        self.clock = pg.time.Clock()

        # sets the enemy group for the aliens
        self.enemy_group = pg.sprite.Group()
        # creates an enemy matrix
        self.enemies = Enemies(self.enemy_group)
        # creates the ship
        self.ship = Ship(300, 500)

        # sets the score to 0
        self.score = 0
        # sets the font to the font in the font file
        self.font = pg.font.Font("font/pixel.ttf", 20)

        # creates a game loop
        self.gameLoop()

    def update_score(self, points):
        """updates the score with the points of the alien"""
        self.score += points

    def draw_score(self):
        """draws the score the window"""
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.window.blit(score_text, (self.width-score_text.get_width() - 20, self.height-score_text.get_height()-20))

    def checkCollisions(self):
        """checks if there are collisions between objects"""
        # checks if a bullet hits an alien
        for bullet in self.ship.bullets:
            collided_enemies = pg.sprite.spritecollide(bullet, self.enemy_group, True)
            if collided_enemies:
                bullet.die()
                for enemy in collided_enemies:

                    self.update_score(enemy.worth)
                    enemy.kill()
                    self.enemies.remove(enemy)

        collision = pg.sprite.spritecollide(self.ship, self.enemies.enemy_bullets, True)
        if collision:
            # if there is a collision the game ends
            # refill the window with black
            self.window.fill((0, 0, 0))
            # set the win message
            win_message = self.font.render("You Lose", True, (255, 255, 255))
            self.window.blit(win_message, (self.width // 2 - win_message.get_width() // 2, self.height // 2))

            # update the display, wait before exiting
            pg.display.update()
            pg.time.wait(3000)
            pg.quit()
            return

    def gameLoop(self):
        """sets the game loop"""
        last_time = time.time()
        self.enemies.create_row(11, 7)

        while True:
            # creates a delta of time that all movements are based on
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            # check if the event is QUIT
            for event in pg.event.get():
                # if it is, leave the game
                if event.type == pg.QUIT:
                    pg.quit()
                    return

            keys = pg.key.get_pressed()
            # if the event is up, shoot
            if keys[pg.K_UP]:
                self.ship.shoot()
            # if the event is left move the ship left
            if keys[pg.K_LEFT] and self.ship.rect.left > 0:
                self.ship.update(dt)
            # if the event is right move the ship right
            if keys[pg.K_RIGHT] and self.ship.rect.right < 600:
                self.ship.update(-dt)

            # color the window black
            self.window.fill((0, 0, 0))

            # render all fired ship bullets
            for bullet in self.ship.bullets:
                bullet.update(dt)
                self.window.blit(bullet.image, bullet.rect)

            # render all fired alien bullets
            for laser in self.enemies.enemy_bullets:
                laser.update(dt)
                self.window.blit(laser.image, laser.rect)

            # check if there are any collisions
            self.checkCollisions()

            # if the alien matrix is empty continue
            if all(not sublist for sublist in self.enemies.row):
                # refill the window with black
                self.window.fill((0, 0, 0))
                # set the win message
                win_message = self.font.render("You Win!", True, (255, 255, 255))
                self.window.blit(win_message, (self.width // 2 - win_message.get_width() // 2, self.height // 2))

                # update the display, wait before exiting
                pg.display.update()
                pg.time.wait(3000)
                pg.quit()
                return

            # move the enemies
            self.enemies.move(dt, self.window)
            # puts the ship onto the window
            self.window.blit(self.ship.image, self.ship.rect)
            # draws the score to the display
            self.draw_score()
            # updates the screen
            pg.display.update()
            self.clock.tick(60)


# creates and runs game
game = Game()
