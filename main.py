from cProfile import run
import imp

from lib2to3.pygram import python_grammar
from operator import imod
from turtle import width
import pygame
import os
pygame.mixer.init()
pygame.font.init()
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My first game!")
WHITE = (255, 255, 255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
FPS = 60
VEl = 5
BULLETS_vel=7
MAXBUll=3
BORDER=pygame.Rect(WIDTH//2-5,0,10,HEIGHT)
BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLETS_FIRE_SOU=pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))
HElt_FONT=pygame.font.SysFont('comicsans',40)
WINNER_FONT=pygame.font.SysFont('comicsans',100)

SPACE_WID, SPACE_HEI = 55, 40
YELLO_HIT=pygame.USEREVENT+1
RED_HIT=pygame.USEREVENT+2
YELLOW_SPACE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACE = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACE_IMAGE, (SPACE_WID, SPACE_HEI)), 90)

RED_SPACE_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACE = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACE_IMAGE, (SPACE_WID, SPACE_HEI)), 270)

SPACE =pygame.transform.scale(pygame.image.load(os.path.join('Assets','fight1.jpg')),(WIDTH,HEIGHT))
def draw_wind(red, yellow,red_bullet,yello_bull ,red_h,yell_h):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    red_h_txt=HElt_FONT.render("Health: "+str(red_h),1,WHITE)
    yellow_h_txt=HElt_FONT.render("Health: "+str(yell_h),1,WHITE)
    WIN.blit(red_h_txt,(WIDTH-red_h_txt.get_width()-10,10))
    WIN.blit(yellow_h_txt,(10,10))

    WIN.blit(YELLOW_SPACE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACE, (red.x, red.y))

    for bullet in red_bullet:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yello_bull:
        pygame.draw.rect(WIN,YELLOW,bullet)

    pygame.display.update()


def yellow_movem(keys_press,yellow):
        if keys_press[pygame.K_a] and yellow.x -VEl>0:
            yellow.x -= VEl
        if keys_press[pygame.K_d] and yellow.x+ VEl +yellow.width<BORDER.x:
            yellow.x += VEl
        if keys_press[pygame.K_w] and yellow.y -VEl>0:
            yellow.y -= VEl
        if keys_press[pygame.K_s] and yellow.y + VEl+yellow.height<HEIGHT-15:
            yellow.y += VEl
def red_movem(keys_press,red):
        if keys_press[pygame.K_LEFT] and red.x -VEl>BORDER.x +BORDER.width:
            red.x -= VEl
        if keys_press[pygame.K_RIGHT] and red.x+ VEl +red.width<WIDTH:
            red.x += VEl
        if keys_press[pygame.K_UP] and red.y -VEl>0:
            red.y -= VEl
        if keys_press[pygame.K_DOWN] and red.y + VEl+red.height<HEIGHT-15:
            red.y += VEl


def handlebull(yelbull,redbu,yellow,red):
    for bullet in yelbull:
        bullet.x +=BULLETS_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yelbull.remove(bullet)
        elif bullet.x>WIDTH:
            yelbull.remove(bullet)

    for bullet in redbu:
        bullet.x -=BULLETS_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLO_HIT))
            redbu.remove(bullet)
        elif bullet.x<0:
            redbu.remove(bullet)


def draw_win(text):
    draw_txt=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_txt,(WIDTH/2-draw_txt.get_width()/2,HEIGHT/2-draw_txt.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)
def main():
    red = pygame.Rect(700, 300, SPACE_WID, SPACE_HEI)
    yellow = pygame.Rect(100, 300, SPACE_WID, SPACE_HEI)

    redbullets=[]
    yellowbullets=[]

    red_hel=10
    yell_hel=10
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type==pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellowbullets)<MAXBUll:
                    bullet=pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,10,5)
                    yellowbullets.append(bullet)
                    BULLETS_FIRE_SOU.play()
                if event.key==pygame.K_RSHIFT and len(redbullets)<MAXBUll:
                    bullet=pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                    redbullets.append(bullet) 
                    BULLETS_FIRE_SOU.play()

            if event.type==RED_HIT:
                red_hel-=1
                BULLET_HIT_SOUND.play()
            if event.type==YELLO_HIT:   
                yell_hel-=1  
                BULLET_HIT_SOUND.play()

        winner_txt=""         

        if red_hel<=0:
            winner_txt="Yellow wins!"
        if yell_hel<=0:
            winner_txt="Red wins!"
        if winner_txt!="":
            draw_win(winner_txt)
            break
        keys_pressed = pygame.key.get_pressed()
        yellow_movem(keys_pressed,yellow)
        red_movem(keys_pressed,red)

        handlebull(yellowbullets,redbullets,yellow,red)
        draw_wind(red, yellow,redbullets,yellowbullets,red_hel,yell_hel)
    main()


if __name__ == "__main__":
    main()
