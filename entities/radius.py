import math


class Radius:
    def __init__(self, x=0.0, y=0.0,
                 direction='right', r=1.0, angle=0.0):
        self.__x = x
        self.__y = y
        self.__r = r
        self.__angle = angle
        self.__circle_x = 0.0
        self.__circle_y = 0.0
        self.move(direction, 0.0, 0.0)

    def move(self, direction, speed_coeff, angle_coeff):
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
