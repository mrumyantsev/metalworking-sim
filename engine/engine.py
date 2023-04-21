from info_screen.info_screen import InfoScreen
from lib import lib
import pygame
import math
from trajectory import trajectory as trajectory_module
from radius import radius as radius_module
from mill import mill as mill_module
from info_screen import info_screen


_SPEED_MULTIPLIER = 2.0
_EXTRA_DISTANCE = 150
_VALUE_LIMIT = 99999.9999


class Engine:

    def __init__(self, cfg) -> None:
        self.__cfg = cfg

        self.__resolution_width = 0
        self.__resolution_height = 0

        self.__choose_resolution()

        self.__fps = cfg['r_fps']

        self.__background_color = lib.get_color_value(
            cfg['r_backgroundColor'])
        self.__steel_color = lib.get_color_value(
            cfg['r_steelColor'])
        self.__trajectory_color = lib.get_color_value(
            cfg['r_trajectoryColor'])
        self.__mill_plate_color = lib.get_color_value(
            cfg['r_millPlateColor'])

        pygame.init()
        pygame.display.set_caption('Metalworking: The Game')
        pygame.mouse.set_visible(False)

        self.__display_surface = pygame.display.set_mode(
            (self.__resolution_width, self.__resolution_height))
        self.__clock = pygame.time.Clock()

        self.__mill_diameter_mm = cfg['ent_millDiameterMm']
        self.__mill_flutes_number = cfg['ent_millFlutesNumber']
        self.__mill_radial_runout_mm = cfg['ent_millRadialRunoutMm']
        self.__spindle_speed_rpm = cfg['ent_spindleSpeedRpm']
        self.__feed_rate_mmpm = cfg['ent_feedRateMmPerMin']

        self.__spindle_x = -_EXTRA_DISTANCE
        self.__spindle_y = self.__resolution_height/2
        self.__is_rotate_clockwise = True
        self.__is_stop_rotation = False
        self.__is_stop_motion = False
        self.__motion_direction = 'right'

        self.__is_game_over = False
        self.__is_stage_over = False

        self.__set_moving_values()

    def __choose_resolution(self) -> None:
        if self.__cfg['r_fullscreenMode']:
            self.__resolution_width = self.__cfg['r_fullscreenResolutionWidth']
            self.__resolution_height = self.__cfg['r_fullscreenResolutionHeight']
        else:
            self.__resolution_width = self.__cfg['r_windowResolutionWidth']
            self.__resolution_height = self.__cfg['r_windowResolutionHeight']
    
    def __set_moving_values(self) -> None:
        if self.__is_stop_rotation:
            self.__angle_coeff = 0.0
        else:
            self.__angle_coeff = self.__spindle_speed_rpm*math.pi*10.0/6.0/self.__fps

        if self.__is_rotate_clockwise:
            self.__angle_coeff = -self.__angle_coeff

        if self.__is_stop_motion:
            self.__speed_coeff = 0.0
        else:
            self.__speed_coeff = self.__feed_rate_mmpm/0.6/self.__fps
        
        if (self.__spindle_speed_rpm > _VALUE_LIMIT):
            self.__spindle_speed_rpm = _VALUE_LIMIT
        
        if (self.__feed_rate_mmpm > _VALUE_LIMIT):
            self.__feed_rate_mmpm = _VALUE_LIMIT

    # General cycle.
    def run(self) -> None:
        while not self.__is_game_over:
            self.__display_surface.fill(self.__steel_color)

            trajectory = trajectory_module.Trajectory(self.__display_surface)
            radius = radius_module.Radius(self.__spindle_x, self.__spindle_y,
                                          self.__motion_direction, self.__mill_radial_runout_mm*100.0,
                                          0.0)
            mill = mill_module.Mill(self.__display_surface, radius.circle_x,
                                    radius.circle_y, self.__mill_diameter_mm/6.0,
                                    0.0, self.__mill_flutes_number)
            info = info_screen.InfoScreen(self.__display_surface, 2, 2, radius)

            self.__run_stage(trajectory, radius, mill, info)

        pygame.quit()

    # Stage sub-cycle.
    def __run_stage(self, trajectory, radius, mill, info) -> None:
        self.__is_stage_over = False

        while not self.__is_stage_over:
            self.__handle_control_keys()
            self.__handle_moving_off_screen(radius)
            self.__set_moving_values()

            radius.move(self.__motion_direction, self.__speed_coeff,
                        self.__angle_coeff)
            
            mill.draw(self.__background_color)
            mill.move(radius.circle_x, radius.circle_y, self.__angle_coeff)
            mill.draw(self.__mill_plate_color)
            
            trajectory.add_point(radius.circle_x, radius.circle_y)
            trajectory.draw(self.__trajectory_color)

            info.update_conditions(self.__spindle_speed_rpm, self.__feed_rate_mmpm,
                                   self.__motion_direction, self.__is_stop_rotation,
                                   self.__is_stop_motion)
            info.draw_info(self.__mill_plate_color, self.__background_color)

            self.__clock.tick(self.__fps)
            pygame.display.flip()

    def __handle_control_keys(self) -> None:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.__react_keydown(event)
    
    def __react_keydown(self, event) -> None:
        if event.key == pygame.K_ESCAPE:
            self.__is_stage_over = True
            self.__is_game_over = True
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            self.__is_stage_over = True
        if event.key == pygame.K_KP_PLUS:
            self.__spindle_speed_rpm *= _SPEED_MULTIPLIER
        if event.key == pygame.K_KP_MINUS:
            self.__spindle_speed_rpm /= _SPEED_MULTIPLIER
        if event.key == pygame.K_KP_MULTIPLY:
            self.__feed_rate_mmpm *= _SPEED_MULTIPLIER
        if event.key == pygame.K_KP_DIVIDE:
            self.__feed_rate_mmpm /= _SPEED_MULTIPLIER
        if event.key == pygame.K_LALT or event.key == pygame.K_RALT:
            self.__is_rotate_clockwise = not self.__is_rotate_clockwise
        if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
            self.__is_stop_rotation = not self.__is_stop_rotation
        if event.key == pygame.K_SPACE:
            self.__is_stop_motion = not self.__is_stop_motion
        if event.key == pygame.K_LEFT:
            self.__motion_direction = 'left'
        if event.key == pygame.K_RIGHT:
            self.__motion_direction = 'right'
        if event.key == pygame.K_UP:
            self.__motion_direction = 'up'
        if event.key == pygame.K_DOWN:
            self.__motion_direction = 'down'
    
    def __handle_moving_off_screen(self, item) -> None:
        if item.x > self.__resolution_width + _EXTRA_DISTANCE:
            self.__spindle_x = -_EXTRA_DISTANCE
            self.__spindle_y = item.y
            self.__motion_direction = 'right'
            self.__is_stage_over = True
        elif item.x < -_EXTRA_DISTANCE:
            self.__spindle_x = self.__resolution_width + _EXTRA_DISTANCE
            self.__spindle_y = item.y
            self.__motion_direction = 'left'
            self.__is_stage_over = True
        elif item.y > self.__resolution_height + _EXTRA_DISTANCE:
            self.__spindle_x = item.x
            self.__spindle_y = -_EXTRA_DISTANCE
            self.__motion_direction = 'down'
            self.__is_stage_over = True
        elif item.y < -_EXTRA_DISTANCE:
            self.__spindle_x = item.x
            self.__spindle_y = self.__resolution_height + _EXTRA_DISTANCE
            self.__motion_direction = 'up'
            self.__is_stage_over = True
