#!/usr/bin/python3


import binimage
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # this goes after 'os' and before 'pygame'
import pygame
import time
import sys


filename = sys.argv[1]
print(f"Loading {filename}")
i = binimage.LedFanBinImage("G224-42")
i.import_bin_movie(filename)
frames = i.total_frames
print(f"Total frames: {frames}")
i.decode_movie()
img = i.get_numpy_frame_cartesian(0)
shapey, shapex, shapez = img.shape
print(f"Shape: {shapex} x {shapey}")

pygame.init()
displaywindow = pygame.display.set_mode((shapex*2+10, shapey*2+10))
pygame.display.set_caption('BIN Player')

running = True
while running:

    for f in range(frames):
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == ord("q"):
                    running = False
        if not running: break

        img = i.get_numpy_frame_cartesian(f)
        surface = pygame.transform.scale2x(pygame.surfarray.make_surface(img))
        displaywindow.blit(surface, (5,5))
        pygame.display.update()

        time.sleep(1/24)

pygame.quit()

