import uuid
import random
import pythonGraph
from SimulationObject import SimulationObject

# ---------------------------------------------------------------
# Smoke
# Course:  CS110
# Description: This represents a single scan area
# ---------------------------------------------------------------
class ScanVis(SimulationObject):

    # The maximum amount of time the smoke can exist (in frames)
    max_duration = 60

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
    def __init__(self, simulation, x_coordinate, y_coordinate, scan_size):

        # Generates an ID
        object_id = "scan-" + str(uuid.uuid1())

        # Calls the Parent Constructor
        super().__init__(object_id, simulation, x_coordinate, y_coordinate)

        # Matches the drawn size to the scan radius
        self.radius = scan_size

        self.x_velocity = 0
        self.y_velocity = 0

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
        return "Scanned_Area"

    # ---------------------------------------------------------------
    # draw
    # Parameters: None
    # Draws the smoke cloud
    # ---------------------------------------------------------------
    def draw(self):
        if self.hit_points >= 60:  
            size_ratio = 1 / ((self.hit_points - 60)/40 + 1)
            #size_ratio = 1
            center_x = self.x_coordinate-self.radius*size_ratio
            center_y = self.y_coordinate-self.radius*size_ratio
            pythonGraph.draw_image("images/ping.png", center_x, center_y, self.radius*2*size_ratio, self.radius*2*size_ratio)
        pythonGraph.draw_circle(self.x_coordinate,self.y_coordinate,self.radius,pythonGraph.colors.ORANGE, False, 2)

    # ---------------------------------------------------------------
    # update
    # Parameters: None
    # Slowly causes the smoke to die
    # ---------------------------------------------------------------
    def update(self):
        SimulationObject.update(self)
        if not self.simulation.paused and self.hit_points > 50:
            self.hit_points -= (100 / self.max_duration)

    def get_scan_tuple(self):
        return (self.x_coordinate, self.y_coordinate, self.radius)