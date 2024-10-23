# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from player import *
from asteroidfield import *
from bullets import *
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shotable = pygame.sprite.Group()
    playable = pygame.sprite.Group()

    Player.containers = (playable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = updatable
    Shot.containers = (shotable, updatable, drawable) 
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player1 = Player(x,y, "player1", 1)
    player2 = Player(x,y, "player2", 2)
#    asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")

        for obj in updatable: 
            obj.update(dt)
            
        for obj in drawable:
            obj.draw(screen)

        for player in playable:
            if player.id == 1:
                player.update_player1(dt)
            if player.id == 2:
                player.update_player2(dt)
                

        
        for bullet in shotable:
            if player1.collision(bullet) == True and bullet.shooter != player1.name:
                print("player1 hit by bullet")
                player1.hit()
                bullet.kill()

            if player2.collision(bullet) == True and bullet.shooter != player2.name:
                print("player2 hit by bullet")
                player2.hit()
                bullet.kill()
            #if bullet.collision(player1) == True and bullet.shooter != player1.name:
                #player1.hit()
                #bullet.kill()
                #print("Player2 won")
                
            #if bullet.collision(player2) == True and bullet.shooter != player2.name:
                #player2.hit()
                #bullet.kill()
                #print("Player1 won")


        for asteroid in asteroids:
            if player1.collision(asteroid) == True or player2.collision(asteroid) == True:
                print("Game Over!")
                sys.exit()
            for bullet in shotable:
               if bullet.collision(asteroid) == True:
                    bullet.kill()
                    asteroid.split()
                    
        if player1.lives == 0:
            msg = f"Game Over! Player2 won!"
            final_msg(msg,screen,x,y)
            player1.kill()
            player2.kill()

        if player2.lives == 0:
            msg = "Game Over! Player1 won!"
            final_msg(msg,screen,x,y)
            player1.kill()
            player2.kill()
        
        pygame.display.flip()

        dt = clock.tick(60) / 1000

def final_msg(msg, screen,x,y):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 40)
    font_width = pygame.font.Font.size(font, msg)[0]
    x_pos = x - font_width/2
    font_msg = pygame.font.Font.render(font,msg, True, "white")
    pygame.Surface.blit(screen,font_msg,(x_pos,y))
    pygame.display.flip()

if __name__ == "__main__":
    main()

