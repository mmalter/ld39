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
      "________________",
      "____________q___",
      "________________",
      "_______s_______m",
      "yyzvvyxwzvvwyxzy"],[]),
    (["adeacbeabdedccac",
      "________________",
      "________p_______",
      "___o____________",
      "_____________g__",
      "zzyyxwvxyyywywyv"],[("0",[14,4])]),
    (["accccbeabdedccac",
      "________________",
      "________________",
      "________________",
      "________________",
      "zzyyxwvxyyywywyv"],[("0",[2,2])]),
    (["accccbeabdedccac",
      "_____u__________",
      "________________",
      "________________",
      "________________",
      "zzyyxwvxyyywywyv"],[("0",[7,3])]),
    (["accccbeabdedccac",
      "________________",
      "________________",
      "________________",
      "________________",
      "zzyyxwvxyyywywyv"],[]),
    (["accccbeabdedccac",
      "________________",
      "________________",
      "________________",
      "________________",
      "zzyyxwvxyyywywyv"],[("0",[9,4])]),
    (["accccbeabdedccac",
      "________________",
      "________________",
      "________________",
      "________________",
      "zzyyxwvxyyywywyv"],[("0",[2,2])]),
    (["abeccdedbadddbee",
      "________u_______",
      "________________",
      "________________",
      "___ijl______r___",
      "yyzywzvyvxzxyvwy"],[]),
    (["accccbeabdedccac",
      "________________",
      "________________",
      "________________",
      "________________",
      "zzyyxwvxyyywywyv"],[]),
    (["accccbeabdedccac",
      "________________",
      "________________",
      "________________",
      "________________",
      "zzyyxwvxyyywywyv"],[("0",[2,3])]),
    (["accccbeabdedccac",
      "_______u________",
      "________________",
      "________________",
      "_______i________",
      "zzyyxwvxyyywywyv"],[]),
    (["accccbeabdedccac",
      "________________",
      "________________",
      "________________",
      "________________",
      "zzyyxwvxyyywywyv"],[("0",[2,3])]),
    (["accccbeabdedccac",
      "________________",
      "________________",
      "________________",
      "____________r___",
      "zzyyxwvxyyywywyv"],[]),
    (["accccbeabdedccac",
      "_______________E",
      "_______________F",
      "_______________G",
      "_______________H",
      "zzyyxwvxyyywywyv"],[("0",[2,3])]),
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
              "E": True,
              "F": True,
              "G": True,
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
              "0": True,
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
        #if self.rect.x < -64:
            #self.kill()

class Streum(pygame.sprite.Sprite):
    def __init__(self, character, default_size=(64,128)):
        pygame.sprite.Sprite.__init__(self)
        self.character = character
        self.default_size = default_size
        self.collidable=COLLIDABLE[self.character]
        self.image = pygame.image.load(IMAGE_FOLDER + "/" + self.character + "0.png")
        self.image = pygame.transform.scale(self.image,(self.default_size))
        self.rect = self.image.get_rect()
    def update(self, dx):
        self.rect.x += dx

