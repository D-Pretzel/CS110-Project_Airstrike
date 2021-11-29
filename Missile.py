import math
from random import paretovariate
import uuid
from SimulationObject import *
from utilities import normalize_angle

# ---------------------------------------------------------------
# Missile
# Course:  CS110
# Description: This represents a single missile
# ---------------------------------------------------------------
class Missile(SimulationObject):

    # Where the missile originated from
    x_origin = 0
    y_origin = 0

    # The entity that fired the missile
    parent = None

    # Missile Performance Characteristics
    max_speed = 6.0
    max_turn_rate = 1
    effective_range = 750
    damage_radius = 25.0
    damage = 10.0
    heading = 0

    # Missile Behaviors
    homing_mode = False
    current_target = None
    a2g_bomb = False

    # ---------------------------------------------------------------
    # __init__
    # Parameters:
    #     - simulation: A reference to the current simulation
    #     - x_coordinate:  The missile's center x coordinate
    #     - y_coordinate:  The missile's center y coordinate
    #     - parent:  The entity that fired the missile (the object, not ID)
    #     - starting_heading:  The initial heading of the missile
    #     - homing:  True if the missile is tracking nearby targets, False otherwise
    # Creates a missile object
    # ---------------------------------------------------------------
    def __init__(self, simulation, x_coordinate, y_coordinate, parent, starting_heading, homing):
        # Generates an ID
        object_id = "{}-{}".format("missile", str(uuid.uuid4())[:8])

        # Calls the Parent Constructor
        super().__init__(object_id, simulation, x_coordinate, y_coordinate)

        self.x_origin = x_coordinate
        self.y_origin = y_coordinate
        self.hit_points = 1.0
        self.heading = starting_heading
        self.parent = parent
        if "bomber" in parent.object_id:
            self.info = "friendly"
        elif "SAM" in parent.object_id:
            self.info = "enemy"
        self.team = 1  # set so missiles are always visible
        self.update_visibility(self.team)
        self.homing = homing
        self.missile_vulnerable = False
        self.scannable = True


    # ---------------------------------------------------------------
    # get_description
    # Parameters: None
    # Returns the description of this object
    # ---------------------------------------------------------------
    def get_description(self):
        return "missile"

    # ---------------------------------------------------------------
    # set_missile_dmg
    # Parameters: new missile damage
    # ---------------------------------------------------------------
    def set_missile_dmg(self, new_dmg_val):
        if new_dmg_val > 1.0:
            self.damage = new_dmg_val

    # ---------------------------------------------------------------
    # draw
    # Parameters: None
    # Draws the missile on the screen
    # ---------------------------------------------------------------
    def draw(self):
        if self.hit_points > 0.0:
            # Center of the Missile
            pythonGraph.draw_circle(self.x_coordinate,
                                    self.y_coordinate, 6, self.parent.default_color, True)
            pythonGraph.draw_line(self.x_coordinate,
                                  self.y_coordinate,
                                  self.x_origin,
                                  self.y_origin, "ORANGE", 1)

            # Tooltip
            if self.distance_to(pythonGraph.get_mouse_x(), pythonGraph.get_mouse_y()) < 20:
                pythonGraph.draw_circle(self.x_coordinate, self.y_coordinate, 15, self.parent.default_color, False, 1)
                
                pythonGraph.draw_rectangle(self.x_coordinate, self.y_coordinate + 20, self.x_coordinate+150, self.y_coordinate+60, "WHITE", True)
                pythonGraph.draw_rectangle(self.x_coordinate, self.y_coordinate + 20, self.x_coordinate+150, self.y_coordinate+60, "BLACK", False, 1)
                pythonGraph.draw_text("Guided Missile", self.x_coordinate + 3, self.y_coordinate + 23, self.parent.default_color, 22)

                if self.current_target != None:
                    pythonGraph.draw_text("Tracking " + self.current_target.get_object_id(),
                                          self.x_coordinate + 3,
                                          self.y_coordinate + 42,
                                          "BLACK", 18)
                else:
                    pythonGraph.draw_text("No Target",
                                          self.x_coordinate + 3,
                                          self.y_coordinate + 42,
                                          "BLACK", 18)
        else:
            pythonGraph.draw_circle(self.x_coordinate,
                                    self.y_coordinate,
                                    self.damage_radius,
                                    "RED", True)

    # ---------------------------------------------------------------
    # update
    # Parameters: None
    # Updates the location of the missile
    # ---------------------------------------------------------------
    def update(self):
        # Movement
        if self.hit_points > 0.0:
            # Maneuvering
            if self.homing:
                self.current_target = self.get_nearest_object("Drone", [self.parent])
                if self.current_target is not None:
                    desired_heading = self.get_heading(self.current_target.x_coordinate,
                                                       self.current_target.y_coordinate)
                    delta_left = normalize_angle(desired_heading - self.heading)
                    delta_right = normalize_angle((self.heading + 360) - desired_heading)
                    if delta_left < delta_right:
                        self.heading += self.max_turn_rate
                    else:
                        self.heading -= self.max_turn_rate

            # Calculates Velocity Based on Current Heading
            self.x_velocity = self.max_speed * math.cos(math.radians(self.heading))
            self.y_velocity = -self.max_speed * math.sin(math.radians(self.heading))
            self.x_coordinate += self.x_velocity
            self.y_coordinate += self.y_velocity

        # Collision Detection
        for obj in self.simulation.simulation_objects:
            # Does not check for collisions against the device that launched it!
            if (obj.missile_vulnerable and
                    obj.object_id != self.object_id and
                    obj.object_id != self.parent.object_id):
                distance = self.distance_to(obj.x_coordinate, obj.y_coordinate)
                if distance < self.damage_radius:
                    positive_hit = False
                    if "drone" in obj.get_description():

                        # missiles fired from bomber drone should not hit other drones
                        if not self.a2g_bomb:
                            print("SAM-fired missile impact!")
                            if self.simulation.drones_take_dmg:
                                obj.hit_points -= self.damage
                            # still display explosion and kill missile even if in ignore damage mode
                            positive_hit = True
                            self.simulation.update_score("drone_damage")
                    else:
                        # ground objects can only be hit by bombs from the bomber
                        if self.a2g_bomb:
                            prior_hit_points = obj.hit_points
                            obj.hit_points -= self.damage
                            positive_hit = True

                            # SAMs are destroyed in one hit when using varying damage challenge mode
                            # this is because recon drone Battle Damage Assessments would be undesirably difficult
                            if "SAM" in obj.object_id and self.simulation.varied_damage:
                                    obj.hit_points -= 100

                            if prior_hit_points > 0 and obj.hit_points <= 0:
                                if "base" in obj.object_id.lower():
                                    self.simulation.update_score("base_destroyed")
                                elif "SAM" in obj.object_id:
                                    self.simulation.update_score("SAM_destroyed")

                    if positive_hit:    
                        self.hit_points = 0
                        pythonGraph.draw_image("images/explosion.png", self.x_coordinate-60, self.y_coordinate-60, 120, 120)
                        
                        # prints text confirmation to console that drone was hit by a missile
                        if "recon" in str(obj.object_id).lower():
                            print("Recon Drone Hit! Health now {}/100.".format(int(obj.hit_points)))
                        elif "bomber" in str(obj.object_id).lower():
                            print("Bomber Drone Hit! Health now {}/100.".format(int(obj.hit_points)))

        # Normalizes Heading
        self.heading = normalize_angle(self.heading)

        # Removes the Missile from the Simulation
        if self.distance_to(self.x_origin, self.y_origin) > self.effective_range:
            self.hit_points = 0
