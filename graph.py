"""
This class represents a graph (function) that can be drawn on the screen.
"""

import pygame
from pygame.locals import *
import numpy as np
from consts import *
from math import pi, sin, cos, tan, atan2, sqrt


class Graph:
    """
    This class represents a graph (function) that can be drawn on the screen.
    """

    def __init__(self, function, color=GRAPH_COLOR, width=GRAPH_WIDTH):
        """
        Initialize the graph with a function, color and width.
        :param function: The function to be plotted.
        :param color: The color of the graph.
        :param width: The width of the graph.
        """
        self.function = function
        self.color = color
        self.width = width

    def draw(self, screen, x_range, y_range, sub_surface, step=0.1):
        """
        Draw the graph on the screen.
        :param screen: The screen to draw on.
        :param x_range: The range of x values (x_min, x_max).
        :param y_range: The range of y values (y_min, y_max).
        :param sub_surface: (pos_x, pos_y, width, height) of the sub-surface
        :param step: The step size for the x values.
        """

        # Create a sub-surface for the graph
        pos_x, pos_y, width, height = sub_surface
        graph_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        graph_surface.fill((0, 0, 0, 0))

        # Calculate the scale factors
        x_scale = width / (x_range[1] - x_range[0])
        y_scale = height / (y_range[1] - y_range[0])

        # Draw the graph
        points = []
        for x in np.arange(x_range[0], x_range[1], step):
            y = self.function(x)
            if y_range[0] <= y <= y_range[1]:
                points.append((x, y))
        if len(points) < 2:
            return
        # Convert points to screen coordinates
        screen_points = [(int((x - x_range[0]) * x_scale),
                          int((y - y_range[0]) * y_scale)) for x, y in points]
        # Draw the graph
        pygame.draw.lines(graph_surface, self.color, False, screen_points, self.width)
        # Draw the graph surface on the main screen
        screen.blit(graph_surface, (pos_x, pos_y))