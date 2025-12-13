from game_env import Game
import math
import random
import json
import os

class PigeonAgent:
    def __init__(self, agent_mode):
        self.agent_mode=agent_mode
        if(agent_mode=="random_agent"):
            self.dir=random.choice(["U","D","L","R"])
            self.spe=random.randint(1,3)
        else:
            self.dir="U"
            self.spe=3
        
        # 學習參數（用於 learnt_agent）
        self.learning_rate = 0.1
        self.danger_threshold = 150  # 危險距離閾值
        self.safe_y_min = 220  # 安全區域 Y 最小值
        self.safe_y_max = 380  # 安全區域 Y 最大值
        self.episode_history = []  # 記錄每回合的結果
        self.survival_strategies = []  # 成功策略記錄
        self.episode_count = 0
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
            if random.random()<0.25:
                self.dir=random.choice(["U","D","L","R"])
        return {   
                    "direction":self.dir,
                    "speed":self.spe
                }
    def learnt_agent(self, last_state, train=False):
        pigeon_pos = last_state["pigeon"]["position"]
        bow_angle = last_state["archer"]["bow_angle"]
        game_state = last_state["env"]["game_state"]
        
        # 弓箭手位置（固定）
        archer_x = 80
        archer_y = 70
        
        # 計算相對位置
        dx = pigeon_pos[0] - archer_x
        dy = pigeon_pos[1] - archer_y
        distance = math.sqrt(dx**2 + dy**2)
        
        # 根據弓的角度預測危險區域
        # 弓角度指向的 Y 座標範圍
        predicted_target_y = archer_y + dx * math.tan(math.radians(bow_angle))
        
        # 判斷是否在危險區域
        in_danger = abs(pigeon_pos[1] - predicted_target_y) < 50 and distance < self.danger_threshold
        
        # 閃避邏輯
        if in_danger:
            # 在危險區域，需要快速閃避
            if pigeon_pos[1] > predicted_target_y:
                # 在瞄準線上方，往上移動
                self.dir = "U"
                self.spe = 3
            else:
                # 在瞄準線下方，往下移動
                self.dir = "D"
                self.spe = 3
        else:
            # 不在危險區域，進行策略性移動
            # 保持在安全 Y 範圍內，同時左右移動增加命中難度
            if pigeon_pos[1] >= self.safe_y_max:
                self.dir = "D"
                self.spe = 2
            elif pigeon_pos[1] <= self.safe_y_min:
                self.dir = "U"
                self.spe = 2
            else:
                # 在安全區域內，進行左右移動
                if pigeon_pos[0] >= 620:
                    self.dir = "L"
                    self.spe = 2
                elif pigeon_pos[0] <= 400:
                    self.dir = "R"
                    self.spe = 2
                else:
                    # 隨機選擇上下移動，增加不可預測性
                    if random.random() < 0.3:
                        self.dir = random.choice(["U", "D"])
                        self.spe = 2
        
        # 學習更新（遊戲結束時）
        if game_state != "continue":
            if game_state == "pigeon win":
                # 鴿子獲勝，記錄成功策略
                self.survival_strategies.append({
                    'safe_y_min': self.safe_y_min,
                    'safe_y_max': self.safe_y_max,
                    'danger_threshold': self.danger_threshold,
                    'success': True
                })
                # 保持最近 50 個成功案例
                if len(self.survival_strategies) > 50:
                    self.survival_strategies.pop(0)
            else:
                # 鴿子失敗，調整策略參數
                if train:
                    if len(self.survival_strategies) > 0:
                        # 從成功案例中學習
                        avg_safe_y_min = sum([s['safe_y_min'] for s in self.survival_strategies]) / len(self.survival_strategies)
                        avg_safe_y_max = sum([s['safe_y_max'] for s in self.survival_strategies]) / len(self.survival_strategies)
                        avg_danger_threshold = sum([s['danger_threshold'] for s in self.survival_strategies]) / len(self.survival_strategies)
                        
                        # 向成功案例的平均值調整
                        self.safe_y_min += (avg_safe_y_min - self.safe_y_min) * self.learning_rate
                        self.safe_y_max += (avg_safe_y_max - self.safe_y_max) * self.learning_rate
                        self.danger_threshold += (avg_danger_threshold - self.danger_threshold) * self.learning_rate
                    else:
                        # 沒有成功案例，進行探索
                        self.safe_y_min += random.uniform(-10, 10)
                        self.safe_y_max += random.uniform(-10, 10)
                        self.danger_threshold += random.uniform(-20, 20)
                        
                        # 確保參數在合理範圍內
                        self.safe_y_min = max(200, min(280, self.safe_y_min))
                        self.safe_y_max = max(350, min(420, self.safe_y_max))
                        self.danger_threshold = max(100, min(250, self.danger_threshold))
            
            self.episode_count += 1
            
            # 每 10 個 episode 輸出學習進度
            if train and self.episode_count % 10 == 0:
                # 計算最近 10 個 episode 的成功率
                recent_strategies = self.survival_strategies[-10:] if len(self.survival_strategies) >= 10 else self.survival_strategies
                if len(recent_strategies) > 0:
                    success_rate = len([s for s in recent_strategies if s['success']]) / len(recent_strategies) * 100
                    print(f"Episode {self.episode_count}: Pigeon Success Rate (last {len(recent_strategies)}): {success_rate:.1f}%, Safe Y Range = [{self.safe_y_min:.1f}, {self.safe_y_max:.1f}]")
            
        
        return {
            "direction": self.dir,
            "speed": self.spe
        }
    def agent(self, last_state, train=False):
        if(self.agent_mode=="up_down_agent"):
            self.up_down_agent(last_state=last_state)
        elif(self.agent_mode=="random_agent"):
            self.random_agent(last_state=last_state)
        elif(self.agent_mode=="learnt_agent"):
            self.learnt_agent(last_state=last_state, train=train)
        return
