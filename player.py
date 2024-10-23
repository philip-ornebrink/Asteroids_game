from circleshape import CircleShape
from constants import *
import pygame
from bullets import *

class Player(CircleShape):
    def __init__(self,x,y, name, id):
        containers = ()
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.name = name
        self.id = id
        self.lives = 3
        self.regenerate = 0
        self.color = "white"

        # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen,self.color,self.triangle(),width=2)

    def rotate(self,dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update_player1(self, dt):
        if self.regenerate > 0:
            self.regenerate -= dt
            return
        self.color = "white"
        keys = pygame.key.get_pressed()
        self.timer -= dt 

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_1]:
            self.shoot()

    def update_player2(self,dt):
        if self.regenerate > 0:
            self.regenerate -= dt
            return
        self.color = "white"
        keys = pygame.key.get_pressed()
        self.timer -= dt 

        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_PERIOD]:
            self.shoot()


    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.timer > 0:
            return
        else:
            direction = pygame.Vector2(0,1).rotate(self.rotation)
            shot = Shot(self.position.x, self.position.y,self.name) 
            shot.velocity = PLAYER_SHOOT_SPEED * direction
            self.timer = PLAYER_SHOOT_COOLDOWN

    def hit(self):
        if self.regenerate > 0:
            return
        if self.lives > 0:
            self.color = "red"
            self.lives -= 1
            self.regenerate = PLAYER_HIT_REGENERATE_TIME
        else:
            self.kill()

    def straight_line_eq(self, point1, point2, obj):
        if point1.x - point2.x == 0:
            return None
        gradient = (point1.y - point2.y) / (point1.x - point2.x) 
        intercept = point1.y - point2.x * gradient
        y = obj.position.x * gradient + intercept
        return y
    
    def collision(self, obj): 
        coordinates = self.triangle()
        pointA = coordinates[0]
        pointB = coordinates[1]
        pointC = coordinates[2]

        cornersY = [pointA.y, pointB.y, pointC.y]
        cornersX = [pointA.x, pointB.x, pointC.x]

        maxY = max(cornersY)
        minY = min(cornersY)
        maxX = max(cornersX)
        minX = min(cornersX)

        yAB = self.straight_line_eq(pointA, pointB, obj)
        yBC = self.straight_line_eq(pointB, pointC, obj)
        yCA = self.straight_line_eq(pointC, pointA, obj)
    
        if (obj.position.y >= minY and obj.position.y <= maxY) and (obj.position.x >= minX and obj.position.x <= maxX):

            yPoints = [yAB, yBC, yCA]
            for y in yPoints:
                if y > maxY or y < minY or y == None:
                    yPoints.remove(y)

            if obj.position.y <= max(yPoints) and obj.position.y >= min(yPoints):
                return True


