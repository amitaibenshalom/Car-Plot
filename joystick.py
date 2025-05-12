"""
Filename: joystick.py
Purpose: Joystick class for the car plotter exhibit.
"""

import pygame
from pygame.locals import *
from consts import JOYSTICK_DEAD_ZONE, JOYSTICK_MAX_VALUE, JOYSTICK_MIN_VALUE

class Joystick:
    def __init__(self, joystick_index=0, logger=None):
        """
        Initialize the joystick with the given index.
        :param joystick_index: The index of the joystick to use.
        """
        self.joystick_index = joystick_index
        self.logger = logger
        self.joystick = None
        self.value = 0
        self.reconnect_waiting = False

        # Try initial connect
        joystick = self.try_connect()
        if not joystick:
            print("No joystick connected.")
            print("Trying to reconnect...")
            self.reconnect_waiting = True

    def try_connect(self):
        """
        Try to connect to the joystick.
        :return: The joystick object if found, None otherwise.
        """
        pygame.joystick.quit()
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            js = pygame.joystick.Joystick(self.joystick_index)
            js.init()
            print("Joystick found.")
            self.joystick = js
            return js
        
        self.joystick = None
        return None