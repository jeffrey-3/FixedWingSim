from panda3d.core import loadPrcFileData
from panda3d.core import PerspectiveLens
from panda3d.core import LPoint3, LVector3
from panda3d.core import Geom, GeomNode, GeomVertexFormat, GeomVertexData
from panda3d.core import GeomVertexWriter, GeomLines
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
import math
import time

# Configure Panda3D window
loadPrcFileData("", "window-title Panda3D Flight Simulator")
loadPrcFileData("", "win-size 800 600")
loadPrcFileData("", "fullscreen false")
loadPrcFileData("", "show-frame-rate-meter true")

class FlightSimulator(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Set background color to black
        self.win.setClearColor((0, 0, 0, 1))

        # Create a grid for the ground
        self.create_ground()

        # Set up the camera
        self.camera.setPos(0, 0, 10)  # Start above the ground
        self.camera.lookAt(0, 0, 0)

        # Fake data for movement
        self.velocity = LVector3(0, 1, 0)  # Move forward along the Y-axis
        self.angle = 0  # For simulating rotation

        # Add the update task
        self.taskMgr.add(self.update, "update_task")

        self.start_time = time.time()

    def create_ground(self):
        # Create a grid using GeomNode
        grid_node = GeomNode("grid")

        # Define vertex format and data
        vformat = GeomVertexFormat.getV3()
        vdata = GeomVertexData("grid_data", vformat, Geom.UHStatic)

        # Vertex writer
        vertex = GeomVertexWriter(vdata, "vertex")

        # Create grid lines
        lines = GeomLines(Geom.UHStatic)
        size = 1000  # Size of the grid
        step = 10  # Spacing between lines

        # Horizontal lines
        for x in range(-size, size + 1, step):
            vertex.addData3(x, -size, 0)
            vertex.addData3(x, size, 0)
            lines.addNextVertices(2)

        # Vertical lines
        for y in range(-size, size + 1, step):
            vertex.addData3(-size, y, 0)
            vertex.addData3(size, y, 0)
            lines.addNextVertices(2)

        # Create the Geom object and add the lines to it
        grid_geom = Geom(vdata)
        grid_geom.addPrimitive(lines)

        # Add the Geom to the GeomNode
        grid_node.addGeom(grid_geom)

        # Attach the grid to the scene
        grid = self.render.attachNewNode(grid_node)
        grid.setColor(0.5, 0.5, 0.5, 1)  # Gray color for the grid

    def update(self, task):
        # Simulate movement using fake data
        dt = self.start_time - time.time()  # Access globalClock via self

        # Move the camera forward
        self.camera.setPos(0, -2*dt, 10)

        # Simulate a slight rotation (yaw)
        # self.angle += 0.001 * dt
        # self.camera.setHpr(self.angle * 50, 0, 0)  # Tilt slightly for realism

        return task.cont

# Run the simulator
app = FlightSimulator()
app.run()