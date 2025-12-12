from abc import ABC
import pygame
import math
import numpy as np

class RenderBasicInfo(ABC):
    def set_display(self):
        pass
    def display(self):
        pass
    def set_position(self):
        pass
    def set_rotation(self):
        pass
    def set_image(self):
        pass
class Hitbox:
    def __init__(self,box_position,box_size, HEIGHT, WIDTH):
        self.HEIGHT=HEIGHT
        self.WIDTH=WIDTH
        self.box_position=box_position # middle of box
        self.box_size=box_size
        self.box_move_vec=np.array([0,0])
    def box_scope(self):
        return [self.box_position[0]-self.box_size[0]/2, self.box_position[1]-self.box_size[1]/2,
                self.box_position[0]+self.box_size[0]/2,  self.box_position[1]+self.box_size[1]/2]
    def move(self, vec):
        if (self.box_scope()[0]<=0 or self.box_scope()[1]<=0 or self.box_scope()[2]>=self.WIDTH or self.box_scope()[3]>=self.HEIGHT):
            return False
        self.box_position=self.box_position.astype(float)+vec.astype(float)
        self.box_move_vec=vec
        return True
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
    def display(self, screen):
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
    def display(self,screen):
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
    def __init__(self, GRAVITY_VEC, HEIGHT, WIDTH ,box_position=np.array([100,100]), box_size=(10,10)):
        self.isOut=False
        self.GRAVITY_VEC=GRAVITY_VEC
        super().__init__(box_position, box_size, HEIGHT, WIDTH)
    def set_display(self, img_path, size):        
        self.img_path=img_path
        self.size=size
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[0]).convert_alpha(),self.size)
        self.img_rotate=self.img.copy()
    def display(self, screen, show_box=True):
        if self.box_move_vec[0]==0 and self.box_move_vec[1]>0:
            angle=0
        elif self.box_move_vec[0]==0:
            angle=180
        elif self.box_move_vec[0]==0 and self.box_move_vec[1]>0:
            angle=90
        elif self.box_move_vec[0]==0:
            angle=270
        else:
            angle=math.degrees(math.atan(self.box_move_vec[1]/self.box_move_vec[0]))
        if(self.box_move_vec[0]<0):
            angle+=180
        self.img_rotate=pygame.transform.rotate(self.img, angle)
        x_sign=int(self.box_move_vec[0] > 0) - int(self.box_move_vec[0] < 0)
        y_sign=int(self.box_move_vec[1] > 0) - int(self.box_move_vec[1] < 0)
        x, y , w, h=self.img_rotate.get_rect(center=(self.box_position[0], self.HEIGHT-(self.box_position[1]-self.box_size[1]/2)+self.size[1]/2))
        self.position=(x-w/2*x_sign,y+h/2*y_sign)
        screen.blit(self.img_rotate,self.position)
        if show_box:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.box_position[0]-self.box_size[0]/2, self.HEIGHT-(self.box_position[1]-self.box_size[1]/2), self.box_size[0], self.box_size[1]),2)
    def set_image(self, frame):
        self.frame=frame
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[frame]).convert_alpha(),self.size)
        return
    def update_vec(self):
        self.isOut = not self.move(self.box_move_vec)
        if self.isOut!= True:
            self.box_move_vec=self.box_move_vec-self.GRAVITY_VEC.astype(float)
        return True
class Archer(RenderBasicInfo, Hitbox):
    def __init__(self, GRAVITY_VEC, HEIGHT, WIDTH, box_position=np.array([80,70]),box_size=(50,100)):
        self.aim_angle=0
        self.arrow_num=3
        self.arrows=[Arrow(GRAVITY_VEC, HEIGHT, WIDTH) for _ in range(self.arrow_num)]
        for arrow in self.arrows:
            arrow.set_box(np.array([100,10]), np.array([0,0]))
        self.current_arrow_index=-1
        self.shoot_cd=0
        super().__init__(box_position, box_size, HEIGHT, WIDTH)
    def set_display(self, img_path, bow_set, arrow_set,size):
        self.img_path=img_path
        self.size=size
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[0]).convert_alpha(),self.size)
        self.bow=bow_set
        for arrow in self.arrows:
            arrow.set_display(arrow_set.img_path,arrow_set.size)
    def display(self, screen, show_box=True):
        self.bow.set_position((self.box_position[0], self.HEIGHT-self.box_position[1]-self.size[1]/5))
        self.bow.set_rotation(self.aim_angle)
        x=self.box_position[0]-self.size[0]/2
        y=self.HEIGHT-self.box_position[1]-self.size[1]/2
        screen.blit(self.img,(x,y))
        self.bow.display(screen)
        for arrow in self.arrows:
            arrow.display(screen,show_box)
        if show_box:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.box_position[0]-self.box_size[0]/2, self.HEIGHT-self.box_position[1]-self.box_size[1]/2, self.box_size[0], self.box_size[1]),2)
    def set_image(self, frame):
        self.frame=frame
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[frame]).convert_alpha(),self.size)
        return
    def shoot(self):        
        if self.shoot_cd>0: 
            return
        if self.current_arrow_index==-1:
            self.current_arrow_index=0
        if(self.current_arrow_index>=0 and self.current_arrow_index<self.arrow_num):
            vec_x, vec_y=10*math.cos(math.radians(self.aim_angle)), 10*math.sin(math.radians(self.aim_angle))
            pos_x=self.box_position[0]+88*math.cos(math.radians(self.aim_angle))
            pos_y=self.box_position[1]+self.box_size[1]/5+88*math.sin(math.radians(self.aim_angle))
            self.arrows[self.current_arrow_index].set_box(np.array([pos_x, pos_y]),
                                                            np.array([vec_x,vec_y]))
            # print(self.current_arrow_index,vec_x,vec_y)
            self.current_arrow_index+=1
            self.shoot_cd=50
    def update_arrows(self):
        if(self.shoot_cd>0): self.shoot_cd-=1
        if(self.current_arrow_index<0): return
        for i in range(len(self.arrows)):
            if(i<self.current_arrow_index):
                self.arrows[i].update_vec()

class Pigeon(RenderBasicInfo, Hitbox):
    def __init__(self, HEIGHT, WIDTH, box_position=np.array([600,200]), box_size=(60,60)):
        super().__init__(box_position, box_size, HEIGHT, WIDTH)
        return
    def set_display(self,img_path, size, frame=0):
        self.img_path=img_path
        self.size=size
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[0]).convert_alpha(),self.size)
        self.frame=frame
    def display(self,screen,show_box=True):
        if show_box:
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.box_position[0]-self.box_size[0]/2, self.HEIGHT-self.box_position[1]-self.box_size[1]/2, self.box_size[0], self.box_size[1]),2)
        x=self.box_position[0]-self.size[0]/2
        y=self.HEIGHT-self.box_position[1]-self.size[1]/2-10
        screen.blit(self.img,(x,y))
        return
    def set_image(self, frame):
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[frame]).convert_alpha(),self.size)
        return
    def update_animation(self):
        self.frame = (self.frame + 1) % len(self.img_path)
        self.set_image(self.frame)
        return
