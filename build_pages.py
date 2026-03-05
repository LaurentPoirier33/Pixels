import pygame
import pygame.gfxdraw
import re
import diffscreens

init = 0

# color of undrawn pixels
pixel_color = (0,0,0)

# where to put the top left corner of either lcd
startx = 50
starty = 50

# oled graphic definitions
pixels_width = 128
pixels_height = 64
oled_width = 145 # pcb width
oled_height = 140 # pcb height

# 280x320 and 240x320 lcd graph definitions
lcd_w = 280
lcd_h = 320
lcd_x = startx+5
lcd_y = starty+5

# 240x240 lcd graph definitions

rnd_lcd_w = 240
rnd_lcd_h = 240
rnd_lcd_x = startx
rnd_lcd_y = starty

print("Usage tips:\n") 
print("128x64 OLED -> screen_type = 64_OLED\n")
print("280x320 lcd -> screen_type = 280LCD\n")
print("240x320 lcd -> screen_type = 240LCD\n")
print("240x240 round lcd -> screen_type = RNDLCD\n")
print("Custom LCD size -> screen_type = CSTMLCD\n")
print("Coding tips:\n")
print("If you want to remove the last function, simply type -1\n")
print("If you want to get rid of all the functions, type 0\n")

while (True):
	screen_type = input("What type of display is the UI being made for?\n")
	if (screen_type == "64_OLED"):
		display_screen = pygame.Surface((128,64),pygame.SRCALPHA)
		# where the first pixel is with respect to start_x&y
		x_pixels = startx+8
		y_pixels = starty+(oled_height/2-pixels_height/2)
		break
	elif (screen_type == "280LCD"):
		display_screen = pygame.Surface((280,320),pygame.SRCALPHA)
		x_pixels = lcd_x
		y_pixels = lcd_y
		break
	elif (screen_type == "240LCD"):
		display_screen = pygame.Surface((240,320),pygame.SRCALPHA)
		x_pixels = lcd_x
		y_pixels = lcd_y
		break
	elif (screen_type == "RNDLCD"):
		display_screen = pygame.Surface((240,240),pygame.SRCALPHA) #SRCALHPA is transparent canvas
		x_pixels = rnd_lcd_x
		y_pixels = rnd_lcd_y
		break
	elif (screen_type == "CSTMLCD"):
		pixel_w = input("Enter screen width in pixels\n")
		pixel_h = input("Enter screen height in pixels\n")
		display_screen = pygame.Surface((int(pixel_w),int(pixel_h)),pygame.SRCALPHA)
		x_pixels = lcd_x
		y_pixels = lcd_y
		break
	else:
		print("Incorrect display type call")

SCN_WDTH = 500
SCN_HGHT = 500


pygame.init()
main_screen = pygame.display.set_mode((int(SCN_WDTH),int(SCN_HGHT)))
clock = pygame.time.Clock()
running = True

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PINK = (255,0,255)
matte = (25,25,25)
screen_blue = (0,0,60)

current_font = pygame.font.SysFont("Courier" , 20, False, False)
textColor = WHITE
backtextColor = BLACK
textSize = 10
cursor = (50,50)

# current page is awful, it needs to be defined AND all used in one place
# additionally, the canvas needs to be in the loop but also keepen track of

