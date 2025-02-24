from panda3d.core import LineSegs, Vec4, PerspectiveLens
from direct.showbase.ShowBase import ShowBase

class Visuals(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Black background color
        self.win.setClearColor(Vec4(0, 0, 0, 1))

        # Set FOV
        lens = PerspectiveLens()
        lens.setFov(120)
        self.cam.node().setLens(lens)

        # Disable default mouse camera control
        self.disableMouse()

        # Create a grid for the ground
        self.create_ground()

        self.roll = 0
        self.pitch = 0
        self.heading = 0
        self.north = 0
        self.east = 0
        self.down = 0

        # Add the flight control task
        self.taskMgr.add(self.update_flight, "update_flight")

    def create_ground(self):
        """Create a grid for the ground using LineSegs."""
        lines = LineSegs()
        lines.setThickness(1)  # Set the thickness of the grid lines
        lines.setColor(0.5, 0.5, 0.5, 1)  # Gray color for the grid

        grid_size = 10000  # Size of the grid
        spacing = 10  # Spacing between grid lines

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

        self.create_runway()

    def create_runway(self):
        """Create a grey runway on the grid."""
        runway_lines = LineSegs()
        runway_lines.setThickness(2)  # Thicker lines for the runway
        runway_lines.setColor(1, 1, 0, 1)  # Grey color for the runway

        # Define runway dimensions
        runway_length = 50  # Length of the runway
        runway_width = 400  # Width of the runway

        # Draw the runway outline
        runway_lines.moveTo(-runway_length / 2, -runway_width / 2, 0)
        runway_lines.drawTo(runway_length / 2, -runway_width / 2, 0)
        runway_lines.drawTo(runway_length / 2, runway_width / 2, 0)
        runway_lines.drawTo(-runway_length / 2, runway_width / 2, 0)
        runway_lines.drawTo(-runway_length / 2, -runway_width / 2, 0)

        # Create the runway node and attach it to the scene
        runway_node = runway_lines.create()
        runway = self.render.attachNewNode(runway_node)
        runway.setPos(0, 300, 0)  # Center the runway at the origin
    
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