# Dataset

49152 aerial images of a region in Adelaide. 

Images are 256x256 and are stored in the dataset folder.

images saved as x/x_y.jpg, where x and y are google tile coordinates 

for google tiles cooridinates between:
1855744<=x<=1855999
1265792<=y<=1265983

# image_newtiler.py

Script to create 51,511,296 new tiles. Takes in all stitched tiles and creates 1048 tiles for each stitched tile. 

Works out to ~51 Million created tiles in total. 

Tiles saved in New_tiles folder. File name is 'New_tile/x/y/x_y_offset(offsetx, offsety) where x and y are tile coordinates and offsetx and offsety are the offsets for both x and y.


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
