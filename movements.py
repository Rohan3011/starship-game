import pygame


class Movement:

    '''
    Handles player movements
    '''

    # constructor
    def __init__(self, height, width, border, velocity):
        self.height = height
        self.width = width
        self.border = border
        self.velocity = velocity

    def player1_handle_movement(self, player1, key_pressed):
        if (key_pressed[pygame.K_a]
                and player1.x - self.velocity) > 0:
            player1.x -= self.velocity

        if (key_pressed[pygame.K_d]
                and player1.x + self.velocity
                + player1.width < self.border.x):
            player1.x += self.velocity

        if (key_pressed[pygame.K_w]
                and player1.y - self.velocity) > 0:
            player1.y -= self.velocity

        if (key_pressed[pygame.K_s] and
                player1.y + self.velocity
                + player1.height < self.height):
            player1.y += self.velocity

    def player2_handle_movement(self, player2, key_pressed):
        if (key_pressed[pygame.K_LEFT]
                and player2.x - self.velocity > self.border.x
                + self.border.width):
            player2.x -= self.velocity

        if (key_pressed[pygame.K_RIGHT]
                and player2.x + self.velocity
                + player2.width < self.width):
            player2.x += self.velocity

        if (key_pressed[pygame.K_UP]
                and player2.y - self.velocity) > 0:
            player2.y -= self.velocity

        if (key_pressed[pygame.K_DOWN]
                and player2.y + self.velocity
                + player2.height < self.height):
            player2.y += self.velocity
