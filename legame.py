#!/usr/bin/env python3

import os
import math
import re
import pygame, math, sys
from pygame.locals import *

X_SCREEN = 1024
Y_SCREEN = 768

FRAMES_PER_SECOND = 40

IMAGE_FOLDER = "images"
GRAVITY = 1.8

level0 = [
    (["cdbaedacdbbeacde",
      "H_______________",
      "H___________q___",
      "H_______________",
      "H______s_______m",
      "yyzvvyxwzvvwyxzy"],"toto"),
    (["adeacbeabdedccac",
      "________________",
      "________p_______",
      "___o____________",
      "_____________g__",
      "zzyyxwvxyyywywyv"],"toto"),
    (["abeccdedbadddbee",
      "________u______H",
      "_______________H",
      "_______________H",
      "___ijl______r__H",
      "yyzywzvyvxzxyvwy"],"toto")
]


level = [
    (["HHHHHHHHHHHHHHHH",
      "H_______________",
      "H_______________",
      "H_______________",
      "H_______________",
      "HHHHHHHHHHHHHHHH"],"toto"),
    (["HHHHHHHHHHHHHHHH",
      "________________",
      "________________",
      "________________",
      "________________",
      "HHHHHHHHHHHHHHHH"],"toto"),
    (["HHHHHHHHHHHHHHHH",
      "_______________H",
      "_______________H",
      "_______________H",
      "_______________H",
      "HHHHHHHHHHHHHHHH"],"toto")
]

COLLIDABLE = {"H": True,
              "_": False,
              "a": True,
              "b": True,
              "c": True,
              "d": True,
              "e": True,
              "g": True,
              "h": True,
              "i": True,
              "j": True,
              "l": True,
              "m": True,
              "o": True,
              "p": True,
              "q": True,
              "r": True,
              "s": True,
              "u": True,
              "v": True,
              "w": True,
              "x": True,
              "y": True,
              "z": True,
             }


class Tile(pygame.sprite.Sprite):
    def __init__(self, character, default_size=(64,128)):
        pygame.sprite.Sprite.__init__(self)
        self.character = character
        self.default_size = default_size
        self.collidable=COLLIDABLE[self.character]
        self.image = pygame.image.load(IMAGE_FOLDER + "/" + self.character + ".png")
        self.image = pygame.transform.scale(self.image,(self.default_size))
        self.rect = self.image.get_rect()
    def update(self, dx):
        self.rect.x += dx
        if self.rect.x < -64:
            self.kill()

class Lulu(pygame.sprite.Sprite):
    def __init__(self, collidable=True, default_size=(64,128), name="lulu"):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.default_size = default_size
        self.collidable=True
        self.state = "walking"
        self.direction = "right"
        self.available_states = self._get_states("walking", "standing","flying")
        self.anim_state=0
        self.image = pygame.image.load(IMAGE_FOLDER + "/" + name +"_" + self.state +"_right_0" + ".png")
        self.image = pygame.transform.scale(self.image,(self.default_size))
        self.rect = self.image.get_rect()
        self.rect.x = 192
        self.rect.y = 672
        self.velocity_x = 0
        self.velocity_y = 0
        self.dx = 0
        self.dy = 0
        self.cd = 0
    def accelerate(self, dx, dy):
        self.velocity_x += dx
        self.velocity_y += dy
    def user_move_x(self,direction):
        if self.state == "standing":
            self.state = "walking"
        self.direction = direction
        l_or_r = {'left' : -1, 'right':1}
        sign = l_or_r[direction]
        self.move(sign*9,0)
        self.accelerate(sign*0.7,0)
    def jump(self):
        self.state = "flying"
        if self.cd = 0
            self.accelerate(0,8)
            self.cd = 30
    def fall(self):
        self.state = "flying"
    def move(self, dx, dy):
        self.dx += dx
        self.dy += dy
    def update(self):
        self.cd -= 1
        self.anim_state += 0.1
        if self.anim_state >= len(self.available_states[self.state])-1:
            self.anim_state = 0
        anim_state = math.floor(self.anim_state)
        print((self.state,self.direction,anim_state,self.anim_state,(self.velocity_x,self.velocity_y)))
        image_name = IMAGE_FOLDER + "/" + self.available_states[self.state][self.direction][anim_state]
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.scale(self.image,(self.default_size))
        #print(self.velocity_y)
        if self.velocity_x > 0:
            self.velocity_x -= (0.1 + self.velocity_x/60)
        if self.velocity_x < 0:
            self.velocity_x += (0.1 - self.velocity_x/60)
        if abs(self.velocity_x) < 0.06:
            self.velocity_x = 0
        if self.state == "flying":
            self.velocity_y -= GRAVITY
        self.move(self.velocity_x, -self.velocity_y)
    def side_collision(self, collided_sprite):
        print(collided_sprite.rect.bottomleft)
        if collided_sprite.rect.bottomleft[0] < self.rect.bottomright[0] and collided_sprite.rect.bottomright[0] > self.rect.bottomleft[0]:
            if collided_sprite.rect.bottomright[0] < self.rect.bottomright[0]:
                self.dx = 10+ (collided_sprite.rect.bottomright[0] - self.rect.bottomleft[0])
            else:
                self.dx = -10 + self.velocity_x/20
            self.velocity_x = self.velocity_x/3
        if collided_sprite.rect.topleft[1] < self.rect.bottomleft[1] and collided_sprite.rect.bottomleft[1] > self.rect.topleft[1]:
            if collided_sprite.rect.bottomleft[1] > self.rect.bottomleft[1]:
                self.dy = collided_sprite.rect.topleft[1] - self.rect.bottomleft[1]
                self.velocity_y = 0
                self.state = "standing"
            else:
                self.dy = 1
                self.velocity_y = -1
    def flush_moves(self):
        move_universe = 0
        if self.rect.x + self.dx > 3*X_SCREEN/4:
            move_universe = self.dx
        elif self.rect.x + self.dx < X_SCREEN/4:
            move_universe = self.dx
        #else:
            #self.rect.x += self.dx
        if self.dx == 0 and self.state =="walking":
            self.state = "standing"
        move_universe = self.dx
        self.dx = 0
        self.rect.y += self.dy
        self.dy = 0
        return -move_universe
    def _get_states(self,*key_states):
        states = dict()
        for state in key_states:
            direction_dict = dict()
            for direction in ["left","right"]:
                images = os.listdir("images")
                regex = re.compile(self.name + "_"+ state + "_" + direction + "_")
                images = list(filter(regex.search, images))
                direction_dict[direction] = images
            states[state] = direction_dict
        return states 

