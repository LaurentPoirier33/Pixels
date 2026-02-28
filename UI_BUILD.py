import pygame
import pygame.gfxdraw
import re
import diffscreens

# skip the graphics entry once, to allow the ui to load
init = 0

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

print("Usage tips:\n") 
print("128x64 OLED -> screen_type = 64_OLED\n")
print("280x320 lcd -> screen_type = 280LCD\n")
print("240x320 lcd -> screen_type = 240LCD\n")
print("240x240 round lcd -> screen_type = RNDLCD\n")
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

function_stack = []

# draw the specific instruction
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
			return
		textColor = arguments[0]

	# c++: setTextSize (uint8_t s)
	# py: textSize = (size)
	if re.search(r"\bsetTextSize\b", function):
		if (len(arguments) != 1):
			print("Invalid setTextSize call at line", i+1)
			return
		textSize = int(arguments[0]) * 10

	# c++: setCursor (int16_t x, int16_t y)
	# py: cursor = (x,y)
	if re.search(r"\bsetCursor\b", function):
		if (len(arguments) != 2):
			print("Invalid setCursor call at line", i+1)
			return
		cursor = (int(arguments[0]), int(arguments[1]))

	# c++: print(string)
	# py: surface = font.render(text, antialias, color, background=None)
	#	  blit(surface, (x,y))
	# antialias is a boolean, if True then smooth letters, this is there because fonts are usually pixel dense
	# no bachground argument for transparent background
	if ("print" in function):
		if (len(arguments) != 1):
			print("Invalid print call")
			return
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

	# c++: clearDisplay (void)
	# py: fill(color, rect=None, special_flags=0)
	if ("clearDisplay" in function):
		lcd.fill("black")

	# c++: fillScreen (uint16_t color)
	# py: fill(color, rect=None, special_flags=0)
	if ("fillScreen" in function):
		if (len(arguments) != 1):
			print("Invalid fillScreen call")
			return
		lcd.fill(arguments[0])

	# c++: drawPixel (int16_t x, int16_t y, uint16_t color)
	# py: pixel(surface, x, y, color)
	if "drawPixel" in function:
		if (len(arguments) != 3):
			print("Invalid drawPixel call")
			return
		pygame.gfxdraw.pixel(lcd, 
			int(arguments[0]), 
			int(arguments[1]), 
			arguments[2])

	# c++: drawFastHLine (int16_t x, int16_t y, int16_t w, uint16_t color)
	# py: hline(surface, x1, x2, y, color)
	if ("drawFastHLine" in function):
		if (len(arguments) != 4):
			print("Invalid drawFastHLine call")
			return
		pygame.gfxdraw.hline(lcd,
			int(arguments[0]),
			(int(arguments[0])+int(arguments[2])), # x1 + w = x2
			int(arguments[1]), 
			arguments[3])
		
	# c++: drawFastVLine (int16_t x, int16_t y, int16_t h, uint16_t color)
	# py: vline(surface, x, y1, y2, color)
	if ("drawFastVLine" in function):
		if (len(arguments) != 4):
			print("Invalid drawFastVLine call")
			return
		pygame.gfxdraw.vline(lcd,
			int(arguments[0]),
			int(arguments[1]),
			(int(arguments[1]) + int(arguments[2])), # y1 + h = y2
			arguments[3])

	# c++: drawLine (int16_t x0, int16_t y0, int16_t x1, int16_t y1, uint16_t color)
	# pi: line(surface, x1, y1, x2, y2, color)
	if("drawLine" in function):
		if (len(arguments) != 5):
			print("Invalid drawLine call")
			return
		pygame.gfxdraw.line(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]),
			arguments[4])

	# c++: drawRect (int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color)
	# py: rectangle(surface, rect, color)
	# note: rect is a quad statement like the color tuple
	# example: (x,y,w,h)
	if ("drawRect" in function):
		if (len(arguments) != 5):
			print("Invalid drawRect call")
			return
		rectangle = (int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]))
		pygame.gfxdraw.rectangle(lcd,
			rectangle,
			arguments[4])

	# c++: fillRect (int16_t x, int16_t y, int16_t w, int16_t h, uint16_t color)
	# py: box(surface, rect, color)
	# note: rect is a quad statement like the color tuple. 
	# example: (x,y,w,h)
	if ("fillRect" in function):
		if (len(arguments) != 5):
			print("Invalid fillRect call")
			return
		rectangle = (int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]))
		pygame.gfxdraw.box(lcd,
			rectangle,
			arguments[4])

	# c++: drawCircle (int16_t x0, int16_t y0, int16_t r, uint16_t color)
	# py: circle(surface, x, y, r, color)
	if ("drawCircle" in function):
		if (len(arguments) != 4):
			print("Invalid drawCircle call")
			return
		pygame.gfxdraw.circle(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			arguments[3])

	# c++: fillCircle (int16_t x0, int16_t y0, int16_t r, uint16_t color)
	# py: filled_circle(surface, x, y, r, color)
	if ("fillCircle" in function):
		if (len(arguments) != 4):
			print("Invalid fillCircle call")
			return
		pygame.gfxdraw.filled_circle(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			arguments[3])

	# c++: drawEllipse (int16_t x0, int16_t y0, int16_t rw, int16_t rh, uint16_t color)
	# py: ellipse(surface, x, y, rx, ry, color)
	if ("drawEllipse" in function):
		if (len(arguments) != 5):
			print("Invalid drawEllipse call")
			return
		pygame.gfxdraw.ellipse(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]),
			arguments[4])

	# c++: fillEllipse (int16_t x0, int16_t y0, int16_t rw, int16_t rh, uint16_t color)
	# py: filled_ellipse(surface, x, y, rx, ry, color)
	if ("fillEllipse" in function):
			if (len(arguments) != 5):
				print("Invalid fillEllipse call")
				return
			pygame.gfxdraw.filled_ellipse(lcd,
				int(arguments[0]),
				int(arguments[1]),
				int(arguments[2]),
				int(arguments[3]),
					arguments[4])

	# c++: drawTriangle (int16_t x0, int16_t y0, int16_t x1, int16_t y1, int16_t x2, int16_t y2, uint16_t color)
	# py: trigon(surface, x1, y1, x2, y2, x3, y3, color)
	if ("drawTriangle" in function):
		if (len(arguments) != 7):
			print("Invalid drawTriangle call")
			return
		pygame.gfxdraw.trigon(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]),
			int(arguments[4]),
			int(arguments[5]),
			arguments[6])

	# c++: fillTriangle (int16_t x0, int16_t y0, int16_t x1, int16_t y1, int16_t x2, int16_t y2, uint16_t color)
	# py: filled_trigon(surface, x1, y1, x2, y2, x3, y3, color)
	if ("fillTriangle" in function):
		if (len(arguments) != 7):
			print("Invalid fillTriangle call")
			return
		pygame.gfxdraw.filled_trigon(lcd,
			int(arguments[0]),
			int(arguments[1]),
			int(arguments[2]),
			int(arguments[3]),
			int(arguments[4]),
			int(arguments[5]),
			arguments[6])
	# c++: drawRoundRect (int16_t x0, int16_t y0, int16_t w, int16_t h, int16_t radius, uint16_t color)
	# py: uses line() and arc()
	# wow, this works well, dynamically too
	# arc() draws flipped unit circle, 0 degrees is positive x, 
	# 90 degrees is negative y
	if ("drawRoundRect" in function):
		if (len(arguments) != 6):
			print("Invalid drawRoundRect call")
			return
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

	# use rectangles and mke a cross looking shape
	# make a rectangle (x+r,y,w-r,h-r)
	# make a rectangle (x,y+r,w-r,h-r)
	if ("fillRoundRect" in function):
		if (len(arguments) != 6):
				print("Invalid fillRoundRect call")
				return
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
# filter the instruction and parse to draw_function
def handle_instruction(instruction):
	global function_stack

	if (instruction == '-1'):
		if (len(function_stack) < 1):
			print("no functions in stack")
			return
		else:
			function_stack.pop()
			print("function removed")
			return
	if (instruction == '0'):
		# wipe function stack
		function_stack = []
		print("stack cleared")
		return
	if (instruction == ''):
		print("skipped line")
		return
	else:
		if "(" not in instruction or ")" not in instruction:
			print("not a real function")
			return
		split_OB_off = instruction.split("(") # split open bracket
		func = split_OB_off[0]
		if (len(split_OB_off) <= 1):
			print("no arguments in function call")
		else:
			args = split_OB_off[1].replace(")","")
			args = args.replace(";","")

		args = args.split(",")
		for j in range(len(args)):
			if (screen_type == "64_OLED"):
				if ("WHITE" in args[j]):
					args[j] = WHITE
				if ("BLACK" in args[j]):
					args[j] = BLACK
				if ("GREEN" in args[j]):
					print("only white or black on this oled")
					return
				if ("RED" in args[j]):
					print("only white or black on this oled")
					return		
				if ("BLUE" in args[j]):
					print("only white or black on this oled")
					return
				if ("YELLOW" in args[j]):
					print("only white or black on this oled")
					return
				if ("PINK" in args[j]):
					print("only white or black on this oled")
					return
			else:
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

	function_stack.append(lambda: draw_function(display_screen, func, args))

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	main_screen.fill("white")
	if (screen_type == "64_OLED"):
		diffscreens.draw128x64oled(main_screen,startx,starty)
	if (screen_type == "280LCD"):
		diffscreens.draw280x320lcd(main_screen,startx,starty)
	if (screen_type == "240LCD"):
		diffscreens.draw240x320lcd(main_screen,startx,starty)
	if (screen_type == "RNDLCD"):
		diffscreens.draw240x240roundlcd(main_screen,startx,starty)

	if (init == 1):
		instruction = input("Enter line\n")
		handle_instruction(instruction)
		for func in function_stack:
			func()
			main_screen.blit(display_screen, (x_pixels,y_pixels))

	init = 1
	pygame.display.flip()
	clock.tick(60) # 60 fps

pygame.quit()