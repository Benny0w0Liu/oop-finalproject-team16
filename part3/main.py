from game_env import Game
import math
import random

class PigeonAgent:
    def __init__(self):
        self.dir=random.choice(["U","D","L","R"])
        self.spe=random.randint(1,3)
    def up_down_agent(self, last_state):
        if(last_state["pigeon"]["position"][1]>=400.0):
            self.dir="D"
        elif(last_state["pigeon"]["position"][1]<=200.0):
            self.dir="U"
        # if(last_state["pigeon"]["position"][0]>=500.0):
        #     self.dir="L"
        # elif(last_state["pigeon"]["position"][0]<=300.0):
        #     self.dir="R"        
    def random_agent(self, last_state):
        pos_x=last_state["pigeon"]["position"][0]
        pos_y=last_state["pigeon"]["position"][1]
        if(pos_x>=620.0):
            self.dir="L"
        elif(pos_x<=300.0):
            self.dir="R"
        elif(pos_y>=400.0):
            self.dir="D"
        elif(pos_y<=200.0):
            self.dir="U"
        else:
            if random.random()<0.3:
                self.dir=random.choice(["U","D","L","R"])
        return {   
                    "direction":self.dir,
                    "speed":self.spe
                }
    def learnt_agent(self, last_state):
        return
class ArcherAgent:
    def __init__(self):
        self.shoot = True
        self.move_angle = 0.1
        # 學習參數
        self.height_adjustment = 0 
        self.learning_rate = 0.05
        self.shot_history = []
        self.current_shot_data = None 
        self.episode_count = 0
        
    def agent(self, last_state):
        # Your code here ->
        pigeon_pos = last_state["pigeon"]["position"]  
        bow_angle = last_state["archer"]["bow_angle"]
        shoot_cd = last_state["archer"]["shoot_cd"]
        game_state = last_state["env"]["game_state"]
        
        archer_x = 80
        archer_y = 70
        
        # 計算到鴿子的距離
        dx = pigeon_pos[0] - archer_x
        dy = pigeon_pos[1] - archer_y
        distance = math.sqrt(dx**2 + dy**2)
        
        # 預測飛行時間（箭的初速度是10，考慮重力影響）
        arrow_initial_speed = 10
        estimated_time = distance / (arrow_initial_speed * 0.7)  # 0.7是經驗係數
        
        # 預測鴿子未來位置
        # 鴿子速度為3，根據當前位置判斷移動方向
        pigeon_speed = 2
        if pigeon_pos[1] >= 400:
            # 鴿子在頂部，會往下移動
            predicted_movement = -pigeon_speed * estimated_time
        elif pigeon_pos[1] <= 200:
            # 鴿子在底部，會往上移動
            predicted_movement = pigeon_speed * estimated_time
        else:
            # 在中間，根據位置判斷趨勢
            if pigeon_pos[1] > 300:
                predicted_movement = pigeon_speed * estimated_time * 0.5
            else:
                predicted_movement = -pigeon_speed * estimated_time * 0.5
        
        # 計算預測的 dy（加上學習的高度調整）
        predicted_dy = dy + predicted_movement + self.height_adjustment
        
        # 計算目標角度
        target_angle = math.degrees(math.atan2(predicted_dy, dx))
        
        # 調整弓的角度
        angle_diff = target_angle - bow_angle
        if abs(angle_diff) > 2:
            self.move_angle = 2 if angle_diff > 0 else -2
        else:
            self.move_angle = angle_diff
        
        # 決定是否射擊
        if shoot_cd == 0 and abs(angle_diff) < 5:
            self.shoot = True
            # 記錄這次射擊的資訊
            self.current_shot_data = {
                'pigeon_y': pigeon_pos[1],
                'predicted_movement': predicted_movement,
                'adjustment': self.height_adjustment,
                'angle': target_angle
            }
        else:
            self.shoot = False
        
        # 學習更新（當遊戲結束時）
        if game_state != "continue":
            if game_state == "archer win":
                # 成功！記錄這次的調整參數
                if self.current_shot_data:
                    self.shot_history.append({
                        'adjustment': self.height_adjustment,
                        'success': True
                    })
                    # 保持最近100次的歷史
                    if len(self.shot_history) > 100:
                        self.shot_history.pop(0)
            else:
                # 失敗，需要調整策略
                if len(self.shot_history) > 0:
                    # 計算成功案例的平均調整值
                    successful_adjustments = [h['adjustment'] for h in self.shot_history if h['success']]
                    if len(successful_adjustments) > 0:
                        # 向成功案例的平均值靠攏
                        avg_success = sum(successful_adjustments) / len(successful_adjustments)
                        self.height_adjustment += (avg_success - self.height_adjustment) * self.learning_rate
                    else:
                        # 沒有成功案例，進行探索
                        
                        self.height_adjustment += random.uniform(-8, 8)
                else:
                    # 初期探索階段
                    self.height_adjustment += random.uniform(-15, 15)
            
            # 重置當前射擊數據
            self.current_shot_data = None
            self.episode_count += 1
            
            # 每100個episode輸出學習進度
            if self.episode_count % 10 == 0:
                success_rate = len([h for h in self.shot_history if h['success']]) / max(len(self.shot_history), 1) * 100
                print(f"Episode {self.episode_count}: Success Rate = {success_rate:.1f}%, Height Adjustment = {self.height_adjustment:.2f}")
        
        return {
            "shoot": self.shoot,
            "move_angle": self.move_angle
        }
            
        #<- Your code here

def run(episodes=1, render=True):
    game = Game(render=render)
    # 在所有 episodes 外初始化 archerAgent，讓它能累積學習經驗
    archerAgent = ArcherAgent()
    
    for episode in range(episodes):
        game.reset()
        # 每個 episode 重新初始化 pigeonAgent
        pigeonAgent = PigeonAgent()
        
        # get into 
        while(1):
            
            result = game.next_step(
                archer_action = {   
                    "shoot": archerAgent.shoot,                     
                    "move_angle": archerAgent.move_angle           
                }, 
                pigeon_action = {   
                    "direction": pigeonAgent.dir,
                    "speed": pigeonAgent.spe
                })
            pigeonAgent.up_down_agent(result)
            archerAgent.agent(result)
            if(result["env"]["game_state"] != "continue"):
                break
            # 移除 print 以加快訓練速度
            # print(result)
    
    # 訓練結束後輸出最終統計
    if len(archerAgent.shot_history) > 0:
        final_success_rate = len([h for h in archerAgent.shot_history if h['success']]) / len(archerAgent.shot_history) * 100
        print(f"\n=== Training Complete ===")
        print(f"Total Episodes: {archerAgent.episode_count}")
        print(f"Final Success Rate (last 100): {final_success_rate:.1f}%")
        print(f"Optimal Height Adjustment: {archerAgent.height_adjustment:.2f}")
    
    game.close()

run(episodes=1000, render=False)
