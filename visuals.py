from panda3d.core import LineSegs, WindowProperties
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, NodePath
from direct.showbase.ShowBase import ShowBase
import numpy as np
import math
import utils
from queue import Queue
from flight_dynamics import VehicleState
from hardware_interface import ControlInput

class Visuals(ShowBase):
    def __init__(self, center_lat, center_lon, vehicle_state_queue: Queue, mouse_keyboard_controls_queue: Queue):
        ShowBase.__init__(self)

        self.center_lat = center_lat
        self.center_lon = center_lon
        self.vehicle_state_queue = vehicle_state_queue
        self.mouse_keyboard_controls_queue = mouse_keyboard_controls_queue

        props = WindowProperties()
        props.setTitle("UAV Simulation")
        self.win.requestProperties(props)

        # Disable default mouse camera control
        self.disableMouse()

        # Create a grid for the ground
        self.create_terrain_mesh()

        self.throttle = 0

        # Add the flight control task
        self.taskMgr.add(self.update_flight, "update_flight")

        # Accept key events
        self.accept("w", self.increase_throttle)
        self.accept("s", self.decrease_throttle)
    
    def create_terrain_mesh(self):
        """Create a terrain mesh using a manually defined lookup table."""
        # Define the size of the terrain grid
        self.grid_size = 200  # Number of grid cells
        self.spacing = 10.0  # Distance between grid points

        # Manually define the lookup table for terrain height
        self.lookup_table = np.zeros((self.grid_size, self.grid_size))
        # self.lookup_table[80:100, 90:100] = 30
        # self.lookup_table[70:80, 90:100] = 10

        # Calculate the total size of the terrain
        total_size = self.grid_size * self.spacing

        # Calculate the offset to center the mesh
        offset = total_size / 2

        # Create a LineSegs object to draw the lines
        lines = LineSegs()
        lines.set_color(1, 1, 1, 1)  # Set the color of the lines (white)

        # Draw the grid lines using the lookup table for height
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                # Get height from the lookup table
                height = self.lookup_table[x][y]

                # Draw lines along the X-axis
                if x < self.grid_size - 1:
                    next_height_x = self.lookup_table[x + 1][y]
                    lines.move_to(x * self.spacing - offset, y * self.spacing - offset, height)
                    lines.draw_to((x + 1) * self.spacing - offset, y * self.spacing - offset, next_height_x)

                # Draw lines along the Y-axis
                if y < self.grid_size - 1:
                    next_height_y = self.lookup_table[x][y + 1]
                    lines.move_to(x * self.spacing - offset, y * self.spacing - offset, height)
                    lines.draw_to(x * self.spacing - offset, (y + 1) * self.spacing - offset, next_height_y)

        # Create a NodePath to hold the lines
        lines_node = lines.create()
        lines_np = NodePath(lines_node)
        lines_np.reparent_to(self.render)
    
    def update_flight(self, task):
        if self.vehicle_state_queue.not_empty():
            vehicle_state: VehicleState = self.vehicle_state_queue.get()

            north, east = utils.calculate_north_east(
                vehicle_state.lat, 
                vehicle_state.lon, 
                self.center_lat, 
                self.center_lon
            )

            self.camera.setHpr(-vehicle_state.yaw, vehicle_state.pitch, vehicle_state.roll)
            self.camera.setPos(east, north, -vehicle_state.alt) # xyz
        
        if self.mouseWatcher.hasMouse():
            self.mouse_keyboard_controls_queue.put(
                ControlInput(
                    self.mouseWatcherNode.getMouseY(),
                    self.mouseWatcherNode.getMouseX(),
                    self.throttle
                )
            )

        return task.cont

    def increase_throttle(self):
        self.throttle += 0.25
        self.throttle = max(0, min(1, self.throttle))
    
    def decrease_throttle(self):
        self.throttle -= 0.25
        self.throttle = max(0, min(1, self.throttle))