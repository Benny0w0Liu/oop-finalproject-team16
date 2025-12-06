from abc import ABC, abstractmethod
import pygame
import math
import numpy as np

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Archer vs Piggy")
GRAVITY_VEC=np.array([0,0.02])
# Clock to control frame rate
clock = pygame.time.Clock()

class RenderBasicInfo(ABC):
    def display(self):
        pass
    def set_position(self):
        pass
    def set_rotation(self):
        pass
    def set_image(self):
        pass
class Hitbox:
    def __init__(self,box_position,box_size):
        self.box_position=box_position # middle of box
        self.box_size=box_size
        self.box_move_vec=np.array([0,0])
    def box_scope(self):
        return [self.box_position[0]-self.box_size[0]/2, self.box_position[1]-self.box_size[1]/2,
                self.box_position[0]+self.box_size[0]/2,  self.box_position[1]+self.box_size[1]/2]
    def move(self, vec):
        self.box_position=self.box_position+vec
        self.box_move_vec=vec
        return self.box_position
    def set_box(self, position, vec):
        self.box_position=position
        self.box_move_vec=vec
# render element 
class Field(RenderBasicInfo):
    def __init__(self, img_path, size, position=(0,0)):
        self.img_path=img_path
        self.position=position
        self.size=size
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[0]).convert_alpha(),self.size)
        return
    def display(self):
        screen.blit(self.img,self.position)
        return
    def set_image(self, frame):
        self.frame=frame
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[frame]).convert_alpha(),self.size)
        return

class Bow(RenderBasicInfo):
    def __init__(self, img_path, size, position=(50, 330)):
        self.img_path=img_path
        self.position=position
        self.none_rotate_position=position
        self.size=size
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[0]).convert_alpha(),self.size)
        self.img_rotate=self.img.copy()
        self.angle=0
        return
    def display(self):
        screen.blit(self.img_rotate,self.position)
        return
    def set_rotation(self, angle):
        self.angle=angle
        self.img_rotate=pygame.transform.rotate(self.img, self.angle)
        x=self.none_rotate_position[0]+math.cos(math.radians(-angle))
        y=self.none_rotate_position[1]+math.sin(math.radians(-angle))
        self.position=self.img_rotate.get_rect(center=(x,y))
    def set_position(self, position):
        self.none_rotate_position=position
    def set_image(self, frame):
        self.frame=frame
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[frame]).convert_alpha(),self.size)

# interact element
class Arrow(RenderBasicInfo, Hitbox):
    def __init__(self, img_path, size, box_position=np.array([100,100]), box_size=(10,10)):
        self.img_path=img_path
        self.size=size
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[0]).convert_alpha(),self.size)
        self.img_rotate=self.img.copy()
        self.angle=0
        super().__init__(box_position, box_size)
    def display(self, show_box=True):
        if self.box_move_vec[0]==0 and self.box_move_vec[1]>0:
            self.angle=0
        elif self.box_move_vec[0]==0:
            self.angle=180
        elif self.box_move_vec[0]==0 and self.box_move_vec[1]>0:
            self.angle=90
        elif self.box_move_vec[0]==0:
            self.angle=270
        else:
            self.angle=math.degrees(math.atan(self.box_move_vec[1]/self.box_move_vec[0]))
        if(self.box_move_vec[0]<0):
            self.angle+=180
        self.img_rotate=pygame.transform.rotate(self.img, self.angle)
        x_sign=int(self.box_move_vec[0] > 0) - int(self.box_move_vec[0] < 0)
        y_sign=int(self.box_move_vec[1] > 0) - int(self.box_move_vec[1] < 0)
        x, y , w, h=self.img_rotate.get_rect(center=(self.box_position[0],HEIGHT-self.box_position[1]))
        self.position=(x-w/2*x_sign,y+h/2*y_sign)
        screen.blit(self.img_rotate,self.position)
        if show_box:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.box_position[0]-self.box_size[0]/2, HEIGHT-self.box_position[1]-self.box_size[1]/2, self.box_size[0], self.box_size[1]),2)
    def set_image(self, frame):
        self.frame=frame
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[frame]).convert_alpha(),self.size)
        return

