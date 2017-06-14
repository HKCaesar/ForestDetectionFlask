# slice large image into small samples
# predict class for each sample
# joint the samples together and save output image 
# in static dir
from image_slicer import Tile
from PIL import Image, ImageDraw
import numpy as np
import math
import keras.models
from keras.models import model_from_json
from keras import backend as K

def slice(filename, number_tiles, columns, rows):
    """
    Split an image into a specified number of tiles.
    Args:
       filename (str):  The filename of the image to split.
       number_tiles (int):  The number of tiles required.
       columns (int): The number of columns
       rows(int): The numebr of rows
    Returns:
        Tuple of :class:`Tile` instances.
    """
    im = Image.open(filename)

    im_w, im_h = im.size
    extras = (columns * rows) - number_tiles
    tile_w, tile_h = int(im_w // columns), int(im_h // rows)
    tiles = []
    number = 1
    for pos_y in range(0, im_h, tile_h): # -rows for rounding error.
        for pos_x in range(0, im_w, tile_w): # as above.
            area = (pos_x, pos_y, pos_x + tile_w, pos_y + tile_h)
            image = im.crop(area)
            position = (int(math.floor(pos_x / tile_w)) + 1,
                        int(math.floor(pos_y / tile_h)) + 1)
            coords = (pos_x, pos_y)
            tile = Tile(image, number, position, coords)
            tiles.append(tile)
            number += 1
    return tuple(tiles)

def join(tiles, columns, rows):
    """
    @param ``tiles`` - Tuple of ``Image`` instances.
    @return ``Image`` instance.
    """
    tile_size = tiles[0].image.size
    size = tile_size[0] * columns, tile_size[1] * rows
    im = Image.new('RGB', size, None)
    for tile in tiles:
        im.paste(tile.image, tile.coords)
    return im
	

def makePrediction(imagestr, model):
	"""
	@param ``imagestr`` - URl of input image, ``model`` 
			network with trained weights
	@return joined tagged image
	"""
	if K.image_data_format() == 'channels_first':
		input_shape = (3, 10, 10)
	else:
		input_shape = (10, 10, 3)
	
	im = Image.open(imagestr)
	im.save(".\static\input.jpg")
	x = im.size[0]
	y = im.size[1]
	rows = (x//10)
	columns = (y//10)
	numberOfTiles = rows * columns
	tiles = slice(imagestr,numberOfTiles,rows,columns)
	x=[]

	for i in range(0,numberOfTiles):
		tile = tiles[i]
		imgArray = np.array(tile.image)
		testImg = imgArray.reshape(input_shape)
		testImg=testImg/255.
		x.append(testImg)

	x=np.array(x)
	out = model.predict(x)

	for i in range(0,numberOfTiles):
			tile = tiles[i]
			if out[i]<=0.5:
				t = out[i] / 0.5
				im = tile.image
				back = Image.new('RGBA', im.size)
				back.paste(im)
				poly = Image.new('RGBA', (10,10))
				pdraw = ImageDraw.Draw(poly)
				pdraw.polygon([(0,0),(0,10),(10,10),(10,0)],
							  fill=(int(math.floor(255*(1.0 - t))),0,int(math.floor(255*(t))),127),outline=None)
				back.paste(poly, (0,0), mask=poly)
				tile.image = back

	result = join(tiles,rows,columns)
	result.save(".\static\output.jpg")