class Lulu(pygame.sprite.Sprite):
    def __init__(self, collidables=None, default_size=(64,128), name="lulu"):
        pygame.sprite.Sprite.__init__(self)
        self.collidables = collidables
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
        self.accel = 0
        self.cd = 0
    def am_i(self,collider):
        self.am_i_dead(collider)
        self.am_i_victorious(collider)
    def am_i_dead(self,collider):
        if isinstance(collider,Streum):
            main()
    def am_i_victorious(self,collider):
        if collider.character in ["E","F","G","H"]:
            victory()
    def move_level(self):
        wedge = self.rect.x - 1*X_SCREEN/2
        if wedge >= 0:
            self.collidables.update(-wedge)
            self.rect.x = 1*X_SCREEN/2
    def accelerate(self, dx, dy):
        self.velocity_x += dx
        self.velocity_y += dy
    def move(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
    def user_move_x(self,direction):
        self.direction = direction
        l_or_r = {'left' : -1, 'right':1}
        sign = l_or_r[direction]
        self.accelerate(sign*2,0)
        self.accel += 0.8
    def jump(self):
        if self.cd < 0:
            self.state = "flying"
            self.accelerate(0,-15)
            self.cd = 30
    def update(self):
        self.cd -=1
        self.anim_state += 0.1
        if self.anim_state >= len(self.available_states[self.state])-1:
            self.anim_state = 0
        anim_state = math.floor(self.anim_state)
        print((self.state,self.direction,anim_state,self.anim_state,(self.velocity_x,self.velocity_y)))
        image_name = IMAGE_FOLDER + "/" + self.available_states[self.state][self.direction][anim_state]
        self.image = pygame.image.load(image_name)
        self.image = pygame.transform.scale(self.image,(self.default_size))
        self.gravity()
        self.velocity_x = self.velocity_x*0.9
        if self.accel <0:
            self.accel =0
        self.rect.x += self.velocity_x + self.accel
        self.accel -= 0.4
        self.move_level()
        for hit in pygame.sprite.spritecollide(self, self.collidables, False):
            self.am_i(hit)
            if self.velocity_x > 0:
                self.rect.right = hit.rect.left
            elif self.velocity_x > 0:
                self.rect.left = hit.rect.right
        self.rect.y += self.velocity_y
        hits = pygame.sprite.spritecollide(self, self.collidables, False)
        for hit in hits:
            self.am_i(hit)
            if self.velocity_y > 0:
                self.rect.bottom = hit.rect.top
            elif self.velocity_y < 0:
                self.rect.top = hit.rect.bottom
            self.velocity_y = 0
    def gravity(self):
        if self.velocity_y == 0:
            self.velocity_y =2
        else:
            self.velocity_y += .45
        hits = pygame.sprite.spritecollide(self, self.collidables, False)
        if self.rect.y >= 5*Y_SCREEN/6 -self.rect.height and self.velocity_y >= 0:
            self.velocity_y = 0
            self.rect.y = 5*Y_SCREEN/6 - self.rect.height
            if self.state != "walking":
                self.state = "standing"
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
        streums = level_map[screen_number][1]
        for streum_t in streums:
            streum = Streum(character=streum_t[0])
            print(streum_t)
            streum.rect.x = screen_number*default_width*input_width+streum_t[1][0]*default_width
            streum.rect.y = streum_t[1][1]*default_height
            collidables.add(streum)
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
    #font = pygame.font.Font("bithigh.ttf",15)
    font = pygame.font.SysFont("arial",15)
    pygame.key.set_repeat(1,10)
    screen = pygame.display.set_mode((X_SCREEN, Y_SCREEN))
    screen.fill((255,255,255))

    clock = pygame.time.Clock()

    collidables, non_collidables = generate_level(level0)
    first_plan = pygame.sprite.Group()
    lulu = Lulu(collidables=collidables)
    lulu.rect.x, lulu.rect.y = 320,512
    first_plan.add(lulu)
    first_plan.draw(screen)

    cd = 20
    power = 100
    vision = True

    while 1:
        if vision == True:
            power -= 0.1
        deltat = clock.tick(FRAMES_PER_SECOND)
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            #TODO: switch with dict
            if event.key == pygame.K_RIGHT:
                lulu.user_move_x("right")
            if event.key == pygame.K_SPACE and cd < 0:
                cd = 20
                if vision == True:
                    vision = False
                else:
                    vision = True
            if event.key == pygame.K_UP:
                lulu.jump()
        first_plan.update()
        cd -= 1
        if power < 0:
            main()


        # Rendering
        if power > 0 and vision == True:
            screen.fill((255,255,255))
            collidables.update(0)
            non_collidables.update(0)
            collidables.draw(screen)
            non_collidables.draw(screen)
            first_plan.draw(screen)
            label = font.render("Vision left :"+str(power),1,(0,0,0))
            screen.blit(label,(20,20))
        else:
            screen.fill((0,0,0))
            label = font.render("Vision left :"+str(power),1,(255,255,255))
            screen.blit(label,(20,20))
        pygame.display.flip()

def victory():
    pygame.init()
    #font = pygame.font.Font("bithigh.ttf",15)
    font = pygame.font.SysFont("arial",20)
    pygame.key.set_repeat(1,10)
    screen = pygame.display.set_mode((X_SCREEN, Y_SCREEN))
    screen.fill((255,255,255))
    label = font.render("You won the game, try-hard. Spacebar",1,(0,0,0))
    screen.blit(label,(20,20))

    clock = pygame.time.Clock()

    while 1:
        deltat = clock.tick(FRAMES_PER_SECOND)
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            #TODO: switch with dict
            if event.key == pygame.K_SPACE:
                main()

        pygame.display.flip()

def update_universe(move_universe,group_sprites):
    for group_sprite in group_sprites:
        group_sprite.move_universe(move_universe)

main()

