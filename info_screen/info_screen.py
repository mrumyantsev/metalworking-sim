import pygame


_INFO_WIDTH = 242
_INFO_HEIGHT = 62

_RPM_SIGN = '[RPM]'
_MMPM_SIGN = '[mm/min]'
_MM_SIGN = '[mm]'
_STOP_SIGN = '[stop]'
_PLUS_SIGN = '[+]'
_MINUS_SIGN = '[-]'
_NO_SIGN = ''


class InfoScreen:

    def __init__(self, surface, x, y, tool) -> None:
        self.__surface = surface
        self.__x = x
        self.__y = y
        self.__tool = tool

        self.__spindle_speed_rpm = 0
        self.__feed_rate_mmpm = 0
        self.__motion_direction = ''
        self.__is_stop_rotation = False
        self.__is_stop_motion = False

        self.__extra_sign = _NO_SIGN

    def update_conditions(self, spindle_speed_rpm, feed_rate_mmpm,
                          motion_direction, is_stop_rotation, is_stop_motion) -> None:
        self.__spindle_speed_rpm = spindle_speed_rpm
        self.__feed_rate_mmpm = feed_rate_mmpm
        self.__motion_direction = motion_direction
        self.__is_stop_rotation = is_stop_rotation
        self.__is_stop_motion = is_stop_motion

    def draw_info(self, forecolor, bgcolor) -> None:
        pygame.draw.rect(self.__surface, bgcolor,
                         (self.__x, self.__y,
                          _INFO_WIDTH, _INFO_HEIGHT))

        if (self.__is_stop_rotation):
            self.__extra_sign = _STOP_SIGN
        else:
            self.__extra_sign = _NO_SIGN

        self.__draw_text(f'S: {self.__spindle_speed_rpm:11.4f} {_RPM_SIGN: <8} {self.__extra_sign}',
                         self.__x, self.__y, forecolor)
        
        if (self.__is_stop_motion):
            self.__extra_sign = _STOP_SIGN
        else:
            self.__extra_sign = _NO_SIGN
        
        self.__draw_text(f'F: {self.__feed_rate_mmpm:11.4f} {_MMPM_SIGN} {self.__extra_sign}',
                         self.__x, self.__y + 15, forecolor)
        
        if (self.__motion_direction == 'right'):
            self.__extra_sign = _PLUS_SIGN
        elif (self.__motion_direction == 'left'):
            self.__extra_sign = _MINUS_SIGN
        else:
            self.__extra_sign = _NO_SIGN

        self.__draw_text(f'X: {self.__tool.x/10.0:11.4f} {_MM_SIGN: <8} {self.__extra_sign}',
                         self.__x, self.__y + 30, forecolor)
        
        if (self.__motion_direction == 'up'):
            self.__extra_sign = _PLUS_SIGN
        elif (self.__motion_direction == 'down'):
            self.__extra_sign = _MINUS_SIGN
        else:
            self.__extra_sign = _NO_SIGN

        self.__draw_text(f'Y: {self.__tool.y/10.0:11.4f} {_MM_SIGN: <8} {self.__extra_sign}',
                         self.__x, self.__y + 45, forecolor)

    def __draw_text(self, text, x, y, color) -> None:
        font = pygame.font.Font('./fonts/FragmentMono-Regular.ttf', 13)
        font_surface = font.render(text, True, color)
        font_place = font_surface.get_rect(x=x + 2, y=y)
        self.__surface.blit(font_surface, font_place)
