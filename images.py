
# images.py : librerie per la creazione di immagini e il calcolo della distanza di colore

# references:  https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html

import itertools
from PIL import Image, ImageDraw
from random import randrange,randint

RED,GREEN,BLUE,ALFA = 0,1,2,3
TRASPARENCY = 128	# trasparenza al 50% circa..
	
def ColourDistanceSquaredRGB(rgb1, rgb2):
	# distanza euclidea fra due colori:
	# distanza euclidea fra due colori in modalita' RGB (3 componenti R,G,B)
	rmean = 0.5 * (rgb1[RED] + rgb2[RED])
	Rdist = ((2 + rmean) * (rgb1[RED] - rgb2[RED]))**2
	Gdist = (4 * (rgb1[GREEN] - rgb2[GREEN])) ** 2
	Bdist = ((3 - rmean) * (rgb1[BLUE] - rgb2[BLUE]))**2
	return Rdist + Gdist + Bdist
	
def ColourDistanceSquaredRGBA(rgba1, rgba2):
	# distanza euclidea fra due colori in modalita' RGBA (4 componenti R,G,B e A)
	# color similarity/distance in RGBA color space
	deltaR = rgba1[RED]		- rgba2[RED]	# Red
	deltaG = rgba1[GREEN]	- rgba2[GREEN]	# Green
	deltaB = rgba1[BLUE] 	- rgba2[BLUE]	# Blue
	deltaAlpha = rgba1[ALFA] - rgba2[ALFA]	# Alpha channel
	rgbDistanceSquared = (deltaR**2 + deltaG**2 + deltaB**2) / 3
	return deltaAlpha**2 / 2.0 + rgbDistanceSquared * rgba1[ALFA] * rgba2[ALFA] / 65025

def SuperImposeNewRectangleRGBA(image,rect,color,canvas):
	# ritorna un nuovo rettangolo fra i punti 'rect' di colore 'color' in un foglio di dimensioni 'canvas'
	width,height = canvas[0],canvas[1]
	
	backgound = image
	foreground = Image.new('RGBA',(width,height))
	draw = ImageDraw.Draw(foreground)
	
	(x1,y1) = rect[0]
	(x2,y2) = rect[1]

	draw.rectangle((x1,y1,x2,y2),color)	# disegna il rettangolo da sovrapporre a 'image'
	
	backgound.paste(foreground,(0,0),foreground)	# sovrappone per trasparenza le due immagini
	return (backgound,((x1,y1),(x2,y2)))
		
def NewRectangle(image,rect,color,canvas,RND,MODE):
	# ritorna un nuovo rettangolo fra i punti 'rect' di colore 'color' in un foglio di dimensioni 'canvas'

	width,height = canvas[0],canvas[1]
	
	backgound = None
	
	if image == None:
		image = Image.new(MODE,(width,height))
		draw = ImageDraw.Draw(image)
	else:
		backgound = image
		foreground = Image.new(MODE,(width,height))
		draw = ImageDraw.Draw(foreground)
	
		
	if not RND:
		(x1,y1) = rect[0]	# limiti del rettangolo in cui giace l'immagine 'image'
		(x2,y2) = rect[1]
	else:
		(x1,y1) = randint(0,width),randint(0,height)
		(x2,y2) = randint(0,width),randint(0,height)
		
		if   MODE == 'RGBA': color = (randint(0,255),randint(0,255),randint(0,255),TRASPARENCY)
		elif MODE == 'RGB' : color = (randint(0,255),randint(0,255),randint(0,255))
		else:
			print(f'{MODE} mode error!')
			return None
	
	draw.rectangle((x1,y1,x2,y2),color)
	
	if backgound != None:
		backgound.paste(foreground,(0,0),foreground)	# sovrappone per trasparenza le due immagini
		return (backgound,((x1,y1),(x2,y2)))
	else:
		return (image,((x1,y1),(x2,y2)))
	
