from panda3d.core import LineSegs, WindowProperties
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, NodePath
from direct.showbase.ShowBase import ShowBase
import numpy as np
import utils
from data_structures import *

class Visuals(ShowBase):
    def __init__(self, center_lat, center_lon, vehicle_state: VehicleState, mouse_keyboard_controls: ControlInput):
        ShowBase.__init__(self)
        self.center_lat = center_lat
        self.center_lon = center_lon
        self.vehicle_state = vehicle_state
        self.mouse_keyboard_controls = mouse_keyboard_controls

        props = WindowProperties()
        props.setTitle("UAV Simulation")
        self.win.requestProperties(props)

        self.disableMouse()

        self.create_ground()

        self.taskMgr.add(self.update_flight, "update_flight")

        self.accept("w", self.increase_throttle)
        self.accept("s", self.decrease_throttle)
    
    def create_ground(self):
        """Create an infinite flat grid."""
        # Define the size of each grid cell
        self.spacing = 10.0  # Distance between grid lines
        
        # Define how many grid lines to draw in each direction from center
        grid_lines = 100  # Number of grid lines in each direction
        
        # Calculate the total size to render
        total_size = grid_lines * self.spacing
        
        # Create a LineSegs object to draw the lines
        lines = LineSegs()
        lines.set_color(1, 1, 1, 1)  # Set the color of the lines (white)
        
        # Draw grid lines along X-axis (east-west)
        for i in range(-grid_lines, grid_lines + 1):
            x = i * self.spacing
            lines.move_to(x, -total_size, 0)
            lines.draw_to(x, total_size, 0)
        
        # Draw grid lines along Y-axis (north-south)
        for i in range(-grid_lines, grid_lines + 1):
            y = i * self.spacing
            lines.move_to(-total_size, y, 0)
            lines.draw_to(total_size, y, 0)
        
        # Create a NodePath to hold the lines
        lines_node = lines.create()
        lines_np = NodePath(lines_node)
        lines_np.reparent_to(self.render)
    
    def update_flight(self, task):
        north, east = utils.calculate_north_east(
            self.vehicle_state.lat, 
            self.vehicle_state.lon, 
            self.center_lat, 
            self.center_lon
        )

        self.camera.setHpr(-self.vehicle_state.yaw, self.vehicle_state.pitch, self.vehicle_state.roll)
        self.camera.setPos(east, north, self.vehicle_state.alt) # xyz
        
        if self.mouseWatcherNode.hasMouse():
            self.mouse_keyboard_controls.elevator = self.mouseWatcherNode.getMouseY()
            self.mouse_keyboard_controls.rudder = self.mouseWatcherNode.getMouseX()

        return task.cont

    def increase_throttle(self):
        self.mouse_keyboard_controls.throttle += 0.25
        self.mouse_keyboard_controls.throttle = max(0, min(1, self.mouse_keyboard_controls.throttle))
    
    def decrease_throttle(self):
        self.mouse_keyboard_controls.throttle -= 0.25
        self.mouse_keyboard_controls.throttle = max(0, min(1, self.mouse_keyboard_controls.throttle))