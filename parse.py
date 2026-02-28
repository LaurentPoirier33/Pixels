import pygame
import pygame.gfxdraw
import re

# CHIP = input("enter chip (e.g SSD1306)\n")

SCN_WDTH = 500
SCN_HGHT = 500
# --- dont forget to uncomment these ---
SCN_WDTH = input("enter screen width\n")
SCN_HGHT = input("enter screen height\n")
# --- 	 							 ---

meow = "meow"

pygame.init()
lcd = pygame.display.set_mode((int(SCN_WDTH),int(SCN_HGHT)))
clock = pygame.time.Clock()
running = True

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PINK = (255,0,255)


lines = []
print("enter c++ graphics text, end input with END")

functions = []
function_args = []

while True: 
	line = input()
	split_OB_off = line.split("(") # split open bracket
	functions.append(split_OB_off[0])
	if (len(split_OB_off) <= 1):
		print("no arguments in function call")
	else:
		temper = split_OB_off[1].replace(")","")
		function_args.append(temper.replace(";",""))
	if line == 'END':
		break
	lines.append(line)

full_text_body = '\n'.join(lines)
print("\n full text body:\n")
print(full_text_body)
print("\n");
for i in range(len(function_args)):
	print("\nfunction: ", functions[i], "function parameters: ", function_args[i], "\n")
# this works, and I like the printing of the full message

# need to replace color strings with color codes.
# for oled (SSD1306) the colors are black and white
# oh, I found tuples...

# text is complex, so here are some initialized values

# usage: # SysFont(name, size, bold=False, italic=False)
current_font = pygame.font.SysFont("Courier" , 20, False, False)
textColor = WHITE
backtextColor = BLACK
textSize = 10
cursor = (50,50)

def draw_function(function, arguments):
	global textColor
	global backtextColor
	global textSize
	global cursor
	# c++: setTextColor (uint16_t c, OPTIONAL uint16_t bg) color, background color
	# py: textColor = (color_tuple), backtextColor = (color_tuple)
	if ("setTextColor" in functions[i]):
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
			print("Invalid print call at line", i+1)
			return
		current_font = pygame.font.SysFont("Courier",
			textSize,
			False, 
			False)
		text = arguments[0].replace('"','')
		currentTextSurface = current_font.render(text,
			False,
			textColor,
			backtextColor)
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
			print("Invalid drawPixel call at line", i+1)
			return
		pygame.gfxdraw.pixel(lcd, 
			int(arguments[0]), 
			int(arguments[1]), 
			arguments[2])

	# c++: drawFastHLine (int16_t x, int16_t y, int16_t w, uint16_t color)
	# py: hline(surface, x1, x2, y, color)
	if ("drawFastHLine" in function):
		if (len(arguments) != 4):
			print("Invalid drawFastHLine call at line", i+1)
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
			print("Invalid drawFastVLine call at line", i+1)
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
			print("Invalid drawLine call at line", i+1)
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
			print("Invalid drawRect call at line", i+1)
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
			print("Invalid fillRect call at line", i+1)
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
			print("Invalid drawCircle call at line", i+1)
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
			print("Invalid fillCircle call at line", i+1)
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
			print("Invalid drawEllipse call at line", i+1)
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
				print("Invalid fillEllipse call at line", i+1)
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
			print("Invalid drawTriangle call at line", i+1)
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
			print("Invalid fillTriangle call at line", i+1)
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
		rect_horz = (x,y+r,w,h-2*r) # horizontal (center) rectangle
		pygame.gfxdraw.box(lcd,rect_vert,color) # verticle rect
		pygame.gfxdraw.box(lcd,rect_horz,color) # horizontal rect
		pygame.gfxdraw.filled_circle(lcd, x+r,y+r,r,color) # top left corner
		pygame.gfxdraw.filled_circle(lcd, x+w-r,y+r,r,color) # top right corner
		pygame.gfxdraw.filled_circle(lcd, x+r,y+h-r,r,color) # bottom left corner
		pygame.gfxdraw.filled_circle(lcd, x+w-r,y+h-r,r,color) # bottom right corner

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	lcd.fill("black")

	for i in range(len(functions)):

		if (i >= len(function_args)):
			break;

# replace colors with tuples
		parameters = function_args[i].split(",")
		for j in range(len(parameters)):
				if ("WHITE" in parameters[j]):
					parameters[j] = WHITE
				if ("BLACK" in parameters[j]):
					parameters[j] = BLACK
				if ("GREEN" in parameters[j]):
					parameters[j] = GREEN
				if ("RED" in parameters[j]):
					parameters[j] = RED
				if ("BLUE" in parameters[j]):
					parameters[j] = BLUE
				if ("YELLOW" in parameters[j]):
					parameters[j] = YELLOW
				if ("PINK" in parameters[j]):
					parameters[j] = PINK

		draw_function(functions[i],parameters)

	pygame.display.flip()
	clock.tick(60) # 60 fps

pygame.quit()

# use: https://www.pygame.org/docs/ref/gfxdraw.html#pygame.gfxdraw.hline
# use: https://adafruit.github.io/Adafruit-GFX-Library/html/class_adafruit___g_f_x.html
# use: https://adafruit.github.io/Adafruit_SSD1306/html/class_adafruit___s_s_d1306.html