def draw_function(lcd, function, arguments):
	global textColor
	global backtextColor
	global textSize
	global cursor
	# c++: setTextColor (uint16_t c, OPTIONAL uint16_t bg) color, background color
	# py: textColor = (color_tuple), backtextColor = (color_tuple)
	if re.search(r"\bsetTextColor\b", function):
		if (len(arguments) != 1):
			print("Invalid setTextColor call at line", i+1)
			return 0
		textColor = arguments[0]
		return 1

	# c++: setTextSize (uint8_t s)
	# py: textSize = (size)
	if re.search(r"\bsetTextSize\b", function):
		if (len(arguments) != 1):
			print("Invalid setTextSize call at line", i+1)
			return 0
		textSize = int(arguments[0]) * 10
		return 1

	# c++: setCursor (int16_t x, int16_t y)
	# py: cursor = (x,y)
	if re.search(r"\bsetCursor\b", function):
		if (len(arguments) != 2):
			print("Invalid setCursor call at line", i+1)
			return 0
		cursor = (int(arguments[0]), int(arguments[1]))
		return 1

	# c++: print(string)
	# py: surface = font.render(text, antialias, color, background=None)
	#	  blit(surface, (x,y))
	# antialias is a boolean, if True then smooth letters, this is there because fonts are usually pixel dense
	# no bachground argument for transparent background
	if ("print" in function):
		if (len(arguments) != 1):
			print("Invalid print call")
			return 0
		current_font = pygame.font.SysFont("Courier",
			textSize,
			False, 
			False)
		text = arguments[0].replace('"','')
		currentTextSurface = current_font.render(text,
			False,
			textColor,
			display_screen.get_at((cursor[0],cursor[1]-1)))
		lcd.blit(currentTextSurface, cursor)
		return 1

	# c++: clearDisplay (void)
	# py: fill(color, rect=None, special_flags=0)
	if ("clearDisplay" in function):
		lcd.fill(pixel_color)
		return 1

	# c++: fillScreen (uint16_t color)
	# py: fill(color, rect=None, special_flags=0)
	if ("fillScreen" in function):
		if (len(arguments) != 1):
			print("Invalid fillScreen call")
			return 0
		lcd.fill(arguments[0])
		return 1

	# c++: drawPixel (int16_t x, int16_t y, uint16_t color)
	# py: pixel(surface, x, y, color)
	if "drawPixel" in function:
		if (len(arguments) != 3):
			print("Invalid drawPixel call")
			return 0
		pygame.gfxdraw.pixel(lcd, 
			int(arguments[0]), 
			int(arguments[1]), 
			arguments[2])
		return 1

	# c++: drawFastHLine (int16_t x, int16_t y, int16_t w, uint16_t color)
	# py: hline(surface, x1, x2, y, color)
	if ("drawFastHLine" in function):
		if (len(arguments) != 4):
			print("Invalid drawFastHLine call")
			return 0
		pygame.gfxdraw.hline(lcd,
			int(arguments[0]),
			(int(arguments[0])+int(arguments[2])), # x1 + w = x2
			int(arguments[1]), 
			arguments[3])
		return 1

	# c++: drawFastVLine (int16_t x, int16_t y, int16_t h, uint16_t color)
	# py: vline(surface, x, y1, y2, color)
	if ("drawFastVLine" in function):
		if (len(arguments) != 4):
			print("Invalid drawFastVLine call")
			return 0
		pygame.gfxdraw.vline(lcd,
			int(arguments[0]),
			int(arguments[1]),
			(int(arguments[1]) + int(arguments[2])), # y1 + h = y2
			arguments[3])
		return 1

	# c++: drawLine (int16_t x0, int16_t y0, int16_t x1, int16_t y1, uint16_t color)
	# pi: line(surface, x1, y1, x2, y2, color)
	if("drawLine" in function):
		if (len(arguments) != 5):
			print("Invalid drawLine call")
			return 0
		pygame.gfxdraw.line(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]),
			arguments[4])
		return 1

	# c++: drawRect (int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color)
	# py: rectangle(surface, rect, color)
	# note: rect is a quad statement like the color tuple
	# example: (x,y,w,h)
	if ("drawRect" in function):
		if (len(arguments) != 5):
			print("Invalid drawRect call")
			return 0
		rectangle = (int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]))
		pygame.gfxdraw.rectangle(lcd,
			rectangle,
			arguments[4])
		return 1

	# c++: fillRect (int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color)
	# py: box(surface, rect, color)
	# note: rect is a quad statement like the color tuple. 
	# example: (x,y,w,h)
	if ("fillRect" in function):
		if (len(arguments) != 5):
			print("Invalid fillRect call")
			return 0
		rectangle = (int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]))
		pygame.gfxdraw.box(lcd,
			rectangle,
			arguments[4])
		return 1

	# c++: drawCircle (int16_t x0, int16_t y0, int16_t r, uint16_t color)
	# py: circle(surface, x, y, r, color)
	if ("drawCircle" in function):
		if (len(arguments) != 4):
			print("Invalid drawCircle call")
			return 0
		pygame.gfxdraw.circle(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			arguments[3])
		return 1

	# c++: fillCircle (int16_t x0, int16_t y0, int16_t r, uint16_t color)
	# py: filled_circle(surface, x, y, r, color)
	if ("fillCircle" in function):
		if (len(arguments) != 4):
			print("Invalid fillCircle call")
			return 0
		pygame.gfxdraw.filled_circle(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			arguments[3])
		return 1

	# c++: drawEllipse (int16_t x0, int16_t y0, int16_t rw, int16_t rh, uint16_t color)
	# py: ellipse(surface, x, y, rx, ry, color)
	if ("drawEllipse" in function):
		if (len(arguments) != 5):
			print("Invalid drawEllipse call")
			return 0
		pygame.gfxdraw.ellipse(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]),
			arguments[4])
		return 1

	# c++: fillEllipse (int16_t x0, int16_t y0, int16_t rw, int16_t rh, uint16_t color)
	# py: filled_ellipse(surface, x, y, rx, ry, color)
	if ("fillEllipse" in function):
			if (len(arguments) != 5):
				print("Invalid fillEllipse call")
				return 0
			pygame.gfxdraw.filled_ellipse(lcd,
				int(arguments[0]),
				int(arguments[1]),
				int(arguments[2]),
				int(arguments[3]),
					arguments[4])
			return 1

	# c++: drawTriangle (int16_t x0, int16_t y0, int16_t x1, int16_t y1, int16_t x2, int16_t y2, uint16_t color)
	# py: trigon(surface, x1, y1, x2, y2, x3, y3, color)
	if ("drawTriangle" in function):
		if (len(arguments) != 7):
			print("Invalid drawTriangle call")
			return 0
		pygame.gfxdraw.trigon(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]),
			int(arguments[4]),
			int(arguments[5]),
			arguments[6])
		return 1

	# c++: fillTriangle (int16_t x0, int16_t y0, int16_t x1, int16_t y1, int16_t x2, int16_t y2, uint16_t color)
	# py: filled_trigon(surface, x1, y1, x2, y2, x3, y3, color)
	if ("fillTriangle" in function):
		if (len(arguments) != 7):
			print("Invalid fillTriangle call")
			return 0
		pygame.gfxdraw.filled_trigon(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]),
			int(arguments[4]),
			int(arguments[5]),
			arguments[6])
		return 1

	# c++: drawRoundRect (int16_t x0, int16_t y0, int16_t w, int16_t h, int16_t radius, uint16_t color)
	# py: uses line() and arc()
	# wow, this works well, dynamically too
	# arc() draws flipped unit circle, 0 degrees is positive x, 
	# 90 degrees is negative y
	if ("drawRoundRect" in function):
		if (len(arguments) != 6):
			print("Invalid drawRoundRect call")
			return 0
		x = int(arguments[0])
		y = int(arguments[1])
		w = int(arguments[2])
		h = int(arguments[3])
		r = int(arguments[4])
		color = arguments[5]
		pygame.gfxdraw.line(lcd,x+r,y,x+w-r,y,color) # top 
		pygame.gfxdraw.line(lcd,x,y+r,x,y+h-r,color) # right
		pygame.gfxdraw.line(lcd,x+w,y+r,x+w,y+h-r,color) # left
		pygame.gfxdraw.line(lcd,x+r,y+h,x+w-r,y+h,color) # bottom
		pygame.gfxdraw.arc(lcd, x+r,y+r,r,180,270,color) # top left corner
		pygame.gfxdraw.arc(lcd, x+w-r,y+r,r,270,0,color) # top right corner
		pygame.gfxdraw.arc(lcd, x+r,y+h-r,r,90,180,color) # bottom left corner
		pygame.gfxdraw.arc(lcd, x+w-r,y+h-r,r,0,90,color) # bottom right corner
		return 1

	# use rectangles and mke a cross looking shape
	# make a rectangle (x+r,y,w-r,h-r)
	# make a rectangle (x,y+r,w-r,h-r)
	if ("fillRoundRect" in function):
		if (len(arguments) != 6):
				print("Invalid fillRoundRect call")
				return 0
		x = int(arguments[0])
		y = int(arguments[1])
		w = int(arguments[2])
		h = int(arguments[3])
		r = int(arguments[4])
		color = arguments[5]
		rect_vert = (x+r,y,w-2*r,h) # vertical (center) rectangle
		rect_horz = (x,y+r,w+1,h-2*r) # horizontal (center) rectangle
		pygame.gfxdraw.box(lcd,rect_vert,color) # verticle rect
		pygame.gfxdraw.box(lcd,rect_horz,color) # horizontal rect
		pygame.gfxdraw.filled_circle(lcd, x+r,y+r,r,color) # top left corner
		pygame.gfxdraw.filled_circle(lcd, x+w-r,y+r,r,color) # top right corner
		pygame.gfxdraw.filled_circle(lcd, x+r,y+h-r,r,color) # bottom left corner
		pygame.gfxdraw.filled_circle(lcd, x+w-r,y+h-r,r,color) # bottom right corner
		return 1

