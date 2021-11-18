from designer import *
from random import randint, uniform

set_window_color('black')

World = {
    'ship': DesignerObject,
    'asteroids': [DesignerObject],
    'xvel': float,
    'yvel': float,
    'rot': int,
    'asteroids xvel': [float],
    'asteroids yvel': [float],
    'asteroids rvel': [float],
    'asteroids size': [int]
}

MAX_VELOCITY: 3

def create_ship() -> DesignerObject:
    ship = image('ship.png')
    ship['scale'] = .75
    return ship

def move_ship(world: World):
    # constantly move ship based on velocity
    world['ship']['x'] += world['xvel']
    world['ship']['y'] += world['yvel']
    
    # wrap around the window if hits the edges
    if world['ship']['x'] < 0:
        world['ship']['x'] = get_width()
    elif world['ship']['x'] > get_width():
        world['ship']['x'] = 0
        
    if world['ship']['y'] < 0:
        world['ship']['y'] = get_height()
    elif world['ship']['y'] > get_height():
        world['ship']['y'] = 0

def change_vel(world: World, key: str):
    # CHANGE THESE TO HOLDING - maintain constant velocity as long as key is held
    if key == 'a':
        world['xvel'] = -3
    elif key == 'd':
        world['xvel'] = 3
    elif key == 'w':
        world['yvel'] = -3
    elif key == 's':
        world['yvel'] = 3
    elif key == 'left':
        world['ship']['angle'] -= 10
    elif key == 'right':
        world['ship']['angle'] += 10
        
def decel(world: World):
    # natural deceleration of ship when rockets are unpowered
    if world['xvel'] < 0:
        world['xvel'] += 0.1
    elif world['xvel'] > 0:
        world['xvel'] -= 0.1
        
    if world['yvel'] < 0:
        world['yvel'] += 0.1
    elif world['yvel'] > 0:
        world['yvel'] -= 0.1
        
def create_asteroid() -> DesignerObject:
    asteroid = image('asteroid.png')
    asteroid['scale'] = 1
    return asteroid

def make_asteroids(world: World):
    # less than 10 asteroids? create an asteroid    
    not_too_many = len(world['asteroids']) < 10
    
    # 4% chance of asteroid creation per frame
    dice = randint(0, 25) == 1
    
    # less than too many asteroids and random chance met
    if not_too_many and dice:
        world['asteroids'].append(create_asteroid())
        index_created = len(world['asteroids']) - 1
        
        xvel = 0
        yvel = 0
        rvel = 0
        size = 0
        
        # set a random velocity property for this asteroid, making sure
        # all movement velocities are non-zero
        while xvel == 0 and yvel == 0:
            xvel = randint(-5, 5)
            yvel = randint(-5, 5)
            rvel = uniform(-5.0, 5.0)
            size = randint(1, 4)
        
        if xvel < 0:
            world['asteroids'][index_created]['x'] = get_width() - 1 # going to left, spawn on right
        else:
            world['asteroids'][index_created]['x'] = 1 # going to right, spawn on left
        
        # maintain velocity for this asteroid
        world['asteroids xvel'].append(xvel)
        world['asteroids yvel'].append(yvel)
        world['asteroids rvel'].append(rvel)
        world['asteroids size'].append(size)
        
def move_asteroids(world: World):
    if len(world['asteroids']) == 0:
        return # nothing to move
    for i in range(len(world['asteroids'])):
        # move each asteroid based on its assocaited velocity
        world['asteroids'][i]['x'] += world['asteroids xvel'][i]
        world['asteroids'][i]['y'] += world['asteroids yvel'][i]
        world['asteroids'][i]['angle'] += world['asteroids rvel'][i]
        
def destroy_out_of_bounds(world: World):
    if len(world['asteroids']) == 0:
        return # nothing to remove
    for i in range(len(world['asteroids'])):
        try:
            if (world['asteroids'][i]['x'] < 0 or world['asteroids'][i]['x'] > get_width() or
                world['asteroids'][i]['y'] < 0 or world['asteroids'][i]['y'] > get_height()):
                # remove the asteroid if it hits the screen edges
                world['asteroids'].pop(i)
                world['asteroids xvel'].pop(i)
                world['asteroids yvel'].pop(i)
                world['asteroids rvel'].pop(i)
                world['asteroids size'].pop(i)
            elif colliding(world['asteroids'][i], world['ship']):
                # remove the asteroid if it hits the ship; split it into chunks and also
                # destroy the ship
                world['asteroids'].pop(i)
                world['asteroids xvel'].pop(i)
                world['asteroids yvel'].pop(i)
                world['asteroids rvel'].pop(i)
                world['asteroids size'].pop(i)
                # then create extra pieces and also destroy ship
            else:
                # remove the asteroid if it hits a projectile; split it into chunks and also
                # destroy the projectile
                # check for every projectile
                pass
        except IndexError:
            continue # finished iteration through the full list
        
def create_world() -> World:
    return {
        'ship': create_ship(),
        'xvel': 0,
        'yvel': 0,
        'rot': 0,
        'asteroids': [],
        'asteroids xvel': [],
        'asteroids yvel': [],
        'asteroids rvel': [],
        'asteroids size': []
    }

when('starting', create_world)
when('updating', move_ship)
when('typing', change_vel)
when('updating', decel)
when('updating', make_asteroids)
when('updating', move_asteroids)
when('updating', destroy_out_of_bounds)
start()