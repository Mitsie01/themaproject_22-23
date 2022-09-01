import pygame
import os
import math
import sys

# Map image dimensions
SCREEN_WIDTH = 1244
SCREEN_HEIGHT = 1016
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

TRACK = pygame.image.load(os.path.join("img", "track.png"))

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # load car image and set defaults
        self.original_image = pygame.image.load(os.path.join("img", "car.png"))
        self.image = self.original_image
        
        self.rect = self.image.get_rect(center=(490, 820))
        self.drive_state = False
        self.reverse = False
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.rotation_vel = 5
        self.direction = 0
        self.alive = True

    
    # Update car position
    def update(self):
        self.drive()
        self.rotate()
        # set specific radar angles
        for radar_angle in (-60, -30, 0, 30, 60):
            self.radar(radar_angle)
        self.collision()
    
    # Drive forward if drive state = True by vector amount
    def drive(self):
        if self.drive_state:
            if self.reverse:
                self.rect.center -= self.vel_vector * 6
            elif not self.reverse:
                self.rect.center += self.vel_vector * 6

    
    # Turn vehicle
    def rotate(self):
        if self.direction == 1:
            self.angle -= self.rotation_vel
            self.vel_vector.rotate_ip(self.rotation_vel)
        elif self.direction == -1:
            self.angle += self.rotation_vel
            self.vel_vector.rotate_ip(-self.rotation_vel)

        self.image = pygame.transform.rotozoom(self.original_image, self.angle, 0.1)
        self.rect = self.image.get_rect(center=self.rect.center)


    def collision(self):
        length = 40
        collision_point_right = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 18)) * length),
                                 int(self.rect.center[1] - math.sin(math.radians(self.angle + 18)) * length)]
        collision_point_left = [int(self.rect.center[0] + math.cos(math.radians(self.angle - 18)) * length),
                                int(self.rect.center[1] - math.sin(math.radians(self.angle - 18)) * length)]

        # stop at collision
        if SCREEN.get_at(collision_point_right) == pygame.Color(2, 105, 31, 255) or SCREEN.get_at(collision_point_left) == pygame.Color(2, 105, 31, 255):
           self.alive = False

        # draw collision point
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_right, 4)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_left, 4)


    def radar(self, radar_angle):
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])

        while not SCREEN.get_at((x, y)) == pygame.Color(2, 105, 31, 255) and length < 200:
            length += 1
            x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * length)
            y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * length)

        # Draw radar
        pygame.draw.line(SCREEN, (255, 255, 255, 255), self.rect.center, (x, y), 1)
        pygame.draw.circle(SCREEN, (0, 255, 0, 0), (x, y), 3)


car = pygame.sprite.GroupSingle(Car())


def eval_genomes():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display track within window
        SCREEN.blit(TRACK, (0, 0))

        # User input
        user_input = pygame.key.get_pressed()
        
        # Drive state False when no keys pressed
        if sum(pygame.key.get_pressed()) <= 1:
            car.sprite.drive_state = False
            car.sprite.direction = 0
        
        # User controls
        if user_input[pygame.K_w]:
            car.sprite.drive_state = True
            car.sprite.reverse = False
        elif user_input[pygame.K_s]:
            car.sprite.drive_state = True
            car.sprite.reverse = True
        if user_input[pygame.K_a]:
            car.sprite.direction = -1
        elif user_input[pygame.K_d]:
            car.sprite.direction = 1
        

        # Update
        car.draw(SCREEN)
        car.update()
        pygame.display.update()



eval_genomes()