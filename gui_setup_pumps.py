#!/usr/bin/env python3

import pygame
import configparser
import RPi.GPIO as GPIO

pygame.init()

WHITE = (255, 255, 255)
ACTIVE_COLOR = pygame.Color('dodgerblue1')
INACTIVE_COLOR = pygame.Color('dodgerblue4')
FONT = pygame.font.Font(None, 50)

pumps = configparser.ConfigParser()
pumps.read('pumps.ini')


def draw_button(button, screen):
    pygame.draw.rect(screen, button['color'], button['rect'])
    screen.blit(button['text'], button['text rect'])


def create_button(pump_id, x, y, w, h):
    text_surf = FONT.render("Pump " + str(pump_id), True, WHITE)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'pump_id': pump_id,
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': INACTIVE_COLOR,
        'state' : False,
        }
    return button


def create_quit_button(x, y, w, h):
    text_surf = FONT.render("Finish", True, WHITE)
    button_rect = pygame.Rect(x, y, w, h)
    text_rect = text_surf.get_rect(center=button_rect.center)
    button = {
        'rect': button_rect,
        'text': text_surf,
        'text rect': text_rect,
        'color': INACTIVE_COLOR,
        }
    return button


def main():
    GPIO.setmode(GPIO.BOARD)

    screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    done = False

    def start_pump(pump_id):
        pin = int(pumps['pump'+str(pump_id)]['pin'])
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
    
    def stop_pump(pump_id): 
        pin = int(pumps['pump'+str(pump_id)]['pin'])
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)

    def quit_game(): 
        nonlocal done
        done = True

    number_of_pumps = 8
    button_list = []
    for p in range(number_of_pumps):
        button_height = 80
        button_width = 200
        button_margin = 5
        row = p if (p < 4) else (p-4)
        x_pos = 10 if (p < 4) else (10 + button_width + button_margin)
        y_pos = button_margin + (button_margin * row) + (row * button_height)
        button_list.append(create_button(p+1, x_pos, y_pos, button_width, button_height))

    quit_button = create_quit_button(500,10, 200,80)
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # This block is executed once for each MOUSEBUTTONDOWN event.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 1 is the left mouse button, 2 is middle, 3 is right.
                if event.button == 1:
                    if quit_button['rect'].collidepoint(event.pos):
                        quit_game()
                    for button in button_list:
                        # `event.pos` is the mouse position.
                        if button['rect'].collidepoint(event.pos):
                            if button['state']:
                                button['color'] = INACTIVE_COLOR
                                button['state'] = False
                                stop_pump(button['pump_id'])	
                            else:
                                button['color'] = ACTIVE_COLOR
                                button['state'] = True
                                start_pump(button['pump_id'])	

        screen.fill(WHITE)
        for button in button_list:
            draw_button(button, screen)
        draw_button(quit_button, screen)
        pygame.display.update()
        clock.tick(30)


main()
pygame.quit()
GPIO.cleanup()

