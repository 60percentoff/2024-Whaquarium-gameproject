import pygame
import sys
import os
import random
import requests as req
import json

'''
Example return data : {"userdata": [[1, "meow", "61be55a8e2f6b4e172338bddf184d6dbee29c98853e0a0485ecee7f27b9af0b4", "{}", "{}", 100, 0, "{}", "{}", "26a989a23abf5ee3ae4106883e9f534a8042846458e34df03ab5ee063692f007", 1]]}

id, username, password, fishes data, foods data, money data, total play duration time, pre_fishes, acheivements, token, level
'''

token = sys.argv[1]
ip_text = sys.argv[2]

# Fetch user data
userdata = json.loads(req.get(f"{ip_text}/api/getUserdata/token/{token}").text)['userdata'][0]

# Initialize Pygame
pygame.init()

# Set the game window size
screen = pygame.display.set_mode((700, 900))
pygame.display.set_caption("Wha!quarim")

# Set colors
background_color = (0, 170, 255)
header_color = (200, 200, 200)
button_color = (255, 255, 255)
button_hover_color = (200, 200, 200)
text_color = (0, 0, 0)
button_border_color = (0, 0, 0)
input_box_color = (255, 255, 255)
input_text_color = (0, 0, 0)

# Load images
corn_image = pygame.image.load('corn.png')
corn_image = pygame.transform.scale(corn_image, (50, 50))

# Font settings
logo_font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 36)

# User attributes
user_attributes = [
    {"name": userdata[1], "money": userdata[5], "level": userdata[-1]}
]

# Button settings
button_width = 175
button_height = 60

# Navigation bar buttons
nav_buttons = ["Purchase", "Aquarium", "Breeding", "Pokedex"]
nav_button_rects = [pygame.Rect((i * button_width, 120), (button_width, button_height)) for i in range(4)]

# Feed buttons
feed_button_rects = [pygame.Rect((90+i * 120, 800), (50, 50)) for i in range(5)]

# Fish settings
fish_images = [pygame.transform.scale(pygame.image.load('whale.png'), (70, 70)) for _ in range(3)]
fish_positions = [[random.randint(100, 600), random.randint(200, 700)] for _ in range(3)]
fish_speeds = [random.choice([i*0.1+0.7 for i in range(10)]) for _ in range(3)]
fish_directions = [random.choice([1, -1]) for _ in range(3)]
dragging_fish = [False for _ in range(3)]
drag_offset_x = [0 for _ in range(3)]
drag_offset_y = [0 for _ in range(3)]

for i in range(len(fish_directions)):
    if fish_directions[i] == 1:
        fish_images[i] = pygame.transform.flip(fish_images[i], True, False)

# Pokedex variables
show_pokedex = False
pokedex_scroll_y = 0
pokedex_scroll_speed = 5
pokedex_items = ["Fish 1", "Fish 2", "Fish 3", "Fish 4", "Fish 5", "Fish 6", "Fish 7", "Fish 8", "Fish 9", "Fish 10"]

# Function to draw buttons
def draw_button(rect, text):
    pygame.draw.rect(screen, button_color, rect)
    pygame.draw.rect(screen, button_border_color, rect, 2)
    button_text = button_font.render(text, True, text_color)
    screen.blit(button_text, (rect.x + (rect.width - button_text.get_width()) // 2, rect.y + (rect.height - button_text.get_height()) // 2))

# Function to draw user attributes
def draw_user_attributes():
    pygame.draw.rect(screen, header_color, (0, 0, 700, 120))
    for i, attr in enumerate(user_attributes):
        screen.blit(corn_image, (20, 20 + i * 40))
        name_text = text_font.render(f"Name: {attr['name']}", True, text_color)
        money_text = text_font.render(f"Money: ${attr['money']}", True, text_color)
        level_text = text_font.render(f"Level: {attr['level']}", True, text_color)
        screen.blit(name_text, (90, 20 + i * 40))
        screen.blit(money_text, (90, 50 + i * 40))
        screen.blit(level_text, (90, 80 + i * 40))

# Function to draw the fish
def draw_fish():
    global fish_images, fish_positions, fish_speeds, fish_directions
    for i in range(len(fish_images)):
        fish_x, fish_y = fish_positions[i]
        fish_direction = fish_directions[i]
        fish_speed = fish_speeds[i]

        if not dragging_fish[i]:
            fish_x += fish_speed * fish_direction
            if fish_x <= 0 or fish_x >= 650:
                fish_direction *= -1
                fish_y += random.randint(-20, 20)
                if fish_y < 200:
                    fish_y = 200
                elif fish_y > 650:
                    fish_y = 650
                fish_images[i] = pygame.transform.flip(fish_images[i], True, False)
        
        fish_positions[i] = [fish_x, fish_y]
        fish_directions[i] = fish_direction
        screen.blit(fish_images[i], (fish_x, fish_y))

# Function to draw Pokedex
def draw_pokedex():
    global pokedex_scroll_y
    pokedex_surface = pygame.Surface((600, 700))
    pokedex_surface.fill((255, 255, 255))
    
    for i, item in enumerate(pokedex_items):
        item_text = text_font.render(item, True, (0, 0, 0))
        pokedex_surface.blit(item_text, (20, 20 + i * 40 - pokedex_scroll_y))
    
    screen.blit(pokedex_surface, (50, 150))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for i, rect in enumerate(feed_button_rects):
                if rect.collidepoint(mouse_pos):
                    print(f"Feed button {i+1} pressed")
            for i, rect in enumerate(nav_button_rects):
                if rect.collidepoint(mouse_pos):
                    print(f"{nav_buttons[i]} button pressed")
            for i in range(len(fish_positions)):
                fish_rect = pygame.Rect(fish_positions[i][0], fish_positions[i][1], 70, 70)
                if fish_rect.collidepoint(mouse_pos):
                    dragging_fish[i] = True
                    drag_offset_x[i] = fish_positions[i][0] - mouse_pos[0]
                    drag_offset_y[i] = fish_positions[i][1] - mouse_pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            for i in range(len(dragging_fish)):
                dragging_fish[i] = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            for i in range(len(dragging_fish)):
                if dragging_fish[i]:
                    fish_positions[i][0] = mouse_pos[0] + drag_offset_x[i]
                    fish_positions[i][1] = mouse_pos[1] + drag_offset_y[i]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pokedex_scroll_y = max(pokedex_scroll_y - pokedex_scroll_speed, 0)
            elif event.key == pygame.K_DOWN:
                pokedex_scroll_y = min(pokedex_scroll_y + pokedex_scroll_speed, len(pokedex_items) * 40 - 700)

    screen.fill(background_color)
    
    draw_user_attributes()
    
    for i, rect in enumerate(nav_button_rects):
        draw_button(rect, nav_buttons[i])

    if show_pokedex:
        draw_pokedex()
    
    for rect in feed_button_rects:
        screen.blit(corn_image, rect.topleft)
    
    draw_fish()
    
    pygame.display.flip()
    pygame.time.Clock().tick(60)

req.get(ip_text+f'/api/userlogout/{token}')
pygame.quit()
sys.exit()
