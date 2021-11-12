import math
import pythonGraph
import random
import uuid
from SimulationObject import SimulationObject
from Missile import Missile
from Smoke import Smoke
from ScanVis import ScanVis
from utilities import normalize_angle

# ---------------------------------------------------------------
# Drone
# Course:  CS110
# Description: This represents a quadcopter drone
# ---------------------------------------------------------------
class Drone(SimulationObject):

    # Drone Behavior Flags
    smoke = False
    turning = False
    scanning = False
    radar_signature = 0
    navigating = False

    # Specifies the Drone's Current State
    # x/y coordiantes and velocity are in simulation_object
    current_heading = 0.0
    desired_heading = 0.0

    # Stores where the drone is currently navigating towards
    x_destination = 0
    y_destination = 0

    # Drone Characteristics
    arm_length = 20
    blade_radius = 12
    heading_arm = 20
    turn_speed = 2.0
    smoke_frequency = 10
    # default values, stored as list so we can vary effectiveness in the future
    a2g_inventory = [100] * 10
    varied_a2g_inventory = [100, 100, 90, 90, 80, 80, 80, 70, 70, 70, 70, 50, 50, 50, 50, 40]


    # ---------------------------------------------------------------
    # __init__
    # Parameters:
    #     - object_id:  The unique ID for this drone
    #     - simulation:  The simulation this drone belongs to
    #     - x_coordiante:  The starting x coordinate
    #     - y_coordinate:  The starting y coordinate
    # Creates a new drone
    # ---------------------------------------------------------------
    def __init__(self, simulation, _type="drone", object_id="", x_coordinate=100, y_coordinate=100):

        # Generates an ID
        object_id = "{}-{}".format(object_id, str(uuid.uuid4())[:8])

        # Calls the Parent Constructor
        super().__init__(object_id, simulation, x_coordinate, y_coordinate)

        if "recon" in object_id:
            self.aircraft_type = "recon"
            self.default_color = "BLUE"
            self.sensor_range = 200
            self.a2g_inventory = []
        elif "bomber" in object_id:
            self.aircraft_type = "bomber"
            self.default_color = "GREEN"
            self.sensor_range = 30
            self.a2g_inventory = [100]*10
            random.shuffle(self.varied_a2g_inventory)

        # Initializes the Drone to Stand Still
        self.x_destination = x_coordinate
        self.y_destination = y_coordinate
        self.current_heading = 0.0
        #self.team = self.simulation.get_team()
        self.update_visibility(self.team)
        self.info = "friendly"
        self.missile_vulnerable = True

    # ---------------------------------------------------------------
    # get_description
    # Parameters: None
    # Returns the description of this object
    # ---------------------------------------------------------------
    def get_description(self):
        return "drone"

    # ---------------------------------------------------------------
    # draw
    # Parameters: None
    # Draws this drone on the screen
    # ---------------------------------------------------------------
    def draw(self):
        # Draws the Center of the Drone
        pythonGraph.draw_circle(self.x_coordinate, self.y_coordinate, 14, "BLACK", True)
        pythonGraph.draw_circle(self.x_coordinate, self.y_coordinate, 12, "WHITE", True)
        

        # Arms / Blades
        for angle in range(45, 405, 90):
            a_x = (self.x_coordinate +
                   self.arm_length *
                   math.cos(math.radians(self.current_heading + angle)))
            a_y = (self.y_coordinate -
                   self.arm_length *
                   math.sin(math.radians(self.current_heading + angle)))

            pythonGraph.draw_line(self.x_coordinate, self.y_coordinate, a_x, a_y, "WHITE", 3)
            pythonGraph.draw_circle(a_x, a_y, self.blade_radius, self.default_color, False, 4)

        # Sensor Range
        if self.scanning:
            pythonGraph.draw_circle(self.x_coordinate,
                                    self.y_coordinate,
                                    self.sensor_range,
                                    self.default_color, False, 1)

        # Draws a Line Representing the Current Heading
        pythonGraph.draw_line(self.x_coordinate,
                              self.y_coordinate,
                              (self.x_coordinate + 0.5 *
                               (self.heading_arm * math.cos(math.radians(self.current_heading)))),
                              (self.y_coordinate - 0.5 *
                               (self.heading_arm * math.sin(math.radians(self.current_heading)))),
                              "BLACK", 5)

        # Draws a Line Representing Where the Drone is Facing
        pythonGraph.draw_line(self.x_coordinate,
                              self.y_coordinate,
                              (self.x_coordinate + self.heading_arm *
                               math.cos(math.radians(self.desired_heading))),
                              (self.y_coordinate - self.heading_arm *
                               math.sin(math.radians(self.desired_heading))),
                              self.default_color, 1)

        # Draws a Line to the Drone's Current Destination
        pythonGraph.draw_line(self.x_coordinate,
                              self.y_coordinate,
                              self.x_destination,
                              self.y_destination,
                              self.default_color,
                              2)

        # Tooltip
        if self.distance_to(pythonGraph.get_mouse_x(), pythonGraph.get_mouse_y()) < self.arm_length * 2:
            if pythonGraph.get_mouse_y() > self.simulation.height - 120:
                starting_y = self.y_coordinate - 150
            else:
                starting_y = self.y_coordinate

            # Draws a little box so that we can see the tooltip on weird backgrounds
            pythonGraph.draw_rectangle(self.x_coordinate - 30, starting_y + 30, self.x_coordinate + 200, starting_y + 120, "WHITE", True)
            pythonGraph.draw_rectangle(self.x_coordinate - 30, starting_y + 30, self.x_coordinate + 200, starting_y + 120, self.default_color, False, 1)

            pythonGraph.draw_rectangle(self.x_coordinate - self.heading_arm,
                                       self.y_coordinate - self.heading_arm,
                                       self.x_coordinate + self.heading_arm,
                                       self.y_coordinate + self.heading_arm,
                                       self.default_color, False, 3)
            pythonGraph.draw_text(self.object_id + " (Team " + str(self.team) + ")",
                                  self.x_coordinate - 20, starting_y + 35, self.default_color, 25)
            pythonGraph.draw_text("HP: {}/100".format(str(int(self.hit_points))),
                                  self.x_coordinate - 20, starting_y + 55, "BLACK", 20)
            pythonGraph.draw_text("X: {}, Y: {}".format(str(int(self.x_coordinate)),
                                                        str(int(self.y_coordinate))),
                                  self.x_coordinate - 20, starting_y + 70, "BLACK", 20)
            pythonGraph.draw_text("Heading: {}".format(str(self.current_heading)),
                                  self.x_coordinate - 20, starting_y + 85, "BLACK", 20)

            if self.navigating:
                pythonGraph.draw_text("Navigating to X: {}, Y: {}".format(str(round(self.x_destination, 1)),
                                                                          str(round(self.y_destination, 1))),
                                  self.x_coordinate - 20, starting_y + 100, "BLACK", 20)
            else:
                pythonGraph.draw_text("Reached Destination",
                                      self.x_coordinate - 20, starting_y + 100, "BLACK", 20)

    # ---------------------------------------------------------------
    # update
    # Parameters: None
    # Performs the drone's per-frame update
    # ---------------------------------------------------------------
    def update(self):
        # Navigation
        delta_x = abs(self.x_coordinate - self.x_destination)
        delta_y = abs(self.y_coordinate - self.y_destination)

        movement_factor = 1.0
        # Scanning Penalty
        if self.scanning:
            movement_factor = 0.5
        # Sets Speeds in the X and Y Directions
        if delta_x < 50.0:
            delta_v_x = 0.02
            max_x_velocity = 0.35
        elif delta_x < 150:
            delta_v_x = 0.05
            max_x_velocity = 1.5
        else:
            delta_v_x = 0.1
            max_x_velocity = 3.0 * movement_factor

        if delta_y < 50.0:
            delta_v_y = 0.02
            max_y_velocity = 0.35
        elif delta_y < 150:
            delta_v_y = 0.05
            max_y_velocity = 1.5 * movement_factor
        else:
            delta_v_y = 0.1
            max_y_velocity = 3.0 * movement_factor

        # Determines if the Drone has Reached Its Destination
        if self.distance_to(self.x_destination, self.y_destination) < 3:
            self.navigating = False
            self.x_coordinate = self.x_destination
            self.y_coordinate = self.y_destination
            self.x_velocity = 0.0
            self.y_velocity = 0.0

        if self.x_destination > self.x_coordinate and self.x_velocity + delta_v_x < max_x_velocity:
            self.x_velocity += delta_v_x
        elif (self.x_destination < self.x_coordinate and
              self.x_velocity - delta_v_x > -max_x_velocity):
            self.x_velocity -= delta_v_x
        elif self.x_velocity > max_x_velocity:
            self.x_velocity -= delta_v_x
        elif self.x_velocity < -max_x_velocity:
            self.x_velocity += delta_v_x

        if (self.y_destination > self.y_coordinate and
                self.y_velocity + delta_v_y <= max_y_velocity):
            self.y_velocity += delta_v_y
        elif (self.y_destination < self.y_coordinate and
              self.y_velocity - delta_v_y >= -max_y_velocity):
            self.y_velocity -= delta_v_y
        elif self.y_velocity > max_x_velocity:
            self.y_velocity -= delta_v_y
        elif self.y_velocity < -max_y_velocity:
            self.y_velocity += delta_v_y

        # Updates Heading Based on the Desired Heading
        if self.current_heading != self.desired_heading:
            if abs(self.current_heading - self.desired_heading) <= self.turn_speed and self.turning:
                self.current_heading = self.desired_heading
                self.turning = False
            else:
                delta_left = normalize_angle(self.desired_heading - self.current_heading)
                delta_right = normalize_angle((self.current_heading + 360) - self.desired_heading)

                if delta_left < delta_right:
                    self.current_heading += self.turn_speed
                else:
                    self.current_heading -= self.turn_speed

        # Updates the Coordinate Based on the Velocity
        self.x_coordinate += self.x_velocity
        self.y_coordinate += self.y_velocity

        # Normalizes Velocity
        self.x_velocity = round(self.x_velocity, 3)
        self.y_velocity = round(self.y_velocity, 3)

        # Normalizes Heading
        self.current_heading = normalize_angle(self.current_heading)

        # Sets the Smoke Every X Frames
        if self.smoke and self.simulation.frame % self.smoke_frequency == 0:
            self.simulation.add_simulation_object(Smoke(self.simulation,
                                                        self.x_coordinate,
                                                        self.y_coordinate))
        
        # resupplies bomber, given resupply base always at x: 100, y: 500
        if "bomber" in self.object_id and \
                    len(self.a2g_inventory) < 2 and \
                    self.distance_to(100,500) <= 50.0:
            # add more bombs to bomber
            if self.simulation.varied_damage:
                # pulls the next bomb off the shuffled varied damage list if there are bombs left
                if len(self.simulation.resupply_base_varied_bombs) >= 2:
                    self.a2g_inventory.append(self.simulation.resupply_base_varied_bombs.pop())
                    if len(self.a2g_inventory) < 2:
                        self.a2g_inventory.append(self.simulation.resupply_base_varied_bombs.pop())
                else:
                    self.a2g_inventory.append(random.randint(70,100))
                    if len(self.a2g_inventory) < 2:
                        self.a2g_inventory.append(random.randint(70,100))
            else:
                self.a2g_inventory.append(100)
                if len(self.a2g_inventory) < 2:
                    self.a2g_inventory.append(100)
                


    # ---------------------------------------------------------------
    # set_destination
    # Parameters:
    #     - x_destination: specifies the x coordinate to navigate to
    #     - y_destination: specifies the y coordinate to navigate to
    # Tells the drone to move somewhere (this deletes all coordinates)
    # ---------------------------------------------------------------
    def set_destination(self, x_destination, y_destination):
        if self.x_coordinate == x_destination and self.y_coordinate == y_destination:
            print("Drone already at destination: {}, {}".format(str(x_destination),
                                                                str(y_destination)))
        else:
            self.navigating = True
            self.x_destination = x_destination
            self.y_destination = y_destination
            print("Setting {} Destination to: {}, {}".format(self.object_id,
                                                            str(x_destination),
                                                            str(y_destination)))

    # ---------------------------------------------------------------
    # set_heading
    # Parameters:
    #     - heading: specifies the desired heading
    # Tells the drone to rotate until it hits the specfied heading
    # 0 degrees is pointing to the right ---->
    # ---------------------------------------------------------------
    def set_heading(self, heading):
        self.turning = True
        self.desired_heading = heading
        print("Setting {} Heading to: {} ".format(self.object_id,
                                                  str(heading)))

    # ---------------------------------------------------------------
    # deploy_air_to_ground
    # Parameters: None
    # Tells the drone to fire a missile at a specific location
    # ---------------------------------------------------------------
    def deploy_air_to_ground(self, target_x, target_y):
        if "bomber" in self.object_id and len(self.a2g_inventory) > 0:
            moab = Missile(self.simulation,
                        self.x_coordinate,
                        self.y_coordinate,
                        self,
                        self.get_heading(target_x, target_y),
                        False)
            moab.damage = self.a2g_inventory.pop(0)
            moab.a2g_bomb = True
            moab.effective_range = 100
            self.simulation.add_simulation_object(moab)
            # print("Air to Ground deployed to x: {}, y: {}.".format(target_x, target_y))
            # print("Air to Ground bomb dmg: {}".format(moab.damage))
        else:
            print("No bombs to deploy!!")

    # ---------------------------------------------------------------
    # fire_missile
    # Parameters: None
    # Tells the drone to fire a dumb missile in the direction it is heading
    # ---------------------------------------------------------------
    def fire_missile(self):
        self.simulation.add_simulation_object(Missile(self.simulation,
                                                      self.x_coordinate,
                                                      self.y_coordinate,
                                                      self,
                                                      self.current_heading,
                                                      False))

    # ---------------------------------------------------------------
    # fire_guided_missile
    # Parameters: None
    # Tells the drone to fire a smart missile in the direction it is heading
    # ---------------------------------------------------------------
    def fire_guided_missile(self):
        print(self.get_object_id() + ": Firing Missile")
        self.simulation.add_simulation_object(Missile(self.simulation,
                                                      self.x_coordinate,
                                                      self.y_coordinate,
                                                      self,
                                                      self.current_heading,
                                                      True))

    # ---------------------------------------------------------------
    # toggle_smoke
    # Parameters: None
    # Tells the drone to either start or stop using smoke
    # ---------------------------------------------------------------
    def toggle_smoke(self, value):
        self.smoke = value

    # ---------------------------------------------------------------
    # toggle_scanning
    # Parameters: None
    # Tells the drone to either start or stop scanning
    # ---------------------------------------------------------------
    def toggle_scanning(self, value):
        self.scanning = value

    # ---------------------------------------------------------------
    # get_scan_results
    # Parameters: None
    # Returns a Table Describing What the Drone Can See
    # ---------------------------------------------------------------
    def get_scan_results(self):
        self.simulation.add_simulation_object(ScanVis(self.simulation,
                                                self.x_coordinate,
                                                self.y_coordinate,
                                                self.sensor_range))

        ret_list = []
        if "recon" in str(self.object_id).lower():
            self.radar_signature = 2
            self.scanning = True
            ret_list = self.get_nearby_objects(self.sensor_range)
            for obj in ret_list:
                self.simulation.get_simulation_object(obj[-1]).update_visibility(self.team)
            return ret_list
        else:
            print("ERROR: Attempted scan, but this drone cannot scan.")
            return []
    # ---------------------------------------------------------------
    # is_destination_reached
    # Parameters: None
    # Returns True if the Drone is at it's destination, and False otherwise
    # ---------------------------------------------------------------
    def is_destination_reached(self):
        return not self.navigating

    # ---------------------------------------------------------------
    # is_rotation_complete
    # Parameters: None
    # Returns True if the Drone has finished rotating, and False otherwise
    # ---------------------------------------------------------------
    def is_rotation_complete(self):
        return not self.turning

    # ---------------------------------------------------------------
    # is_taking_off
    # Parameters: None
    # Returns True if this is the Drone's first tick, and False otherwise
    # ---------------------------------------------------------------
    def is_taking_off(self):
        return self.time_created == self.simulation.tick

    def on_simulation_tick(self):
        # drone will not be visible to Sam Site a certain period after get_scan_results
        # if get_scan_results is not called again
        if self.radar_signature > 0:
            self.radar_signature -= 1
        else:
            self.scanning = False

    # returns count of bombs left
    def get_bomb_inventory(self):
        return len(self.a2g_inventory)

    # used for development only to test different sizes of scan radius
    def dev_set_scan_size(self, new_size):
        if "recon" in str(self.object_id).lower():
            self.sensor_range = new_size

    # enables student to check health of current drone
    def get_drone_health(self):
        return self.hit_points

    # enables option of scenario for bombs of varying effectiveness
    def vary_bomb_effectiveness(self):
        self.a2g_inventory.clear()
        self.a2g_inventory = self.varied_a2g_inventory

    def reduce_inventory_to_two(self):
        while len(self.a2g_inventory) > 2:
            self.a2g_inventory.pop()