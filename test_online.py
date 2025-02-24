import sys
import folium
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl  # Import QUrl to handle URLs

class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Folium Map in PyQt5")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and set the layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a QWebEngineView to display the Folium map
        self.browser = QWebEngineView()
        layout.addWidget(self.browser)

        # Create a Folium map
        self.map = folium.Map(location=[45.5236, -122.6750], zoom_start=13)

        # Save the map to an HTML file
        self.map.save("map.html")

        # Load the HTML file into the QWebEngineView using QUrl
        self.browser.setUrl(QUrl.fromLocalFile("map.html"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec_())