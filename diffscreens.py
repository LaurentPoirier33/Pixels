import pygame
import pygame.gfxdraw

# colors
pcb_blue = (0,120,160)
screen_blue = (0,0,60)
solder_silver = (150,150,150)
white = (255,255,255)
black = (0,0,0)
orange = (250,170,0)
grey = (100,100,100)
matte = (25,25,25)

def draw128x64oled(screen,x,y):
	# entire pcb dimesnions
	oled_width = 145 # pcb width
	oled_height = 140 # pcb height
	
	# amount of space between the top of the backing and top of pcb
	top_clearence = 25

	# actual pixel area
	pixels_width = 128
	pixels_height = 64
	x_pixels = x+8
	y_pixels = y+(oled_height/2-pixels_height/2)

	# black screen backing (backing of actual pixel area)
	scn_back_w = pixels_width+8
	scn_back_h = pixels_height+25
	scn_back_x = x+(oled_width/2-scn_back_w/2)
	scn_back_y = y+top_clearence

	# orange ribbon cable
	scn_back_ext_w = oled_width/3
	scn_back_ext_h = 19
	scn_back_ext_x = x+(oled_width/2-scn_back_ext_w/2)
	scn_back_ext_y = y+(oled_height-scn_back_ext_h-7)

	# black over orange ribbon cable
	ribn_cov_x = scn_back_ext_x + 4
	ribn_cov_y = scn_back_ext_y
	ribn_cov_w = scn_back_ext_w - 8
	ribn_cov_h = scn_back_ext_h

	# pcb notch for ribbon cable
	pcb_notch_w = oled_width/2.5
	pcb_notch_h = 10
	pcb_notch_x = x+(oled_width/2-pcb_notch_w/2)
	pcb_notch_y = y+(oled_height-pcb_notch_h)

	pin_x = 10
	pin_y = 10
	pin1_x = x+50
	pin2_x = pin1_x+11
	pin3_x = pin2_x+11
	pin4_x = pin3_x+11

	# rectangle definitions
	pin1 = (pin1_x,y+2,pin_x,pin_y)
	pin2 = (pin2_x,y+2,pin_x,pin_y)
	pin3 = (pin3_x,y+2,pin_x,pin_y)
	pin4 = (pin4_x,y+2,pin_x,pin_y)
	pcb = (x,y,oled_width,oled_height)
	pixels = (x_pixels,y_pixels,pixels_width,pixels_height)
	scn_back = (scn_back_x,scn_back_y,scn_back_w,scn_back_h)
	scn_back_ext = (scn_back_ext_x,scn_back_ext_y,scn_back_ext_w,scn_back_ext_h)
	ribn_cov = (ribn_cov_x,ribn_cov_y,ribn_cov_w,ribn_cov_h)
	pcb_notch = (pcb_notch_x,pcb_notch_y,pcb_notch_w,pcb_notch_h)

	# stacked in a specific order
	pygame.gfxdraw.box(screen,pcb,pcb_blue)
	pygame.gfxdraw.box(screen,pcb_notch,white)
	pygame.gfxdraw.box(screen,scn_back,black)
	pygame.gfxdraw.box(screen,scn_back_ext,orange)
	pygame.gfxdraw.box(screen,ribn_cov,black)
	pygame.gfxdraw.box(screen,pixels,screen_blue)
	pygame.gfxdraw.box(screen,pin1,solder_silver)
	pygame.gfxdraw.box(screen,pin2,solder_silver)
	pygame.gfxdraw.box(screen,pin3,solder_silver)
	pygame.gfxdraw.box(screen,pin4,solder_silver)
	pygame.gfxdraw.filled_circle(screen,x+10,y+10,10,solder_silver)
	pygame.gfxdraw.filled_circle(screen,x+10,y+10,5,white)
	pygame.gfxdraw.filled_circle(screen,x+oled_width-11,y+10,10,solder_silver)
	pygame.gfxdraw.filled_circle(screen,x+oled_width-11,y+10,5,white)
	pygame.gfxdraw.filled_circle(screen,x+10,y+oled_height-11,10,solder_silver)
	pygame.gfxdraw.filled_circle(screen,x+10,y+oled_height-11,5,white)
	pygame.gfxdraw.filled_circle(screen,x+oled_width-11,y+oled_height-11,10,solder_silver)
	pygame.gfxdraw.filled_circle(screen,x+oled_width-11,y+oled_height-11,5,white)
def draw280x320lcd(screen,x,y):
	# x and y are starting point for everything
	lcd_w = 280
	lcd_h = 320
	lcd_x = x+5
	lcd_y = y+5

	carrier_w = lcd_w + 10 # 5 pixels on each side
	carrier_h = lcd_h + 30 # large bump at bottom

	# Ribbon Cable Width
	r_c_w = lcd_w/1.5 
	r_c_h = 30
	r_c_x = x+(carrier_w/2-r_c_w/2)
	r_c_y = y+carrier_h

	# Secondary Ribbon Cable
	rc2_w = r_c_w/1.5
	rc2_h = 45
	rc2_x = r_c_x+(r_c_w/2-rc2_w/2)
	rc2_y = r_c_y+r_c_h

	# Black bar on secondary ribbon cable
	bs_w = r_c_w/1.5
	bs_h = 23
	bs_x = r_c_x+(r_c_w/2-rc2_w/2)
	bs_y = rc2_y+bs_h

	# rectangles
	pcb = (x,y,carrier_w,carrier_h)
	pixels = (lcd_x,lcd_y,lcd_w,lcd_h)
	ribbon = (r_c_x,r_c_y,r_c_w,r_c_h)
	ribbon2 = (rc2_x,rc2_y,rc2_w,rc2_h)
	blackspot = (bs_x,bs_y,bs_w,bs_h)

	# draws
	pygame.gfxdraw.box(screen,pcb,black)
	pygame.gfxdraw.box(screen,pixels,matte)
	pygame.gfxdraw.box(screen,ribbon,orange)
	pygame.gfxdraw.box(screen,ribbon2,orange)
	pygame.gfxdraw.box(screen,blackspot,black)
