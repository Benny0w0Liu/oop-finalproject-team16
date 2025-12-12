import pygame
import numpy as np
from Archer_Pippy import Field, Arrow, Archer, Pigeon, Bow
"""
game environment class
"""
class Game:
    """
    create the game environment: set render or not
    """
    def __init__(self, render=True):
        # env setting
        self.render=render
        self.WIDTH, self.HEIGHT = 800, 450
        self.GRAVITY_VEC = np.array([0,0.02])
        self.total_frame=200
        
    """
    reset the game, set all the environment
    """
    def reset(self):
        # env setting
        self.current_frame=0
        self.bow_animation_counter=0
        # character setting
        self.archer = Archer(self.GRAVITY_VEC, self.HEIGHT, self.WIDTH)
        self.pigeon = Pigeon(self.HEIGHT, self.WIDTH,np.array([600,300]))
        # render setting
        if (self.render):            
            pygame.init()
            self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
            pygame.display.set_caption("Archer vs Piggy")
            self.clock = pygame.time.Clock()
            self.background = Field(img_path=[r".\sprites\field.png"],size=(800,450))
            arrow = Arrow(self.GRAVITY_VEC, self.HEIGHT, self.WIDTH)
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

            self.pigeon_ani_speed = 15 
    """
    update the environment
    input:  archer_action = {   -> set the archer action
                "shoot":(bool),                     -> shoot or not
                "move_angle":(float)                -> new bow angle = old + move_angle
            }, 
            pigeon_action = {   -> set the pigeon action
                "move_vector":(str)   -> direction 'L': left, 'R': right, 'U': up, 'D': down
            }
    output: observed_data=  {
                "env":{
                    "current_frame":(int)           -> current frame number
                    "game_state":(str)              -> "continue": game keep going
                                                       "pigeon win": game end, pigeon win
                                                       "archer win": game end, archer win
                },
                "archer":{
                    "bow_angle":(float),            -> new bow_angle
                    "left_arrows_num":(int),        -> number of left arrows
                    "shoot_cd":(int)                -> cd time of shooting
                }, 
                "pigeon":{
                    "position":(np.array,dim=(2,))  -> pigeon's position
                }, 
            }
    """
    def next_step(  self, 
                    archer_action={
                        "shoot":False,
                        "move_angle":0
                    }, 
                    pigeon_action={ 
                        "direction":"None"               
                    }
                 ):
        #update current_frame
        self.current_frame+=1
        
        #archer and arrows statement
        if self.archer.shoot_cd==0 and archer_action["shoot"]:
            self.archer.shoot()
            # Reset bow animation counter after shooting
            self.bow_animation_counter = 0
        else:
            # Increment bow animation counter
            if self.bow_animation_counter<50: 
                self.bow_animation_counter = (self.bow_animation_counter + 1)
        
        self.archer.update_arrows()
        self.archer.aim_angle+=archer_action["move_angle"]
        #update pigion statement
        pigeon_speed=3
        if pigeon_action["direction"]=="L":
            pigeon_action["move_vector"]=np.array([-pigeon_speed,0])
        elif pigeon_action["direction"]=="R":
            pigeon_action["move_vector"]=np.array([pigeon_speed,0])
        elif pigeon_action["direction"]=="D":
            pigeon_action["move_vector"]=np.array([0,-pigeon_speed])
        elif pigeon_action["direction"]=="U":
                pigeon_action["move_vector"]=np.array([0,pigeon_speed])
        self.pigeon.move(vec=pigeon_action["move_vector"])
        #write result of this frame
        observed_data=  {
            "env":{
                "current_frame":self.current_frame,
                "game_state":"continue"
            },
            "archer":{
                "bow_angle":self.archer.aim_angle, 
                "left_arrows_num":self.archer.arrow_num-self.archer.current_arrow_index,
                "shoot_cd":self.archer.shoot_cd
            }, 
            "pigeon":{
                "position":self.pigeon.box_position
            }
        }
        if self.archer.arrows[-1].isOut or self.current_frame>=self.total_frame:
            observed_data["env"]["game_state"]="pigeon win"
        archer_win=False
        for arrow in self.archer.arrows:
            a=arrow.box_scope()
            b=self.pigeon.box_scope()
            if not (a[2]<b[0] or a[0]>b[2] or a[3]<b[1] or a[1]>b[3]):
                archer_win=True
                break
        if archer_win:
            observed_data["env"]["game_state"]="archer win"
        #render if True
        if self.render:
            if self.bow_animation_counter < 20 and self.bow_animation_counter != 0:
                # none_draw_bow (index 0) for first 120 frames
                self.archer.bow.set_image(0)
            elif self.bow_animation_counter < 40 and self.bow_animation_counter != 0:
                # half_draw_bow (index 1) for next 20 frames (120-139)
                self.archer.bow.set_image(1)
            elif self.bow_animation_counter < 50 or self.bow_animation_counter == 0:
                # full_draw_bow (index 2) for last 10 frames (140-149)
                self.archer.bow.set_image(2)
            self.background.display(self.screen)
            self.archer.display(self.screen, self.HEIGHT)
            self.pigeon.display(self.screen, self.HEIGHT)
            pygame.display.flip()
            self.clock.tick(60)
        return observed_data
    """
    close the game env
    """
    def close(self):
        if (self.render):
            pygame.quit()
