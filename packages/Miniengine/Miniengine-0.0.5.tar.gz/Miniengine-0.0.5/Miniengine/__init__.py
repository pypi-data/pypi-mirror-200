import math
import pygame
class Simulation():
    def __init__(self, width, height, tittle, collisions, dt, steps, speed):
        self.width = width
        self.height = height
        self.tittle = tittle
        self.objects = []
        self.positions_history = []
        self.dt = dt
        self.collisions = collisions
        self.steps = steps
        self.speed = round((speed*1.7)/(dt*100))
        self.gravity_objects = []
        self.collisionLayers = []
    def add_object(self, obj):
        self.objects.append(obj)
        for object in self.objects:
            if object.collisionLayer != 0:
                self.collisionLayers.append(object.collisionLayer)
            if object.gravity:
                self.gravity_objects.append(object)
    def store_positions(self):
        current_positions = []
        for obj in self.objects:
            current_positions.append([obj, obj.position])
        self.positions_history.append(current_positions)
    def run(self, fps=60, frames='all'):
        if frames == 'all': frames = len(self.positions_history)
        display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.tittle)
        frame = 0
        clock = pygame.time.Clock()
        for objects in self.positions_history[:frames]:
            display.fill('dark green')
            for object in objects:
                object[0].position = object[1]
                if object[0].circle:
                    pygame.draw.circle(display, object[0].color, object[0].position, object[0].width/2)
                else:
                    display.blit(object[0].body, (object[0].position))
            pygame.display.update()
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            frame += 1
    def calculate(self):
        y =0
        for i in range(self.steps):
            if self.collisions: 
                for i in range(len(self.objects)):
                    object1 = self.objects[i]
                    for j in range(i + 1, len(self.objects)):
                        object2 = self.objects[j]
                        if object1.collisionLayer == object2.collisionLayer:
                            if checkCollision(object1, object2):
                                Collide(object1, object2)
            for i in range(len(self.gravity_objects)):
                object1 = self.gravity_objects[i]
                for j in range(i + 1, len(self.gravity_objects)):
                    object2 = self.gravity_objects[j]
                    if object1 != object2:
                        gravitate(object1, object2)
            
            for object in self.objects:
                object.updatePosition()
                if object.dV != 0:
                    object.accelerate()
                if object.hitBorder:
                    border(object)
            if y == self.speed:
                self.store_positions()
                y = 0
            y += 1
class Object(pygame.Surface):
    def __init__(self, height, width, position, mass, speed, direction, color, simulation,circle=False, collisionLayer=0, hitBorder=False):
        self.height = height
        self.width = width
        self.gravity = False
        self.downGravity = False
        self.dt = simulation.dt
        self.position = position
        self.circle = circle
        self.mass = mass
        self.speed = speed
        self.simpleGravity = False
        self.color = color
        self.hitBorder = hitBorder
        self.collisionLayer = collisionLayer
        self.direction = direction
        self.simulation = simulation
        self.body = pygame.Surface((self.width, self.height))
        self.body.fill(color)
        self.dV = 0
    def addAcceleration(self, dV, angle):
        self.dV = dV
        self.angle = angle
    def addGravity(self, g=0, downGravity=False, simpleGravity=False, lock=False):
        if g != 0:
            self.gravity = True
        self.lock = lock
        self.g = g
        self.simpleGravity = simpleGravity
        self.downGravity = downGravity
    def updatePosition(self):
        x, y = self.position
        radians = math.radians(self.direction)
        dx = self.speed * math.cos(radians)
        dy = self.speed * math.sin(radians)
        new_x = x + dx * self.dt
        new_y = y + dy * self.dt
        self.position = (new_x, new_y)

    def accelerate(self):
        directionRad = math.radians(self.direction)

        # Calculate the object's current x and y velocity components
        speedX = self.speed * math.cos(directionRad)
        speedY = self.speed * math.sin(directionRad)

        # Calculate the x and y components of the speed_change
        DeltaVX = self.dV * math.cos(self.angle-180)
        DeltaVY = self.dV * math.sin(self.angle-180)

        # Add the speed_change components to the current speed components
        new_speedX = speedX + DeltaVX
        new_speedY = speedY + DeltaVY

        # Calculate the new speed and direction
        new_speed = math.sqrt(new_speedX ** 2 + new_speedY ** 2)
        new_direction = math.degrees(math.atan2(new_speedY, new_speedX))

        # Update the object's speed and direction
       
        self.speed = new_speed
        self.direction = new_direction
