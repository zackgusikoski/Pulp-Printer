import tkinter
from tkinter import *
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from image_readers import reader
from image_processors import processor
from image_writers import writer
from image_viewers import viewer
from gcode_visualizer import visualizer
import cv2


NUM_COLUMNS = 30
NUM_ROWS = 60
COMPRESSION = ["Linear", "Cubic", "Nearest", "Area", "Lanczos"]
SHEET = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7"]
VISUALIZE = ["Dots", "Path"]
PROCESSORS = ["Shades", "Channels"]

# create window class
class window(tkinter.Tk):
    def __init__(self):
        super().__init__()  # initialize Tk
        self.title("Pulp Painter")

        # set window size and set window to be a fixed size
        self.geometry("1000x650")

        # add logo to window
        #self.iconphoto(False, PhotoImage(file="logo.png"))

        # define menu frame
        self.menu = Frame(self).grid(row=0, column=0, columnspan=NUM_COLUMNS, sticky="ew")

        # define main self.page properties
        self.page = Frame(self).grid(row=1, rowspan=NUM_ROWS, column=0, sticky="ns")

        # define grid in rows and columns
        for i in range(NUM_COLUMNS):
            self.grid_columnconfigure(i, weight=1)

        for i in range(NUM_ROWS):
            self.grid_columnconfigure(i, weight=1)


        # Machine Inputs
        # feedrate input
        Label(self.page, text="Feed Rate (mm/min):").grid(row=1, column=0)
        self.feedrate = Entry(self.page, width=10)
        self.feedrate.grid(row=1, column=1)

        # flowrate input
        Label(self.page, text="Flow Rate (mm/min):").grid(row=2, column=0)
        self.flowrate = Entry(self.page, width=10)
        self.flowrate.grid(row=2, column=1)

        # flowstep input
        Label(self.page, text="Flow Step (mm):").grid(row=3, column=0)
        self.flowstep = Entry(self.page, width=10)
        self.flowstep.grid(row=3, column=1)

        # droplet input
        Label(self.page, text="Number of Droplets per pixel:").grid(row=4, column=0)
        self.num_drops = Entry(self.page, width=10)
        self.num_drops.grid(row=4, column=1)

        # delay input
        Label(self.page, text="Delay Between Droplets (s):").grid(row=5, column=0)
        self.delay = Entry(self.page, width=10)
        self.delay.grid(row=5, column=1)

        # Art Inputs
        # image selection button
        Button(self.page, text="Select Image", command=self.image_selection).grid(row=1, column=2)

        # compression selection
        Label(self.page, text="Image Resizing:").grid(row=2, column=2)
        self.compression_selection = StringVar(self.page)
        self.compression_selection.set(COMPRESSION[0])
        dropdown = OptionMenu(self.page, self.compression_selection, *COMPRESSION).grid(row=2, column=3)

        # paint drop size input
        Label(self.page, text="Paint Drop Diameter (mm):").grid(row=3, column=2)
        self.paint_drop_diameter = Entry(self.page, width=10)
        self.paint_drop_diameter.grid(row=3, column=3)

        # sheet size selection
        Label(self.page, text="Sheet Size:").grid(row=4, column=2)
        self.sheet_selection = StringVar(self.page)
        self.sheet_selection.set(SHEET[0])
        dropdown = OptionMenu(self.page, self.sheet_selection, *SHEET).grid(row=4, column=3)

        # color1 input
        Label(self.page, text="Color 1 (r, g, b):").grid(row=1, column=4)
        self.color1 = Entry(self.page, width=10)
        self.color1.grid(row=1, column=5)

        # color2 input
        Label(self.page, text="Color 2 (r, g, b):").grid(row=2, column=4)
        self.color2 = Entry(self.page, width=10)
        self.color2.grid(row=2, column=5)

        # color3 input
        Label(self.page, text="Color 3 (r, g, b):").grid(row=3, column=4)
        self.color3 = Entry(self.page, width=10)
        self.color3.grid(row=3, column=5)

        # base color input
        Label(self.page, text="Base Color (r, g, b):").grid(row=4, column=4)
        self.base_color = Entry(self.page, width=10)
        self.base_color.grid(row=4, column=5)


        # Apply settings button
        Button(self.page, text="Apply Settings", command=self.run).grid(row=4, column=6)

        # save settings
        Button(self.page, text="Save Settings", command=self.save_settings).grid(row=1, column=6)


        # load settings
        Button(self.page, text="Load Settings", command=self.load_settings).grid(row=2, column=6)

        #visualization type selection
        Label(self.page, text="Visualization:").grid(row=5, column=4)
        self.visualization = StringVar(self.page)
        self.visualization.set(VISUALIZE[0])
        dropdown = OptionMenu(self.page, self.visualization, *VISUALIZE).grid(row=5, column=5)

        #processor type selection
        Label(self.page, text="Color Separation:").grid(row=5, column=2)
        self.processor_selection = StringVar(self.page)
        self.processor_selection.set(PROCESSORS[0])
        dropdown = OptionMenu(self.page, self.processor_selection, *PROCESSORS).grid(row=5, column=3)

        # output file name
        Label(self.page, text="Output File Name").grid(row=10, column=0)
        self.output_file_name = Entry(self.page, width=10)
        self.output_file_name.grid(row=10, column=1)

        # save output
        self.save_gcode = IntVar()
        self.save_gcode_button = Checkbutton(self.page, text="Save G-Code", variable=self.save_gcode)
        self.save_gcode_button.grid(row=10, column=2)

        # persistent menu buttons
        help_button = Button(self.menu, text="Help", command=None).grid(row=0, column=21)
    
    # image selection
    def image_selection(self):
        self.image = filedialog.askopenfilename(title="Select an Image", filetypes=(("Image Files", "*.jpg"), ("Image Files", "*.png"), ("All Files", "*.*")))
        # display image name
        image_name = self.image.split('/')
        Label(self.page, text=image_name[-1]).grid(row=1, column=3)
    
    def run(self):

            IMAGE = self.image
            SHEET_SIZE = self.sheet_selection.get()
            PAINT_DROP_SIZE = int(self.paint_drop_diameter.get())
            COMPRESSION_TYPE = self.compression_selection.get()
            FLOW_STEP = float(self.flowstep.get())
            FLOW_RATE = int(self.flowrate.get())
            FEED_RATE = int(self.feedrate.get())
            DROPLETS = int(self.num_drops.get())
            DELAY = float(self.delay.get())
            COLOR1 = [int(a) for a in self.color1.get().split(',')]
            COLOR2 = [int(a) for a in self.color2.get().split(',')]
            COLOR3 = [int(a) for a in self.color3.get().split(',')]
            PROCESSOR_TYPE = self.processor_selection.get()

            if self.base_color.get() != '':
                BASE_COLOR = [int(a) for a in self.base_color.get().split(',')]
            else:
                 BASE_COLOR = "NA"


            FILE_NAME = str(self.output_file_name.get())
            WRITE = bool(self.save_gcode.get())
            VISUALIZER_TYPE = self.visualization.get()

            image = reader(IMAGE, SHEET_SIZE)
            image = processor(image, BASE_COLOR, SHEET_SIZE, PAINT_DROP_SIZE, COMPRESSION_TYPE, PROCESSOR_TYPE)
            writer(image, COLOR1, COLOR2, COLOR3, BASE_COLOR, WRITE, FILE_NAME, PAINT_DROP_SIZE, FLOW_STEP, DROPLETS, FEED_RATE, FLOW_RATE, DELAY)
            display_image = viewer(image, COLOR1, COLOR2, COLOR3, BASE_COLOR, SHEET_SIZE)
            coordinates, color_list = visualizer(FILE_NAME, VISUALIZER_TYPE, COLOR1, COLOR2, COLOR3)

            image_fig = Figure(figsize=(6, 4))
            ax = image_fig.add_subplot(111)

            # Plot Data
            display_image = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)
            ax.imshow(display_image)

            # Embed Canvas
            canvas = FigureCanvasTkAgg(image_fig, master=self.page)
            canvas.draw()
            canvas.get_tk_widget().grid(row=6, column=0, columnspan=3)

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
            plt.close()
            
            # plot data in tkinter window
            canvas = FigureCanvasTkAgg(fig, self.page)
            canvas.get_tk_widget().grid(row=6, column=3, columnspan=4)
    
    def save_settings(self):
            SHEET_SIZE = self.sheet_selection.get()
            PAINT_DROP_SIZE = self.paint_drop_diameter.get()
            COMPRESSION_TYPE = self.compression_selection.get()
            FLOW_STEP = self.flowstep.get()
            FLOW_RATE = self.flowrate.get()
            FEED_RATE = self.feedrate.get()
            DROPLETS = self.num_drops.get()
            DELAY = self.delay.get()
            COLOR1 = self.color1.get()
            COLOR2 = self.color2.get()
            COLOR3 = self.color3.get()
            BASE_COLOR = self.base_color.get()
            FILE_NAME = self.output_file_name.get()
            WRITE = self.save_gcode.get()
            VISUALIZER_TYPE = self.visualization.get()
            PROCESSOR_TYPE = self.processor_selection.get()

            settings = [SHEET_SIZE, PAINT_DROP_SIZE, COMPRESSION_TYPE, FLOW_STEP, FLOW_RATE, FEED_RATE, DROPLETS, DELAY, COLOR1, COLOR2, COLOR3, BASE_COLOR, FILE_NAME, WRITE, VISUALIZER_TYPE, PROCESSOR_TYPE]

            settings_file = open("settings.pulp", 'w')

            for i in settings[:-1]:
                settings_file.write("%s\n" % i)
            settings_file.write(settings[-1])

            settings_file.close()

    def load_settings(self):
            settings_file = open("settings.pulp")
            lines = settings_file.readlines()

            self.sheet_selection.set(lines[0].replace("\n", ''))
            self.paint_drop_diameter.delete(0, END)
            self.paint_drop_diameter.insert(0, lines[1].replace("\n", ''))
            self.compression_selection.set(lines[2].replace("\n", ''))
            self.flowstep.delete(0, END)
            self.flowstep.insert(0, lines[3].replace("\n", ''))
            self.flowrate.delete(0, END)
            self.flowrate.insert(0, lines[4].replace("\n", ''))
            self.feedrate.delete(0, END)
            self.feedrate.insert(0, lines[5].replace("\n", ''))
            self.num_drops.delete(0, END)
            self.num_drops.insert(0, lines[6].replace("\n", ''))
            self.delay.delete(0, END)
            self.delay.insert(0, lines[7].replace("\n", ''))
            self.color1.delete(0, END)
            self.color1.insert(0, lines[8].replace("\n", ''))
            self.color2.delete(0, END)
            self.color2.insert(0, lines[9].replace("\n", ''))
            self.color3.delete(0, END)
            self.color3.insert(0, lines[10].replace("\n", ''))
            self.base_color.delete(0, END)
            self.base_color.insert(0, lines[11].replace("\n", ''))
            self.output_file_name.delete(0, END)
            self.output_file_name.insert(0, lines[12].replace("\n", ''))
            self.save_gcode.set(bool(lines[13].replace("\n", '')))
            self.visualization.set(lines[14].replace("\n", ''))
            self.processor_selection.set(lines[15].replace("\n", ''))


if __name__ == '__main__':
    app = window()  # instantiate class
    app.mainloop()  # run the app