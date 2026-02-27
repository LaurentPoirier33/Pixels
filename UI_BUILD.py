import pygame
import pygame.gfxdraw

SCN_WDTH = 500
SCN_HGHT = 500

SCN_WDTH = input("enter screen width\n")
SCN_HGHT = input("enter screen height\n")

pygame.init()
lcd = pygame.display.set_mode((int(SCN_WDTH),int(SCN_HGHT)))
clock = pygame.time.Clock()
running = True

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

current_font = pygame.font.SysFont("Courier" , 20, False, False)
textColor = WHITE
backtextColor = BLACK
textSize = 10
cursor = (50,50)

function_stack = []

# draw the specific instruction
def draw_function(function, arguments):
	global textColor
	global backtextColor
	global textSize
	global cursor
	# c++: setTextColor (uint16_t c, OPTIONAL uint16_t bg) color, background color
	# py: textColor = (color_tuple), backtextColor = (color_tuple)
	if ("setTextColor" in function):
		if (len(arguments) != 1):
			print("Invalid setTextColor call at line", i+1)
			return
		textColor = arguments[0]

	# c++: setTextSize (uint8_t s)
	# py: textSize = (size)
	if ("setTextSize" in function):
		if (len(arguments) != 1):
			print("Invalid setTextSize call at line", i+1)
			return
		textSize = int(arguments[0]) * 10

	# c++: setCursor (int16_t x, int16_t y)
	# py: cursor = (x,y)
	if ("setCursor" in function):
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

	function_stack.append(lambda: draw_function(func, args))

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	lcd.fill("black")

	instruction = input("Enter line\n")
	handle_instruction(instruction)
	for func in function_stack:
		func()

	pygame.display.flip()
	clock.tick(60) # 60 fps

pygame.quit()