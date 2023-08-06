import pygame
import time
import sys
from MiniEngine import Window, Object, Colide
# Create the simulation engine
class Renderer:
    def __init__(self, window, objects, dt=1/60, lenght=2, speed = 1, gravity=False):
        self.positions_history = []
        self.gravity = gravity
        self.lenght = lenght
        self.window = window
        self.speed = speed
        self.objects = objects
        self.dt = dt
        self.speed = round((speed*1.7)/(dt*100))

    def bake(self, cor=1):
        steps = int(self.lenght / self.dt)
        y = 1
        for i in range(steps):
            x = 0
            for object in self.objects:
                for obje in self.objects:
                    if object.checkColision(obje):
                        Colide(object, obje, cor)
                object.border()
                if self.gravity:
                    object.updatePosition(self.dt)
                else:
                    object.updatePosition(self.dt)
                x += 1
            if y == self.speed:
                print(i)
                self.store_positions()
                y = 0
            y += 1
    def store_positions(self):
        current_positions = []
        for obj in self.objects:
            current_positions.append([obj, obj.position])
        self.positions_history.append(current_positions)

def run(renderer, fps=60, frames='all'):
    if frames == 'all': frames = len(renderer.positions_history)
    yt = time.time()
    display = pygame.display.set_mode((renderer.window.width, renderer.window.height))
    pygame.display.set_caption(renderer.window.tittle)
    frame = 0
    clock = pygame.time.Clock()
    for objects in renderer.positions_history[:frames]:
        display.fill((0, 0, 0))
        for object in objects:
            object[0].position = object[1]
            display.blit(object[0].body, object[0].position)
        pygame.display.update()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        frame += 1
    print(time.time() - yt)
  