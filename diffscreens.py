import pygame
import pygame.gfxdraw

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
	
	# colors
	pcb_blue = (0,120,160)
	screen_blue = (0,0,60)
	solder_silver = (150,150,150)
	white = (255,255,255)
	black = (0,0,0)
	orange = (250,180,0)

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
	

