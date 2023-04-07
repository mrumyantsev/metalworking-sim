import pygame
import entities.tool as tool_module
import math
import config.config as config


class Engine:
    def __init__(self, cfg) -> None:
        self.__cfg = cfg

        self.__resolution_width = self.__cfg['r_resolutionWidth']
        self.__resolution_height = self.__cfg['r_resolutionHeight']

        self.__fps = cfg['r_fps']

        self.__background_color = config.get_color_value(
            cfg['ent_backgroundColor'])
        self.__steel_color = config.get_color_value(
            cfg['ent_steelColor'])
        self.__trajectory_color = config.get_color_value(
            cfg['ent_trajectoryColor'])
        self.__mill_plate_color = config.get_color_value(
            cfg['ent_millPlateColor'])

        pygame.init()
        pygame.display.set_caption('Metalworking: The Game')
        pygame.mouse.set_visible(False)

        self.__display_surface = pygame.display.set_mode(
            (self.__resolution_width, self.__resolution_height))
        self.__clock = pygame.time.Clock()

        self.__is_game_over = False
        self.__is_stage_over = False

        self.__tool_center_x = -150
        self.__tool_center_y = self.__resolution_height/2
        self.__plates_number = 4
        self.__eccentricity_radius = 1.0

        self.__tool_diameter_mm = 2
        self.__rotation_rpm = 20
        self.__speed_mmpm = 30
        self.__is_rotate_clockwise = True
        self.__is_stop_rotation = False
        self.__is_stop_motion = False
        self.__motion_direction = 'right'
        self.__set_moving_values()
    
    def __set_moving_values(self) -> None:
        if self.__is_stop_rotation:
            self.__angle_coeff = 0.0
        else:
            self.__angle_coeff = self.__rotation_rpm*math.pi*10.0/6.0/self.__fps

        if self.__is_rotate_clockwise:
            self.__angle_coeff = -self.__angle_coeff

        if self.__is_stop_motion:
            self.__speed_coeff = 0.0
        else:
            self.__speed_coeff = self.__speed_mmpm/0.6/self.__fps

    # General cycle.
    def run(self) -> None:
        while not self.__is_game_over:
            self.__display_surface.fill(self.__steel_color)

            trajectory = tool_module.Trajectory(self.__display_surface)
            axis = tool_module.Axis(
                self.__motion_direction, self.__tool_center_x, self.__tool_center_y,
                0.0, self.__eccentricity_radius)
            mill = tool_module.Mill(
                self.__display_surface, self.__tool_diameter_mm/6.0, axis.center_x,
                axis.center_y, 0.0, self.__plates_number)

            self.__run_stage(axis, mill, trajectory)

        pygame.quit()

    # Stage sub-cycle.
    def __run_stage(self, axis, mill, trajectory) -> None:
        self.__is_stage_over = False

        while not self.__is_stage_over:
            self.__handle_control_keys()
            self.__set_moving_values()

            axis.move(
                self.__motion_direction, self.__angle_coeff, self.__speed_coeff)

            mill.draw(self.__background_color)
            mill.move(axis, self.__angle_coeff)
            mill.draw(self.__mill_plate_color)
            
            trajectory.add_point(axis.point_x, axis.point_y)
            trajectory.draw(self.__trajectory_color)

            self.__clock.tick(self.__fps)
            pygame.display.flip()

            self.__handle_moving_off_screen(axis)

    def __handle_control_keys(self) -> None:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                self.__react_keydown(event)
    
    def __react_keydown(self, event) -> None:
        multiplier = 1.5

        if event.key == pygame.K_ESCAPE:
            self.__is_stage_over = True
            self.__is_game_over = True
        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            self.__is_stage_over = True
        if event.key == pygame.K_KP_PLUS:
            self.__rotation_rpm *= multiplier
        if event.key == pygame.K_KP_MINUS:
            self.__rotation_rpm /= multiplier
        if event.key == pygame.K_KP_MULTIPLY:
            self.__speed_mmpm *= multiplier
        if event.key == pygame.K_KP_DIVIDE:
            self.__speed_mmpm /= multiplier
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
    
    def __handle_moving_off_screen(self, tool) -> None:
        extra_distance = 150

        if tool.center_x > self.__resolution_width + extra_distance:
            self.__tool_center_x = -extra_distance
            self.__tool_center_y = tool.center_y
            self.__motion_direction = 'right'
            self.__is_stage_over = True
        if tool.center_x < -extra_distance:
            self.__tool_center_x = self.__resolution_width + extra_distance
            self.__tool_center_y = tool.center_y
            self.__motion_direction = 'left'
            self.__is_stage_over = True
        if tool.center_y > self.__resolution_height + extra_distance:
            self.__tool_center_x = tool.center_x
            self.__tool_center_y = -extra_distance
            self.__motion_direction = 'down'
            self.__is_stage_over = True
        if tool.center_y < -extra_distance:
            self.__tool_center_x = tool.center_x
            self.__tool_center_y = self.__resolution_height + extra_distance
            self.__motion_direction = 'up'
            self.__is_stage_over = True
