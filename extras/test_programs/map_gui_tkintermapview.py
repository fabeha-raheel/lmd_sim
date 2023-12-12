import tkinter as tk
import tkintermapview
from tkinter import ttk
 
 
locations = [(73, (-35.3632889, 149.1652927)), (159, (-35.3632467, 149.1652594)), (103, (-35.36327, 149.1652015))]

class MappingApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.locations = locations
        self.inital_zoom = 20
        self.initial_position = (-35.3632621, 149.1652374)

        self.label = tk.LabelFrame(self)
        self.label.pack(pady=20)

        self.map_widget = tkintermapview.TkinterMapView(self.label, width=1000, height=700, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
        self.map_widget.set_position(self.initial_position[0], self.initial_position[1])
        self.map_widget.set_zoom(self.inital_zoom)
        # self.mapFrame = tk.LabelFrame(self)
        # self.zoom_slider = ttk.Scale(self.mapFrame, from_=4, to=20, orient=tk.HORIZONTAL, command=self.slide, value=20, length=220)

        # Set Markers
        for location in locations:
            index = locations.index(location)
            text = "Landmine " + str(index)
            self.map_widget.set_marker(location[1][0], location[1][1], text=text)

        
        # self.mapFrame.pack(pady=10)
        # self.map_widget.pack()
    
    def slide(self):
        self.map_widget.set_zoom(self.zoom_slider.get())
        


root = MappingApp()
root.locations = locations
root.mainloop()