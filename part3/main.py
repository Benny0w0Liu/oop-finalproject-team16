from abc import ABC, abstractmethod
import pygame

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Archer vs Piggy")

# Clock to control frame rate
clock = pygame.time.Clock()

class ElementBasicInfo(ABC):
    def display(self):
        pass
    def set_position(self):
        pass
    def set_rotation(self):
        pass
    def set_image(self):
        pass
class Field(ElementBasicInfo):
    def __init__(self, img_path, size, position=(0,0)):
        self.img_path=img_path
        self.position=position
        self.size=size
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[0]).convert_alpha(),self.size)
        return
    def display(self):
        screen.blit(self.img,self.position)
        return
class Archer(ElementBasicInfo):
    def __init__(self, img_path, size, position=(30,330)):
        self.img_path=img_path
        self.position=position
        self.size=size
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[0]).convert_alpha(),self.size)
        return
    def display(self):
        screen.blit(self.img,self.position)
        return
class Bow(ElementBasicInfo):
    def __init__(self, img_path, size, position=(50,300)):
        self.img_path=img_path
        self.position=position
        self.size=size
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[0]).convert_alpha(),self.size)
        self.angle=0
        return
    def display(self):
        screen.blit(self.img,self.position)
        return
    def set_rotation(self,angle):

        return
    def set_image(self, frame):
        self.img=pygame.transform.scale(pygame.image.load(self.img_path[frame]).convert_alpha(),self.size)
        return
archer = Archer(img_path=[r"D:\Github\114-1-OOP-group-project\part3\sprites\archer.png"],size=(100,100))
background = Field(img_path=[r"D:\Github\114-1-OOP-group-project\part3\sprites\field.png"],size=(800,450))
bow = Bow(img_path=[r"D:\Github\114-1-OOP-group-project\part3\sprites\none_draw_bow.png",
                    r"D:\Github\114-1-OOP-group-project\part3\sprites\half_draw_bow.png",
                    r"D:\Github\114-1-OOP-group-project\part3\sprites\full_draw_bow.png"],
                    size=(160,120))


# archer_img  = pygame.transform.scale(pygame.image.load(archer.img_path).convert_alpha(),archer.size)
# background_img = pygame.transform.scale(pygame.image.load(background.img_path).convert_alpha(),background.size)

# Initialize Pygame
pygame.init()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Fill background
    background.display()
    archer.display()
    bow.display()
    # Update display
    pygame.display.flip()

    # Limit frame rate to 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()