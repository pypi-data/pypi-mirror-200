import pygame
import math


class Window():
    def __init__(self, width, height, tittle):
        self.width = width
        self.height = height
        self.tittle = tittle
        self.objects = []
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption(tittle)
    def add_object(self, obj):
        self.objects.append(obj)
    def draw(self, object):
        self.window.blit(object.body, object.position)

    
class Object(pygame.Surface):
    def __init__(self, height, width, position, mass, speed, direction, color, window, gravity=False):
        self.height = height
        self.width = width
        self.position = position
        self.mass = mass
        self.speed = speed
        self.direction = direction
        self.window = window
        self.gravity = gravity
        self.body = pygame.Surface((self.width, self.height))
        self.body.fill(color)
    def updatePosition(self, dt, gravity=None):
        x, y = self.position
        self.dt = dt
        radians = math.radians(self.direction)
        dx = self.speed * math.cos(radians)
        dy = self.speed * math.sin(radians)
        g = 9.8  # acceleration due to gravity in m/s²
        if (self.gravity and gravity != False) or gravity==True:
            direction_rad = math.radians(self.direction)

            current_speed_x = self.speed * math.cos(direction_rad)
            current_speed_y = self.speed * math.sin(direction_rad)

            # Add the specified speed to the y-axis
            new_speed_y = current_speed_y + 9.8 * dt

            # Calculate the new speed and direction
            new_speed = math.sqrt(current_speed_x ** 2 + new_speed_y ** 2)
            new_direction = math.degrees(math.atan2(new_speed_y, current_speed_x))

            # Update the object's speed and direction
            self.speed = new_speed
            self.direction = new_direction
        new_x = x + dx * dt
        new_y = y + dy * dt
        self.position = (new_x, new_y)
    def checkColision(self, object):
        if self.position[0] + self.width > object.position[0] and self.position[0] < object.position[0] + object.width:
            if self.position[1] + self.height > object.position[1] and self.position[1] < object.position[1] + object.height:
                return True
            else:
                return False
        else:
            return False
    def border(self):
        x, y = self.position
        if x <= 0 or x >= self.window.width:
            self.direction = 180 - self.direction
        if y <= 0 or y >= self.window.height:
            self.direction = 360 - self.direction
    def accelerate(self, dV, angle):
        directionRad = math.radians(self.direction)

        # Calculate the object's current x and y velocity components
        speedX = self.speed * math.cos(directionRad)
        speedY = self.speed * math.sin(directionRad)

        # Calculate the x and y components of the speed_change
        DeltaVX = dV * math.cos(angle)
        DeltaVY = dV * math.sin(angle)

        # Add the speed_change components to the current speed components
        new_speedX = speedX + DeltaVX
        new_speedY = speedY + DeltaVY

        # Calculate the new speed and direction
        new_speed = math.sqrt(new_speedX ** 2 + new_speedY ** 2)
        new_direction = math.degrees(math.atan2(new_speedY, new_speedX))

        # Update the object's speed and direction
        self.speed = new_speed
        self.direction = new_direction

    def gravitate(self, object2, lock=False, dt=1/60, g=0, distance = False):
        cG = 6.67430 * (10 ** -11)
        dx = object2.position[0] - self.position[0]
        dy = object2.position[1] - self.position[1]
        angle1 = math.atan2(dy, dx)
        angle2 = math.atan2(-dy, -dx)
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if g == 0:
            # Calculate the gravitational force
            force = cG * self.mass * object2.mass / (distance ** 2)

            # Calculate the acceleration due to gravity for both objects
            acceleration1 = (force / self.mass)*10000000000000
            acceleration2 = (force / object2.mass)*10000000000000

            # Determine the direction of the gravitational force for each object
        elif distance == True:
            acceleration1 = g/((distance**2)/10000)
            acceleration2 = g/((distance**2)/10000)
        else:
            # If g is specified, use it as the acceleration due to gravity
            acceleration1 = g
            acceleration2 = g
        # Update the speed and direction of both objects based on the time interval dt
        self.accelerate(acceleration1 * dt, angle1)
        if lock == False:
            object2.accelerate(acceleration2 * dt, angle2)
        
def distance(objeto1, objeto2):
    x1, y1 = objeto1.position
    x2, y2 = objeto2.position
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx ** 2 + dy ** 2)
def Colide(object1, object2, COR=1):
    x1, y1 = object1.position
    x2, y2 = object2.position
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

    # Update the velocities and directions of the objects
    object1.speed = v1f
    object1.direction = d1f
    object2.speed = v2f
    object2.direction = d2f
    return object1, object2