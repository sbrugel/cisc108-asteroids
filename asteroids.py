from designer import *
from random import randint, uniform
import math

set_window_color('black')
enable_keyboard_repeating()

World = {
    'ship': DesignerObject,
    'score': int,
    'score display': DesignerObject,
    'asteroids': [DesignerObject],
    'xvel': float,
    'yvel': float,
    'rot': int,
    'asteroids xvel': [float],
    'asteroids yvel': [float],
    'asteroids rvel': [float],
    'asteroids size': [int],
    'projectiles': [DesignerObject],
    'projectiles xvel': [float],
    'projectiles yvel': [float],
    'bonus': [DesignerObject],
    'bonus xvel': [float],
    'bonus yvel': [float],
    'bonus rvel': [float],
    'particles': [DesignerObject],
    'particles xvel': [float],
    'particles yvel': [float],
}

MAX_VEL = 3
DECEL_RATE = 0.05

def create_ship() -> DesignerObject:
    # create the player controlled ship object
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
    # wrap around the window if hits the edges    
    if world['ship']['y'] < 0:
        world['ship']['y'] = get_height()
    elif world['ship']['y'] > get_height():
        world['ship']['y'] = 0

def change_vel(world: World, key: str):
    # movement to sides - maximum velocity at a time per direction is 3 units/frame
    if key == 'a':
        world['xvel'] = -MAX_VEL
    if key == 'd':
        world['xvel'] = MAX_VEL
    if key == 'w':
        world['yvel'] = -MAX_VEL
    if key == 's':
        world['yvel'] = MAX_VEL
        
    # launch projectile
    if key == 'space':
        make_projectile(world)
        
    # change angle of ship using arrows
    if key == 'left':
        world['ship']['angle'] -= 10
    if key == 'right':
        world['ship']['angle'] += 10
        
def decel(world: World):
    # natural deceleration of ship when rockets are unpowered
    if world['xvel'] < 0:
        world['xvel'] += DECEL_RATE
    elif world['xvel'] > 0:
        world['xvel'] -= DECEL_RATE
        
    if world['yvel'] < 0:
        world['yvel'] += DECEL_RATE
    elif world['yvel'] > 0:
        world['yvel'] -= DECEL_RATE
        
def create_asteroid() -> DesignerObject:
    asteroid = image('asteroid.png')
    return asteroid

def make_asteroids(world: World):
    # less than 10 asteroids? create an asteroid    
    not_too_many = len(world['asteroids']) < 10
    
    # 2% chance of asteroid creation per frame (updated 30 times per second)
    dice = randint(0, 50) == 1
    
    # less than too many asteroids and random chance met
    if not_too_many and dice:
        world['asteroids'].append(create_asteroid())
        
        # this line is used to find the newly created asteroid
        # to add a velocity to
        index_created = len(world['asteroids']) - 1
        
        # initialize the asteroid properties
        xvel = 0 # x velocity
        yvel = 0 # y velocity
        rvel = 0 # rotation velocity
        size = 0 # size - small/medium/large corresponds to 1/2/3
        
        # set a random velocity property for this asteroid, making sure
        # all movement velocities are non-zero
        while xvel == 0 and yvel == 0:
            xvel = randint(-3, 3)
            yvel = randint(-3, 3)
            rvel = uniform(-3.0, 3.0)
            size = randint(1, 4)
        
        if xvel < 0:
            world['asteroids'][index_created]['x'] = get_width() - 1 # going to left, spawn on right
        else:
            world['asteroids'][index_created]['x'] = 1 # going to right, spawn on left
        
        if size == 1:
            world['asteroids'][index_created]['scale'] = 0.3
        elif size == 2:
            world['asteroids'][index_created]['scale'] = 0.5
        elif size == 3:
            world['asteroids'][index_created]['scale'] = 0.7
        # maintain properties for this asteroid until destroyed
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
        
def create_bonus() -> DesignerObject:
    bonus = image('coin.png')
    return bonus

def make_bonus(world: World):
    # less than 10 asteroids? create an asteroid    
    not_too_many = len(world['bonus']) < 1
    
    # 0.5% chance of coin creation per frame (updated 30 times per second)
    dice = randint(0, 200) == 1
    
    # no bonus already exists and random chance met
    if not_too_many and dice:
        world['bonus'].append(create_bonus())
        
        # initialize the bonus properties
        xvel = 0 # x velocity
        yvel = 0 # y velocity
        rvel = 0 # rotation velocity
        
        # set a random velocity property for this bonus, making sure
        # all movement velocities are non-zero
        while xvel == 0 and yvel == 0:
            xvel = randint(-3, 3)
            yvel = randint(-3, 3)
            rvel = uniform(-3.0, 3.0)
        
        if xvel < 0:
            world['bonus'][0]['x'] = get_width() - 1 # going to left, spawn on right
        else:
            world['bonus'][0]['x'] = 1 # going to right, spawn on left
        
        # maintain properties for this bonus until destroyed
        world['bonus xvel'].append(xvel)
        world['bonus yvel'].append(yvel)
        world['bonus rvel'].append(rvel)
        
def move_bonus(world: World):
    if len(world['bonus']) == 0:
        return # nothing to move
    for i in range(len(world['bonus'])):
        # move each asteroid based on its assocaited velocity
        world['bonus'][i]['x'] += world['bonus xvel'][i]
        world['bonus'][i]['y'] += world['bonus yvel'][i]
        world['bonus'][i]['angle'] += world['bonus rvel'][i]
        
