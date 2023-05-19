import pygame_widgets
import pygame
import subprocess
import threading
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import sys


pygame.init()
win = pygame.display.set_mode((1000, 600))

dropdown = Dropdown(
    win, 100, 200, 200, 50, name='Resolution',
    choices=[        
        '800 x 600',
        '1024 x 768',        
        '1280 x 720',        
        '1366 x 768',        
        '1920 x 1080',        
        '2560 x 1440',        
        '3840 x 2160',    
    ],
)

 
def open_python_file(circle_size, resolution):
    command = ['python', 'Aimlabs.py', str(circle_size), str(resolution[0]), str(resolution[1])]
    subprocess.run(command)

def start_button_callback():
    circle_size = slider.getValue()
    resolution_str = dropdown.getSelected()

    if resolution_str:
        resolution = parse_resolution(resolution_str)
    else:
        resolution = (800, 600)

    threading.Thread(target=open_python_file, args=(circle_size, resolution)).start()
def parse_resolution(resolution_str):
    width, height = resolution_str.split(' x ')
    return int(width), int(height)

button = Button(
    win, 700, 200, 200, 50,  text='Start', fontSize=30,
    margin=20, inactiveColour=(175, 175, 175), pressedColour=(100, 100, 100),
    textVAlign='bottom', onClick=start_button_callback
)

slider_label = TextBox(win, 450, 10, 125, 50, fontSize=30)
slider = Slider(win, 100, 100, 800, 40, min=1, max=100, step=1)
output = TextBox(win, 450, 200, 100, 100, fontSize=60)
Title = TextBox(win, 120, 350, 760, 100, fontSize=50)

slider_label.disable()
output.disable() 

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            sys.exit()

    win.fill((255, 255, 255))

    slider_label.setText("Circle Size")
    # Too lazy to find out how to text align, don't judge
    Title.setText("          Aimbot trainer by WabooJoneies")

    circle_size = slider.getValue()
    dropdown_value = dropdown.getSelected()

    output.setText(slider.getValue())

    pygame_widgets.update(events)
    pygame.display.update()
