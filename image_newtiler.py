"""
image newtiler for nearmap



Script to create 51,511,296 new tiles. Takes in all stitched tiles and creates 1048 tiles for each stitched tile. 

Works out to ~51 Million created tiles in total. 



Example of how it works. The following is a stitched image with dimensions 768x768.

(0,768) -----------------------------(768,768)
	    |							|
	    |							|
	    |							|
	    |							|
	    |							|
	    |							|
	    |							|
	    |							|
	    |							|
	    |							|
	    |------------				|
	    |	  |		| 				|
	    | img1|img2 |				|
	    |	  |		|		    	|
	    -----------------------------
	   (0,0) (16,0)	(32,0)		    (768,0)

starts at (0,0) and creates a 256x256 image (img1)

Then moves to (16,0) and creates another 256x256 image (img2)

So on and so forth

In reality there is a large degree of overlap between img1 and img2

Handles edgecases where the image size is different (on corners and edges)

"""
import os
import cv2

#function to create directory
def create_directory(directory_name):
    name = os.getcwd()+'/'+str(directory_name)
    try:
        os.makedirs(name)    
    except FileExistsError:
        pass

def crop_image(img, tile_x, tile_y):

	"""
	function to crop a single image and save cropped image into New_tiles folder. Will move x and y independantly by 16. 
	eg. (x=0, y = 0), (x = 16, y = 0), (x = 32, y = 0)......
	"""

	w = 256
	h = 256

	#get height, width and channels of image
	height, width, channels = img.shape

	for x in range(0, width, 16):		

		for y in range(0, height, 16):

			if((y+h)<= height and (x+w)<=width):
				crop_img = img[y:y+h, x:x+w]

				#{original x, y}_offset(x, y)
				file_name = os.getcwd() + "/New_tiles/" + str(tile_x)+ "/" + str(tile_y) + "/" + str(tile_x) + "_" + str(tile_y) + "_" + "offset(" + str(x) + "," + str(y) + ")" + ".jpg"
				#print(file_name)
				cv2.imwrite(file_name, crop_img)


def data_calculations():

	"""
	function to get an idea of how many images are created
	"""

	length = 1855999 - 1855744 + 1
	width = 1265983 - 1265792 + 1

	#each tile is used to create additional tiles. Excluding edgecases 1048 additional are created for each stitched tile.

	images_created = length * width * 1048

	print("{} images will be created\n".format(images_created))
	print("images stored in 'New_tiles/x/y', where x and y are the tile coordinates of the stiched tile\n")
	#print("estimated completion time is: {}", )


#create dataset directory
create_directory('New_tiles')

#data estimation
data_calculations()


#iterate through all tiles
for tile_x in range(1855744, (1855744)+10):

	for tile_y in range(1265792, (1265792)+10):

		#create x_folder directory
		create_directory('New_tiles/'+ str(tile_x) + "/" + str(tile_y))

		#read image
		img = cv2.imread(os.getcwd()+"/stitched/"+str(tile_x)+"/"+str(tile_x)+"_"+str(tile_y)+".jpg")

		crop_image(img, tile_x, tile_y)




