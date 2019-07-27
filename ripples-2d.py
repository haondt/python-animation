from tkinter import *

window = Tk()

target_fps = 30
canvas_width = 500
canvas_height = 500

canvas = Canvas(window, width=canvas_width, height=canvas_height)

def draw_rect():
	canvas.create_rectangle(0,0,10,10, fill="#FFFFFF")
	


canvas.pack()

y = int(canvas_height /2)
#canvas.create_line(0,y,canvas_width,y,fill="#476042")
#myRect = canvas.create_rectangle(0,0,10,10,fill="#FFFFFF")

rects = []
rect_spacing = 0
rect_width = 25
rect_height = 200
num_rects = (canvas_width-100) // (rect_spacing+rect_width)
if num_rects % 2 == 0: num_rects -= 1

vert_center = canvas_height // 2
hori_center = canvas_width//2
for i in range(num_rects):
	x1 = hori_center + (i - (num_rects//2))*(rect_spacing+rect_width)

	x2 = x1+rect_width
	y1 = vert_center - rect_height // 2
	y2 = y1 + rect_height
	rects.append(canvas.create_rectangle(x1,y1,x2,y2,fill="#FFFFFF",outline=""))

def scale_rects(rects,heights):
	for i in range(len(rects)):
		#x1,y1,x2,y2 = canvas.coords(rect)
		x1 = hori_center + (i - (num_rects//2))*(rect_spacing+rect_width)

		x2 = x1+rect_width
		y1 = vert_center - heights[i] // 2
		y2 = y1 + heights[i]

		canvas.coords(rects[i], x1,y1,x2,y2)

min_height = 100
max_height = canvas_height-100

rectPos = 0
direction = 1
wavelength = 10
init_step = (max_height-min_height)//wavelength
step = 10
max_height = min_height + init_step*wavelength
directions = [step for i in range(num_rects)]
rect_sizes = [None for i in range(len(rects))]
init_dir = init_step
init_size = min_height

start_dir = -step

for i in range(num_rects//2+1):
	
	if (init_size <= min_height):
		init_size = min_height
		init_dir = init_step
		start_dir = -step
	elif (init_size >= max_height):
		init_size = max_height
		init_dir = -init_step
		start_dir = step
	rect_sizes[num_rects//2+i] = init_size
	rect_sizes[num_rects//2-i] = init_size
	directions[num_rects//2+i] = start_dir
	directions[num_rects//2-i] = start_dir
	init_size += init_dir

def frame_step():
	global rectPos, direction, target_fps
	global rects, rect_sizes, directions
	global canvas_width
	global min_height, max_height
	for i in range(num_rects):
		if rect_sizes[i] >= max_height:
			rect_sizes[i] = 2*max_height - rect_sizes[i]
			directions[i] = -step
		elif rect_sizes[i] <= min_height:
			rect_sizes[i] = 2*min_height - rect_sizes[i]
			directions[i] = step
	for i in range(num_rects):
		rect_sizes[i] += directions[i]
	
		
	scale_rects(rects, rect_sizes)
	canvas.after(1000//target_fps, frame_step)

frame_step()

input()
