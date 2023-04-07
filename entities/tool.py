import pygame
import math
import libs.sll as sll
import libs.lib as lib


class Trajectory:
    def __init__(self, display_surface: pygame.Surface) -> None:
        self.__display_surface = display_surface
        self.__trajectory_path = sll.Sll()
    
    def add_point(self, x: float, y: float) -> None:
        new_point = (lib.pbround(x), lib.pbround(y))

        self.__trajectory_path.add_to_tail(new_point)

    def draw(self, color: tuple) -> None:
        self.__trajectory_path.traverse_from_head(
            self.__display_surface.set_at, color)


class Axis:
    def __init__(self, direction='right', center_x=0.0,
                 center_y=0.0, angle=0.0, eccentricity_radius=1.0):
        self.direction = direction
        self.center_x = center_x
        self.center_y = center_y
        self.angle = angle
        # 0.01 mm = 1 pixel (default scale).
        self.eccentricity_radius = eccentricity_radius
        self.point_x = 0.0
        self.point_y = 0.0
        self.move()

    def move(self, direction='right',
             angle_coeff=0.0, speed_coeff=0.0):
        self.angle += angle_coeff

        if direction == 'right':
            self.center_x += speed_coeff
        elif direction == 'left':
            self.center_x -= speed_coeff
        elif direction == 'up':
            self.center_y -= speed_coeff
        elif direction == 'down':
            self.center_y += speed_coeff

        self.point_x = self.center_x + self.eccentricity_radius*math.sin(self.angle*(math.pi/180.0))
        self.point_y = self.center_y + self.eccentricity_radius*math.cos(self.angle*(math.pi/180.0))


class Plate:
    def __init__(self, size_coeff=1.0, start_x=0.0, start_y=0.0, angle=0.0):
        self.size_coeff = size_coeff
        self.start_x = start_x
        self.start_y = start_y
        self.angle = angle
        self.points = ()
        self.move()

    def move(self):
        self.points = ((self.start_x + self.size_coeff*100.0*math.sin(self.angle*(math.pi/180.0)),
                        self.start_y + self.size_coeff*100.0*math.cos(self.angle*(math.pi/180.0))),
                       (self.start_x + self.size_coeff*300.0*math.sin(self.angle*(math.pi/180.0)),
                        self.start_y + self.size_coeff*300.0*math.cos(self.angle*(math.pi/180.0))),
                       (self.start_x + self.size_coeff*280.0*math.sin((self.angle + 15.0)*(math.pi/180.0)),
                        self.start_y + self.size_coeff*280.0*math.cos((self.angle + 15.0)*(math.pi/180.0))),
                       (self.start_x + self.size_coeff*145.0*math.sin((self.angle + 30.0)*(math.pi/180.0)),
                        self.start_y + self.size_coeff*145.0*math.cos((self.angle + 30.0)*(math.pi/180.0))))


class Mill:
    def __init__(self, display_surface, size_coeff=1.0,
                 center_x=0.0, center_y=0.0, angle=0.0,
                 plates_number=4):
        self.size_coeff = size_coeff
        self.display_surface = display_surface
        self.center_x = center_x
        self.center_y = center_y
        self.angle = angle
        self.plates_number = plates_number
        self.segment = 360.0 / self.plates_number
        self.plates = []

        for i in range(self.plates_number):
            plate = Plate(size_coeff=self.size_coeff, start_x=self.center_x,
                          start_y=self.center_y, angle=i * self.segment)
            self.plates.append(plate)

    def move(self, axis, angle_coeff=0.0):
        self.angle += angle_coeff
        self.center_x = axis.point_x
        self.center_y = axis.point_y

        for i in range(self.plates_number):
            self.plates[i].start_x = self.center_x
            self.plates[i].start_y = self.center_y
            self.plates[i].angle = self.angle + i * self.segment
            self.plates[i].move()

    def draw(self, color):
        for plate in self.plates:
            pygame.draw.polygon(self.display_surface, color,
                                ((plate.points[0][0], plate.points[0][1]),
                                 (plate.points[1][0], plate.points[1][1]),
                                 (plate.points[2][0], plate.points[2][1]),
                                 (plate.points[3][0], plate.points[3][1])))
