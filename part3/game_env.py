from abc import ABC, abstractmethod
import pygame
import math
import numpy as np
from main import Field, Arrow, Archer, Pigeon, Bow

class Game:
    def __init__(self, render=True):
        self.WIDTH, self.HEIGHT = 800, 450
        self.render=render
    def reset(self):
        self.archer = Archer()
        self.pigeon = Pigeon()
        if (self.render):            
            pygame.init()
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption("Archer vs Piggy")
            clock = pygame.time.Clock()
            self.background = Field(img_path=[r".\sprites\field.png"],size=(800,450))
            arrow = Arrow()
            arrow.set_display(img_path=[r".\sprites\arrow.png"],size=(88*2,6))
            self.archer.set_display(img_path=[r".\sprites\archer.png"], 
                            size=(100,100), 
                            bow_set=Bow(img_path=[r".\sprites\none_draw_bow.png",
                                r".\sprites\half_draw_bow.png",
                                r".\sprites\full_draw_bow.png"],
                                size=(320,120)),
                            arrow_set=arrow)
            self.pigeon.set_display(img_path=[r".\sprites\pigeon_up.png",
                                    r".\sprites\pigeon_down.png"],
                                    size=(80,80))
            self.frame_counter = 0
            self.pigeon_ani_speed = 15 
    def next_step(self, archer_move, pigeon_move):
        observed_data={"archer":[], "pigeon":[]}
        return observed_data
    def close(self):
        if (self.render):
            print(self.render)
            pygame.quit()
game = Game(render=False)
game.reset()

game.close()
# pygame.init()

# # Screen dimensions
# WIDTH, HEIGHT = 800, 450
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# pygame.display.set_caption("Archer vs Piggy")
# GRAVITY_VEC=np.array([0,0.02])
# # Clock to control frame rate
# clock = pygame.time.Clock()

# background = Field(img_path=[r".\sprites\field.png"],size=(800,450))
# arrow = Arrow()
# arrow.set_display(img_path=[r".\sprites\arrow.png"],size=(88*2,6))
# archer = Archer()
# archer.set_display(img_path=[r".\sprites\archer.png"], 
#                 size=(100,100), 
#                 bow_set=Bow(img_path=[r".\sprites\none_draw_bow.png",
#                     r".\sprites\half_draw_bow.png",
#                     r".\sprites\full_draw_bow.png"],
#                     size=(320,120)),
#                 arrow_set=arrow)
# pigeon = Pigeon()
# pigeon.set_display(img_path=[r".\sprites\pigeon_up.png",
#                           r".\sprites\pigeon_down.png"],
#                           size=(80,80))


# frame_counter = 0
# pigeon_ani_speed = 15 

# bow_angle=0
# pigeon_angle=0
# running = True
# archer_vec=np.array([1,0])
# pigeon_vec=np.array([0,0])
# archer.bow.set_image(2)
# for i in range(100):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     frame_counter += 1
#     if frame_counter >= pigeon_ani_speed:
#         frame_counter = 0
#         pigeon.update_animation()

#     # Fill background
#     background.display()
#     archer.display()
#     pigeon.display()
#     # arrow.display()
#     # Update display
#     pygame.display.flip()

#     # Limit frame rate to 60 FPS
#     clock.tick(60)
#     if frame_counter%50==0:
#         archer.shoot()
#         print("shoot")
#     archer.update_arrow()
#     #expirement
#     archer.aim_angle+=0.5
#     pigeon_angle+=0.05
#     # bow.set_image(bow_angle%3)
#     # bow.set_rotation(bow_angle)
#     # archer.move(vec=archer_vec)
#     pigeon.move(vec=pigeon_vec)
#     pigeon_vec=np.array([math.cos(pigeon_angle)*5, math.sin(pigeon_angle)*5])
#     archer_vec=np.array([math.cos(pigeon_angle)*2,0])

# # Quit Pygame
# pygame.quit()