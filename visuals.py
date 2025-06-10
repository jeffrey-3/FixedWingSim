from panda3d.core import LineSegs, WindowProperties
from direct.showbase.ShowBase import ShowBase
from panda3d.core import LineSegs, NodePath
from direct.showbase.ShowBase import ShowBase
import numpy as np
import math
import utils

class Visuals(ShowBase):
    def __init__(self, rwy_lat, rwy_lon, rwy_hdg):
        ShowBase.__init__(self)

        self.rwy_lat = rwy_lat
        self.rwy_lon = rwy_lon
        self.rwy_hdg = rwy_hdg

        props = WindowProperties()
        props.setTitle("UAV Simulation")
        self.win.requestProperties(props)

        # Disable default mouse camera control
        self.disableMouse()

        # Create a grid for the ground
        self.create_terrain_mesh()
        self.create_runway()

        self.roll = 0
        self.pitch = 0
        self.heading = 0
        self.north = 0
        self.east = 0
        self.down = 0
        self.terrain_height = 0

        self.rudder = 0
        self.elevator = 0
        self.throttle = 1001

        # Add the flight control task
        self.taskMgr.add(self.update_flight, "update_flight")
        self.taskMgr.add(self.get_mouse_pos, "MousePositionTask")

        # Accept key events
        self.accept("w", self.change_throttle, [1])
        self.accept("s", self.change_throttle, [-1])
        self.accept("l", self.hand_launch)
    
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

    def get_terrain_height(self, x, y):
        """Calculate the terrain height at a given (x, y) position using bilinear interpolation."""
        # Normalize the position to grid coordinates
        grid_x = (x + (self.grid_size * self.spacing / 2)) / self.spacing
        grid_y = (y + (self.grid_size * self.spacing / 2)) / self.spacing

        # Get the indices of the surrounding grid points
        x1 = int(grid_x)
        y1 = int(grid_y)
        x2 = min(x1 + 1, self.grid_size - 1)
        y2 = min(y1 + 1, self.grid_size - 1)

        # Get the heights of the surrounding grid points
        h11 = self.lookup_table[x1][y1]
        h12 = self.lookup_table[x1][y2]
        h21 = self.lookup_table[x2][y1]
        h22 = self.lookup_table[x2][y2]

        # Perform bilinear interpolation
        dx = grid_x - x1
        dy = grid_y - y1
        height = (h11 * (1 - dx) * (1 - dy) +
                 h21 * dx * (1 - dy) +
                 h12 * (1 - dx) * dy +
                 h22 * dx * dy)

        return height

    def create_runway(self):
        """Create a grey runway on the grid."""
        runway_lines = LineSegs()
        runway_lines.setThickness(5)  # Thicker lines for the runway
        runway_lines.setColor(1, 1, 0, 1)  # Grey color for the runway

        # Define runway dimensions
        runway_length = 400  # Length of the runway
        runway_width = 10  # Width of the runway

        # Draw the runway outline
        runway_lines.moveTo(-runway_width / 2, -runway_length / 2, 0)
        runway_lines.drawTo(runway_width / 2, -runway_length / 2, 0)
        runway_lines.drawTo(runway_width / 2, runway_length / 2, 0)
        runway_lines.drawTo(-runway_width / 2, runway_length / 2, 0)
        runway_lines.drawTo(-runway_width / 2, -runway_length / 2, 0)

        # Create the runway node and attach it to the scene
        runway_node = runway_lines.create()
        runway = self.render.attachNewNode(runway_node)
        runway.setPos(runway_length/2 * math.sin(math.radians(self.rwy_hdg)), runway_length/2 * math.cos(math.radians(self.rwy_hdg)), 0)  # Center the runway at the origin
        runway.setHpr(-self.rwy_hdg, 0, 0)
    
    def update_state(self, roll, pitch, heading, lat, lon, alt):
        north, east = utils.calculate_north_east(lat, lon, self.rwy_lat, self.rwy_lon)
        self.roll = roll
        self.pitch = pitch
        self.heading = heading
        self.north = north
        self.east = east
        self.down = -alt

    def update_flight(self, task):
        self.terrain_height = self.get_terrain_height(self.east, self.north)
        self.camera.setHpr(-self.heading, self.pitch, self.roll)
        self.camera.setPos(self.east, self.north, -self.down) # xyz
        return task.cont

    def get_mouse_pos(self, task):
        if self.mouseWatcherNode.hasMouse():
            self.rudder = utils.map_range(self.mouseWatcherNode.getMouseX(), -1, 1, 1000, 2000)
            self.elevator = utils.map_range(self.mouseWatcherNode.getMouseY(), -1, 1, 1000, 2000)
        return task.cont

    def change_throttle(self, delta):
        self.throttle += delta * 250  # Adjust step size
        self.throttle = max(1000, min(2000, self.throttle))  # Clamp between 1000 and 2000
    
    def hand_launch(self):
        print("Hand launch")