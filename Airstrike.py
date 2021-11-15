# Project Part 3 - Airstrike
# Author(s): C4C Petzold & C4C Cho
# Course: CS110, Fall 2021
# Final Turn-in Options: 
# DOCUMENTATION: C/4C Anderson assisted in logic surrounding drone_bomber bombing behavior

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
def get_hit_coords(targets):
    target_list = list()
    checked = list()

    for item in targets:
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
    global kill_it

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
        print("Done scanning!")
        bomb = True

    ## ============ ##


## Globals for Drone Bomber ##
kill_it = list()
hit_ids = list()

def drone_bomber():
    # In order to kill something, "set_destination(x, y)" and "deploy_air_to_ground(x, y)" should be used together
    #! Bomber has 100 pixel radius
    global all_targets, kill_it, hit_ids, targets_to_hit

    kill_it = get_hit_coords(targets_to_hit)

    x = get_x_location()
    y = get_y_location()

    if bomb:
        
        base = kill_it.pop(0)
        # base = ["id", x, y]

        if base[0] not in hit_ids:
            set_destination(base[1], base[2])
            deploy_air_to_ground(base[1], base[2])
            print("base:", base)
            hit_ids.append(base[0])
            
        else:
            pass
                
        if len(kill_it) == 0:   # Completion case
            mission_complete()
        


# This loads the simulation scenario
# DO NOT TOUCH
if __name__ == "__main__":
    import Scenario3