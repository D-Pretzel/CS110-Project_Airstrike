import random
import pythonGraph
import Airstrike
from Simulation import Simulation
from NeutralObject import neutral_object
from Drone import Drone
from EnemyBuilding import EnemyBuilding
from SamSite import SamSite
from utilities import function_definitions
from utilities import binary_map

# Current Version
CURRENT_VERSION = "0.4.1"

# Constants
WINDOW_HEIGHT = 1000
WINDOW_WIDTH = 1800

# Simulation
current_simulation = None

# Constants
TICKS_PER_TURN = 30
TOCK = 0

# Airstrike Variables
superSAMs = False

# Initializes the Simulation
s = Simulation(WINDOW_WIDTH, WINDOW_HEIGHT)
current_simulation = s.get_instance()
s.set_background("images/colorado.jpg")
s.current_perspective = 1
s.show_notifications = False

# Pulls all drone functions from Student code
drone_code = tuple(function_name for function_name in
                   tuple(function_definitions("Airstrike.py")) if function_name.startswith("drone_"))

print(drone_code)

#initializes the number of object based on a md5 hash converted into a binary string
object_map = binary_map(Airstrike.MAP_SEED)

# Creates Drones - start them in the DMZ
for drone_id in drone_code:
    if "recon" in drone_id:
        start_x = 700
        start_y = 500
    elif "bomber" in drone_id:
        start_x = 150
        start_y = 200
    else:
        start_x = 100
        start_y = 600
    next_drone = Drone(current_simulation, "drone", drone_id, start_x, start_y)
    current_simulation.add_simulation_object(next_drone)

# Set up student-chosen challenge modes
# 1-min scans, 2-min bomber dmg, 3-varying bomb damage, 4-Advanced SAMs, 5-limited bombs
if 1 in Airstrike.challenge_modes:
    pass  # scan score calculated using functions in utilities module
if 2 in Airstrike.challenge_modes:
    pass  # need to set thresholds for success, but it depends on the scenario
if 3 in Airstrike.challenge_modes:
    current_simulation.varied_damage = True
    _d = current_simulation.get_simulation_object("drone_bomber")
    _d.vary_bomb_effectiveness()
if 4 in Airstrike.challenge_modes:
    superSAMs = True
if 5 in Airstrike.challenge_modes:  # will create friendly base and start bomber with only 2 bombs
    _d = current_simulation.get_simulation_object("drone_bomber")
    _d.reduce_inventory_to_two()
    # add resupply base for visual feedback only
    resupply_base = EnemyBuilding(current_simulation, "", 100, 500)
    resupply_base.info = "friendly"
    resupply_base.update_visibility(_d.team)
    current_simulation.add_simulation_object(resupply_base)

# nested dictionary of lists of tuples for base and SAM location for each defined scenario
object_initialization = {'one': {'SAMs': [], 'bases': []},
                         'two': {'SAMs': [], 'bases': []},
                         'three': {'SAMs': [], 'bases': []},
                         'five': {'SAMs': [], 'bases': []},
                         'SAM-protected': {'SAMs': [], 'bases': []},
                         'dev static two': {'SAMs': [], 'bases': []},
                         'test range': {'SAMs': [], 'bases': []}}

# only one SAM but two bases, all with a modest amount of randomization in placement
object_initialization["one"]["SAMs"] = [(1200 + random.randint(-50,50), random.randint(200,400))]
object_initialization["one"]["bases"] = [(random.randint(1500,1700), random.randint(50,250)), 
                                         (random.randint(1200,1700), random.randint(600,s.height-50))]

# randomize vertical location for full screen and horizontal location slightly
object_initialization["two"]["SAMs"] = [(1200 + random.randint(-300,300), random.randint(500,s.height-100)),
                                        (1200 + random.randint(-100,100), random.randint(100,200))]
object_initialization["two"]["bases"] = [(random.randint(1450,1700), random.randint(50,250)), 
                                         (random.randint(1200,1700), random.randint(600,s.height-50))]

# randomize vertical location for full screen and horizontal location slightly
object_initialization["three"]["SAMs"] = [(1200 + random.randint(-300,300), random.randint(500,s.height-100)),
                                        (1200 + random.randint(-100,100), random.randint(100,200))]
object_initialization["three"]["bases"] = [(random.randint(1450,1700), random.randint(50,250)), 
                                         (random.randint(1200,1700), random.randint(600,s.height-300)),
                                         (random.randint(1200,1700), random.randint(s.height - 290,s.height-50))]

SAM_two = (1000 + random.randint(-200,200), random.randint(600,s.height-200))
# randomize vertical location for full screen and horizontal location slightly
object_initialization["five"]["SAMs"] = [(1100 + random.randint(-100,100), random.randint(100,200)),
                                         SAM_two]
