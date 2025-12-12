from game_env import Game
class PigeonAgent:
    def __init__(self):
        self.dir="U"
    def up_down_agent(self, last_state):
        if(last_state["pigeon"]["position"][1]>=400.0):
            self.dir="D"
        elif(last_state["pigeon"]["position"][1]<=200.0):
            self.dir="U"
        return {   
                    "direction":self.dir
                }
class ArcherAgent:
    def __init__(self):
        self.shoot=False
        self.move_angle=0.0
        # you may add other variables for the agent
    def agent(self, last_state): # you may add other parameter for the agent
        # Your code here ->

        
        #<- Your code here
        return {   
                    "shoot":self.shoot,                     
                    "move_angle":self.move_angle            
                }

def run(episodes=1, render=True):
    game = Game(render=render)
    for episode in range(episodes):
        game.reset()
        # initialize Agent
        pigeonAgent=PigeonAgent()
        archerAgent=ArcherAgent()
        # get into 
        while(1):
            result=game.next_step(
                archer_action = {   
                    "shoot":archerAgent.shoot,                     
                    "move_angle":archerAgent.move_angle           
                }, 
                pigeon_action = {   
                    "direction":pigeonAgent.dir
                })
            pigeonAgent.up_down_agent(result)
            archerAgent.agent(result)
            if(result["env"]["game_state"]!="continue"):
                break
    game.close()
run()