def draw_lcd_overlay(screen_type, screen, startx, starty):
	if (screen_type == "64_OLED"):
		diffscreens.draw128x64oled(main_screen,startx,starty)
		pixel_color = screen_blue
	if (screen_type == "280LCD"):
		diffscreens.draw280x320lcd(main_screen,startx,starty)
		pixel_color = matte
	if (screen_type == "240LCD"):
		diffscreens.draw240x320lcd(main_screen,startx,starty)
		pixel_color = matte
	if (screen_type == "RNDLCD"):
		diffscreens.draw240x240roundlcd(main_screen,startx,starty)
		pixel_color = matte
	if (screen_type == "CSTMLCD"):
		diffscreens.drawlcd(main_screen,startx,starty,int(pixel_w),int(pixel_h))
		pixel_color = matte

def clear_lcd(screen_type, screen, startx, starty):
	main_screen.fill("white")
	display_screen.fill(pygame.SRCALPHA)
	draw_lcd_overlay(screen_type, screen, startx, starty)
	pygame.display.flip()

class pages(list):
	# this is an array of dictionaries: 
	# {"id": page_name, "functions": function}

	# here "functions" should be an array of function calls

	# i honestly think pages should control the canvas aswell


	# initialize with root page
	def __init__(self, root_page_name):
		if root_page_name == "":
			print("root name cannot be nothing, try root")
			return

		page_root = {"id": root_page_name, "functions": []} # no functions for now
		self.append(page_root)

		print("Pages initialized with root page name: ", root_page_name, "\n")

		return

	# return root page name that was initialized at the begining
	def root_page_name(self):
		return self[0]["id"]

	# return index of the name of a page
	def index_at_name(self, page_name):
		for i in range(len(self)):
			if self[i]["id"] == page_name:
				return i
		print("index_at_name: name not found")
		return -1

	# returns the functions for that page name
	def functions_at_name(self, page_name):
		for i in range(len(self)):
			if self[i]["id"] == page_name:
				return self[i]["functions"]
		print("functions_at_name: name not found")
		return 0

	def contains_name(self, page_name):
		for i in range(len(self)):
			if self[i]["id"] == page_name:
				return 1
		print("contains name: name not found")
		return 0

	# print out all the items (pages and functions) in the page array
	def list(self):
		for i in range(len(self)):
			print("Name: ", self[i]["id"], "\n")
			print("Functions: ", self[i]["functions"], "\n")
		return

	# create a new page, with the option to load it with functions
	def new(self, page_name, page_functions=[]):
		if self.contains_name(page_name):
			print("New: a page with that name already exists")
			return
		else:
			new_page = {"id": page_name, "functions": page_functions}
			self.append(new_page)
			print("New page: ", page_name, "created\n")
			return

	# load the current scope with all the functions currently in select page
	def load(self, page_name):
		clear_lcd(screen_type, main_screen, startx, starty)
		if self.contains_name(page_name):
			if len(self.functions_at_name(page_name)) != 0:
				for funcs, *args in self.functions_at_name(page_name):
					funcs(*args)
				main_screen.blit(display_screen, (x_pixels,y_pixels))
				pygame.display.flip()
				return self[self.index_at_name(page_name)]["functions"]
			else:
				print("Load: add some functions to the page")
				return
		else:
			print("Load: page not found, load failed\n")

	def edit(self, page_name, screen_layer):
		clear_lcd(screen_type, main_screen, startx, starty)
		if self.contains_name(page_name):
			function_stack = self[self.index_at_name(page_name)]["functions"]
			command = ""
			while command != "END":
				# Issue is here:::
				if len(function_stack) != 0:
					for funcs, *args in function_stack:
						funcs(*args)
						main_screen.blit(display_screen, (x_pixels,y_pixels))
						pygame.display.flip()
				command = input("Enter drawing function\n")
				# update screen to keep it updated with the commands
				if (command == '-1'):
					if (len(function_stack) < 1):
						print("no functions in stack\n")
						continue
					else:
						function_stack.pop()
						screen_layer.fill(pygame.SRCALPHA)
						draw_lcd_overlay(screen_type, main_screen, startx, starty)
						pygame.display.flip()
						print("function removed\n")
						continue
				if (command == '0'):
					# wipe function stack
					function_stack = []
					screen_layer.fill(pygame.SRCALPHA)
					draw_lcd_overlay(screen_type, main_screen, startx, starty)
					pygame.display.flip()
					print("stack cleared\n")
					continue
				if (command == ''):
					print("skipped line\n")
					continue

				if "(" in command or ")" in command:
					split_OB_off = command.split("(") # split open bracket
					func = split_OB_off[0]
					if (len(split_OB_off) <= 1):
						print("no arguments in function call\n")
					else:
						args = split_OB_off[1].replace(")","")
						args = args.replace(";","")

					args = args.split(",")
					for j in range(len(args)):
						if ("WHITE" in args[j]):
							args[j] = WHITE
						if ("BLACK" in args[j]):
							args[j] = BLACK
						if ("GREEN" in args[j]):
							args[j] = GREEN
						if ("RED" in args[j]):
							args[j] = RED
						if ("BLUE" in args[j]):
							args[j] = BLUE
						if ("YELLOW" in args[j]):
							args[j] = YELLOW
						if ("PINK" in args[j]):
							args[j] = PINK

					# as long as draw function does not return 0, add it to stack
					if draw_function(screen_layer, func, args):
						function_stack.append((draw_function, screen_layer, func, args))
			print("editing finished")
			self[self.index_at_name(page_name)]["functions"] = function_stack
			return
		else:
			print("Edit: page not found, edit failed\n")
			return

	def remove(self, page_name):
		if page_name == self.root_page_name():
			print("Remove: cannot remove root page")
			return 0
		if self.pop(self.index_at_name(page_name)):
			print("Remove: ", page_name, "success")
			self.load(self.root_page_name())
			return 1
		else:
			print("Remove: page not found, remove failed\n")
			return 0