def create_projectile() -> DesignerObject:
    proj = image('projectile.png')
    return proj
        
def make_projectile(world: World):
    # only fire one projectile at a time (for now)
    not_too_many = len(world['projectiles']) < 1
    
    # less than too many projectiles
    if not_too_many:
        world['projectiles'].append(create_projectile())
        index_created = len(world['projectiles']) - 1
        
        # set direction of projectile based on ship direction
        radianangle = math.radians(world['ship']['angle'])
        xvel = math.cos(radianangle) * 20
        yvel = math.sin(radianangle) * -20 # negative since on designer, a positive y vel means it goes down
        
        world['projectiles'][index_created]['x'] = world['ship']['x']
        world['projectiles'][index_created]['y'] = world['ship']['y']
        world['projectiles'][index_created]['angle'] = world['ship']['angle']
        
        # maintain velocity for this projectile
        world['projectiles xvel'].append(xvel)
        world['projectiles yvel'].append(yvel)
        
def move_projectiles(world: World):
    if len(world['projectiles']) == 0:
        return # nothing to move
    for i in range(len(world['projectiles'])):
        # move each asteroid based on its assocaited velocity
        world['projectiles'][i]['x'] += world['projectiles xvel'][i]
        world['projectiles'][i]['y'] += world['projectiles yvel'][i]
        
def destroy_if_hit(world: World):
    # handle asteroids
    if not len(world['asteroids']) == 0:
        for i in range(len(world['asteroids'])):
            try:
                if (world['asteroids'][i]['x'] < 0 or world['asteroids'][i]['x'] > get_width() or
                    world['asteroids'][i]['y'] < 0 or world['asteroids'][i]['y'] > get_height()):
                    # remove the asteroid if it hits the screen edges
                    remove_asteroid_at_index(i, world)
                elif colliding(world['asteroids'][i], world['ship']):
                    # remove the asteroid if it hits the ship, also destroy ship and game over
                    world['ship']['scale'] = 0
                    remove_asteroid_at_index(i, world)
                else:
                    # remove the asteroid if it hits a projectile; split it into chunks and also
                    # destroy the projectile
                    # check for every projectile
                    pass
            except IndexError:
                continue # finished iteration through the full list
        
    # handle projectiles
    if not len(world['projectiles']) == 0:
        for i in range(len(world['projectiles'])):
            try:
                # only one case needed here, the other case (when hitting an asteroid) is handled above
                if (world['projectiles'][i]['x'] < 0 or world['projectiles'][i]['x'] > get_width() or
                    world['projectiles'][i]['y'] < 0 or world['projectiles'][i]['y'] > get_height()):
                    # remove the projectile if it hits the screen edges
                    remove_projectile_at_index(i, world)
            except IndexError:
                continue # finished iteration through the full list
    
    # handle bonus
    if len(world['bonus']) == 0:
        return # nothing to remove
    for i in range(len(world['bonus'])):
        try:
            if (world['bonus'][i]['x'] < 0 or world['bonus'][i]['x'] > get_width() or
                world['bonus'][i]['y'] < 0 or world['bonus'][i]['y'] > get_height()):
                # remove the bonus if it hits the screen edges
                remove_bonus_at_index(i, world)
            elif colliding(world['bonus'][i], world['ship']):
                remove_bonus_at_index(i, world)
                world['score'] += 500
        except IndexError:
            continue # finished iteration through the full list
        
def remove_asteroid_at_index(index: int, world: World):
    # remove the asteroid at the specified array index
    # used in tandem with the destroy_if_hit function
    # which iterates through the full list of asteroids
    # and removes every index that is colliding with the edge,
    # a projectile, or the ship
    world['asteroids'].pop(index)
    world['asteroids xvel'].pop(index)
    world['asteroids yvel'].pop(index)
    world['asteroids rvel'].pop(index)
    world['asteroids size'].pop(index)
    
def remove_projectile_at_index(index: int, world: World):
    # remove the projectile at the specified array index
    # used in tandem with the destroy_if_hit function
    # which iterates through the full list of projectiles
    # and removes every index that is colliding with the edge,
    # or an asteroid
    world['projectiles'].pop(index)
    world['projectiles xvel'].pop(index)
    world['projectiles yvel'].pop(index)
    
def remove_bonus_at_index(index: int, world: World):
    # remove the bonus at the specified array index
    # used in tandem with the destroy_if_hit function
    # which iterates through the full list of bonus items
    # and removes every index that is colliding with the edge,
    # or the ship
    world['bonus'].pop(index)
    world['bonus xvel'].pop(index)
    world['bonus yvel'].pop(index)
    world['bonus rvel'].pop(index)
        
def create_world() -> World:
    return {
        'ship': create_ship(),
        'score': 0,
        'xvel': 0,
        'yvel': 0,
        'rot': 0,
        'asteroids': [],
        'asteroids xvel': [],
        'asteroids yvel': [],
        'asteroids rvel': [],
        'asteroids size': [],
        'projectiles': [],
        'projectiles xvel': [],
        'projectiles yvel': [],
        'bonus': [],
        'bonus xvel': [],
        'bonus yvel': [],
        'bonus rvel': [],
    }

when('starting', create_world)
when('updating', move_ship)
when('typing', change_vel)
when('updating', decel)
when('updating', make_asteroids)
when('updating', move_asteroids)
when('updating', make_bonus)
when('updating', move_bonus)
when('updating', move_projectiles)
when('updating', destroy_if_hit)
start()