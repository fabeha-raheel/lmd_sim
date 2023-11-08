from tkinter import *
import tkintermapview

root = Tk()
root.title('Tkinter MapView')
# root.iconbitmap('')
root.geometry('900x800')

def lookup():
    pass

def slide(e):
    pass

my_label = LabelFrame(root)
my_label.pack(pady=20)

map_widget = tkintermapview.TkinterMapView(my_label, width=800, height=600, corner_radius=0)

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

my_slider = Scale(my_frame, from_=4, to=20, orient=HORIZONTAL, command=slide)
my_slider.grid(row=0, column=2, padx=)

root.mainloop()