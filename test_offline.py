import sys
import os
import folium
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

# Step 1: Save map tiles locally
def save_map_tiles(location, zoom_level, save_path):
    """
    Creates a folium map and saves it as an HTML file.
    """
    # Create a folium map
    m = folium.Map(location=location, zoom_start=zoom_level)

    # Add a marker for the location (optional)
    folium.Marker(location).add_to(m)

    # Save the map to an HTML file
    m.save(save_path)
    print(f"Map saved to {save_path}")

# Step 2: Create a PyQt5 application to display the offline map
class MapWindow(QMainWindow):
    def __init__(self, map_file_path):
        super().__init__()

        # Set up the main window
        # self.setWindowTitle("Offline Map")
        # self.setGeometry(100, 100, 800, 600)

        # Create a QWebEngineView to display the map
        self.browser = QWebEngineView()

        # Load the offline map HTML file using QUrl
        self.browser.setUrl(QUrl.fromLocalFile(os.path.abspath(map_file_path)))

        # Set the central widget
        self.setCentralWidget(self.browser)

# Main function
def main():
    # Define the location and zoom level
    location = [40.7128, -74.0060]  # New York City coordinates
    zoom_level = 13

    # Define the path to save the offline map
    save_path = "offline_map.html"

    # Step 1: Save the map tiles
    save_map_tiles(location, zoom_level, save_path)

    # Step 2: Create and run the PyQt5 application
    app = QApplication(sys.argv)
    window = MapWindow(save_path)
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()