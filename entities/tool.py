import pygame
import math
import libs.sll as sll
import libs.lib as lib


class Trajectory:
    def __init__(self, display_surface: pygame.Surface) -> None:
        self.__display_surface = display_surface
        self.__points_list = sll.Sll()
    
    def add_point(self, x: float, y: float) -> None:
        new_point = (lib.pbround(x), lib.pbround(y))

        self.__points_list.add_to_tail(new_point)

    def draw(self, color: tuple) -> None:
        self.__points_list.traverse_from_head(
            self.__display_surface.set_at, color)


class Radius:
    def __init__(self, x=0.0, y=0.0,
                 r=1.0, angle=0.0):
        self.__x = x
        self.__y = y
        self.__r = r
        self.__angle = angle
        self.__circle_x = 0.0
        self.__circle_y = 0.0
        self.move()

    def move(self, direction='right',
             speed_coeff=0.0, angle_coeff=0.0):
        if direction == 'right':
            self.__x += speed_coeff
        elif direction == 'left':
            self.__x -= speed_coeff
        elif direction == 'up':
            self.__y -= speed_coeff
        elif direction == 'down':
            self.__y += speed_coeff
        
        self.__angle += angle_coeff

        self.__circle_x = self.__x + self.__r*math.sin(self.__angle*(math.pi/180.0))
        self.__circle_y = self.__y + self.__r*math.cos(self.__angle*(math.pi/180.0))
    
    @property
    def x(self) -> float:
        return self.__x
    
    @property
    def y(self) -> float:
        return self.__y

    @property
    def circle_x(self) -> float:
        return self.__circle_x
    
    @property
    def circle_y(self) -> float:
        return self.__circle_y


class Plate:
    def __init__(self, x=0.0, y=0.0, size_coeff=1.0, angle=0.0):
        self.__x = x
        self.__y = y
        self.__size_coeff = size_coeff
        self.__angle = angle
        self.__points = ()
        self.move()

    def move(self, x=0.0, y=0.0, angle=0.0):
        self.__x = x
        self.__y = y
        self.__angle = angle

        self.__points = (
            (self.__x + self.__size_coeff*100.0*math.sin(self.__angle*(math.pi/180.0)),
             self.__y + self.__size_coeff*100.0*math.cos(self.__angle*(math.pi/180.0))),
            (self.__x + self.__size_coeff*300.0*math.sin(self.__angle*(math.pi/180.0)),
             self.__y + self.__size_coeff*300.0*math.cos(self.__angle*(math.pi/180.0))),
            (self.__x + self.__size_coeff*280.0*math.sin((self.__angle + 15.0)*(math.pi/180.0)),
             self.__y + self.__size_coeff*280.0*math.cos((self.__angle + 15.0)*(math.pi/180.0))),
            (self.__x + self.__size_coeff*145.0*math.sin((self.__angle + 30.0)*(math.pi/180.0)),
             self.__y + self.__size_coeff*145.0*math.cos((self.__angle + 30.0)*(math.pi/180.0))))

    @property
    def points(self) -> tuple:
        return self.__points


class Mill:
    def __init__(self, display_surface: pygame.Surface, x=0.0,
                 y=0.0, size_coeff=1.0, angle=0.0,
                 plates_number=4):
        self.__display_surface = display_surface
        self.__x = x
        self.__y = y
        self.__angle = angle
        self.__plates_number = plates_number
        self.__segment_angle = 360.0/self.__plates_number

        plates_list = []

        for i in range(self.__plates_number):
            plate = Plate(x, y, size_coeff, i*self.__segment_angle)
            plates_list.append(plate)
        
        self.__plates = tuple(plates_list)
        self.move()

    def move(self, x=0.0, y=0.0, angle_coeff=0.0):
        self.__x = x
        self.__y = y
        self.__angle += angle_coeff

        for i in range(self.__plates_number):
            self.__plates[i].move(self.__x, self.__y, self.__angle + i*self.__segment_angle)

    def draw(self, color):
        for plate in self.__plates:
            pygame.draw.polygon(self.__display_surface, color,
                                ((plate.points[0][0], plate.points[0][1]),
                                 (plate.points[1][0], plate.points[1][1]),
                                 (plate.points[2][0], plate.points[2][1]),
                                 (plate.points[3][0], plate.points[3][1])))
