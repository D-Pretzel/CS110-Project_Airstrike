from inspect import stack
from Simulation import Simulation

def get_x_location():
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    return _d.get_x_location()

def get_y_location():
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    return _d.get_y_location()

def get_scan_results():
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    return _d.get_scan_results()

def set_destination(x, y):
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    _d.set_destination(x, y)

def set_heading(heading):
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    _d.set_heading(heading)

def fire_missile():
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    _d.fire_guided_missile()

def smoke_on():
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    _d.toggle_smoke(True)

def smoke_off():
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    _d.toggle_smoke(False)

def toggle_scanning(value):
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    _d.toggle_scanning(value)

def distance_to(x, y):
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    return _d.distance_to(x, y)

def destination_reached():
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    return _d.is_destination_reached()

def taking_off():
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    return _d.is_taking_off()

def mission_complete():
    _s = Simulation.get_instance()
    _s.complete = True

def intel_report():
    _s = Simulation.get_instance()
    return _s.get_intel_report()

def engage_hyperspeed():
    _s = Simulation.get_instance()
    _s.set_ticks_per_draw(5)

def engage_plaidspeed():
    _s = Simulation.get_instance()
    _s.set_ticks_per_draw(15)

def deploy_air_to_ground(target_x, target_y):
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    return _d.deploy_air_to_ground(target_x, target_y)

def get_bomb_inventory():
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    return _d.get_bomb_inventory()

def get_drone_health():
    _s = Simulation.get_instance()
    _d = _s.get_simulation_object(_get_calling_id_from_stack())
    return _d.get_drone_health()

def ignore_drone_damage():
    _s = Simulation.get_instance()
    return _s.ignore_drone_damage()

def _get_calling_id_from_stack():
    drone_id = ""

    for frame_info in stack():
        if "drone_recon" in frame_info.function or "drone_bomber" in frame_info.function:
            drone_id = str(frame_info.function)
            break

    return drone_id