_base_3 = (random.randint(1275,1700), random.randint(600,s.height-300))
object_initialization["five"]["bases"] = [(1450, 100),
                                         (random.randint(1450,1700), random.randint(200,350)), 
                                         _base_3,
                                         (_base_3[0]-75, _base_3[1]+75),
                                         (SAM_two[0] + random.randint(75,125), SAM_two[1] + random.randint(75,125))]

# all of the bases are within range of a SAM
SAM_1 = (1200 + random.randint(-300,300), random.randint(500,s.height-100))
SAM_2 = (1200 + random.randint(-100,100), random.randint(200,300))
object_initialization["SAM-protected"]["SAMs"] = [SAM_1, SAM_2]
object_initialization["SAM-protected"]["bases"] = [(SAM_1[0] + random.randint(50, 150), SAM_1[1] + random.randint(50,150)), 
                                         (SAM_2[0] + random.randint(50, 150), SAM_2[1] - random.randint(50,150)),
                                         (SAM_2[0] - random.randint(50, 150), SAM_2[1] - random.randint(50,150))]

# completely static setup used for development testing                                         
object_initialization["dev static two"]["SAMs"] = [(1200, 200),
                                                    (1300, 600)]
object_initialization["dev static two"]["bases"] = [(1500, 100), 
                                                    (1400, 650)]     

# setup for the "tutorial" as described in the Canvas project writeup
object_initialization["test range"]["SAMs"] = [(900, 250)]
object_initialization["test range"]["bases"] = [(1400, 250)]

# object_initialization["SEED NAME"]["SAMs"] = [(),
#                                                ()]
# object_initialization["SEED NAME"]["bases"] = [(), 
#                                                 ()]

# Adds the SAMs and bases to the simulation according to the seed set in the project main file
for _base in object_initialization[Airstrike.MAP_SEED]["bases"]:
    current_simulation.add_simulation_object(EnemyBuilding(current_simulation, "", _base[0], _base[1]))
for _SAM in object_initialization[Airstrike.MAP_SEED]["SAMs"]:
    next_SAM = SamSite(current_simulation, "", _SAM[0], _SAM[1])
    if superSAMs:
        next_SAM.set_super_mode()
    current_simulation.add_simulation_object(next_SAM)

# Update intel report with the number of expected enemy bases
current_simulation.set_enemy_base_count(len(object_initialization[Airstrike.MAP_SEED]["bases"]))

# Always ignore damage in the test range scenario
if Airstrike.MAP_SEED == "test range":
    s.ignore_drone_damage()

# Opens the Graphics Window
pythonGraph.open_window(WINDOW_WIDTH, WINDOW_HEIGHT)

current_simulation.set_ticks_per_draw(1)

# Main Animation Loop
while pythonGraph.window_not_closed() and not current_simulation.is_simulation_complete():

    if current_simulation.ticks_per_draw > 0 and TOCK % current_simulation.ticks_per_draw == 0:
        # Erases everything on the screen
        pythonGraph.clear_window("WHITE")

        # Draws the Current Frame of the Simulation
        current_simulation.draw()

        # Draws DMZ line
        pythonGraph.draw_line(300,0,300,s.height,"RED")

    # Updates the simulation
    current_simulation.update()

    # Determines if a tick (i.e., one second) has elapsed, and calls on the
    # drones to decide what they want to do
    if not current_simulation.paused and TOCK % TICKS_PER_TURN == 0:
        # Updates the Simulation Objects
        # TODO:  Consider Removing if Other Objects Don't Have AI
        current_simulation.update_simulation_tick()

        # Updates the Drones
        for func in drone_code:
            # Checks to see if this drone exists before calling its AI function
            if current_simulation.get_simulation_object(func) is not None:
                getattr(Airstrike, func)()

    if current_simulation.ticks_per_draw > 0 and TOCK % current_simulation.ticks_per_draw == 0:
        pythonGraph.update_window()

    # Increments the counter
    if not current_simulation.paused:
        TOCK += 1


if 1 in Airstrike.challenge_modes:
    print("Calculating scan efficiency score. Please wait, this could take up to 30 seconds...")
    efficiency_score = current_simulation.calc_scan_efficiency()
    print("You conducted {} scans for an efficiency raw score of: {}.".format(efficiency_score[0], efficiency_score[2]))

# Keep window running after completion of simulation
while pythonGraph.window_not_closed():
    current_simulation.draw()
    pythonGraph.update_window()    


# This is a friendly message that is printed to let us know the simulation has ended
print("Program Complete")