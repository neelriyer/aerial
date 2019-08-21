# Datasets

1. Dataset

- 49152 aerial images of a region in Adelaide. 
- Images are 256x256 and are stored in the dataset folder.
- images saved as x/x_y.jpg, where x and y are google tile coordinates 

- for google tiles cooridinates between: 1855744<=x<=1855999 and 1265792<=y<=1265983

2. Stitched

- Dataset of stitched tiles
- takes input from the Dataset folder
- Uses image_stitcher.py
- 

3. New_tiles

- Dataset of offset tiles
- Uses image_newtiler.py to run
- [see example here](https://github.com/pyggteam/aerials/blob/master/New_tiles/1855744/1265792/1855744_1265792_offset(0%2C0).jpg)


4. Labelled_images

- JSON payload of labelled images
- images labelled into 3 classes: driveways, edge_of_road, offstreet_parking_bays
- [see example here](https://github.com/pyggteam/aerials/blob/master/labelled_images/1855744/ann/1855744_1265792.jpg.json)

5. processed_JSON

- converted JSON payload from labelled_images dataset into .txt file
- .txt file contains:
	- classification of image (0 = driveway, 1 = curb, 2 = off street parking bay)
	- x pixel coordinate of driveway/curb/offstreet parking bay
	- y pixel coordinate of driveway/curb/offstreet parking bay
	- theta (angle between line designating object and horizontal)
-.txt named after google tile that it refers to the image location
- [see example here](https://github.com/pyggteam/aerials/blob/master/processed_JSON/1855744/1855744_1265792.csv)

# image_newtiler.py

Script to create 51,511,296 new tiles. Takes in all stitched tiles and creates 1048 tiles for each stitched tile. 

Works out to ~51 Million created tiles in total. 

Tiles saved in New_tiles folder. File name is 'New_tile/x/y/x_y_offset(offsetx, offsety) where x and y are tile coordinates and offsetx and offsety are the offsets for both x and y.


Example of how it works. The following is a stitched image with dimensions 768x768.

	(0,768) ------------------------------------------------(768,768)
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
	    |---------------------				|
	    |	  |		| 				|
	    | img1|	img2    |				|
	    |	  |		|		    	        |
	    -----------------------------------------------------
	   (0,0) (16,0)	     (32,0)		   	     (768,0)

starts at (0,0) and creates a 256x256 image (img1)

Then moves to (16,0) and creates another 256x256 image (img2)

So on and so forth



In reality there is a large degree of overlap between img1 and img2

Handles edgecases where the image size is different (on corners and edges)



# image_stitcher.py

Image_stitcher.py is a python script to stitch images together.

    Grid:
    ----------------------
    top left|top    | top right
    -------|-------|-------
    left   | middle| right
    -------|-------|-------
    bottom left|bottom | bottom right
    -------|-------|-------

From a middle image stitches all 8 surrounding tiles in their relevant positions and returns this stitched image

Current middle image is: "1855779_1265826.jpg". Open image_stitcher.py and change the file_name variable to modify this.

Handles corner images and side images. Will return as many surrounding tiles as necessary (either 4 tiles or 6 tiles for edgecases)


# image_scraper.py

image_scraper.py is a small python script to scrape images from nearmap

api call: "https://api.nearmap.com/tiles/v3/Vert/21/"+str(x)+"/"+str(y)+".jpg?apikey=ODI0M2IxNzEtMmJhMy00NGRkLWEzMTItYTE0ZDk1ZGFmMmI5"

images saved in the Dataset folder


