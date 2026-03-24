from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from image_readers import reader
from image_processors import processor
from image_writers import writer
from image_viewers import viewer
from gcode_visualizer import visualizer

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
flowrate = Entry(page, width=10)
flowrate.grid(row=2, column=1)

# flowstep input
Label(page, text="Flow Step (mm):").grid(row=3, column=0)
flowstep = Entry(page, width=10)
flowstep.grid(row=3, column=1)

# droplet input
Label(page, text="Number of Droplets per pixel:").grid(row=4, column=0)
num_drops = Entry(page, width=10)
num_drops.grid(row=4, column=1)

# delay input
Label(page, text="Delay Between Droplets (s):").grid(row=5, column=0)
delay = Entry(page, width=10)
delay.grid(row=5, column=1)

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

def run():

    IMAGE = window.image
    SHEET_SIZE = sheet_selection.get()
    PAINT_DROP_SIZE = int(paint_drop_diameter.get())
    COMPRESSION_TYPE = compression_selection.get()
    FLOW_STEP = int(flowstep.get())
    FLOW_RATE = int(flowrate.get())
    FEED_RATE = int(feedrate.get())
    DROPLETS = int(num_drops.get())
    DELAY = float(delay.get())
    COLOR1 = [int(a) for a in color1.get().split(',')]
    COLOR2 = [int(a) for a in color2.get().split(',')]
    COLOR3 = [int(a) for a in color3.get().split(',')]
    BASE_COLOR = [int(a) for a in base_color.get().split(',')]
    FILE_NAME = str(output_file_name.get())
    WRITE = bool(save_gcode.get())
    VISUALIZER_TYPE = visualization.get()

    image = reader(IMAGE, SHEET_SIZE)
    image = processor(image, BASE_COLOR, SHEET_SIZE, PAINT_DROP_SIZE, COMPRESSION_TYPE)
    writer(image, COLOR1, COLOR2, COLOR3, BASE_COLOR, WRITE, FILE_NAME, PAINT_DROP_SIZE, FLOW_STEP, DROPLETS, FEED_RATE, FLOW_RATE, DELAY)
    viewer(image, COLOR1, COLOR2, COLOR3, BASE_COLOR, SHEET_SIZE)
    coordinates, color_list = visualizer(FILE_NAME, VISUALIZER_TYPE, COLOR1, COLOR2, COLOR3)

    # Plot G-Code
    fig, ax = plt.subplots()

    #TODO fix redundant if statements in gcode_visualizer

    if VISUALIZER_TYPE == "Path":
        for i in range(len(coordinates)):
            plt.plot(coordinates[i][0], coordinates[i][1], color=color_list[i] , alpha=0.3)
    else:
        for i in range(len(coordinates)):
            plt.scatter(coordinates[i][0], coordinates[i][1], color=color_list[i] , alpha=0.3)

    plt.xlabel("X (mm)")
    plt.ylabel("Y (mm)")
    plt.title("G-Code")
    
    # plot data in tkinter window
    canvas = FigureCanvasTkAgg(fig, page)
    canvas.get_tk_widget().grid(row=5, column=3, rowspan=18)


# Apply settings button
Button(page, text="Apply Settings", command=run).grid(row=5, column=4)

def save_settings():
    SHEET_SIZE = sheet_selection.get()
    PAINT_DROP_SIZE = paint_drop_diameter.get()
    COMPRESSION_TYPE = compression_selection.get()
    FLOW_STEP = flowstep.get()
    FLOW_RATE = flowrate.get()
    FEED_RATE = feedrate.get()
    DROPLETS = num_drops.get()
    DELAY = delay.get()
    COLOR1 = color1.get()
    COLOR2 = color2.get()
    COLOR3 = color3.get()
    BASE_COLOR = base_color.get()
    FILE_NAME = output_file_name.get()
    WRITE = save_gcode.get()
    VISUALIZER_TYPE = visualization.get()

    settings = [SHEET_SIZE, PAINT_DROP_SIZE, COMPRESSION_TYPE, FLOW_STEP, FLOW_RATE, FEED_RATE, DROPLETS, DELAY, COLOR1, COLOR2, COLOR3, BASE_COLOR, FILE_NAME, WRITE, VISUALIZER_TYPE]

    settings_file = open("settings.pulp", 'w')

    for i in settings[:-1]:
        settings_file.write("%s\n" % i)
    settings_file.write(settings[-1])

    settings_file.close()

# save settings
Button(page, text="Save Settings", command=save_settings).grid(row=5, column=5)

def load_settings():
    settings_file = open("settings.pulp")
    lines = settings_file.readlines()

    sheet_selection.set(lines[0].replace("\n", ''))
    paint_drop_diameter.insert(0, lines[1].replace("\n", ''))
    compression_selection.set(lines[2].replace("\n", ''))
    flowstep.insert(0, lines[3].replace("\n", ''))
    flowrate.insert(0, lines[4].replace("\n", ''))
    feedrate.insert(0, lines[5].replace("\n", ''))
    num_drops.insert(0, lines[6].replace("\n", ''))
    delay.insert(0, lines[7].replace("\n", ''))
    color1.insert(0, lines[8].replace("\n", ''))
    color2.insert(0, lines[9].replace("\n", ''))
    color3.insert(0, lines[10].replace("\n", ''))
    base_color.insert(0, lines[11].replace("\n", ''))
    output_file_name.insert(0, lines[12].replace("\n", ''))
    save_gcode.set(bool(lines[13].replace("\n", '')))
    visualization.set(lines[14].replace("\n", ''))


# load settings
Button(page, text="Load Settings", command=load_settings).grid(row=6, column=5)

#visualization type selection
Label(page, text="Visualization:").grid(row=5, column=2)
visualization = StringVar(page)
visualization.set(VISUALIZE[0])
dropdown = OptionMenu(page, visualization, *VISUALIZE).grid(row=5, column=3)

# output file name
Label(page, text="Output File Name").grid(row=10, column=0)
output_file_name = Entry(page, width=10)
output_file_name.grid(row=10, column=1)

# save output
save_gcode = IntVar()
save_gcode_button = Checkbutton(page, text="Save G-Code", variable=save_gcode)
save_gcode_button.grid(row=10, column=2)

# persistent menu buttons
help_button = Button(menu, text="Help", command=None).grid(row=0, column=21)


mainloop()