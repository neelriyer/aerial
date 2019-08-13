from PIL import Image
import os
import cv2
import numpy as np
import shutil
import sys

"""
Script to stitch images together:
---------------------------------

    Grid:
    -----------------------
   top left|top    | top right
    -------|-------|-------
    left   | middle| right
    -------|-------|-------
bottom left|bottom | bottom right
    -------|-------|-------

from a middle image stitches all 8 surrounding tiles in their relevant positions and returns this stitched image

current middle image is: "1855779_1265826.jpg". Change the file_name variable to modify this.

Edgecases:
---------
handles corner images and side images. Will return as many surrounding tiles as necessary (either 4 tiles or 6 tiles for edgecases)

"""

def merge_images(centre, adjacent_images):
	
    """
    function to merge all adjacent images.

    Seperates work into 3 layers: top middle and bottom layers

    Merges images in each layer, then merges each layer with each other

    stores image as x_y.jpg where (x,y) are the tile coordinates of the centre tile

        Grid:
    -----------------------
  top left |top    | top right
    -------|-------|-------
    left   | middle| right
    -------|-------|-------
bottom left|bottom | bottom right
    -------|-------|-------

    """
    #open all images
    images = [None] * len(adjacent_images)

    for i in range(len(adjacent_images)):
        if(adjacent_images[i] is not None):

            images[i] = Image.open(adjacent_images[i])
            #print(images[i].size)


    #left, right, top, bottom, etc. tiles
    left = images[1]
    top_left_corner = images[0]
    bottom_left_corner = images[2]

    top = images[3]
    middle = images[4]
    bottom = images[5]

    top_right_corner = images[6]
    right = images[7]
    bottom_right_corner = images[8]

    #create each layer individually
    #middle layer
    middle_layer = merge_layers_horizontally(left, right, middle, 'middle_layer')

    #top layer
    top_layer = merge_layers_horizontally(top_left_corner, top_right_corner, top, 'top_layer')

    #bottom layer
    bottom_layer = merge_layers_horizontally(bottom_left_corner, bottom_right_corner, bottom, 'bottom_layer')


    #merge layers vertically
    final = middle_layer

    #if top layer exists merge with final
    try:
        final = np.concatenate((final, top_layer), axis=0)
    except:
        #print('No top layer')
        pass

    #if bottom layer exists merge with final layer
    try:
        final = np.concatenate((bottom_layer, final), axis=0)
    except:
        #print('No bottom layer')
        pass


    #store as centre
    file_name = os.getcwd()+'/stitched/'+str(centre[0])+'/'+str(centre[0]) + '_' + str(centre[1])+'.jpg'
    cv2.imwrite(file_name, final)
    #print(str(centre[0]) + '_' + str(centre[1])+'.jpg saved to ' + str(os.getcwd()+'/stitched'))


def merge_layers_horizontally(left, right, middle, file_name):

    """
    function to merge layers horizontally, so axis = 1

    returns merged layer

    stores layer as a jpg file for debugging
    """

    layer = None

    #if left and right exist
    if(left and right):
        layer = np.concatenate((left, middle), axis=1)
        layer = np.concatenate((layer, right), axis=1)
        #cv2.imwrite(str(file_name)+'.jpg', layer)
        #print('\n'+str(file_name)+'.jpg saved to ' + str(os.getcwd()))

    #if only right exists
    elif(right and not left):
        layer = np.concatenate((middle, right), axis=1)
        #cv2.imwrite(str(file_name)+'.jpg', layer)
        #print('\n'+str(file_name)+'.jpg saved to ' + str(os.getcwd()))

    #if only left exists
    elif(left and not right):
        layer = np.concatenate((left, middle), axis=1)
        #cv2.imwrite(str(file_name)+'.jpg', layer)
        #print('\n'+str(file_name)+'.jpg saved to ' + str(os.getcwd()))

    return layer
    