def draw240x320lcd(screen,x,y):
	# x and y are starting point for everything
	lcd_w = 240
	lcd_h = 320
	lcd_x = x+5
	lcd_y = y+5

	carrier_w = lcd_w + 10 # 5 pixels on each side
	carrier_h = lcd_h + 30 # large bump at bottom

	# Ribbon Cable Width
	r_c_w = lcd_w/1.5 
	r_c_h = 30
	r_c_x = x+(carrier_w/2-r_c_w/2)
	r_c_y = y+carrier_h

	# Secondary Ribbon Cable
	rc2_w = r_c_w/1.5
	rc2_h = 45
	rc2_x = r_c_x+(r_c_w/2-rc2_w/2)
	rc2_y = r_c_y+r_c_h

	# Black bar on secondary ribbon cable
	bs_w = r_c_w/1.5
	bs_h = 23
	bs_x = r_c_x+(r_c_w/2-rc2_w/2)
	bs_y = rc2_y+bs_h

	# rectangles
	pcb = (x,y,carrier_w,carrier_h)
	pixels = (lcd_x,lcd_y,lcd_w,lcd_h)
	ribbon = (r_c_x,r_c_y,r_c_w,r_c_h)
	ribbon2 = (rc2_x,rc2_y,rc2_w,rc2_h)
	blackspot = (bs_x,bs_y,bs_w,bs_h)

	# draws
	pygame.gfxdraw.box(screen,pcb,black)
	pygame.gfxdraw.box(screen,pixels,matte)
	pygame.gfxdraw.box(screen,ribbon,orange)
	pygame.gfxdraw.box(screen,ribbon2,orange)
	pygame.gfxdraw.box(screen,blackspot,black)
def draw240x240roundlcd(screen,x,y):

	screen_width = 240
	screen_height = 240
	screen_radius = 120	
	backing_radius = screen_radius+5 # 5 pixels everywhere
	x_center = x+screen_radius
	y_center = x+screen_radius # purposfully repeated

	rbn_back_w = screen_radius
	rbn_back_h = 40
	rbn_back_x = x_center-(rbn_back_w/2)
	rbn_back_y = y_center+(screen_radius-rbn_back_h/2)

	rbn_w = screen_radius-6 # three pixels on either side
	rbn_h = rbn_back_h+5 # overlapping rbn_back
	rbn_x = x_center-(rbn_w/2)
	rbn_y = y_center+(screen_radius-rbn_back_h/2)

	# rectangles:
	rbn_back = (rbn_back_x,rbn_back_y,rbn_back_w,rbn_back_h)
	rbn = (rbn_x,rbn_y,rbn_w,rbn_h)

	pygame.gfxdraw.box(screen,rbn_back,black)
	pygame.gfxdraw.box(screen,rbn,orange)
	pygame.gfxdraw.filled_circle(screen,x_center,y_center,backing_radius,black)
	pygame.gfxdraw.filled_circle(screen,x_center,y_center,screen_radius,matte)

def drawlcd(screen,x,y,lcd_w,lcd_h):
	# x and y are starting point for everything
	lcd_x = x+5
	lcd_y = y+5

	carrier_w = lcd_w + 10 # 5 pixels on each side
	carrier_h = lcd_h + 30 # large bump at bottom

	# Ribbon Cable Width
	r_c_w = lcd_w/1.5 
	r_c_h = 30
	r_c_x = x+(carrier_w/2-r_c_w/2)
	r_c_y = y+carrier_h

	# Secondary Ribbon Cable
	rc2_w = r_c_w/1.5
	rc2_h = 45
	rc2_x = r_c_x+(r_c_w/2-rc2_w/2)
	rc2_y = r_c_y+r_c_h

	# Black bar on secondary ribbon cable
	bs_w = r_c_w/1.5
	bs_h = 23
	bs_x = r_c_x+(r_c_w/2-rc2_w/2)
	bs_y = rc2_y+bs_h

	# rectangles
	pcb = (x,y,carrier_w,carrier_h)
	pixels = (lcd_x,lcd_y,lcd_w,lcd_h)
	ribbon = (r_c_x,r_c_y,r_c_w,r_c_h)
	ribbon2 = (rc2_x,rc2_y,rc2_w,rc2_h)
	blackspot = (bs_x,bs_y,bs_w,bs_h)

	# draws
	pygame.gfxdraw.box(screen,pcb,black)
	pygame.gfxdraw.box(screen,pixels,matte)
	pygame.gfxdraw.box(screen,ribbon,orange)
	pygame.gfxdraw.box(screen,ribbon2,orange)
	pygame.gfxdraw.box(screen,blackspot,black)
