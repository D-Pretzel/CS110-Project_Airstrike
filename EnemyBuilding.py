import uuid
import random
import pythonGraph
from SimulationObject import SimulationObject
from utilities import random_neutral
from Missile import Missile

# ---------------------------------------------------------------
# SAM Site
# Course:  CS110
# Description: This represents a single building
# ---------------------------------------------------------------

class EnemyBuilding(SimulationObject):

    populace = 500

    # ---------------------------------------------------------------
    # __init__
    # Parameters:
    #     - simulation: A reference to the current simulation
    #     - x_coordinate:  The building center x coordinate
    #     - y_coordinate:  The building center y coordinate
    # Creates a object
    # ---------------------------------------------------------------
    def __init__(self, simulation, object_id, x_loc, y_loc): #="", x_coord=random.randint(0, simulation.width), y=random.randint(0, simulation.height)):

        # Generates an ID
        object_id = "{}-{}".format("Base", str(uuid.uuid4())[:8])

        # Calls the Parent Constructor
        super().__init__(object_id, simulation, x_loc, y_loc)

        # Makes it Scannable
        self.scannable = True

        # Makes it Not Collidable
        self.colliable = True

        # Makes it collidable by missiles
        self.missile_vulnerable = True

        self.width = 40
        self.height = 40

        self.info = "enemy"
            
            
    # ---------------------------------------------------------------
    # get_description
    # Parameters: None
    # Returns the description of this object
    # ---------------------------------------------------------------
    def get_description(self):
        return "base"


    # ---------------------------------------------------------------
    # draw
    # Parameters: None
    # Draws the smoke cloud
    # ---------------------------------------------------------------
    def draw(self):
        center_x = self.x_coordinate - self.width/2
        center_y = self.y_coordinate - self.height/2
        pythonGraph.draw_image("images/building1.png", center_x, center_y, self.width, self.height)
        if self.hit_points <= 0:
            pythonGraph.draw_image("images/fire.png", center_x, center_y, self.width, self.height)
        #pythonGraph.draw_circle(self.x_coordinate, self.y_coordinate, self.missile_range, "ORANGE", False, 3)
        
        # Tooltip
        if self.distance_to(pythonGraph.get_mouse_x(), pythonGraph.get_mouse_y()) < 20:
            
            # Box surrounding the object
            pythonGraph.draw_rectangle(self.x_coordinate - self.width/2 - 5,
                                       self.y_coordinate - self.height/2 - 5,
                                       self.x_coordinate + self.width/2 + 5,
                                       self.y_coordinate + self.height/2 + 5, self.default_color, False, 3)
            
            if pythonGraph.get_mouse_y() > self.simulation.height - 120:
                starting_y = self.y_coordinate - 110
            else:
                starting_y = self.y_coordinate
            
            # Draws a white background so you can see it on different maps
            pythonGraph.draw_rectangle(self.x_coordinate - 30,
                                       starting_y + 30,
                                       self.x_coordinate + 180,
                                       starting_y + 90, "WHITE", True)
            pythonGraph.draw_rectangle(self.x_coordinate - 30,
                                       starting_y + 30,
                                       self.x_coordinate + 180,
                                       starting_y + 90, "Black", False, 1)
            
            pythonGraph.draw_text(self.get_description() + " (" + self.object_id + ")", self.x_coordinate - 20, starting_y + 35, self.default_color, 22)
            pythonGraph.draw_text("HP: " + str(self.hit_points), self.x_coordinate - 20, starting_y + 53, self.default_color, 20)            

    # ---------------------------------------------------------------
    # update
    # Parameters: None
    # ---------------------------------------------------------------
    def update(self):
        SimulationObject.update(self)


    def set_new_location_bad(self, x_coord, y_coord):
        self.x_coordinate = x_coord
        self.y_coordinate = y_coord
    
    # ---------------------------------------------------------------
    # On Simulation Tick
    # Parameters: None
    # ---------------------------------------------------------------
    def on_simulation_tick(self):
        # building by default just sits there
        pass

