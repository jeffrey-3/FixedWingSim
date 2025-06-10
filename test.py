import numpy as np
import matplotlib.pyplot as plt

class L1Controller:
    def __init__(self, L1_gain=1.5, k=0.6, T=0.1):
        """
        Initializes the L1 path-following controller.
        :param L1_gain: The main L1 gain parameter.
        :param k: Adaptation gain for robustness.
        :param T: Time constant for control law.
        """
        self.L1_gain = L1_gain  # L1 adaptive gain
        self.k = k  # Adaptation gain
        self.T = T  # Control law time constant

    def compute_control(self, velocity, course_angle, path_angle, wind_velocity=np.array([0, 0])):
        """
        Computes the lateral control command (roll angle or yaw rate).
        :param velocity: UAV airspeed (m/s).
        :param course_angle: Current UAV heading/course (radians).
        :param path_angle: Desired path direction (radians).
        :param wind_velocity: Wind velocity vector [Vx, Vy] (m/s).
        :return: Desired roll angle (phi_command) in radians.
        """
        # Compute cross-track error (e_y)
        path_tangent = np.array([np.cos(path_angle), np.sin(path_angle)])
        uav_velocity = np.array([velocity * np.cos(course_angle), velocity * np.sin(course_angle)]) - wind_velocity
        cross_track_error = np.cross(path_tangent, uav_velocity)

        # Compute desired course rate
        omega_command = -self.L1_gain * cross_track_error

        # Apply adaptive control law
        phi_command = np.arctan2(self.k * omega_command, velocity)

        return phi_command

# Simulation parameters
dt = 0.1  # Time step (s)
total_time = 100  # Simulation duration (s)
num_steps = int(total_time / dt)

# UAV Parameters
velocity = 15.0  # m/s (constant speed assumption)
initial_heading = np.radians(30)  # Initial heading in radians
wind_velocity = np.array([2, 1])  # Wind in x, y (m/s)

# Define waypoints for the UAV to follow (X, Y coordinates in meters)
waypoints = np.array([[0, 0], [100, 50], [200, 150], [300, 200], [400, 250]])

# Initialize UAV state
x, y = 0, 0  # Initial position
heading = initial_heading  # Initial heading (rad)
phi = 0  # Initial roll angle (rad)

# Initialize Controller
controller = L1Controller()

# Data Logging
x_log, y_log, waypoint_log = [], [], []
current_waypoint_idx = 1  # Start at first target waypoint

# Run Simulation with Waypoints
for _ in range(num_steps):
    # Get current and next waypoint
    if current_waypoint_idx < len(waypoints):
        waypoint = waypoints[current_waypoint_idx]
        
        # Compute desired path angle to the next waypoint
        path_angle = np.arctan2(waypoint[1] - y, waypoint[0] - x)

        # Compute control command
        phi = controller.compute_control(velocity, heading, path_angle, wind_velocity)

        # Update UAV position and heading
        x += velocity * np.cos(heading) * dt
        y += velocity * np.sin(heading) * dt
        turn_rate = (9.81 / velocity) * np.tan(phi)  # Yaw rate from bank angle
        heading += turn_rate * dt

        # Check if waypoint is reached
        distance_to_waypoint = np.linalg.norm([waypoint[0] - x, waypoint[1] - y])
        if distance_to_waypoint < 20:  # Switch to next waypoint if close enough
            current_waypoint_idx += 1

    # Log data
    x_log.append(x)
    y_log.append(y)
    waypoint_log.append(current_waypoint_idx)

# Plot the UAV path and waypoints
plt.figure(figsize=(10, 6))
plt.plot(x_log, y_log, label="UAV Path", color="b")
plt.scatter(waypoints[:, 0], waypoints[:, 1], color="r", label="Waypoints", zorder=3)
plt.scatter([x_log[0]], [y_log[0]], color="g", label="Start Position", zorder=3)
plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.title("L1 Path Following with Waypoints")
plt.legend()
plt.grid()
plt.axis("equal")
plt.show()
