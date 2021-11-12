import math
import random
import pythonGraph
from utilities import normalize_angle

# ---------------------------------------------------------------
# Simulation Object
# Course:  CS110
# Description: Represents every object that can be drawn
#              in the simulation.
# ---------------------------------------------------------------
class SimulationObject:

    # Reference to the Simulation that this object belongs to
    simulation = None

    # A unique identifier for this object (assigned at creation)
    object_id = None

    # Specifies what PythonGraph color to use when drawing this object
    # NOTE:  Many simulation objects use multiple colors
    default_color = None

    # Specifies whether or not this object can be scanned by a drone
    scannable = True

    # Specifies whether or not this object can be collided with
    colliable = True

    # Specifies whether any missile type can damage this object
    missile_vulnerable = False

    # Specifies the tick this object was created
    time_created = 0

    # Health of the simulation object.  When 0, the simulation automagically removes it
    hit_points = 100

    # Specifies what "team" the object belongs to
    team = 1

    # Coordinates and velocity of the object
    x_coordinate = 0
    y_coordinate = 0
    x_velocity = 0
    y_velocity = 0

    # A friendly description of the object (drawn on the screen)
    description = "Unspecified"

    # Approved Random colors
    random_color_list = ["RED", "BLUE", "GREEN", "ORANGE"]

    # ------------------------------------------------------------
    # __init__
    # Parameters:
    #     - object_id:  a string that uniquely identifies this object
    #     - simulation:  a reference to the simulation this object lives in
    #     - x_coordinate:  the starting x coordinate of this object
    #     - y_coordinate:  the starting y coordinate of this object
    # Constructor used to create a new simulation object
    # ------------------------------------------------------------
    def __init__(self, object_id, simulation, x_coordinate, y_coordinate):
        self.object_id = object_id
        self.simulation = simulation
        self.default_color = random.sample(self.random_color_list, 1)[0]
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.time_created = self.simulation.tick + 1
        self.info = None
        self.visibility = set()

    # ------------------------------------------------------------
    # get_object_id
    # Parameters:  None
    # Returns the simulation object's unique identifier
    # ------------------------------------------------------------
    def get_object_id(self):
        return self.object_id

    # ------------------------------------------------------------
    # get_description
    # Parameters:  None
    # Returns the simulation object's description
    # ------------------------------------------------------------
    def get_description(self):
        return self.description

    # ------------------------------------------------------------
    # get_description
    # Parameters:
    #      - target_x:  the x coordinate we want to find the distance to
    #      - target_y:  the y coordinate we want to find the distance to
    # Returns the distance between this object, and a (x,y) coordinate
    # ------------------------------------------------------------
    def distance_to(self, target_x, target_y):
        return ((self.x_coordinate - target_x)**2.0 + (self.y_coordinate - target_y)**2.0)**.5

    # ------------------------------------------------------------
    # get_x_location
    # Parameters:  None
    # Returns the x coordinate of this object
    # ------------------------------------------------------------
    def get_x_location(self):
        return self.x_coordinate

    # ------------------------------------------------------------
    # get_y_location
    # Parameters:  None
    # Returns the y coordinate of this object
    # ------------------------------------------------------------
    def get_y_location(self):
        return self.y_coordinate

    # ------------------------------------------------------------
    # get_velocity
    # Parameters:  None
    # Returns the magnitude of the velocity for this object
    # (x and y components are combined)
    # ------------------------------------------------------------
    def get_velocity(self):
        return (self.x_velocity**2.0 + self.y_velocity**2.0)**.5

    # ------------------------------------------------------------
    # get_heading
    # Parameters:  None
    # Returns the angle between this object, and a coordinate, in DEGREES
    # 0.0 degrees is pointing to the right ------>
    # ------------------------------------------------------------
    def get_heading(self, target_x, target_y):
        opposite = target_y - self.y_coordinate
        adjacent = target_x - self.x_coordinate
        return normalize_angle(360 - math.degrees(math.atan2(opposite, adjacent)))

    # ------------------------------------------------------------
    # get_nearby_objects
    # Parameters:
    #     - distance:  The distance in pixels an object needs to be
    #                  within to be considered 'nearby'
    # Returns all objects that are within <distance> of this object
    # as a two-dimensional list with the following columns:
    # Obj TYPE, DISTANCE, HEADING, Attribute, HEALTH/DMG, X, Y, Unique ID
    # ------------------------------------------------------------
    def get_nearby_objects(self, distance):
        result = []

        for obj in self.simulation.simulation_objects:
            if (obj != self and
                    obj.scannable and
                    self.distance_to(obj.x_coordinate, obj.y_coordinate) <= distance):
                
                health_or_dmg = obj.hit_points
                if obj.get_description() == "missile":
                    health_or_dmg = obj.damage

                new_row = [obj.get_description(),
                           round(self.distance_to(obj.x_coordinate, obj.y_coordinate), 2),
                           round(self.get_heading(obj.x_coordinate, obj.y_coordinate), 2),
                           obj.info,
                           health_or_dmg,
                           round(obj.x_coordinate, 2),
                           round(obj.y_coordinate, 2),
                           obj.object_id]
                result.append(new_row)

        result.sort()
        return result

    # ------------------------------------------------------------
    # get_nearest_object
    # Parameters:
    #     - description:  the description of the object we are interested in
    #     - exclusion_list (Optional):  A list of objects to not consider
    # Returns the nearest object of a specified description type
    # ------------------------------------------------------------
    def get_nearest_object(self, description, exclusion_list):
        result = None
        min_distance = 999999999999999

        for obj in self.simulation.simulation_objects:
            distance = self.distance_to(obj.x_coordinate, obj.y_coordinate)
            if (obj != self and
                    not exclusion_list or obj not in exclusion_list and
                    distance <= min_distance):
                if description is not  None and obj.get_description() == description:
                    result = obj
                    min_distance = distance

        return result

    def get_visibility(self, team):
        return team in self.visibility

    def update_visibility(self, team):
        self.visibility.add(team)
    
    
    # ------------------------------------------------------------
    # on_simulation_tick
    # Parameters: None
    # Updates the simulation object's properties/behavior every simulation tick
    # ------------------------------------------------------------
    def on_simulation_tick(self):
        pass


    # ------------------------------------------------------------
    # update
    # Parameters: None
    # Updates the simulation object's properties every frame
    # ------------------------------------------------------------
    def update(self):
        self.x_coordinate += self.x_velocity
        self.y_coordinate += self.y_velocity


    # ------------------------------------------------------------
    # draw
    # Parameters: None
    # Draws the simulation object
    # ------------------------------------------------------------
    def draw(self):
        pythonGraph.draw_circle(self.x_coordinate, self.y_coordinate, 10, self.default_color, True)
        pythonGraph.draw_text(self.get_description() + ":" + str(self.object_id),
                              self.x_coordinate - 50,
                              self.y_coordinate - 25,
                              "BLACK",
                              20)