class ArcherAgent:
    def __init__(self, train=True):
        self.shoot = True
        self.move_angle = 0.1
        # 學習參數
        self.height_adjustment = 0 
        self.learning_rate = 0.05
        self.current_shot_data = None 
        self.episode_count = 0
        
        # 檔案路徑
        self.dataset_dir = r".\dataset"
        self.successful_history_path = r".\dataset\successful_history"
        self.history_path = r".\dataset\history"
        
        if not train:
            successful_history = self._load_history_from_file(self.successful_history_path)
            if len(successful_history) > 0:
                avg_adjustment = sum([h['adjustment'] for h in successful_history]) / len(successful_history)
                self.height_adjustment = avg_adjustment
                print(f"[Archer] 載入訓練參數：Height Adjustment = {self.height_adjustment:.2f}")
            else:
                print("[Archer] 警告：找不到訓練資料，使用預設參數")
    
    def _load_history_from_file(self, filepath):
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history_to_file(self, filepath, data):
        # 確保目錄存在
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def agent(self, last_state, train=True):
        # Your code here ->
        pigeon_pos = last_state["pigeon"]["position"]  
        bow_angle = last_state["archer"]["bow_angle"]
        shoot_cd = last_state["archer"]["shoot_cd"]
        game_state = last_state["env"]["game_state"]
        """
        1. if train is true: build a empty file 
            else: read the file
        """
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
            # 載入歷史記錄
            all_history = self._load_history_from_file(self.history_path)
            successful_history = self._load_history_from_file(self.successful_history_path)
            
            # 準備當前 episode 的資料
            current_episode_data = {
                'episode': self.episode_count + 1,
                'pigeon_y': pigeon_pos[1] if self.current_shot_data else None,
                'bow_angle': bow_angle,
                'adjustment': self.height_adjustment,
                'success': game_state == "archer win",
                'game_state': game_state
            }
            
            if game_state == "archer win":
                # 成功！記錄到成功歷史
                if self.current_shot_data:
                    successful_data = {
                        'episode': self.episode_count + 1,
                        'adjustment': self.height_adjustment,
                        'pigeon_y': self.current_shot_data['pigeon_y'],
                        'predicted_movement': self.current_shot_data['predicted_movement'],
                        'angle': self.current_shot_data['angle'],
                        'success': True
                    }
                    successful_history.append(successful_data)
                    
                    # 保持最近100次成功的歷史
                    if len(successful_history) > 100:
                        successful_history = successful_history[-100:]
                    
                    # 儲存成功歷史
                    self._save_history_to_file(self.successful_history_path, successful_history)
            else:
                # 失敗，需要調整策略
                if len(successful_history) > 0:
                    # 從成功案例中學習
                    successful_adjustments = [h['adjustment'] for h in successful_history]
                    if len(successful_adjustments) > 0:
                        # 向成功案例的平均值靠攏
                        avg_success = sum(successful_adjustments) / len(successful_adjustments)
                        self.height_adjustment += (avg_success - self.height_adjustment) * self.learning_rate
                    else:
                        # 沒有成功案例，進行探索
                        self.height_adjustment += random.uniform(-8, 8)
                else:
                    # 初期探索階段
                    self.height_adjustment += random.uniform(-20, 20)
            
            # 將當前 episode 加入完整歷史
            all_history.append(current_episode_data)
            
            # 保持最近10次的完整歷史
            if len(all_history) > 10:
                all_history = all_history[-10:]
            
            # 儲存最近10筆歷史
            self._save_history_to_file(self.history_path, all_history)
            
            self.current_shot_data = None
            self.episode_count += 1
            
            # 每10個episode輸出學習進度
            if train and self.episode_count % 10 == 0:
                # 從檔案讀取最近的記錄來計算成功率
                recent_history = self._load_history_from_file(self.history_path)
                if len(recent_history) > 0:
                    success_count = len([h for h in recent_history if h['success']])
                    success_rate = success_count / len(recent_history) * 100
                    print(f"Episode {self.episode_count}: Archer Success Rate (last {len(recent_history)}): {success_rate:.1f}%, Height Adjustment = {self.height_adjustment:.2f}")
            
        return {
            "shoot": self.shoot,
            "move_angle": self.move_angle
        }
        #<- Your code here