def find_adjacent_images(file1):


    """
    function to find adjacent images to center image. Takes in a file name.
            
    returns file names of these surrounding images


    Grid:
    -----------------------
  (x-1,y+1)|(x,y+1)| (x+1,y+1)
    -------|-------|-------
    (x-1,y)| (x,y) | (x+1,y)
    -------|-------|-------
  (x-1,y-1)|(x,y-1)| (x+1,y-1)
    -------|-------|-------

    returned list: [left corner, left, bottom left corner, top, middle, bottom, top right corner, right, bottom right corner]

    If coordinates of an image are outside bounding box: 1855744<=x<=1855999, 1265792<=y<=1265983, changes to None.

    """

    #1855744<=x<=1855999
    #1265792<=y<=1265983

    file_name = str(file1).split('_', 2)


    #x,y coordinates (convert from string to int)
    x = int(file_name[0])
    y = int(file_name[1])


    #find coordinates of proposed adjacent tiles
    left = (x-1, y)
    top_left_corner = (x-1,y+1)
    bottom_left_corner = (x-1,y-1)

    top = (x,y+1)
    middle = (x,y)
    bottom = (x,y-1)

    top_right_corner = (x+1,y+1)
    right = (x+1,y)
    bottom_right_corner = (x+1,y-1)


    #early exit
    if(not 1855744<=middle[0]<=1855999):
        return None

    if(not 1265792<=middle[1]<=1265983):
        return None


    #test if these tiles are within the bounding box
    tiles_to_test = [top_left_corner,left,bottom_left_corner,top,middle,bottom,top_right_corner,right,bottom_right_corner]

    for tile in range(len(tiles_to_test)):

        x_tile = tiles_to_test[tile][0]
        y_tile = tiles_to_test[tile][1]

        #if not within bounding box change to None
        if((1855744<=x_tile<=1855999) and (1265792<=y_tile<=1265983)):
            pass
        else:
            tiles_to_test[tile] = None


    return tiles_to_test


def tuple_replace(list1):

    """
    function to replace tuples with a path to file name
            
    eg.(1855999,1265983) is replaced with cwd()+/Dataset/1855999/1855999_1265983.jpg in the list
    """

    for i in range(len(list1)):

        t1 = list1[i]

        if(t1 is not None):

            x = t1[0]
            y = t1[1]

            replacement = os.getcwd()+'/Dataset'+'/'+str(x)+'/'+str(x)+'_'+str(y)+'.jpg'

            list1[i] = replacement

    return list1


#function to create directory
def create_directory(directory_name):
    name = os.getcwd()+'/'+str(directory_name)
    try:
        os.makedirs(name)    
    except FileExistsError:
        pass


def driver_function(file_name):

    """
    main driver function to run program
    """

    target_image = os.path.splitext(file_name)[0]

    #store centre image
    centre = target_image.split('_', 2)

    #convert to int
    centre[0] = int(centre[0])
    centre[1] = int(centre[1])

    #early exit
    if(not 1855744<=centre[0]<=1855999):
        raise Exception('x must be between [1855744, 1855999]. The value of x was: {}'.format(centre[0]))


    if(not 1265792<=centre[1]<=1265983):
        raise Exception('y must be between [1265792, 1265983]. The value of y was: {}'.format(centre[1]))


    #find all adjancent images to target image
    images = find_adjacent_images(target_image)

    #add path name to each image for easy access
    images_replaced = tuple_replace(images)

    #stitch images
    merge_images(centre,images_replaced)


#Dataset not found
if(not os.path.isdir(os.getcwd()+'/Dataset')):
    sys.exit('error: /Dataset directory not found\nRun image_scraper.py first')


#create directory for stitched images
create_directory('stitched')

#download all images in range
for x in range(1855744, (1855999)+1):

    #create x_folder directory
    create_directory('stitched/'+ str(x))

    for y in range(1265792, (1265983)+1):

        file_name = str(x) + '_' + str(y) + '.jpg'

        driver_function(file_name)





