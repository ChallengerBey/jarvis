import pygame
import sys
import time
import random

# Oyun penceresini oluştur
pygame.init()
ekran = pygame.display.set_mode((800, 600))

# Renkleri tanımla
beyaz = (255, 255, 255)
kirmizi = (255, 0, 0)
siyah = (0, 0, 0)

# Yılanın başlangıç konumunu ve hızını tanımla
yilan_konumu = [100, 50]
yilan_hizi = [1, 0]

# Yılanın uzunluğunu tanımla
yilan_uzunlugu = 1

# Yılanın gövdesini tanımla
yilan_govdesi = [[100, 50]]

# Yem konumu
yem_konumu = [random.randint(0, 790), random.randint(0, 590)]

# Oyun döngüsü
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and yilan_hizi != [0, 1]:
                yilan_hizi = [0, -1]
            elif event.key == pygame.K_DOWN and yilan_hizi != [0, -1]:
                yilan_hizi = [0, 1]
            elif event.key == pygame.K_LEFT and yilan_hizi != [1, 0]:
                yilan_hizi = [-1, 0]
            elif event.key == pygame.K_RIGHT and yilan_hizi != [-1, 0]:
                yilan_hizi = [1, 0]

    # Yılanın yeni konumunu hesapla
    yilan_konumu[0] += yilan_hizi[0]
    yilan_konumu[1] += yilan_hizi[1]

    # Yılanın gövdesini güncelle
    yilan_govdesi.insert(0, list(yilan_konumu))
    if len(yilan_govdesi) > yilan_uzunlugu:
        yilan_govdesi.pop()

    # Yılanın yemle temasını kontrol et
    if yilan_konumu[0] == yem_konumu[0] and yilan_konumu[1] == yem_konumu[1]:
        yilan_uzunlugu += 1
        yem_konumu = [random.randint(0, 790), random.randint(0, 590)]

    # Yılanın duvarla temasını kontrol et
    if (yilan_konumu[0] < 0 or yilan_konumu[0] > 790) or (yilan_konumu[1] < 0 or yilan_konumu[1] > 590):
        pygame.quit()
        sys.exit()

    # Yılanın kendi gövdesiyle temasını kontrol et
    for i in range(1, len(yilan_govdesi)):
        if yilan_konumu[0] == yilan_govdesi[i][0] and yilan_konumu[1] == yilan_govdesi[i][1]:
            pygame.quit()
            sys.exit()

    # Ekranı güncelle
    ekran.fill(siyah)
    for pos in yilan_govdesi:
        pygame.draw.rect(ekran, beyaz, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(ekran, kirmizi, pygame.Rect(yem_konumu[0], yem_konumu[1], 10, 10))
    pygame.display.update()
    time.sleep(0.1)