import pygame
import sys
import random

pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # 设置为可调整大小
pygame.display.set_caption("Mouse Follow Example")

background = pygame.image.load("background.png")
girl = pygame.image.load("girl.png")
stick = pygame.image.load("stick.png")
bubble = pygame.image.load("bubble.png")
circle1 = pygame.image.load("circle1.png")
circle2 = pygame.image.load("circle2.png")
circle3 = pygame.image.load("circle3.png")
circle4 = pygame.image.load("circle4.png")
circle5 = pygame.image.load("circle5.png")
circle6 = pygame.image.load("circle6.png")
circle7 = pygame.image.load("circle7.png")
circle8 = pygame.image.load("circle8.png")

pygame.mixer.init()
bubble_pop_sound = pygame.mixer.Sound("bubble2.wav")
background_music = pygame.mixer.Sound("bubble2.wav")

background_music.play(loops=-1, maxtime=0)


def scale_image(image, scale_factor):
    width, height = image.get_size()
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return pygame.transform.scale(image, (new_width, new_height))

def calculate_scale_factor():
    return screen_width / 1920  


scale_factor = calculate_scale_factor()

background = scale_image(background, scale_factor)
girl = scale_image(girl, scale_factor)
stick = scale_image(stick, scale_factor)
bubble = scale_image(bubble, scale_factor)
circle1 = scale_image(circle1, scale_factor * 0.6)
circle2 = scale_image(circle2, scale_factor * 0.6)
circle3 = scale_image(circle3, scale_factor * 0.6)
circle4 = scale_image(circle4, scale_factor * 0.6)
circle5 = scale_image(circle5, scale_factor * 0.6)
circle6 = scale_image(circle6, scale_factor * 0.6)
circle7 = scale_image(circle7, scale_factor * 0.6)
circle8 = scale_image(circle8, scale_factor * 0.6)


girl_rect = girl.get_rect()
girl_rect.topright = (screen_width - 50, screen_height // 2 - girl_rect.height // 2)

class Bubble:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.speed = random.uniform(2, 5)
        self.alpha = 255
        self.creation_time = pygame.time.get_ticks()
        self.length = random.uniform(screen_width / 3, screen_width / 2)

    def update(self):
        self.x -= self.speed
        self.y -= random.uniform(0, 1)
        self.rect.x = self.x
        self.rect.y = self.y

        elapsed_time = pygame.time.get_ticks() - self.creation_time
        if elapsed_time > 1000:
            self.alpha = max(0, 255 - int((elapsed_time - 1000) / 5))

        self.image.set_alpha(self.alpha)

        if self.x < -self.length:
            return True
        return False


running = True
bubbles = []
last_bubble_time = 0
bubble_frequency = 500  

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if stick.get_rect(center=(mouse_x, mouse_y)).colliderect(girl_rect):

        current_time = pygame.time.get_ticks()
        if current_time - last_bubble_time > bubble_frequency:

            bubble_type = random.choice([bubble, circle1, circle2, circle3, circle4, circle5, circle6, circle7, circle8])
            bubbles.append(Bubble(mouse_x, mouse_y - stick.get_height() / 2, bubble_type))
            bubble_pop_sound.play()
            last_bubble_time = current_time

    bubbles = [b for b in bubbles if not b.update()]

    screen.blit(background, (0, 0))


    screen.blit(girl, girl_rect)

    stick_rect = stick.get_rect(center=(mouse_x, mouse_y))
    screen.blit(stick, stick_rect)

    for b in bubbles:
        screen.blit(b.image, b.rect)


    pygame.display.flip()

    pygame.time.Clock().tick(60)


pygame.quit()
sys.exit()