def angle_difference(angle1, angle2):
    diff = (angle1 - angle2) % 360
    return diff if diff < 180 else 360 - diff
def checkCollision(object1, object2):
    if object1.circle and object2.circle:
        if distance(object1, object2) <= object1.width/2 + object2.width/2:
                return True
        return False
    elif object1.circle == object2.circle:
        if (object1.position[0] < object2.position[0] + object2.width and
        object1.position[0] + object1.width > object2.position[0]):
        
        # Check if the rectangles are overlapping along the y-axis
            if (object1.position[1] < object2.position[1] + object2.height and object1.position[1] + object1.height > object2.position[1]):
            
            # The rectangles are overlapping
                return True

    # The rectangles are not overlapping
        return False

def border(object):
    x, y = object.position
    x += object.width/2
    y += object.height/2
    if object.circle:
        x, y = object.position
        radius = object.width // 2
        # Check collision with left or right border
        if x - radius <= 0 or x + radius >= object.simulation.width:
            object.direction = 180 - object.direction

        # Check collision with top or bottom border
        if y - radius <= 0 or y + radius >= object.simulation.height:
            object.direction = 360 - object.direction
    else:
        object_width, object_height = object.width, object.height
        if x <= object_width/2 or x + object_width/2 >= object.simulation.width:
            object.direction = 180 - object.direction
            print(object.position)
        if y <= object_width/2 or y + object_height/2 >= object.simulation.height:
            object.direction = 360 - object.direction


def gravitate(object1, object2):
    cG = 6.67430 * (10 ** -11)
    dx = object2.position[0] - object1.position[0]
    dy = object2.position[1] - object1.position[1]
    angle1 = math.atan2(dy, dx)
    angle2 = math.atan2(-dy, -dx)

    distance = math.sqrt(dx ** 2 + dy ** 2)
    if object1.simpleGravity:
        acceleration1 = object1.g
    if object2.simpleGravity:
        acceleration2 = object2.g
    else:
        acceleration1 = (object1.g/((distance**2)/100000))/(object1.mass)
        acceleration2 = (object2.g/((distance**2)/100000))/(object2.mass)
    if not object1.lock:# Update the speed and direction of both objects based on the time interval dt
        object1.accelerate(acceleration1 * object1.dt, angle1)
    if not object2.lock:
        object2.accelerate(acceleration2 * object2.dt, angle2)
    
