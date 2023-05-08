import pygame_widgets
import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown

pygame.init()
win = pygame.display.set_mode((1000, 600))

dropdown = Dropdown(
    win, 120, 10, 100, 50, name='Resolution',
    choices=[
        '1280 x 720',
        '1920 x 1080',
        '2560 x 1440',
        '3840 x 2160',
    ],
)

def print_value():
    print(dropdown.getSelected())

button = Button(
    win, 10, 10, 100, 50, text='Print Value', fontSize=30,
    margin=20, inactiveColour=(255, 0, 0), pressedColour=(0, 255, 0),
    radius=5, onClick=print_value, font=pygame.font.SysFont('calibri', 10),
    textVAlign='bottom'
)

slider_label = TextBox(win, 450, 10, 125, 50, fontSize=30)
slider = Slider(win, 100, 100, 800, 40, min=0, max=99, step=1)
output = TextBox(win, 475, 200, 50, 50, fontSize=30)

slider_label.disable()
output.disable() 


run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))


    slider_label.setText("Circle Size")
    output.setText(slider.getValue())

    pygame_widgets.update(events)
    pygame.display.update()