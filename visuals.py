from panda3d.core import LineSegs, Vec4
from direct.showbase.ShowBase import ShowBase

class Visuals(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Black background color
        self.win.setClearColor(Vec4(0, 0, 0, 1))

        # Disable default mouse camera control
        self.disableMouse()

        # Create a grid for the ground
        self.create_ground()

        self.roll = 0
        self.pitch = 0
        self.heading = 0
        self.north = 0
        self.east = 0
        self.down = -1

        # Add the flight control task
        self.taskMgr.add(self.update_flight, "update_flight")

    def create_ground(self):
        """Create a grid for the ground using LineSegs."""
        lines = LineSegs()
        lines.setThickness(1)  # Set the thickness of the grid lines
        lines.setColor(0.5, 0.5, 0.5, 1)  # Gray color for the grid

        grid_size = 10000  # Size of the grid
        spacing = 20  # Spacing between grid lines

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
    
    def update_flight_state(self, roll, pitch, heading, north, east, down):
        """Update the flight state variables."""
        self.roll = roll
        self.pitch = pitch
        self.heading = heading
        self.north = north
        self.east = east
        self.down = down

    def update_flight(self, task):
        self.camera.setHpr(-self.heading, self.pitch, self.roll)
        self.camera.setPos(self.east, self.north, -self.down)

        return task.cont