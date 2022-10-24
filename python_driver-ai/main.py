import pygame
import os
import math
import sys
import neat

# Map image dimensions
SCREEN_WIDTH = 1485
SCREEN_HEIGHT = 1016
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

TRACK = pygame.image.load(os.path.join("img", "track5.png"))

marker = False

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # load car image and set defaults
        self.original_image = pygame.image.load(os.path.join("img", "car.png"))
        self.image = self.original_image
        
        self.rect = self.image.get_rect(center=(490, 820))
        self.vel_vector = pygame.math.Vector2(0.8, 0)
        self.angle = 0
        self.drivestate = True
        self.reverse = False
        self.rotation_vel = 5
        self.direction = 0
        self.alive = True
        self.radars = []
        self.marker = False
        self.found = False

    
    # Update car position
    def update(self):
        self.radars.clear()
        self.drive()
        self.rotate()
        # set specific radar angles
        for radar_angle in (-135, -45, 0, 45, 135):
            self.radar(radar_angle)
        self.collision()
        self.data()
    
    # Drive forward if drive state = True by vector amount
    def drive(self):
        if self.drivestate:
            if self.reverse:
                self.rect.center -= self.vel_vector * 6
            if not self.reverse:
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
        collision_point_rightf = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 18)) * length),
                                 int(self.rect.center[1] - math.sin(math.radians(self.angle + 18)) * length)]
        collision_point_leftf = [int(self.rect.center[0] + math.cos(math.radians(self.angle - 18)) * length),
                                int(self.rect.center[1] - math.sin(math.radians(self.angle - 18)) * length)]
        collision_point_rightr = [int(self.rect.center[0] + math.cos(math.radians(self.angle + 162)) * length),
                                 int(self.rect.center[1] - math.sin(math.radians(self.angle + 162)) * length)]
        collision_point_leftr = [int(self.rect.center[0] + math.cos(math.radians(self.angle - 162)) * length),
                                int(self.rect.center[1] - math.sin(math.radians(self.angle - 162)) * length)]


        # stop at collision
        if SCREEN.get_at(collision_point_rightf) == pygame.Color(2, 105, 31, 255) or SCREEN.get_at(collision_point_leftf) == pygame.Color(2, 105, 31, 255) \
        or SCREEN.get_at(collision_point_rightr) == pygame.Color(2, 105, 31, 255) or SCREEN.get_at(collision_point_leftr) == pygame.Color(2, 105, 31, 255):
           self.alive = False
        elif SCREEN.get_at(collision_point_rightf) == pygame.Color(255, 127, 39, 255) or SCREEN.get_at(collision_point_leftf) == pygame.Color(255, 127, 39, 255) \
        or SCREEN.get_at(collision_point_rightr) == pygame.Color(255, 127, 39, 255) or SCREEN.get_at(collision_point_leftr) == pygame.Color(255, 127, 39, 255):
            if self.found == False:
                self.found = True
                self.marker = True
                print('found')
            else:
                self.marker = False

        # draw collision point
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_rightf, 4)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_leftf, 4)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_rightr, 4)
        pygame.draw.circle(SCREEN, (0, 255, 255, 0), collision_point_leftr, 4)

    def radar(self, radar_angle):
        length = 0
        x = int(self.rect.center[0])
        y = int(self.rect.center[1])

        try:
            while not SCREEN.get_at((x, y)) == pygame.Color(2, 105, 31, 255) and length < 200:
                length += 1
                x = int(self.rect.center[0] + math.cos(math.radians(self.angle + radar_angle)) * length)
                y = int(self.rect.center[1] - math.sin(math.radians(self.angle + radar_angle)) * length)
        except:
            pass

        # Draw radar
        pygame.draw.line(SCREEN, (255, 255, 255, 255), self.rect.center, (x, y), 1)
        pygame.draw.circle(SCREEN, (0, 255, 0, 0), (x, y), 3)

        dist = int(math.sqrt(math.pow(self.rect.center[0] - x, 2) + math.pow(self.rect.center[1] - y, 2)))

        self.radars.append([radar_angle, dist])


    def data(self):
        input = [0, 0, 0, 0, 0]
        for i, radar in enumerate(self.radars):
            input[i] = int(radar[1])
        return input



def remove(index):
    cars.pop(index)
    ge.pop(index)
    nets.pop(index)


def eval_genomes(genomes, config):
    global cars, ge, nets

    cars = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        cars.append(pygame.sprite.GroupSingle(Car()))
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0


    run = True
    t = 0
    while run:
        t = t + 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Display track within window
        SCREEN.blit(TRACK, (0, 0))

        if len(cars) == 0:
            break

        for i, car in enumerate(cars):
            ge[i].fitness += 1//(0.1*t)
            
            if car.sprite.drivestate == True and car.sprite.reverse == False:
                ge[i].fitness += 0
            
            if car.sprite.marker:
                ge[i].fitness += 100
                print(f"points given to {i}")
            if not car.sprite.alive or t >= 10**3:
                remove(i)

        for i, car in enumerate(cars):
            output = nets[i].activate(car.sprite.data())
            if output[0] > 0.7 and output[2] > 0.7:
                car.sprite.direction = 1
                car.sprite.reverse = True
                car.sprite.drivestate = True
            if output[1] > 0.7 and output[2] > 0.7:
                car.sprite.direction = -1
                car.sprite.reverse = True
                car.sprite.drivestate = True
            if output[0] <= 0.7 and output[1] <= 0.7 and output[2] > 0.7:
                car.sprite.direction = 0
                car.sprite.reverse = True
                car.sprite.drivestate = True
            if output[0] > 0.7 and output[3] > 0.7:
                car.sprite.direction = 1
                car.sprite.reverse = False
                car.sprite.drivestate = True
            if output[1] > 0.7 and output[3] > 0.7:
                car.sprite.direction = -1
                car.sprite.reverse = False
                car.sprite.drivestate = True
            if output[0] <= 0.7 and output[1] <= 0.7 and output[3] > 0.7:
                car.sprite.direction = 0
                car.sprite.reverse = False
                car.sprite.drivestate = True
            if output[0] > 0.7 and output[2] <= 0.7 and output[3] <= 0.7:
                car.sprite.direction = 1
                car.sprite.drivestate = False
            if output[1] > 0.7 and output[2] <= 0.7 and output[3] <= 0.7:
                car.sprite.direction = -1
                car.sprite.drivestate = False


        # Update
        for car in cars:
            car.draw(SCREEN)
            car.update()
        pygame.display.update()


# NEAT setup
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)

    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    pop.run(eval_genomes, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)