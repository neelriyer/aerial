"""
image scraper from nearmap
api call: "https://api.nearmap.com/tiles/v3/Vert/21/"+str(x)+"/"+str(y)+".jpg?apikey=ODI0M2IxNzEtMmJhMy00NGRkLWEzMTItYTE0ZDk1ZGFmMmI5"

for google tiles cooridinates between:
1855744<=x<=1855999
1265792<=y<=1265983

49152 images to download

images saved as x_y.jpg, where x and y are google tile coordinates 

"""

import urllib.request
import os
import shutil
import time

#function to download image from image_url on google tile coordinates specified by x and y
def downloader(image_url, x, y):

	#file name
	full_file_name = 'Dataset/'+ str(x) + '/' + str(x) + '_' + str(y) + '.jpg'

	#download image
	urllib.request.urlretrieve(image_url,full_file_name)


#function to create directory
#if directory already exists: delete and recreate
def create_directory(directory_name):
	name = os.getcwd()+'/'+str(directory_name)
	try:
	    os.makedirs(name)    
	except FileExistsError:
	    shutil.rmtree(name) 
	    os.makedirs(name) 

#function to return estimated completion time in seconds
def estimated_completion(sleep_count):

	iterations = (1855999 - 1855744 + 1) * (1265983 - 1265792 + 1)

	return iterations*sleep_count

print("49152 images to download")
print("estimated completion time is: {} hours\n".format(estimated_completion(0.25)/(60*60)))



#create dataset directory
#create_directory('Dataset')

#completion time

#download all images in range
for x in range(1855744, (1855999)+1):

	#create x_folder directory
	create_directory('Dataset/'+ str(x))

	for y in range(1265792, (1265983)+1):
		#url call
		url = "https://api.nearmap.com/tiles/v3/Vert/21/"+str(x)+"/"+str(y)+".jpg?apikey=ODI0M2IxNzEtMmJhMy00NGRkLWEzMTItYTE0ZDk1ZGFmMmI5"

		#download image
		downloader(url, x, y)

		#sleep
		time.sleep(0.25)


















