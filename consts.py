"""
This file contains constants for the exhibit
"""
import os

# screen dimensions
VIEWPORT = (800, 600)  # default viewport size
FULLSCREEN = True  # if True, the game will run in fullscreen mode (ignoring the viewport size)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# graph
GRAPH_COLOR = RED  # color of the graph
GRAPH_WIDTH = 3  # width of the graph

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")  # directory where the assets are stored

# dict of picture names, their sizes and position to load on screen
PICTURES_TO_LOAD = {
    "background3.png": (("full", "full"), (0, 0)),
    "grid.png": (("70%", "70%"),("25%", "25%")),
}

