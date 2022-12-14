#!/usr/bin/env python3

import pygame
import RPi.GPIO as GPIO
import configparser
import list_drinks
import os.path
import time

pumps = configparser.ConfigParser()
pumps.read('pumps.ini')

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ACTIVE_COLOR = pygame.Color('dodgerblue1')
INACTIVE_COLOR = pygame.Color('dodgerblue4')
FONT = pygame.font.Font(None, 50)

PUMP_SECONDS_NEEDED_PER_ML = 8

def draw_drink_title(title, screen):
    text = FONT.render(title, True, BLACK)
    text_rect = text.get_rect(center=(800/2, 30))
    screen.blit(text, text_rect)


def draw_button(button, screen):
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


def create_button(title, x, y, w, h, callback):
    text_surf = FONT.render(title, True, WHITE)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': INACTIVE_COLOR,
        'callback' : callback,
        }
    return button


def main():
    GPIO.setmode(GPIO.BOARD)

    screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
    #screen = pygame.display.set_mode((800, 480))
    clock = pygame.time.Clock()
    done = False

    current_drink_id = 0
    drinks = list_drinks.get_available_drinks()
    
    def start_pump(pump_id):
        pin = int(pumps[str(pump_id)]['pin'])
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    def stop_pump(pump_id): 
        pin = int(pumps[str(pump_id)]['pin'])
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

    def next_drink():
        nonlocal current_drink_id
        current_drink_id += 1
        if current_drink_id > len(drinks)-1:
            current_drink_id = 0
    
    def prev_drink():
        nonlocal current_drink_id
        current_drink_id -= 1
        if current_drink_id < 0:
            current_drink_id = len(drinks)-1
    
    def serve_drink(): 
        print("serve drink called")
        drink = drinks[current_drink_id]
        for i in drink['ingredients']:
            for k,v in i.items():
               volume = v
               ingredient = k
               pump_id = list_drinks.get_pump_by_ingredient(ingredient)
               print(pump_id)
               start_pump(pump_id)
               time.sleep(volume*PUMP_SECONDS_NEEDED_PER_ML)
               stop_pump(pump_id)

    def quit_game():
        nonlocal done
        done = True

    button_list = []
    button_list.append(create_button("Prev",10, 390, 200, 80, prev_drink))
    button_list.append(create_button("Next",590, 390, 200, 80, next_drink))
    button_list.append(create_button("Serve Drink",260, 390, 300, 80, serve_drink))
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    for button in button_list:
                        # `event.pos` is the mouse position.
                        if button['rect'].collidepoint(event.pos):
                            button['callback']()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    quit_game()

        screen.fill(WHITE)
        for button in button_list:
            draw_button(button, screen)
        
        if 'image' in drinks[current_drink_id]:
            filename = 'drink-images/'+drinks[current_drink_id]['image']
            if os.path.isfile(filename):
                image = pygame.image.load(filename)
                screen.blit(pygame.transform.scale(image,(300,300)), (220,80))
        
        draw_drink_title(drinks[current_drink_id]['name'], screen)

        pygame.display.update()
        clock.tick(30)
main()
pygame.quit()
GPIO.cleanup()

