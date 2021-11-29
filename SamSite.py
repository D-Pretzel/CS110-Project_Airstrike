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

class SamSite(SimulationObject):

    # Radius
    missile_range = 200
    missile_count = 20
    missile_damage = 10.0

    # ---------------------------------------------------------------
    # __init__
    # Parameters:
    #     - simulation: A reference to the current simulation
    #     - x_coordinate:  The building center x coordinate
    #     - y_coordinate:  The building center y coordinate
    # Creates a smoke object
    # ---------------------------------------------------------------
    def __init__(self, simulation, object_id, x_loc, y_loc):

        # Generates an ID
        object_id = "{}-{}".format("SAM", str(uuid.uuid4())[:8])

        # Calls the Parent Constructor
        super().__init__(object_id, simulation, x_loc, y_loc)

        # Makes it Not Scannable
        self.scannable = True

        # Makes it Not Collidable
        self.colliable = False

        self.width = 40
        self.height = 40

        self.info = self.missile_range
        self.missile_vulnerable = True
            
            
    # ---------------------------------------------------------------
    # get_description
    # Parameters: None
    # Returns the description of this object
    # ---------------------------------------------------------------
    def get_description(self):
        return "SAM"


    # ---------------------------------------------------------------
    # draw
    # Parameters: None
    # Draws the SAM building
    # ---------------------------------------------------------------
    def draw(self):
        center_x = self.x_coordinate - self.width/2
        center_y = self.y_coordinate - self.height/2
        pythonGraph.draw_image("images/sam.png", center_x, center_y, self.width, self.height)
        if self.hit_points <= 0:
            pythonGraph.draw_image("images/fire.png", center_x, center_y, self.width, self.height)
        else:
            pythonGraph.draw_circle(self.x_coordinate, self.y_coordinate, self.missile_range, "RED", False, 4)
        
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
            pythonGraph.draw_text("Missiles Remaining: " + str(self.missile_count), self.x_coordinate - 20, starting_y + 70, self.default_color, 20)
            
    # ---------------------------------------------------------------
    # update
    # Parameters: None
    # ---------------------------------------------------------------
    def update(self):
        SimulationObject.update(self)

# ---------------------------------------------------------------
    # update
    # Parameters: None
    # ---------------------------------------------------------------
    def set_super_mode(self):
        self.hit_points = 200
        self.missile_range = 300
        self.missile_damage = 10.0
        self.info = self.missile_range

    # ---------------------------------------------------------------
    # On Simulation Tick
    # Parameters: None
    # ---------------------------------------------------------------
    def on_simulation_tick(self):

        if self.hit_points <= 0:
            # no longer can shoot missiles
            pass
        else:
            nearby_objects = self.get_nearby_objects(self.missile_range)
            
            for obj in nearby_objects:
                sam_visible_target = False
                
                if obj[0] == "drone":
                    # checks if object in range is a drone and whether it is emitting, scanning
                    if self.simulation.get_simulation_object(obj[-1]).scanning:
                        sam_visible_target = True
                    elif "bomber" in obj[-1]:
                        sam_visible_target = True
                
                if sam_visible_target:
                    heading = self.get_heading(obj[5], obj[6])
            
                    if self.missile_count > 0:
                        # Creates the Missile
                        missile = Missile(self.simulation, self.x_coordinate, self.y_coordinate, self, heading, True)
                        missile.effective_range = self.missile_range
                        missile.set_missile_dmg(self.missile_damage)
                        
                        # Fires ze Missile
                        self.simulation.add_simulation_object(missile)
                        self.missile_count -= 1
