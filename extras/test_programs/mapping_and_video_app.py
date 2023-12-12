import tkinter as tk
import tkintermapview
from tkinter import ttk
import cv2
from PIL import Image, ImageTk 
 
 
locations = [(73, (-35.3632889, 149.1652927)), (159, (-35.3632467, 149.1652594)), (103, (-35.36327, 149.1652015))]

class MappingVideoApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.locations = locations
        self.inital_zoom = 20
        self.initial_position = (-35.3632621, 149.1652374)

        self.mapFrame = tk.LabelFrame(self)
        self.mapFrame.pack(pady=20, side="right")

        self.map_widget = tkintermapview.TkinterMapView(self.mapFrame, width=500, height=500, corner_radius=0)
        self.map_widget.pack(fill="both", expand=True)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
        self.map_widget.set_position(self.initial_position[0], self.initial_position[1])
        self.map_widget.set_zoom(self.inital_zoom)

        # Define a video capture object 
        self.vid = cv2.VideoCapture(0) 

        # Declare the width and height in variables 
        width, height = 500, 500
        # Set the width and height 
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, width) 
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.videoFrame = tk.Label(self) 
        self.videoFrame.pack(side="right") 

        # Set Markers
        for location in locations:
            index = locations.index(location)
            text = "Landmine " + str(index)
            self.map_widget.set_marker(location[1][0], location[1][1], text=text)

        self.open_camera()
        # self.mapFrame.pack(pady=10)
        # self.map_widget.pack()
    
    def slide(self):
        self.map_widget.set_zoom(self.zoom_slider.get())
    
    def open_camera(self): 

        # Capture the video frame by frame 
        _, frame = self.vid.read() 

        # Convert image from one color space to other 
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 

        # Capture the latest frame and transform to image 
        captured_image = Image.fromarray(opencv_image) 

        # Convert captured image to photoimage 
        photo_image = ImageTk.PhotoImage(image=captured_image) 

        # Displaying photoimage in the label 
        self.videoFrame.photo_image = photo_image
        # self.videoFrame.photo_image.pack(fill="both", expand=True) 

        # Configure image in the label 
        self.videoFrame.configure(image=photo_image) 

        # Repeat the same process after every 10 seconds 
        self.videoFrame.after(10, self.open_camera) 
        


root = MappingVideoApp()
root.locations = locations



root.mainloop()