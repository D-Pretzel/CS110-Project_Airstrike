from collections import defaultdict
import pythonGraph
import random
import utilities
from Drone import Drone
from NeutralObject import neutral_object
from SamSite import SamSite
from EnemyBuilding import EnemyBuilding

# ---------------------------------------------------------------
# Simulation
# Course:  CS110
# Description: Models and visualizes a collection of simulation objects
# ---------------------------------------------------------------
class Simulation:

    # Singleton Instance
    _instance = None

    # Simulation Dimensions
    width = 0
    height = 0

    # Perspective from which to view the simulation from
    # 0 = everything; 1+ equals the team you want to see
    current_perspective = 0

    #starting drone team
    drone_team = 1

    # The background to draw
    background_image = None

    # A List of Objects that the Simulation is... Simulating
    simulation_objects = []
    recon_scans = []

    # Simulation Runtime State
    paused = False
    complete = False
    show_notifications = True
    tick = 0
    ticks_per_draw = 1
    frame = 0

    #Intel Info
    enemy_base_count = 0

    # Runtime mechanic options
    drones_take_dmg = True
    varied_damage = False
    score = 1000
    score_events = {"time_passed": -10, "drone_damage":-50, "base_destroyed":1000, "SAM_destroyed":1500}
    up_arrow_armed = True
    down_arrow_armed = True
    resupply_base_varied_bombs = [100, 100, 100, 90, 90, 90, 90, 80, 80, 80, 80, 80, 80, 70, 70, 70, 70, 50, 50, 50, 50, 40]

    # ---------------------------------------------------------------
    # Get Instance
    # Parameters: None
    # Returns the Current Simulation Instance
    # ---------------------------------------------------------------
    @staticmethod
    def get_instance():
        if Simulation._instance is None:
            Simulation()
        return Simulation._instance


    # ------------------------------------------------------------
    # __init__
    # Parameters:
    #     - width:  the horizontal size of the simulation
    #     - height:  the vertical size of the simulation
    # Constructor used to create a new simulation
    # ------------------------------------------------------------
    def __init__(self, width=1920, height=1080):
        if Simulation._instance is None:
            self.width = width
            self.height = height
            Simulation._instance = self
            random.shuffle(self.resupply_base_varied_bombs)


    # ------------------------------------------------------------
    # is_simulation_complete
    # Parameters: None
    # Returns True if the simulation is complete, and False otherwise
    # ------------------------------------------------------------
    def is_simulation_complete(self):
        return self.complete

    # For Project Airstrike
    # Returns total number of enemy bases that will appear on the map
    def set_enemy_base_count(self, count_bases):
        self.enemy_base_count = count_bases

    # For Project Airstrike
    # Returns total number of enemy bases that will appear on the map
    def get_intel_report(self):
        return self.enemy_base_count

    # ------------------------------------------------------------
    # get team
    # Parameters: None
    # Returns a drone team to be on increments for the next drone team
    # ------------------------------------------------------------
    def get_team(self):
        ret_team = self.drone_team
        self.drone_team += 1
        return ret_team


    # ------------------------------------------------------------
    # add_simulation_object
    # Parameters:
    #     - new_object:  The new object to add
    # Adds a new simulation object to the simulation
    # ------------------------------------------------------------
    def add_simulation_object(self, new_object):
        if self.get_simulation_object(new_object.get_object_id()) is None:
            self.simulation_objects.append(new_object)
            if "scan" in new_object.get_object_id():
                self.recon_scans.append(new_object.get_scan_tuple())
        else:
            print("ERROR: Object with ID {} has already been added".format(new_object.get_object_id()))


    # ------------------------------------------------------------
    # remove_simulation_object
    # Parameters:
    #     - object_to_remove:  The object to remove
    # Removes a simulation object from the simulation
    # ------------------------------------------------------------
    def remove_simulation_object(self, object_to_remove):
        if object_to_remove in self.simulation_objects:
            self.simulation_objects.remove(object_to_remove)
        else:
            print("WARNING: Tried to remove {} but it was not in the list".format(object_to_remove.get_object_id()))


    # ------------------------------------------------------------
    # get_simulation_object
    # Parameters:
    #     - object_id:  The id of the object to find
    # Returns the simulation object with the matching ID, or None if not found
    # ------------------------------------------------------------
    def get_simulation_object(self, object_id):
        for obj in self.simulation_objects:
            if object_id in obj.get_object_id():
                return obj

        return None


    # ------------------------------------------------------------
    # get_simulation_objects
    # Parameters:
    #     - descriptions:  A list of descriptions you are interested in getting
    # Returns a list containing all objects with the specified descriptions.
    # If descriptions is empty, then return all objects
    # ------------------------------------------------------------
    def get_simulation_objects(self, descriptions=None):
        result = []

        for obj in self.simulation_objects:
            if descriptions or obj.get_description() in descriptions:
                result.append(obj)

        # Returns the list
        return result


    # ------------------------------------------------------------
    # update_simulation_tick
    # Parameters: None
    # Lets all Simulation Objects Perform a Per Tick Update
    # ------------------------------------------------------------
    def update_simulation_tick(self):
        for obj in self.simulation_objects:
            obj.on_simulation_tick()

        self.tick += 1
        self.update_score("time_passed")

    # ------------------------------------------------------------
    # set_background
    # Parameters:
    #     - background_image:  the name of the file to display
    # Sets the background image for the simulation
    # ------------------------------------------------------------
    def set_background(self, background_image):
        self.background_image = background_image


    # ------------------------------------------------------------
    # update
    # Parameters: None
    # Lets all Simulation Perform their Per Frame Update
    # ------------------------------------------------------------
    def update(self):
        # Increments the Frame Counter
        self.frame += 1

        # Checks for Key Press Events
        if pythonGraph.key_pressed("space"):
            self.paused = not self.paused
            #self.ticks_per_draw = 1
            print("Pause is enabled:", self.paused)
        elif pythonGraph.key_pressed("1"):
            print("Perspective Changed to Team 1")
            self.current_perspective = 1
        elif pythonGraph.key_pressed("2"):
            print("Perspective Changed to Team 2")
            self.current_perspective = 2
        elif pythonGraph.key_pressed("0"):
            print("Perspective Changed to EVERYONE")
            self.current_perspective = 0
        elif pythonGraph.key_pressed("up") and self.ticks_per_draw < 50 and self.up_arrow_armed and not self.paused:
            self.ticks_per_draw = int(self.ticks_per_draw * 1.2) + 1
            self.up_arrow_armed = False
        elif pythonGraph.key_pressed("down") and self.ticks_per_draw > 1 and self.down_arrow_armed and not self.paused:
            self.ticks_per_draw = int(self.ticks_per_draw / 1.2)
            self.down_arrow_armed = False

        if pythonGraph.key_released("up"):
            self.up_arrow_armed = True

        if pythonGraph.key_released("down"):
            self.down_arrow_armed = True


        # Contains a list of objects to remove
        pruning_list = []

        # Updates the Simulation Objects (if not paused)
        if not self.paused:
            for simObject in self.simulation_objects:
                simObject.update()
                if simObject.hit_points <= 0 and not ("base" in simObject.object_id.lower() or "SAM" in simObject.object_id):
                    pruning_list.append(simObject)

            for simObject in pruning_list:
                self.remove_simulation_object(simObject)

    # ------------------------------------------------------------
    # draw
    # Parameters: None
    # Draws the simulation objects to the screen
    # ------------------------------------------------------------
    def draw(self):
        # Updates the Titlebar
        title = "DroneTestEnvironment (Time = " + str(self.tick)
        title += " Objects: " + str(len(self.simulation_objects)) + ")"
        title += " - x:" + str(pythonGraph.get_mouse_x()) + ", y:" + str(pythonGraph.get_mouse_y())

        pythonGraph.set_window_title(title)

        # Draws the Background
        if self.background_image is not None:
            pythonGraph.draw_image(self.background_image, 0, 0, self.width, self.height)

        # Specifies the Draw Priority
        draw_order = ['drone', 'missile', 'SAM', 'base']
        object_categories = defaultdict(list)
        #visible_targets = set()

        # Draws all nonpriority items first, and stores the rest in a dictionary
        for obj in self.simulation_objects:

            if obj.get_description() in draw_order:
                object_categories[obj.get_description()].append(obj)
            elif obj.get_visibility(self.current_perspective) or self.current_perspective == 0:
                obj.draw()

        # Draws the priority items from the dictionary
        for description_type in reversed(draw_order):
            if description_type in object_categories:
                for obj in object_categories[description_type]:
                    if obj.get_visibility(self.current_perspective) or self.current_perspective == 0:
                        obj.draw()
        
        if self.is_simulation_complete():
            pythonGraph.draw_text("Mission Complete!", 100, self.height - 100, pythonGraph.colors.LIGHT_GREEN, 128)

        pythonGraph.draw_rectangle(10,self.height-60, 275, self.height-100, "WHITE", True)
        pythonGraph.draw_text("Score: {}".format(self.score), 15,self.height - 95, "BLACK", font_size=48)
        
        # Displays a Warning Message if the user mucked with the perspective
        if self.show_notifications and self.current_perspective != 0:
            pythonGraph.draw_rectangle(5, 5, 450, 55, (255, 255, 255), True)
            pythonGraph.draw_text("Now Viewing from Team " + str(self.current_perspective) + "'s Perspective", 8, 8, "BLACK", 30)
            pythonGraph.draw_text("(Press '0' to see everything)", 8, 33, "BLACK", 25)

        if self.paused:
            pythonGraph.draw_rectangle(775, 5, 1025, 50, "YELLOW", True)
            pythonGraph.draw_text("SIMULATION PAUSED", 792, 10, "BLACK", 30)
            pythonGraph.draw_text("Press 'Space' to Resume", 812, 30, "BLACK", 22)

        if self.current_perspective == 0:
            pythonGraph.draw_rectangle(10, self.height - 45, 300, self.height, "BLUE", True)
            pythonGraph.draw_text("SCAN VIEW MODE", 20, self.height - 40, "WHITE", 30)
            pythonGraph.draw_text("Press 1 to see what your drone sees.", 20, self.height - 20, "WHITE", 22)

        if not self.drones_take_dmg:
            pythonGraph.draw_rectangle(10, self.height - 155, 275, self.height-110, "ORANGE", True)
            pythonGraph.draw_text("IGNORE DAMAGE ON", 20, self.height - 145, "WHITE", font_size=32)
            
    # ------------------------------------------------------------
    # set_ticks_per_draw
    # Parameters: speed
    # Modifies how many updates happen to the simulation state before a redraw to screen
    # ------------------------------------------------------------        
    def set_ticks_per_draw(self, speed):
        self.ticks_per_draw = speed

    # ------------------------------------------------------------
    # ignore_drone_damage
    # Parameters: None
    # Modifies simulation flag to configure missiles to not damage drones
    # ------------------------------------------------------------
    def ignore_drone_damage(self):
        self.drones_take_dmg = False

    # ------------------------------------------------------------
    # update_score
    # Parameters: event
    # Modifies score based on what score event just occured
    # ------------------------------------------------------------
    def update_score(self, event):
        if event in self.score_events:
            self.score += self.score_events[event]
        else:
            print("SIM ERROR: Improper score event update occured.")
    
    # ------------------------------------------------------------
    # calc_scan_efficiency
    # Parameters: none
    # Returns a tuple (count_scans, count_pix_scanned, raw_score) where:
    #   + count_scans is the number of scans performed by the drone
    #   + count_pix_scanned is total number of enemy zone pixels covered
    #   + raw_score is the (num_pix_scanned/count_scans) * (num_pix_scanned/total_enemy_pix)
    # ------------------------------------------------------------
    def calc_scan_efficiency(self):
        count_pixels_scanned = utilities.check_all_points(self.recon_scans)
        count_scans = len(self.recon_scans)
        raw_score = round((count_pixels_scanned/ count_scans) * (count_pixels_scanned/1500000), 2)
        return (count_scans, count_pixels_scanned, raw_score)