page_list = pages("root")

# page_list.new("menu")
# page_list.list()
# page_list.remove("menu")
# page_list.list()

# function_example = [(draw_function, main_screen, 'drawRect', (5,5,200,200,(255,0,255)))]

# page_list.new("home", function_example)

# page_list.list()

# page_list.load("home")

# #page_list.edit("home", main_screen)

# page_list.list()


while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	if init == 0:
		main_screen.fill("white")
		display_screen.fill(pygame.SRCALPHA)
		draw_lcd_overlay(screen_type, main_screen, startx, starty)
		pygame.display.flip()

	cmd = input("enter page command\n")
	split_space = cmd.split(" ")

	if (len(split_space) < 2):
		print("Page: Invalid page call")
		continue
	# split_space[0] is just page (or should be)
	cmd = split_space[1]
	# for single command page calls
	if ("page" in split_space[0]):
		if (len(split_space) == 2):
			if (cmd == "current_page"):
				page_list.current_page()
				continue
			if (cmd == "list"):
				page_list.list()
				continue
		# now that the single cmd page calls left:
		if (len(split_space) != 3):
			print("Page: invalid page call")
			continue
		call_name = split_space[2]
		if (cmd == "new"):
			page_list.new(call_name)
			continue
		if (cmd == "remove"):
			page_list.remove(call_name)
			continue
		if (cmd == "load"):
			page_list.load(call_name)
			continue
		if (cmd == "edit"):
			page_list.edit(call_name, display_screen)

	init = 1
	main_screen.blit(display_screen, (x_pixels,y_pixels))

	pygame.display.flip()


	clock.tick(60)


