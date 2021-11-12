# Project Part 3 - Airstrike
# Author(s): C4C Petzold & C4C Cho
# Course: CS110, Fall 2021
# Final Turn-in Options: 
# DOCUMENTATION: 

## ======================== ##
#   Gate Check Requirements   #
    #* 1. Identify the location of at least one (of severl) enemy bases by scanning with the recon drone
    #* 2. Use the drone bomber to attack the base identified by the recon drone (you can leave "ignore_drone_damage" on)
    #* 3. Map used must be "MAP_SEED = 'three'"
## ======================== ##

import random
import drone_api
from cs110 import autograder
from drone_api import set_destination
from drone_api import get_x_location
from drone_api import get_y_location
from drone_api import destination_reached
from drone_api import taking_off
from drone_api import mission_complete
from drone_api import engage_hyperspeed
from drone_api import engage_plaidspeed
from drone_api import get_scan_results
from drone_api import intel_report
from drone_api import deploy_air_to_ground
from drone_api import get_bomb_inventory
from drone_api import ignore_drone_damage
from drone_api import get_drone_health


# MAP_SEED = "two"
MAP_SEED = "three"
# MAP_SEED = "five"
# MAP_SEED = "SAM-protected"
# MAP_SEED = "test range"

# 1-minimum scans, 2-minimum bomber dmg, 3-varying bomb damage, 4-Advanced SAMs, 5-limited bomb capacity
# include desired mode numbers in list variable below
challenge_modes = []

# == Initialize the global stuff == #
all_targets = list()
targets_to_hit = list()
bomb = bool()
# ================================= #

# Returns 2D list containing all ordered pairs of targets to hit
def get_hit_coords(everything_list):
    target_list = list()
    checked = list()

    for item in everything_list:
        if item[7] in checked:  # If the object ID HAS been checked already...do nothing
            pass
        else:   # Otherwise add the x and y coordinates as a tuple to "target_list" and add the id to "checked"
            target_list.append([item[7], item[5], item[6]])
            checked.append(item[7])
    
    return(target_list)


def drone_recon():
    global all_targets
    global targets_to_hit
    global bomb

    ignore_drone_damage()
    engage_plaidspeed()

    x = get_x_location()
    y = get_y_location()

    data = get_scan_results()

    # Empty list checker
    if len(data) != 0: 
        all_targets += data  # concatonates all data to all_targets (replacement for flattening)
        for row in all_targets:
            if (row[0] == 'base'):     #! Change this line to change what the bomber drone bombs
                targets_to_hit.append(row)
    else:   # Don't do anything with an empty list
        pass
 
    ## DRONE MOVES ##
    if taking_off():
        set_destination(300, 200)
    if destination_reached():
        if x == 300 and y == 200:
            set_destination(1600, 200)
        if x == 1600 and y == 200:
            set_destination(1600, 600)
        if x == 1600 and y == 600:
            set_destination(300, 600)
        if x == 300 and y == 600:
            set_destination(300, 1000)
        if x == 300 and y == 1000:
            set_destination(1600, 1000)
    if destination_reached() and (x == 1600 and y == 1000):
        #mission_complete()
        print("This is where we'd normally finish.")
        bomb = True
    ## ============ ##


## Globals for Drone Bomber ##
kill_it = list()
hit_ids = list()

#! This bwoken...
def drone_bomber():
    # In order to kill something, "set_destination(x, y)" and "deploy_air_to_ground(x, y)" should be used together
    #! Bomber has 100 pixel radius
    global all_targets, kill_it, hit_ids, targets_to_hit
    
    kill_it = get_hit_coords(targets_to_hit)    # Makes "kill_it" the list of targets to hit
    
    if bomb:
                
        for item in kill_it:
    
            id = item[0]
            x = item[1]
            y = item[2]
            
            # !!! FIXME:
            # print("kill_it:", kill_it)
            # print("hit_ids", hit_ids)
            print("Item:", item)
            print("Intel:", intel_report())
            print("Bombs left:", get_bomb_inventory())

            #! This can all be optimized later
            if id not in hit_ids and destination_reached():
                set_destination(x, y)   # Set the bomber's destination to the location of the object
                deploy_air_to_ground(x, y)  # KILL IT
                hit_ids.append(id)  # Add the obejct id to "hit_ids"
            else:
                set_destination(x, y)

        #! Terminating Conidition:
        if len(hit_ids) == len(kill_it):
            pass
            # mission_complete()      # Mission complete when all of the items have been hit

    else:
        pass

# This loads the simulation scenario
# DO NOT TOUCH
if __name__ == "__main__":
    import Scenario3