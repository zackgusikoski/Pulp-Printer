from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt

NUM_COLUMNS = 30
NUM_ROWS = 60
COMPRESSION = ["Linear", "Cubic", "Nearest", "Area", "Lanczos"]
SHEET = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7"]
VISUALIZE = ["Dots", "Path"]

# create window
window = Tk()
window.title("Pulp Painter")

# set window size and set window to be a fixed size
window.geometry("1000x650")

# add logo to window
window.iconphoto(False, PhotoImage(file="test_image30.jpg"))

# define menu frame
menu = Frame(window).grid(row=0, column=0, columnspan=NUM_COLUMNS, sticky="ew")

# define main page properties
page = Frame(window).grid(row=1, rowspan=NUM_ROWS, column=0, sticky="ns")

# define grid in rows and columns
for i in range(NUM_COLUMNS):
    window.grid_columnconfigure(i, weight=1)

for i in range(NUM_ROWS):
    window.grid_columnconfigure(i, weight=1)


# Machine Inputs
# feedrate input
Label(page, text="Feed Rate (mm/min):").grid(row=1, column=0)
feedrate = Entry(page, width=10)
feedrate.grid(row=1, column=1)

# flowrate input
Label(page, text="Flow Rate (mm/min):").grid(row=2, column=0)
feedrate = Entry(page, width=10)
feedrate.grid(row=2, column=1)

# flowstep input
Label(page, text="Flow Step (mm):").grid(row=3, column=0)
feedrate = Entry(page, width=10)
feedrate.grid(row=3, column=1)

# droplet input
Label(page, text="Number of Droplets per pixel:").grid(row=4, column=0)
feedrate = Entry(page, width=10)
feedrate.grid(row=4, column=1)

# delay input
Label(page, text="Delay Between Droplets (s):").grid(row=5, column=0)
feedrate = Entry(page, width=10)
feedrate.grid(row=5, column=1)

# Art Inputs
# image selection
def image_selection():
    window.image = filedialog.askopenfilename(title="Select an Image", filetypes=(("Image Files", "*.jpg"), ("Image Files", "*.png"), ("All Files", "*.*")))
    # display image name
    image_name = window.image.split('/')
    Label(page, text=image_name[-1]).grid(row=1, column=3)

# image selection button
Button(page, text="Select Image", command=image_selection).grid(row=1, column=2)

# compression selection
Label(page, text="Image Resizing:").grid(row=2, column=2)
compression_selection = StringVar(page)
compression_selection.set(COMPRESSION[0])
dropdown = OptionMenu(page, compression_selection, *COMPRESSION).grid(row=2, column=3)

# paint drop size input
Label(page, text="Paint Drop Diameter (mm):").grid(row=3, column=2)
paint_drop_diameter = Entry(page, width=10)
paint_drop_diameter.grid(row=3, column=3)

# sheet size selection
Label(page, text="Sheet Size:").grid(row=4, column=2)
sheet_selection = StringVar(page)
sheet_selection.set(SHEET[0])
dropdown = OptionMenu(page, sheet_selection, *SHEET).grid(row=4, column=3)

# color1 input
Label(page, text="Color 1 (r, g, b):").grid(row=1, column=4)
color1 = Entry(page, width=10)
color1.grid(row=1, column=5)

# color2 input
Label(page, text="Color 2 (r, g, b):").grid(row=2, column=4)
color2 = Entry(page, width=10)
color2.grid(row=2, column=5)

# color3 input
Label(page, text="Color 3 (r, g, b):").grid(row=3, column=4)
color3 = Entry(page, width=10)
color3.grid(row=3, column=5)

# base color input
Label(page, text="Base Color (r, g, b):").grid(row=4, column=4)
base_color = Entry(page, width=10)
base_color.grid(row=4, column=5)

#visualization type selection
Label(page, text="Visualization:").grid(row=5, column=2)
visualization = StringVar(page)
visualization.set(VISUALIZE[0])
dropdown = OptionMenu(page, visualization, *VISUALIZE).grid(row=5, column=3)

# persistent menu buttons
help_button = Button(menu, text="Help", command=None).grid(row=0, column=21)


mainloop()