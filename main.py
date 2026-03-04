from image_readers import reader
from image_processors import processor
from image_writers import writer
from image_viewers import viewer
from gcode_visualizer import visualizer

PAINT_DROP_SIZE = 15 #mm^2
FEED_RATE = 400
FLOW_RATE = 400
FLOW_STEP = 1 #mm
DROPLETS = 3 #number of droplets deposited per dot
DELAY = 0.01 #delay between droplet deposition (seconds)
SHEET_SIZE = "A1"
IMAGE = "test_image17.jpg"
COLOR1 = [0, 0, 0]#[140, 120, 100]
COLOR2 = [0, 0, 0]#[180, 150, 120]    # TODO write the section that pulls color suggestions (it will help to view how palette effects the result)
COLOR3 = [0, 0, 0]#[255, 255, 150]
BASE_COLOR = [255, 255, 255] # set to "NA" if there is no base sheet
WRITE = True
FILE_NAME = "star_2D_test.gcode"
VISUALIZER_TYPE = "Path"

def main():
    image = reader(IMAGE, SHEET_SIZE)
    image = processor(image, BASE_COLOR, SHEET_SIZE, PAINT_DROP_SIZE)
    writer(image, COLOR1, COLOR2, COLOR3, BASE_COLOR, WRITE, FILE_NAME, PAINT_DROP_SIZE, FLOW_STEP, DROPLETS, FEED_RATE, FLOW_RATE, DELAY)
    viewer(image, COLOR1, COLOR2, COLOR3, BASE_COLOR, SHEET_SIZE)
    visualizer(FILE_NAME, VISUALIZER_TYPE, COLOR1, COLOR2, COLOR3)


if __name__ == "__main__":
    main()