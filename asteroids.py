from designer import *
from random import randint

background_image('black.jpg')

World = {
    'ship': DesignerObject,
    'xvel': float,
    'yvel': float
}

MAX_VELOCITY: 3

def create_ship() -> DesignerObject:
    ship = image('ship.png')
    ship['scale'] = .5
    return ship

def create_world() -> World:
    return {
        'ship': create_ship(),
        'xvel': 0,
        'yvel': 0
    }

def move_ship(world: World):
    world['ship']['x'] += world['xvel']
    world['ship']['y'] += world['yvel']
    if world['ship']['x'] < 0:
        world['ship']['x'] = get_width()
    elif world['ship']['x'] > get_width():
        world['ship']['x'] = 0
        
    if world['ship']['y'] < 0:
        world['ship']['y'] = get_height()
    elif world['ship']['y'] > get_height():
        world['ship']['y'] = 0

def change_vel(world: World, key: str):
    if key == 'a':
        world['xvel'] = -3
    elif key == 'd':
        world['xvel'] = 3
    elif key == 'w':
        world['yvel'] = -3
    elif key == 's':
        world['yvel'] = 3
        
def decel(world: World):
    if world['xvel'] < 0:
        world['xvel'] += 0.1
    elif world['xvel'] > 0:
        world['xvel'] -= 0.1
        
    if world['yvel'] < 0:
        world['yvel'] += 0.1
    elif world['yvel'] > 0:
        world['yvel'] -= 0.1

when('starting', create_world)
when('updating', move_ship)
when('typing', change_vel)
when('updating', decel)
start()