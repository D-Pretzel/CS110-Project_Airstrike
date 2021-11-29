import ast
import random
import hashlib
import math


# ---------------------------------------------------------------
# function_definitions
# Parameters: A Python filename
# Returns a list of all functions in a file
# ---------------------------------------------------------------
def function_definitions(filename):
    with open(filename, "rt") as file:
        body = ast.parse(file.read(), filename=filename).body
    return (f.name for f in body if isinstance(f, ast.FunctionDef))


# ---------------------------------------------------------------
# normalize_angle
# parameters: an angle, in degrees
# converts a degree value to a value between 0.0 - 360.0
# ---------------------------------------------------------------
def normalize_angle(angle):
    a = angle % 360
    if a < 0:
        return a + 360
    else:
        return a

# ---------------------------------------------------------------
# random_neutral
# parameters: none
# returns a path to a random building picture
# ---------------------------------------------------------------
def random_neutral(_type):
    if _type == "vehicle":
        return random.choice(("images/vehicle1.png",
                              "images/vehicle2.png",
                              "images/vehicle3.png"))
    elif _type == "building":
        return random.choice(("images/building1.png",
                              "images/building2.png",
                              "images/building3.png"))
    elif _type == "person":
        return random.choice(("images/person1.png",
                              "images/person2.png"))
    return None


def binary_map(_string):
    return bin(int(hashlib.md5(bytes(_string, 'utf-8')).hexdigest(), 16))[2:]

def dist_between(x1,y1,x2,y2):
    return ((((x2 - x1 )**2) + ((y2-y1)**2) )**0.5)
    
def y_coord_of_collision(x,y,scan_x,scan_y,scan_rad):
    dist = dist_between(x,y,scan_x,scan_y)
    x_diff = scan_x - x
    y_diff = scan_y - y
    
    if abs(x_diff) > scan_rad or y > scan_y:
        return 1000000
    
#     print(x,y,scan_x,scan_y,scan_rad**2,x_diff**2)
    y1 = math.sqrt(scan_rad**2-x_diff**2)
    y2 = y_diff - y1
    new_y = y + y2
    return math.ceil(new_y)
    
#Out of the 1,800,000 pixels on the map, let's count each that has been scanned
def check_all_points(scans):
    num_points_scanned = 0
    x = 300
    while x < 1800:
        y = 0
        while y < 1000:
            point_scanned = False
            lowest_y_collision_coord = 100000
            for scan in scans:  
                scan_x = scan[0]
                scan_y = scan[1]
                scan_rad = scan[2]
                
                dist = dist_between(x,y,scan_x,scan_y)
                
                if dist <= scan_rad:
                    x_diff = scan_x - x
                    y_diff = scan_y - y
                    y_advancement = min(999-y,int(math.sqrt(scan_rad**2-x_diff**2) + y_diff))
                    y+=y_advancement
                    num_points_scanned+=y_advancement
                    point_scanned = True
                    break
                else:
                    y_collision_coord = y_coord_of_collision(x,y,scan_x,scan_y,scan_rad)
                    lowest_y_collision_coord = min(y_collision_coord,lowest_y_collision_coord)
            if point_scanned:
                num_points_scanned+=1
            else:
                y = min(lowest_y_collision_coord-1,999)
                
            y+=1
        x+=1
    return num_points_scanned