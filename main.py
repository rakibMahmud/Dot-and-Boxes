from Play import *
import pygame_menu
from pygame_menu import themes

pygame.init()

rows = 5
cols = 5
depth = 2

surface = pygame.display.set_mode((480, 480))

def set_depth(d, value):
    global depth
    if value==1:
        depth = 2
    elif value==2:
        depth = 3
    elif value==3:
        depth = 4
    

def set_size(value, id): 
    global rows
    global cols
    if id == 1:
        rows, cols= 5, 5
    elif id == 2:
        rows, cols = 7, 7
    elif id == 3:
        rows, cols = 9, 9
    elif id == 4:
        rows, cols = 11, 11



def start_the_game():
    mainmenu._open(loading)
    pygame.time.set_timer(update_loading, 30)

def depth_menu():
    mainmenu._open(depthbut)

def grid_menu():
    mainmenu._open(grd)


custom_theme = pygame_menu.themes.Theme(
    background_color=(0, 0, 0),  # Change the background color to RGB (0, 0, 0) - black
    title_font_size=30,  # Increase the title font size to 30 pixels
    widget_font_size=18,  # Decrease the widget font size to 18 pixels
    widget_font_color=(255, 255, 255),  # Change the widget font color to RGB (255, 255, 255) - white
    selection_color=(0, 128, 255),  # Change the selection color to RGB (0, 128, 255) - blue
    widget_padding=(10, 10),  # Modify the widget padding to (10, 10)
    widget_margin=(0, 15),  # Modify the widget margin to (0, 15)
    title_font='calibri',  # Change the title font to 'calibri'
    widget_font='calibri'  # Change the widget font to 'calibri'
)



mainmenu = pygame_menu.Menu('Welcome', 480, 480, theme=custom_theme)
mainmenu.add.label('Cap the Cells!!!', font_size=30, font_color=(255, 255, 255))
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Select Depth', depth_menu)
mainmenu.add.button('Select Grid Size', grid_menu)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)

grd = pygame_menu.Menu('Select a Size', 480, 480, theme=custom_theme)
grd.add.selector('Grid :', [('2 * 2', 1), ('3 * 3', 2), ('4 * 4', 3), ('5 * 5', 4)], onchange=set_size)
grd.add.button('Back', pygame_menu.events.BACK)
depthbut = pygame_menu.Menu('Select Depth', 480, 480, theme=custom_theme)
depthbut.add.selector('Depth :', [('2', 1), ('3', 2) , ('4', 3)], onchange=set_depth)
depthbut.add.button('Back', pygame_menu.events.BACK)
loading = pygame_menu.Menu('Loading the Game...', 480, 480, theme=custom_theme)
loading.add.progress_bar("Progress", progressbar_id="1", default=0, width=200)

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(20, 30))  


update_loading = pygame.USEREVENT + 0

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == update_loading:
            progress = loading.get_widget("1")
            progress.set_value(progress.get_value() + 1)
            if progress.get_value() == 100:
                pygame.time.set_timer(update_loading, 0)
                Match = Play(cols, rows, depth)
                Match.start()
        if event.type == pygame.QUIT:
            running = False

    if mainmenu.is_enabled():
        mainmenu.update(events)
        mainmenu.draw(surface)
        if mainmenu.get_current().get_selected_widget():
            selected_widget = mainmenu.get_current().get_selected_widget()
            pygame.draw.rect(
                surface,
                (255, 255, 255),
                (
                    selected_widget.get_rect().x - 5,
                    selected_widget.get_rect().y - 5,
                    selected_widget.get_rect().width + 10,
                    selected_widget.get_rect().height + 10,
                ),
                3,
            )
            arrow.draw(surface, mainmenu.get_current().get_selected_widget())

    pygame.display.update()