def run(episodes=1, render=True, archer_train=False, pigeon_train=False, pigeon_mode="random_agent"):
    game = Game(render=render)
    archerAgent = ArcherAgent(train=archer_train)  # 傳遞 train 參數
    pigeonAgent = PigeonAgent(agent_mode=pigeon_mode)
    
    # 統計勝負次數
    archer_wins = 0
    pigeon_wins = 0
    
    for episode in range(episodes):
        game.reset()
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
            pigeonAgent.agent(result, pigeon_train)
            archerAgent.agent(result, archer_train)
            if(result["env"]["game_state"] != "continue"):
                # 統計勝負
                if result["env"]["game_state"] == "archer win":
                    archer_wins += 1
                elif result["env"]["game_state"] == "pigeon win":
                    pigeon_wins += 1
                break
            # print(result)
    
    # 訓練結束後輸出最終統計
    if archer_train:
        successful_history = archerAgent._load_history_from_file(archerAgent.successful_history_path)
        if len(successful_history) > 0:
            print(f"\n=== Archer Training Complete ===")
            print(f"Total Episodes: {archerAgent.episode_count}")
            print(f"Total Successful Shots Recorded: {len(successful_history)}")
            print(f"Average Height Adjustment: {sum([h['adjustment'] for h in successful_history]) / len(successful_history):.2f}")
    
    if pigeon_train and len(pigeonAgent.survival_strategies) > 0:
        final_success_rate = len([s for s in pigeonAgent.survival_strategies if s['success']]) / len(pigeonAgent.survival_strategies) * 100
        print(f"\n=== Pigeon Training Complete ===")
        print(f"Total Episodes: {pigeonAgent.episode_count}")
        print(f"Final Pigeon Success Rate (last 50): {final_success_rate:.1f}%")
        print(f"Final Safe Y Range: [{pigeonAgent.safe_y_min:.1f}, {pigeonAgent.safe_y_max:.1f}]")
    
    # 測試階段統計
    if not archer_train and not pigeon_train:
        print(f"\n=== Test Results ===")
        print(f"Total Episodes: {episodes}")
        print(f"Archer Wins: {archer_wins} ({archer_wins/episodes*100:.1f}%)")
        print(f"Pigeon Wins: {pigeon_wins} ({pigeon_wins/episodes*100:.1f}%)")
        print(f"Win Rate - Archer: {archer_wins}/{episodes}, Pigeon: {pigeon_wins}/{episodes}")
    
    game.close()



print("開始訓練")

# 階段 1: 訓練 Archer 對抗 Random Agent 的 Pigeon
# print("\n【階段 1】訓練 Archer 對抗隨機移動的 Pigeon...")
# print("-" * 60)
# run(episodes=1000, render=False, archer_train=True, pigeon_train=False, pigeon_mode="random_agent")

# 階段 2: 訓練 Pigeon (learnt_agent) 對抗已訓練好的 Archer
print("\n【階段 2】訓練 Pigeon 對抗已訓練好的 Archer...")
print("-" * 60)
run(episodes=1000, render=False, archer_train=False, pigeon_train=True, pigeon_mode="learnt_agent")

#先鴿子再弓箭手好像比較好 大概55?
print("\n【階段 2.5】訓練 Archer 對抗隨機移動的 Pigeon...")
print("-" * 60)
run(episodes=1000, render=False, archer_train=True, pigeon_train=False, pigeon_mode="random_agent")

# 階段 3: 測試階段，觀察訓練成果
print("\n【階段 3】測試訓練成果...")
print("-" * 60)
run(episodes=10, render=True, archer_train=False, pigeon_train=False, pigeon_mode="learnt_agent")

print("訓練流程完成！")
