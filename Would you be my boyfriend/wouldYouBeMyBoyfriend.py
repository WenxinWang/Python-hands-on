# Python App - Would you be my boyfriend
# Author: Tiffany Wang
# Email: wenxin.wxw@gmail.com
# date: 9/28/2018

# Configuration: Windows10, amd64
# introduction 
# 1. Download pygame package "pygame-1.9.4-cp37-cp37m-win_amd64.whl" from here: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame
# 2. Move the downloaded .whl file to your python37/Scripts directory
# 3. Enter the command: "pip3 install pygame-1.9.4-cp37-cp37m-win_amd64.whl"
# 4. Download the picture "me.jpg", music file "love.mp3", and font file"simkai.ttf"
# 5. Execute the file by command "py wouldYouBeMyBoyfriend.py"



import os
import sys
import random
import pygame
from pygame.locals import *
WIDTH, HEIGHT = 640, 480
BACKGROUND = (255, 255, 255)
if getattr(sys, 'frozen', False):
        # include musicpath/fontpath/imgpath
        CurrentPath = sys._MEIPASS
        # not include musicpath/fontpath/imgpath
        # CurrentPath = os.getcwd()
else:
        CurrentPath = os.path.dirname(__file__)
FONTPATH = os.path.join(CurrentPath, 'simkai.ttf')
MUSICPATH = os.path.join(CurrentPath, 'love.mp3')
IMGPATH = os.path.join(CurrentPath, 'me.jpg')
# button
def button(text, x, y, w, h, color, screen):
        pygame.draw.rect(screen, color, (x, y, w, h))
        font = pygame.font.Font(FONTPATH, 20)
        textRender = font.render(text, True, (0, 0, 0))
        textRect = textRender.get_rect()
        textRect.center = ((x+w/2), (y+h/2))        
        screen.blit(textRender, textRect)
# Title
def title(text, screen, scale, color=(255, 0, 0)):
        font = pygame.font.Font(FONTPATH, WIDTH//(len(text)*2))
        textRender = font.render(text, True, color)
        textRect = textRender.get_rect()
        textRect.midtop = (WIDTH/scale[0], HEIGHT/scale[1])
        screen.blit(textRender, textRect)
# Make random position
def get_random_pos():
        x, y = random.randint(20, 620), random.randint(20, 460)
        return x, y
# page after clicking 'Okay' button
def show_like_interface(text, screen, color=(255, 0, 0)):
        screen.fill(BACKGROUND)
        font = pygame.font.Font(FONTPATH, WIDTH//(len(text)))
        textRender = font.render(text, True, color)
        textRect = textRender.get_rect()
        textRect.midtop = (WIDTH/2, HEIGHT/2)
        screen.blit(textRender, textRect)
        pygame.display.update()
        while True:
                for event in pygame.event.get():
                        if event.type == QUIT:
                                pygame.quit()
                                sys.exit()
# main function
def main():
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('Would you be my boyfriend?')
        clock = pygame.time.Clock()
        pygame.mixer.music.load(MUSICPATH)
        pygame.mixer.music.play(1,3.0)
        pygame.mixer.music.set_volume(0.6)
        unlike_pos_x = 330
        unlike_pos_y = 250
        unlike_pos_width = 100
        unlike_pos_height = 50
        unlike_color = (0, 191, 255)
        like_pos_x = 180
        like_pos_y = 250
        like_pos_width = 100
        like_pos_height = 50
        like_color = (0, 191, 255)
        running = True
        while running:
                screen.fill(BACKGROUND)
                img = pygame.image.load(IMGPATH)
                imgRect = img.get_rect()
                imgRect.midtop = int(WIDTH/1.3), HEIGHT//7
                screen.blit(img, imgRect)
                for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                mouse_pos = pygame.mouse.get_pos()
                                if mouse_pos[0] < like_pos_x+like_pos_width+5 and mouse_pos[0] > like_pos_x-5 and\
                                        mouse_pos[1] < like_pos_y+like_pos_height+5 and mouse_pos[1] > like_pos_y-5:
                                        like_color = BACKGROUND
                                        running = False
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] < unlike_pos_x+unlike_pos_width+5 and mouse_pos[0] > unlike_pos_x-5 and\
                        mouse_pos[1] < unlike_pos_y+unlike_pos_height+5 and mouse_pos[1] > unlike_pos_y-5:
                        while True:
                                unlike_pos_x, unlike_pos_y = get_random_pos()
                                if mouse_pos[0] < unlike_pos_x+unlike_pos_width+5 and mouse_pos[0] > unlike_pos_x-5 and\
                                        mouse_pos[1] < unlike_pos_y+unlike_pos_height+5 and mouse_pos[1] > unlike_pos_y-5:
                                        continue
                                break
                title('Boy, I like you', screen, scale=[3, 8])
                title('Would you be my boyfriend?', screen, scale=[3, 4])
                button('Okay', like_pos_x, like_pos_y, like_pos_width, like_pos_height, like_color, screen)
                button('No, thanks', unlike_pos_x, unlike_pos_y, unlike_pos_width, unlike_pos_height, unlike_color, screen)
                pygame.display.flip()
                pygame.display.update()
                clock.tick(60)
        show_like_interface('I know you like me too!', screen, color=(255, 0, 0))
if __name__ == '__main__':
        main()
