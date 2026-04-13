from tools import KNN_order_optimization, KNN_order_optimization_2nd_order, KNN_order_optimization_multi_order
from tools import color_search

def write_Gcode(image, color1, color2, color3, base_color, paint_drop_size, flow_step, droplets, feed_rate, flow_rate, delay):
    # calculate scaling factor (converts pixel index to mm of machine movement)
    scaling_factor = paint_drop_size#math.sqrt(paint_drop_size)
    # create an array of pixel coordinates and pixel colors [x, y, color]
    pixels = []
    # when there is a base sheet, divide colors
    if base_color == "NA":
        for y in range(len(image)):
            pixel_row = []
            for x in range(len(image[y])):
                # light colors are painted last
                if image[y][x] >= 250:
                    color = 3
                # darker colors are painted first
                elif image[y][x] <= 15:
                    color = 1
                else:
                    color = 2
                pixel_row.append([(scaling_factor*x)+scaling_factor, (scaling_factor*y)+scaling_factor, color])
            pixels.append(pixel_row)
    # when there is no base sheet, sort out each color and then divide them
    else:
        image_colors = color_search(image, 4)
        for y in range(len(image)):
            pixel_row = []
            for x in range(len(image[y])):
                # light colors are painted last
                # base sheet doesn't get painted, so it's listed as 4 (to avoid it being lumped into the else statement) which is unused.
                if image[y][x] == image_colors[3]:
                    color = 4
                elif image[y][x] == image_colors[2]:
                    color = 3
                # darker colors are painted first
                elif image[y][x] == image_colors[0]:
                    color = 1
                else:
                    color = 2
                pixel_row.append([(scaling_factor*x)+scaling_factor, (scaling_factor*y)+scaling_factor, color])
            pixels.append(pixel_row)
    
    pixels = KNN_order_optimization(pixels)
    pixels = KNN_order_optimization_2nd_order(pixels)

    # count number of each colors (for setting flow steps in correct order (0-some number))
    count_1 = 0
    count_2 = 0
    for y in range(len(pixels)):
        for x in range(len(pixels[y])):
            if pixels[y][x][2] == 1:
                count_1 += 1
            elif pixels[y][x][2] == 2:
                count_2 += 1

    # generate Gcode
    string1 = ''
    string2 = ''
    string3 = ''
    z_pseudo_location_1 = 0
    z_pseudo_location_2 = flow_step*droplets*count_1
    z_pseudo_location_3 = z_pseudo_location_2 + (flow_step*droplets*count_2)
    for y in range(len(pixels)):
        gcode = "G90 ; absolute distance mode\nG21 ; set millimeters\nG94 ; Units per Minute Feed Rate Mode\nG1 X0 Y0 F400\nG92 Z0 ; zero the z axis\nM9\nM3 S0\n\n"
        gcode += "G0 X-46 Y15\nG0 Z120\nG92 Z0\nG0 Z1\nG0 Y30\n"
        # initial purge
        for i in range(3, 13):
            gcode += "G0 Z%s\n" % (i-1)
            gcode += "G0 Y%s\n" % (i*15)
        gcode += "G0 Z12\n"
        gcode += "G92 Z0\n"

        for x in range(len(pixels[y])):

            if (y%2) != 0:
                x = len(pixels[y])- 1 - x

            if pixels[y][x][2] == 1:
                z_pseudo_location_1 += flow_step
                string1 += "F%s\n" % (feed_rate)
                string1 += "G0 X%s Y%s\n" % (round(pixels[y][x][0], 3), round(pixels[y][x][1], 3))
                string1 += "F%s\n" % (flow_rate)
                if droplets > 1:
                    for i in range(droplets-1):
                        string1 += "G0 Z%s\n" % round(z_pseudo_location_1, 2)
                        string1 += "G4 P%s\n" % (delay)
                        z_pseudo_location_1 += flow_step
                    string1 += "G0 Z%s\n" % round(z_pseudo_location_1, 2)
                else:
                    string1 += "G0 Z%s\n" % round(z_pseudo_location_1, 2)

            elif pixels[y][x][2] == 2:
                z_pseudo_location_2 += flow_step
                string2 += "F%s\n" % (feed_rate)
                string2 += "G0 X%s Y%s\n" % (round(pixels[y][x][0], 3), round(pixels[y][x][1], 3))
                string2 += "F%s\n" % (flow_rate)
                if droplets > 1:
                    for i in range(droplets-1):
                        string2 += "G0 Z%s\n" % round(z_pseudo_location_2, 2)
                        string2 += "G4 P%s\n" % (delay)
                        z_pseudo_location_2 += flow_step
                    string2 += "G0 Z%s\n" % round(z_pseudo_location_2, 2)
                else:
                    # adds all steps needed for color 1
                    string2 += "G0 Z%s\n" % round(z_pseudo_location_2, 2)

            elif pixels[y][x][2] == 3:
                z_pseudo_location_3 += flow_step
                string3 += "F%s\n" % (feed_rate)
                string3 += "G0 X%s Y%s\n" % (round(pixels[y][x][0], 3), round(pixels[y][x][1], 3))
                string3 += "F%s\n" % (flow_rate)
                if droplets > 1:
                    for i in range(droplets-1):
                        string3 += "G0 Z%s\n" % round(z_pseudo_location_3, 2)
                        string3 += "G4 P%s\n" % (delay)
                        z_pseudo_location_3 += flow_step
                    string3 += "G0 Z%s\n" % round(z_pseudo_location_3, 2)
                else:
                    string3 += "G0 Z%s\n" % round(z_pseudo_location_3, 2)
        
    # if there is a base sheet
    if base_color != "NA":

        # only add color if color is not set to blend into base sheet
        if color1 != base_color:
            gcode += string1

        if color2 != base_color:

            # only change pumps if colors are supposed to be different
            if (color1 != color2):
                gcode_lines = gcode.split('\n')
                z_setpoint = gcode_lines[-2].split(' ')[-1].replace('Z', '')
                gcode += "G92 Z0\n"
                gcode += "G0 Z-10\n"
                gcode += "M8\nM3 S0\n"#M8 is coolant flood on
                #gcode += "G0 X-10 Y15 F400\nG92 Z0\nZ15 F400\nG92 Z%s\n" % z_setpoint#add purge cycle
    
                gcode += "G0 X-46 Y15\nG0 Z120\nG92 Z0\nG0 Z1\nG0 Y30\n"
                for i in range(3, 13):
                    gcode += "G0 Z%s\n" % (i-1)
                    gcode += "G0 Y%s\n" % (i*15)
                gcode += "G0 Z12\n"
                gcode += "G92 Z%s\n" % z_setpoint

            gcode += string2

        if color3 != base_color:
            
            if (color2 != color3) and (color1 != color3):
                gcode_lines = gcode.split('\n')
                z_setpoint = gcode_lines[-2].split(' ')[-1].replace('Z', '')
                gcode += "G92 Z0\n"
                gcode += "G0 Z-10\n"
                gcode += "M8\nM3 S1000\n"#M3 is spindle on clockwise
                #gcode += "X-10 F400\nG92 Z0\nZ15 F400\nG92 Z%s\n" % z_setpoint #add purge cycle
                
                gcode += "G0 X-46 Y15\nG0 Z120\nG92 Z0\nG0 Z1\nG0 Y30\n"
                for i in range(3, 13):
                    gcode += "G0 Z%s\n" % (i-1)
                    gcode += "G0 Y%s\n" % (i*15)
                gcode += "G0 Z12\n"
                gcode += "G92 Z%s\n" % z_setpoint

            gcode += string3

    # if there is no base sheet
    else:
        gcode += string1

        if color1 != color2:
            gcode_lines = gcode.split('\n')
            z_setpoint = gcode_lines[-2].split(' ')[-1].replace('Z', '')
            gcode += "G92 Z0\n"
            gcode += "G0 Z-10\n"
            gcode += "M8\nM3 S0\n"#M8 is coolant flood on
            #gcode += "X-10 F400\nG92 Z0\nZ15 F400\nG92 Z%s\n" % z_setpoint #add purge cycle
            
            gcode += "G0 X-46 Y15\nG0 Z120\nG92 Z0\nG0 Z1\nG0 Y30\n"
            for i in range(3, 13):
                gcode += "G0 Z%s\n" % (i-1)
                gcode += "G0 Y%s\n" % (i*15)
            gcode += "G0 Z12\n"
            gcode += "G92 Z%s\n" % z_setpoint

        gcode += string2
        
        if (color2 != color3) and (color1 != color3):
            gcode_lines = gcode.split('\n')
            z_setpoint = gcode_lines[-2].split(' ')[-1].replace('Z', '')
            gcode += "G92 Z0\n"
            gcode += "G0 Z-10\n"
            gcode += "M8\nM3 S1000\n"#M3 is spindle on clockwise
            #gcode += "X-10 F400\nG92 Z0\nZ15 F400\nG92 Z%s\n" % z_setpoint #add purge cycle
            
            gcode += "G0 X-46 Y15\nG0 Z120\nG92 Z0\nG0 Z1\nG0 Y30\n"
            for i in range(3, 13):
                gcode += "G0 Z%s\n" % (i-1)
                gcode += "G0 Y%s\n" % (i*15)
            gcode += "G0 Z12\n"
            gcode += "G92 Z%s\n" % z_setpoint

        gcode += string3
    
    gcode += "F400\nG0 X0 Y0\n"
    gcode += "M5\n" # spindle off
    gcode += "M09\n" # coolant off
    gcode += "M2"

    return gcode

def writer(image, color1, color2, color3, base_color, write, file_name, paint_drop_size, flow_step, droplets, feed_rate, flow_rate, delay):
    if write == True:
        gcode = write_Gcode(image, color1, color2, color3, base_color, paint_drop_size, flow_step, droplets, feed_rate, flow_rate, delay)
        output_file = open(file_name, 'w')
        output_file.write(gcode)
        output_file.close()