import uuid
import random
import pythonGraph
from SimulationObject import SimulationObject

# ---------------------------------------------------------------
# Smoke
# Course:  CS110
# Description: This represents a single smoke cloud
# ---------------------------------------------------------------
class Smoke(SimulationObject):

    # The maximum amount of time the smoke can exist (in frames)
    max_duration = 5400

    # Radius
    radius = 50

    # ---------------------------------------------------------------
    # __init__
    # Parameters:
    #     - simulation: A reference to the current simulation
    #     - x_coordinate:  The smoke cloud's center x coordinate
    #     - y_coordinate:  The smoke cloud's center y coordinate
    # Creates a smoke object
    # ---------------------------------------------------------------
    def __init__(self, simulation, x_coordinate, y_coordinate):

        # Generates an ID
        object_id = "smoke-" + str(uuid.uuid1())

        # Calls the Parent Constructor
        super().__init__(object_id, simulation, x_coordinate, y_coordinate)

        # Creates a random size for the smoke cloud
        self.radius = random.randint(20, 50)

        self.x_velocity = random.random() * 0.005 - 0.0025
        self.y_velocity = random.random() * 0.005 - 0.0025

        # Makes it Not Scannable
        self.scannable = False

        # Makes it Not Collidable
        self.colliable = False
        self.missile_vulnerable = False

    # ---------------------------------------------------------------
    # get_description
    # Parameters: None
    # Returns the description of this object
    # ---------------------------------------------------------------
    def get_description(self):
        return "Smoke"

    # ---------------------------------------------------------------
    # draw
    # Parameters: None
    # Draws the smoke cloud
    # ---------------------------------------------------------------
    def draw(self):
        center_x = self.x_coordinate-self.radius/2
        center_y = self.y_coordinate-self.radius/2
        pythonGraph.draw_image("images/smoke.png", center_x, center_y, self.radius, self.radius)

    # ---------------------------------------------------------------
    # update
    # Parameters: None
    # Slowly causes the smoke to die
    # ---------------------------------------------------------------
    def update(self):
        SimulationObject.update(self)
        if not self.simulation.paused:
            self.hit_points -= (100 / self.max_duration)
