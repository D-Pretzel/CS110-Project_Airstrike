import uuid
import random
import pythonGraph
from SimulationObject import SimulationObject
from utilities import random_neutral

# ---------------------------------------------------------------
# Building
# Course:  CS110
# Description: This represents a single building
# ---------------------------------------------------------------


class neutral_object(SimulationObject):

    object_description = "UNKNOWN"

    # ---------------------------------------------------------------
    # __init__
    # Parameters:
    #     - simulation: A reference to the current simulation
    #     - x_coordinate:  The building center x coordinate
    #     - y_coordinate:  The building center y coordinate
    # Creates a smoke object
    # ---------------------------------------------------------------
    def __init__(self, simulation, _type="building", object_id=""):

        # Generates an ID
        object_id = "{}-{}".format(_type, str(uuid.uuid4())[:8])

        # Calls the Parent Constructor
        super().__init__(object_id, simulation,
                         random.randint(int(simulation.width/70), int(simulation.width - simulation.width/70)),
                         random.randint(int(simulation.height/70), int(simulation.height - simulation.height/70)))

        # Makes it Not Scannable
        self.scannable = True

        # Makes it Not Collidable
        self.colliable = False

        # Choose a random building image
        self.img_path = random_neutral(_type)

        if _type == "building":
            self.width = simulation.width/50
            self.height = simulation.width/50
            self.default_color = "RED"
            self.object_description = "building"
            #Sq Footage
            self.info = random.randint(1000, 20000)
        elif _type == "vehicle":
            self.width = simulation.width/40
            self.height = self.width
            self.default_color = "BLUE"
            self.object_description = "vehicle"
            #GVWT
            self.info = random.randint(2000, 40000)
        elif _type == "person":
            self.width = simulation.width/65
            self.height = simulation.width/65
            self.default_color = "GREEN"
            self.object_description = "person"
            #Height in cm
            self.info = random.randint(50, 200)
        else:
            self.width = None
            self.height = None
            self.info = None


    # ---------------------------------------------------------------
    # get_description
    # Parameters: None
    # Returns the description of this object
    # ---------------------------------------------------------------
    def get_description(self):
        return self.object_description


    # ---------------------------------------------------------------
    # draw
    # Parameters: None
    # Draws the smoke cloud
    # ---------------------------------------------------------------
    def draw(self):
        center_x = self.x_coordinate-self.width/2
        center_y = self.y_coordinate-self.height/2
        # draw highlight to help image stand out against background
        pythonGraph.draw_image("images/highlight.png", center_x-25, center_y-25, self.width+50, self.height+50)
        pythonGraph.draw_image(self.img_path, center_x, center_y, self.width, self.height)

        # Tooltip
        if self.distance_to(pythonGraph.get_mouse_x(), pythonGraph.get_mouse_y()) < 20:
            pythonGraph.draw_rectangle(self.x_coordinate - self.width/2 - 5,
                                       self.y_coordinate - self.height/2 - 5,
                                       self.x_coordinate + self.width/2 + 5,
                                       self.y_coordinate + self.height/2 + 5, self.default_color, False, 3)

            if pythonGraph.get_mouse_y() > self.simulation.height - 120:
                starting_y = self.y_coordinate - 110
            else:
                starting_y = self.y_coordinate

            # TOOLTIP display
            # Draws a white background so you can see the Tooltip on different maps
            pythonGraph.draw_rectangle(self.x_coordinate - 30,
                                       starting_y + 30,
                                       self.x_coordinate + 200,
                                       starting_y + 100, "WHITE", True)
            pythonGraph.draw_rectangle(self.x_coordinate - 30,
                                       starting_y + 30,
                                       self.x_coordinate + 200,
                                       starting_y + 100, "Black", False, 1)

            pythonGraph.draw_text(self.get_description() + " (" + self.object_id + ")", self.x_coordinate - 20, starting_y + 35, self.default_color, 22)

            # Sets Custom Tooltips Depending on the Type of Object
            if self.get_description() == "vehicle":
                pythonGraph.draw_text("Gross Weight: " + str(self.info), self.x_coordinate - 20, starting_y + 55, self.default_color, 20)
            elif self.get_description() == "person":
                pythonGraph.draw_text("Height (in cm): " + str(self.info), self.x_coordinate - 20, starting_y + 55, self.default_color, 20)
            elif self.get_description() == "building":
                pythonGraph.draw_text("Square Footage: " + str(self.info), self.x_coordinate - 20, starting_y + 55, self.default_color, 20)
            else:
                pythonGraph.draw_text("UNKNOWN OBJECT", self.x_coordinate - 20, starting_y + 55, self.default_color, 20)

            pythonGraph.draw_text("X: {}, Y: {}".format(str(self.x_coordinate), str(self.y_coordinate)) , self.x_coordinate - 20, starting_y + 75, self.default_color, 20)


    # ---------------------------------------------------------------
    # update
    # Parameters: None
    # Slowly causes the smoke to die
    # ---------------------------------------------------------------
    def update(self):
        SimulationObject.update(self)
