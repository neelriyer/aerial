# aerials
49152 aerial images of a region in Adelaide. Images are 256x256 and are stored in the dataset folder.

for google tiles cooridinates between:
1855744<=x<=1855999
1265792<=y<=1265983

images saved as x/x_y.jpg, where x and y are google tile coordinates 

image_scraper.py is a small python script to scrape images from nearmap
api call: "https://api.nearmap.com/tiles/v3/Vert/21/"+str(x)+"/"+str(y)+".jpg?apikey=ODI0M2IxNzEtMmJhMy00NGRkLWEzMTItYTE0ZDk1ZGFmMmI5"
