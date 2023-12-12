import sys
from qgis.core import QgsApplication, QgsVectorLayer, QgsField, QgsGeometry, QgsFeature
from qgis.gui import QgsMapCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QVariant

class DroneMapApp(QMainWindow):
    def __init__(self, locations):
        super().__init__()
        self.title = "Drone Landmine Mapping"
        self.setGeometry(100, 100, 800, 600)
        self.locations = locations

        # Initialize QGIS application
        self.qgs = QgsApplication([], False)
        self.qgs.initQgis()

        self.initUI()

    # def initUI(self):
    #     self.setWindowTitle(self.title)

    #     # Create a map canvas
    #     self.canvas = QgsMapCanvas()
    #     self.canvas.setCanvasColor(QColor(255, 255, 255))
    #     self.canvas.enableAntiAliasing(True)

    #     # Create a widget to hold the map canvas
    #     self.map_widget = QWidget(self)
    #     self.map_widget.setLayout(QVBoxLayout())
    #     self.map_widget.layout().addWidget(self.canvas)
    #     self.setCentralWidget(self.map_widget)

    #     # Add landmine locations to the map
    #     self.add_landmine_locations()

#     def add_landmine_locations(self):
#         # Create a memory layer to store the landmine locations
#         layer_name = "Landmine Locations"
#         crs = QgsCoordinateReferenceSystem('EPSG:4326', QgsCoordinateReferenceSystem.PostgisCrsId)
#         self.landmine_layer = QgsVectorLayer("Point?crs={}".format(crs.toWkt()), layer_name, "memory")
#         provider = self.landmine_layer.dataProvider()
#         self.landmine_layer.startEditing()

#         # Add a field to store additional data, if needed
#         provider.addAttributes([QgsField("Description", QVariant.String)])

#         # Add landmine locations to the layer
#         for location in self.locations:
#             x, y = location  # Assuming the location is a tuple of (longitude, latitude)
#             point = QgsGeometry.fromPointXY(QgsPointXY(x, y))
#             feature = QgsFeature()
#             feature.setGeometry(point)
#             feature.setAttributes(["Landmine Description"])  # You can customize this field

#             self.landmine_layer.addFeature(feature)

#         self.landmine_layer.commitChanges()
#         QgsProject.instance().addMapLayer(self.landmine_layer)

# def main():
#     app = QApplication(sys.argv)
#     app.setApplicationName("Drone Landmine Mapping")

#     # Replace this with your dynamic list of landmine locations (latitude, longitude)
#     locations = [(35.123, -97.456), (35.456, -97.789), (35.789, -97.123)]

#     window = DroneMapApp(locations)
#     window.show()

#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()