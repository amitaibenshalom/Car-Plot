
import pygame
from pygame.locals import *
from consts import USER_GRAPH_COLOR, USER_GRAPH_MAX_POINTS

class User:
    def __init__(self, screen, x_range, y_range, sub_surface, max_points=USER_GRAPH_MAX_POINTS, color=USER_GRAPH_COLOR, graph_line_width=3, step=[1, 10]):
        """
        Initialize the user with a position, a list of points, and a step size.
        :param screen: The screen to draw on.
        :param x_range: The range of x values (min_x, max_x) (to normalize the graph).
        :param y_range: The range of y values (min_y, max_y) (to normalize the graph).
        :param sub_surface: (pos_x, pos_y, width, height) of the sub-surface (the area where the graph will be drawn).
        :param max_points: The maximum number of points to consider for the score calculation.
        :param color: The color of the graph.
        """
        self.screen = screen  # The screen to draw on
        self.x_range = x_range  # Range of x values (min_x, max_x) (to normalize the graph)
        self.y_range = y_range  # Range of y values (min_y, max_y) (to normalize the graph)
        self.sub_surface = sub_surface  # (pos_x, pos_y, width, height) of the sub-surface
        self.max_points = max_points  # Maximum number of points to consider for the score calculation
        self.color = color  # Color of the graph
        self.graph_line_width = graph_line_width
        self.step = step  # Step size for x and y movements

        self.score = 0  # Initialize score to 0
        self.position = [self.x_range[0], self.y_range[1]]  # Initial position of the user
        self.user_points = []  # List to store user points

        _, _, width, height = self.sub_surface
        self.scale = [width / (self.x_range[1] - self.x_range[0]), height / (self.y_range[1] - self.y_range[0])]  # Scale factors for x and y axes

    def reset(self):
        """
        Reset the user position and points.
        """
        self.position[0] = self.x_range[0]  # Reset x position to min_x
        self.user_points.clear()  # Clear user points
    
    def move_x(self):
        """
        Move the user in the x direction.
        :return: True if the user has wrapped around the x-axis, False otherwise.
        """
        self.position[0] += self.step[0]

        if self.position[0] > self.x_range[1]:
            self.reset()  # Reset the user position if it exceeds max_x (wrap around)
            return True
        
        return False

    def move_y(self, direction_up=True):
        self.position[1] += -self.step[1] if direction_up else self.step[1]

        if self.position[1] > self.y_range[1]:
            self.position[1] = self.y_range[1]

        elif self.position[1] < self.y_range[0]:
            self.position[1] = self.y_range[0]
    
    def set_y(self, y):
        self.position[1] = y

    def add_point(self):
        self.user_points.append(self.position.copy())

    def calc_score(self, graph, max_error=100000):
        """
        Calculate the score based on the mean squared error (MSE) between the user points and the graph function.
        The score is calculated as:
        score = 100 * (1 - mse / max_error)
        where mse is the mean squared error between the user points and the graph function.
        :param graph: The graph object.
        :param max_error: The maximum error allowed, used to normalize the score.
                            If the MSE is greater than max_error, the score will be 0.
        :return: The score as a percentage (0 to 100).
        """
        if len(self.user_points) < 2:
            return 0
        errors = [(y - graph.function(x))**2 for x, y in self.user_points[-self.max_points:]]  # Calculate the squared errors for the last max_points points
        mse = sum(errors) / len(errors)
        self.score = round(max(0, 100 * (1 - mse / max_error)))
        return self.score
    
    def show_score(self):
        """
        Display the score on the screen.
        """
        font = pygame.font.Font(None, 36)  # Create a font object
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

    def draw_graph(self):
        """
        Draw the user's graph on the screen.
        """
        if len(self.user_points) < 2:
            return

        pos_x, pos_y, width, height = self.sub_surface  
        graph_surface = pygame.Surface((width, height), pygame.SRCALPHA)  # Create a new surface with size of the sub-surface
        graph_surface.fill((0, 0, 0, 0))  # Fill with transparent color

        x_scale = width / (self.x_range[1] - self.x_range[0])  # Scale factor for x-axis
        y_scale = height / (self.y_range[1] - self.y_range[0])  # Scale factor for y-axis

        screen_points = [(int((x - self.x_range[0]) * x_scale),
                          int((y - self.y_range[0]) * y_scale)) for x, y in self.user_points]  # Convert to screen coordinates
        pygame.draw.lines(graph_surface, self.color, False, screen_points, self.graph_line_width)  # Draw the line on the graph surface

        self.screen.blit(graph_surface, (pos_x, pos_y))  # Blit the graph surface onto the main screen

    def draw_user_lines(self):
        """
        Draw the lines from the user position to the edges of the graph.
        """
        pos_x, pos_y, width, height = self.sub_surface

        pygame.draw.circle(self.screen, self.color, (pos_x + int((self.position[0] - self.x_range[0]) * self.scale[0]),
                                                pos_y + int((self.position[1] - self.y_range[0]) * self.scale[1])), 5)
        
        # pygame.draw.circle(self.screen, self.color, (pos_x,
        #                                         pos_y + int((self.position[1] - self.y_range[0]) * self.scale[1])), 3)
        
        pygame.draw.line(self.screen, self.color, (pos_x + int((self.position[0] - self.x_range[0]) * self.scale[0]),
                                                pos_y + int((self.position[1] - self.y_range[0]) * self.scale[1])),
                                                (pos_x, pos_y + int((self.position[1] - self.y_range[0]) * self.scale[1])), 2)
        pygame.draw.line(self.screen, self.color, (pos_x + int((self.position[0] - self.x_range[0]) * self.scale[0]),
                                                pos_y + int((self.position[1] - self.y_range[0]) * self.scale[1])),
                                                (pos_x + int((self.position[0] - self.x_range[0]) * self.scale[0]),
                                                pos_y + height), 2)
        
        if len(self.user_points) >= self.max_points:
            pygame.draw.line(self.screen, (128, 128, 128), (pos_x + int((self.user_points[-self.max_points][0] - self.x_range[0]) * self.scale[0]),
                                                    pos_y + height),
                                                    (pos_x + int((self.position[0] - self.x_range[0]) * self.scale[0]),
                                                    pos_y + height), 10)
            
        elif len(self.user_points) > 0:
            pygame.draw.line(self.screen, (128, 128, 128), (pos_x + int((self.user_points[0][0] - self.x_range[0]) * self.scale[0]),
                                                    pos_y + height),
                                                    (pos_x + int((self.position[0] - self.x_range[0]) * self.scale[0]),
                                                    pos_y + height), 10)