def NewPixelImage(name,width,height,MODE,SAVE):
	print(f'...creating {MODE} image file "{name}.png" as random pixel image.')
	img = Image.new(MODE,(width,height))

	if MODE == 'RGBA':
		for i,j in itertools.product(range(width),range(height)):
			#               (x,y),(R,G,B,A)
			img.putpixel((i,j),(randint(0,255),randint(0,255),randint(0,255),randint(200,255)))
	elif MODE == 'RGB':
		for i,j in itertools.product(range(width),range(height)):
			#               (x,y),(R,G,B)
			img.putpixel((i,j),(randint(0,255),randint(0,255),randint(0,255)))
	else:
		print(f'{MODE} mode error!')
		return None
		
	if SAVE:
		img.save(name + ".png")
		print('saved.')
		
	print(f'Done.')
	return img
	
def NewCircleImage(name,width,height,n,f,MODE,SAVE):
	print(f'...creating {MODE} image file "{name}.png" as random circles image.')
	img = Image.new(MODE,(width,height))

	draw = ImageDraw.Draw(img)
	
	if MODE == 'RGBA':
		for i in range(n):
			r = randrange(int(max((width,height))/f))
			x,y = randint(0,width),randint(0,height)
			fill = (randint(0,255),randint(0,255),randint(0,255),randint(200,255))
			draw.ellipse((x-r,y-r,x+r,y+r),fill)
	elif MODE == 'RGB':
		for i in range(n):
			r = randrange(int(max((width,height))/f))
			x,y = randint(0,width),randint(0,height)
			fill = (randint(0,255),randint(0,255),randint(0,255))
			draw.ellipse((x-r,y-r,x+r,y+r),fill)
	else:
		print(f'{MODE} mode error!')
		return None
		
	if SAVE:
		img.save(name + ".png")
		print('saved.')
		
	print(f'Done.')
	return img
	
def NewTiledImage(name, img, width, height, n_di_rettangoli, proporzione, MODE='RGBA', SAVE=False):
	
	if name != None:
		print(f'...creating {MODE} image file "{name}.png" as random tiled image.')
	
	if img == None:
		img = Image.new(MODE,(width,height))

	draw = ImageDraw.Draw(img)
	
	if MODE == 'RGBA':
		for i in range(n_di_rettangoli):
			r = randrange(int(max((width,height))/proporzione))
			x,y = randint(0,width),randint(0,height)
			fill = (randint(0,255),randint(0,255),randint(0,255),randint(200,255))
			draw.rectangle((x-r,y-r,x+r,y+r),fill)
	elif MODE == 'RGB':
		for i in range(n_di_rettangoli):
			r = randrange(int(max((width,height))/proporzione))
			x,y = randint(0,width),randint(0,height)
			fill = (randint(0,255),randint(0,255),randint(0,255))
			draw.rectangle((x-r,y-r,x+r,y+r),fill)
	else:
		print(f'{MODE} mode error!')
		return None
		
	if name != None:
		if SAVE:
			img.save(name + ".png")
			print('saved.')
		
	# print(f'Done.')
	return img
	
def NewPoligonImage(name, img, width, height, n_di_poligoni, n_di_lati, proporzione=None, MODE='RGBA', SAVE=False):

	if name != None:
		print(f'...creating {MODE} image file "{name}.png" as random polygon image.')
	
	if img == None:
		img = Image.new(MODE,(width,height))

	draw = ImageDraw.Draw(img)
	
	if MODE == 'RGBA':
		for i in range(n_di_poligoni):	# n. of polygon
			vertex = []
			for j in range(n_di_lati):	# n. of vertex
				# r = randrange(int(max((width,height))/proporzione))
				x,y = randint(0,width),randint(0,height)
				vertex.append((x,y))
			fill = (randint(0,255),randint(0,255),randint(0,255),randint(200,255))
			draw.polygon(vertex,fill)
	elif MODE == 'RGB':
			vertex = []
			for j in range(n_di_lati):	# n. of vertex
				# r = randrange(int(max((width,height))/proporzione))
				x,y = randint(0,width),randint(0,height)
				vertex.append((x,y))
			fill = (randint(0,255),randint(0,255),randint(0,255))
			draw.polygon(vertex,fill)
	else:
		print(f'{MODE} mode error!')
		return None
		
	if name != None:
		if SAVE:
			img.save(name + ".png")
			print('saved.')
		
	# print(f'Done.')
	return img	
