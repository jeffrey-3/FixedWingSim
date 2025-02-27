from panda3d.core import LineSegs, Vec4, WindowProperties
from direct.showbase.ShowBase import ShowBase
from utils import *

class Visuals(ShowBase):
    def __init__(self, rwy_lat, rwy_lon, rwy_hdg):
        ShowBase.__init__(self)

        self.rwy_lat = rwy_lat
        self.rwy_lon = rwy_lon
        self.rwy_hdg = rwy_hdg

        props = WindowProperties()
        props.setTitle("UAV Simulation")
        self.win.requestProperties(props)

        # Black background color
        self.win.setClearColor(Vec4(0, 0, 0, 1))

        # Disable default mouse camera control
        self.disableMouse()

        # Create a grid for the ground
        self.create_ground()
        self.create_runway()

        self.roll = 0
        self.pitch = 0
        self.heading = 0
        self.north = 0
        self.east = 0
        self.down = 0

        self.aileron = 0
        self.elevator = 0
        self.throttle = 0.0001

        # Add the flight control task
        self.taskMgr.add(self.update_flight, "update_flight")
        self.taskMgr.add(self.get_mouse_pos, "MousePositionTask")

        # Accept key events
        self.accept("w", self.change_throttle, [1])
        self.accept("s", self.change_throttle, [-1])

    def create_ground(self):
        """Create a grid for the ground using LineSegs."""
        lines = LineSegs()
        lines.setThickness(1)  # Set the thickness of the grid lines
        lines.setColor(1, 1, 1, 0.2)  # Gray color for the grid

        grid_size = 1000  # Size of the grid
        spacing = 5  # Spacing between grid lines

        # Draw horizontal lines
        for i in range(-grid_size, grid_size + 1, spacing):
            lines.moveTo(i, -grid_size, 0)
            lines.drawTo(i, grid_size, 0)

        # Draw vertical lines
        for i in range(-grid_size, grid_size + 1, spacing):
            lines.moveTo(-grid_size, i, 0)
            lines.drawTo(grid_size, i, 0)

        # Create the grid node and attach it to the scene
        grid_node = lines.create()
        grid = self.render.attachNewNode(grid_node)
        grid.setPos(0, 0, 0)

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
        runway.setPos(0, 0, 0)  # Center the runway at the origin
        runway.setHpr(-self.rwy_hdg, 0, 0)
    
    def update_state(self, roll, pitch, heading, lat, lon, alt):
        north, east = calculate_north_east(lat, lon, self.rwy_lat, self.rwy_lon)
        self.roll = roll
        self.pitch = pitch
        self.heading = heading
        self.north = north
        self.east = east
        self.down = -alt

    def update_flight(self, task):
        self.camera.setHpr(-self.heading, self.pitch, self.roll)
        self.camera.setPos(self.east, self.north, -self.down) # xyz

        return task.cont

    def get_mouse_pos(self, task):
        if self.mouseWatcherNode.hasMouse():
            self.aileron = self.mouseWatcherNode.getMouseX()
            self.elevator = self.mouseWatcherNode.getMouseY()
        return task.cont  # Continue the task

    def change_throttle(self, delta):
        self.throttle += delta * 0.25  # Adjust step size
        self.throttle = max(0.0, min(1.0, self.throttle))  # Clamp between 0 and 1