class Archer(RenderBasicInfo, Hitbox):
    def __init__(self, img_path, bow ,size ,box_position=np.array([80,70]),box_size=(50,100)):
        self.img_path=img_path
        self.size=size
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[0]).convert_alpha(),self.size)
        self.bow=bow
        super().__init__(box_position, box_size)
    def display(self, show_box=True):
        self.bow.set_position((self.box_position[0], HEIGHT-self.box_position[1]-self.size[1]/5))
        x=self.box_position[0]-self.size[0]/2
        y=HEIGHT-self.box_position[1]-self.size[1]/2
        screen.blit(self.img,(x,y))
        if show_box:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.box_position[0]-self.box_size[0]/2, HEIGHT-self.box_position[1]-self.box_size[1]/2, self.box_size[0], self.box_size[1]),2)
    def set_image(self, frame):
        self.frame=frame
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[frame]).convert_alpha(),self.size)
        return

class Pigeon(RenderBasicInfo, Hitbox):
    def __init__(self, img_path, size, box_position=np.array([600,200]), box_size=(60,60),frame=0):
        self.img_path=img_path
        self.size=size
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[0]).convert_alpha(),self.size)
        self.frame=frame
        super().__init__(box_position, box_size)
        return
    def display(self,show_box=True):
        if show_box:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.box_position[0]-self.box_size[0]/2, HEIGHT-self.box_position[1]-self.box_size[1]/2, self.box_size[0], self.box_size[1]),2)
        x=self.box_position[0]-self.size[0]/2
        y=HEIGHT-self.box_position[1]-self.size[1]/2-10
        screen.blit(self.img,(x,y))
        return
    def set_image(self, frame):
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[frame]).convert_alpha(),self.size)
        return
    def update_animation(self):
        self.frame = (self.frame + 1) % len(self.img_path)
        self.set_image(self.frame)
        return

background = Field(img_path=[r".\sprites\field.png"],size=(800,450))
bow = Bow(img_path=[r".\sprites\none_draw_bow.png",
                    r".\sprites\half_draw_bow.png",
                    r".\sprites\full_draw_bow.png"],
                    size=(320,120))
archer = Archer(img_path=[r".\sprites\archer.png"], 
                size=(100,100), bow=bow)

pigeon = Pigeon(img_path=[r".\sprites\pigeon_up.png",
                          r".\sprites\pigeon_down.png"],
                          size=(80,80))
arrow = Arrow(img_path=[r".\sprites\arrow.png"],size=(88*2,6))

bow.set_image(0)

# Initialize Pygame
pygame.init()
frame_counter = 0
pigeon_ani_speed = 15 

bow_angle=0
pigeon_angle=0
running = True
arrow_vec=np.array([2,2])
archer_vec=np.array([1,0])
pigeon_vec=np.array([0,0])
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    frame_counter += 1
    if frame_counter >= pigeon_ani_speed:
        frame_counter = 0
        pigeon.update_animation()

    # Fill background
    background.display()
    archer.display()
    bow.display()
    pigeon.display()
    arrow.display()
    # Update display
    pygame.display.flip()

    # Limit frame rate to 60 FPS
    clock.tick(60)

    #expirement
    bow_angle+=1
    pigeon_angle+=0.05
    bow.set_image(bow_angle%3)
    bow.set_rotation(bow_angle)
    arrow.move(vec=arrow_vec)
    archer.move(vec=archer_vec)
    pigeon.move(vec=pigeon_vec)
    pigeon_vec=np.array([math.cos(pigeon_angle)*5, math.sin(pigeon_angle)*5])
    archer_vec=np.array([math.cos(pigeon_angle)*2,0])
    arrow_vec=arrow_vec-GRAVITY_VEC

# Quit Pygame
pygame.quit()