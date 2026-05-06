import pygame
import sys
import random

# Pygame başlangıç
pygame.init()

# Ekran boyutları
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Renkler
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Sinek sınıfı
class Sinek:
    def __init__(self):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(0, screen_height)
        self.speed_x = random.choice([-1, 1])
        self.speed_y = random.choice([-1, 1])

    def hareket_et(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < 0 or self.x > screen_width:
            self.speed_x *= -1
        if self.y < 0 or self.y > screen_height:
            self.speed_y *= -1

# Sinek oluşturma
sinek = Sinek()

# Oyun döngüsü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Ekranı temizle
    screen.fill(white)

    # Sineği hareket ettir
    sinek.hareket_et()

    # Sineği çiz
    pygame.draw.circle(screen, black, (sinek.x, sinek.y), 10)

    # Ekranı güncelle
    pygame.display.flip()
    pygame.time.Clock().tick(60)