def generate_level(level_map):
    input_width = len(level_map[0][0][0])
    input_height = len(level_map[0][0])
    default_width = X_SCREEN/input_width
    default_height = Y_SCREEN/input_height
    collidables = pygame.sprite.Group()
    non_collidables = pygame.sprite.Group()
    for screen_number in range(len(level_map)):
        for screen_row in range(len(level_map[screen_number][0])):
            for screen_col in range(len(level_map[screen_number][0][screen_row])):
                current_input = level_map[screen_number][0][screen_row][screen_col]
                block = Tile(character=current_input)
                block.rect.x = screen_number*input_width*default_width+screen_col*default_width
                block.rect.y = screen_row*default_height
                if COLLIDABLE[current_input] is True:
                    collidables.add(block)
                else:
                    non_collidables.add(block)
                    #TODO:check for collision separately x y
    return (collidables,non_collidables)

def main():
    pygame.init()
    pygame.key.set_repeat(1,10)
    screen = pygame.display.set_mode((X_SCREEN, Y_SCREEN))
    screen.fill((255,255,255))

    clock = pygame.time.Clock()

    collidables, non_collidables = generate_level(level0)
    first_plan = pygame.sprite.Group()
    lulu = Lulu()
    lulu.rect.x, lulu.rect.y = 320,512
    first_plan.add(lulu)
    first_plan.draw(screen)

    while 1:
        deltat = clock.tick(FRAMES_PER_SECOND)
        old_position = lulu.rect
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            #TODO: switch with dict
            if event.key == pygame.K_RIGHT:
                lulu.user_move_x("right")
            #if event.key == pygame.K_LEFT:
                #lulu.user_move_x("left")
            if event.key == pygame.K_UP:
                lulu.jump()
        first_plan.update()
        collided_sprites=list()
        collided_sprites.append(pygame.sprite.spritecollideany(lulu,collidables))
        for collided_sprite in collided_sprites:
            if collided_sprite is not None:
                lulu.side_collision(collided_sprite)
        move_universe = lulu.flush_moves()
        fall_path = lulu.rect.copy()
        fall_path.move(0,10)
        toto = pygame.sprite.Sprite()
        toto.rect = fall_path
        #fp_sp = list()
        #fp_sp.append()
        if pygame.sprite.spritecollideany(toto,collidables) is None:
            lulu.fall()


        # Rendering
        screen.fill((255,255,255))
        collidables.update(move_universe)
        non_collidables.update(move_universe)
        collidables.draw(screen)
        non_collidables.draw(screen)
        first_plan.draw(screen)
        pygame.display.flip()

def update_universe(move_universe,group_sprites):
    for group_sprite in group_sprites:
        group_sprite.move_universe(move_universe)

main()