def distance(objeto1, objeto2):
    x1, y1 = objeto1.position
    x2, y2 = objeto2.position
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx ** 2 + dy ** 2)
def Collide(object1, object2, COR=0.9):
    x1, y1 = object1.position
    x2, y2 = object2.position
    if not object1.circle:
        x1 += object1.width/2
        y1 += object1.height/2
    if not object2.circle:
        x2 += object2.width/2
        y2 += object2.height/2
    v1 = object1.speed
    v2 = object2.speed
    d1 = object1.direction
    d2 = object2.direction
    m1 = object1.mass
    m2 = object2.mass

    # Convert direction to radians
    r1 = math.radians(d1)
    r2 = math.radians(d2)

    # Calculate the normal vector (unit vector) between the two objects
    
    delta_x = x2 - x1
    delta_y = y2 - y1
    distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
    if distance == 0:
        normal_x, normal_y = 0,0
    else:
        normal_x = delta_x / distance
        normal_y = delta_y / distance

    # Calculate the relative velocity along the normal vector
    relative_velocity_x = v2 * math.cos(r2) - v1 * math.cos(r1)
    relative_velocity_y = v2 * math.sin(r2) - v1 * math.sin(r1)
    relative_velocity = relative_velocity_x * normal_x + relative_velocity_y * normal_y

    # Calculate the impulse using the COR
    impulse = 2 * relative_velocity * COR / (1/m1 + 1/m2)

    # Calculate the final velocities using the impulse
    if COR != 0:
        
        v1fx = v1 * math.cos(r1) + (impulse * normal_x) / m1
        v1fy = v1 * math.sin(r1) + (impulse * normal_y) / m1
        v2fx = v2 * math.cos(r2) - (impulse * normal_x) / m2
        v2fy = v2 * math.sin(r2) - (impulse * normal_y) / m2
    else:
        # In the case of COR = 0 (perfectly inelastic collision), objects stick together
        v1fx = (m1 * v1 * math.cos(r1) + m2 * v2 * math.cos(r2)) / (m1 + m2)
        v1fy = (m1 * v1 * math.sin(r1) + m2 * v2 * math.sin(r2)) / (m1 + m2)
        v2fx = v1fx
        v2fy = v1fy

    # Calculate the magnitudes and directions of the final velocities
    v1f = math.sqrt(v1fx ** 2 + v1fy ** 2)
    v2f = math.sqrt(v2fx ** 2 + v2fy ** 2)
    d1f = math.degrees(math.atan2(v1fy, v1fx))
    d2f = math.degrees(math.atan2(v2fy, v2fx))
    if object1.circle and object2.circle:
        dx = object2.position[0] - object1.position[0]
        dy = object2.position[1] - object1.position[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Calculate the sum of the radii of the two circles, plus one unit of distance
        radius_sum = (object1.width / 2) + (object2.width / 2)

        # Check if the circles are overlapping or touching
        if distance < radius_sum:
            # Calculate the overlap distance, plus one unit of distance
            overlap = radius_sum - distance

            # Calculate the unit vector in the direction from circle1 to circle2
            unit_vector_x = dx / distance
            unit_vector_y = dy / distance

            # Move the circles apart by half the overlap distance each, in opposite directions
            object1.position = list(object1.position)
            object2.position = list(object2.position)
            object1.position[0] -= (unit_vector_x * (overlap / 2)+0.0)
            object1.position[1] -= (unit_vector_y * (overlap / 2)+0.0)
            object2.position[0] += (unit_vector_x * (overlap / 2)+0.0)
            object2.position[1] += (unit_vector_y * (overlap / 2)+0.0)
            object1.position = tuple(object1.position)
            object2.position = tuple(object2.position)
    elif object1.circle == object2.circle:
        # Check if the rectangles are overlapping along the x-axis
        if (object1.position[0] < object2.position[0] + object2.width and
            object1.position[0] + object1.width > object2.position[0]):
            
            # Check if the rectangles are overlapping along the y-axis
            if (object1.position[1] < object2.position[1] + object2.height and
                object1.position[1] + object1.height > object2.position[1]):
                
                # Calculate the overlap distances along the x and y axes
                overlap_x = min(object1.position[0] + object1.width - object2.position[0],
                                object2.position[0] + object2.width - object1.position[0])
                overlap_y = min(object1.position[1] + object1.height - object2.position[1],
                                object2.position[1] + object2.height - object1.position[1])

                # Separate the rectangles along the axis with the least overlap
                if overlap_x < overlap_y:
                    if object1.position[0] < object2.position[0]:
                        object1.position = list(object1.position)
                        object2.position = list(object2.position)
                        object1.position[0] -= overlap_x / 2
                        object2.position[0] += overlap_x / 2
                        object1.position = tuple(object1.position)
                        object2.position = tuple(object2.position)
                    else:
                        object1.position = list(object1.position)
                        object2.position = list(object2.position)
                        object1.position[0] += overlap_x / 2
                        object2.position[0] -= overlap_x / 2
                        object1.position = tuple(object1.position)
                        object2.position = tuple(object2.position)
                else:
                    if object1.position[1] < object2.position[1]:
                        object1.position = list(object1.position)
                        object2.position = list(object2.position)
                        object1.position[1] -= overlap_y / 2
                        object2.position[1] += overlap_y / 2
                        object1.position = tuple(object1.position)
                        object2.position = tuple(object2.position)
                    else:
                        object1.position = list(object1.position)
                        object2.position = list(object2.position)
                        object1.position[1] += overlap_y / 2
                        object2.position[1] -= overlap_y / 2
                        object1.position = tuple(object1.position)
                        object2.position = tuple(object2.position)

    # Update the velocities and directions of the objects
    object1.speed = v1f
    object1.direction = d1f
    object2.speed = v2f
    object2.direction = d2f
    return object1, object2


