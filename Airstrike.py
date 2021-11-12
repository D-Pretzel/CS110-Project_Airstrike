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
#MAP_SEED = "three"
# MAP_SEED = "five"
# MAP_SEED = "SAM-protected"
MAP_SEED = "test range"

# 1-min scans, 2-min bomber dmg, 3-varying bomb damage, 4-Advanced SAMs, 5-limited bomb capacity
# include desired mode numbers in list variable below
challenge_modes = []

# == Initialize the global stuff == #
all_targets = list()
id_set = set()
kill_it = list()
hit_ids = list()
# ================================= #

# Returns 2D list containing all ordered pairs of targets to hit
def get_hit_coords(everything_list):
    target_list = list()
    checked = list()

    for item in everything_list:
        if item[7] in checked:  # If the object ID HAS been checked already...do nothing
            pass
        else:   # Otherwise add the x and y coordinates as a tuple to "target_list" and add the id to "checked"
            target_list.append((item[7], item[5], item[6]))
            checked.append(item[7])
    
    return(target_list)


def drone_recon():
    global all_targets
    global id_set

    ignore_drone_damage()
    engage_plaidspeed()

    x = get_x_location()
    y = get_y_location()

    data = get_scan_results()

    # Empty list checker
    if len(data) != 0: 
        all_targets += data  # concatonates all data to all_targets (replacement for flattening)
        for row in all_targets:
            if (row[0] == 'base'):  # adds id to set of base ids
                id_set.add(row[7])
    else:   # Don't do anything with an empty list
        pass 
    

    ## === THE DEBUG ARENA === ##


    ## ======================= ##


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
            set_destination(300, 800)
        if x == 300 and y == 800:
            set_destination(1600, 800)
    if destination_reached() and (x == 1600 and y == 800):
        mission_complete()
    ## ============ ##

def drone_bomber():
    # In order to kill something, "set_destination(x, y)" and "deploy_air_to_ground(x, y)" should be used together
    # Bomber has 100 pixel radius
    global all_targets, kill_it, hit_ids

    kill_it = get_hit_coords(all_targets)
    
    if len(kill_it) != 0:   # If there's actually something to kill...
        for item in kill_it:
    
            id, x, y = item[0], item[1], item[2]    # Break out the tuples into the obejct's id, x, and y coordinates
            
            if id not in hit_ids:   # If the id hasn't been hit yet...
                set_destination(x, y)
                deploy_air_to_ground(x, y)
                hit_ids.append(id)  # Add it to the "hit_ids" list if it's been hit...
            else:
                set_destination(299, 100)
    
    else:
        set_destination(299, 100)
        pass    # Don't do anything if there's nothing to kill...duh


# This loads the simulation scenario
# DO NOT TOUCH
if __name__ == "__main__":
    import Scenario3