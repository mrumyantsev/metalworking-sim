import pygame
import math


class _Plate:
    def __init__(self, x=0.0, y=0.0, size_coeff=1.0, angle=0.0):
        self.__x = x
        self.__y = y
        self.__size_coeff = size_coeff
        self.__angle = angle
        self.__points = ()
        self.move(x, y, angle)

    def move(self, x, y, angle):
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
            plate = _Plate(x, y, size_coeff, i*self.__segment_angle)
            plates_list.append(plate)
        
        self.__plates = tuple(plates_list)
        self.move(x, y, 0.0)

    def move(self, x, y, angle_coeff):
        self.__x = x
        self.__y = y
        self.__angle += angle_coeff

        for i in range(self.__plates_number):
            self.__plates[i].move(self.__x, self.__y, self.__angle + i*self.__segment_angle)

    def draw(self, color):
        for plate in self.__plates:
            pygame.draw.polygon(self.__display_surface, color, plate.points)
