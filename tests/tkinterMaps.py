from tkinter import *
import tkintermapview
from tkinter import ttk

root = Tk()
root.title('Tkinter MapView')
# root.iconbitmap('')
root.geometry('900x800')

def lookup():
    map_widget.set_position(36.1699, -115.1396)
    my_slider.config(value=9)

def slide(e):
    map_widget.set_zoom(my_slider.get())

my_label = LabelFrame(root)
my_label.pack(pady=20)

map_widget = tkintermapview.TkinterMapView(my_label, width=800, height=600, corner_radius=0)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite

# Set Coordinates
map_widget.set_position(36.1699, -115.1396)

# Set zoom level
map_widget.set_zoom(10)

map_widget.pack()

my_frame = LabelFrame(root)
my_frame.pack(pady=10)

my_entry = Entry(my_frame, font=("Helvetica", 28))
my_entry.grid(row=0, column=0, pady=20, padx=10)

my_button = Button(my_frame, text="Lookup", font=("Helvetica", 18), command=lookup)
my_button.grid(row=0, column=1, padx=10)

my_slider = ttk.Scale(my_frame, from_=4, to=20, orient=HORIZONTAL, command=slide, value=20, length=220)
my_slider.grid(row=0, column=2, padx=10)

root.mainloop()