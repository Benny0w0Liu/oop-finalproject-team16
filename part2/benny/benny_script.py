import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle

def run(episodes, is_training=True, render=False):

    env = gym.make('FrozenLake-v1', map_name="8x8", is_slippery=True, render_mode='human' if render else None)

    if(is_training):
        q = np.zeros((env.observation_space.n, env.action_space.n)) # init a 64 x 4 array
    else:
        f = open('frozen_lake8x8.pkl', 'rb')
        q = pickle.load(f)
        f.close()

    # Hyperparameters
    learning_rate_a = 0.9 # High initial alpha
    min_learning_rate_a = 0.01
    learning_rate_decay = 0.9993 # Decay factor
    
    discount_factor_g = 0.999 # Gamma
    
    epsilon = 1         # 1 = 100% random actions
    
    # Decay epsilon over the first ~12000 episodes
    decay_end_episode = 12000
    epsilon_decay_rate = epsilon / decay_end_episode
    
    rng = np.random.default_rng()   # random number generator

    rewards_per_episode = np.zeros(episodes)

    for i in range(episodes):
        state = env.reset()[0]  # states: 0 to 63, 0=top left corner,63=bottom right corner
        terminated = False      # True when fall in hole or reached goal
        truncated = False       # True when actions > 200

        while(not terminated and not truncated):
            if is_training and rng.random() < epsilon:
                action = env.action_space.sample() # actions: 0=left,1=down,2=right,3=up
            else:
                action = np.argmax(q[state,:])

            new_state,reward,terminated,truncated,_ = env.step(action)

            if is_training:
                # Reward Shaping
                custom_reward = reward
                if terminated and reward == 0:
                    custom_reward = -0.5 # Penalty for falling in hole
                elif not terminated:
                    custom_reward = -0.001 # Small penalty for each step to encourage speed
                
                # Q-learning update with custom_reward
                q[state,action] = q[state,action] + learning_rate_a * (
                    custom_reward + discount_factor_g * np.max(q[new_state,:]) - q[state,action]
                )

            state = new_state

        # Decay epsilon
        if is_training:
            epsilon = max(epsilon - epsilon_decay_rate, 0)
            # Decay learning rate
            learning_rate_a = max(learning_rate_a * learning_rate_decay, min_learning_rate_a)

        if reward == 1:
            rewards_per_episode[i] = 1
        
        # Optional: Print progress every 1000 episodes
        if is_training and (i + 1) % 1000 == 0:
            print(f"Episode {i+1}: Epsilon {epsilon:.4f}, Alpha {learning_rate_a:.4f}, Last 100 avg reward: {np.mean(rewards_per_episode[max(0, i-99):i+1]):.2f}")

    env.close()

    sum_rewards = np.zeros(episodes)
    for t in range(episodes):
        sum_rewards[t] = np.sum(rewards_per_episode[max(0, t-100):(t+1)])
    plt.plot(sum_rewards)
    plt.savefig('frozen_lake8x8.png')
    
    if is_training:
        f = open("frozen_lake8x8.pkl","wb")
        pickle.dump(q, f)
        f.close()
        print("Training finished and Q-table saved.")
    else:
        # Evaluation results
        total_episodes = len(rewards_per_episode)
        success_count = np.sum(rewards_per_episode)
        success_rate = (success_count / total_episodes) * 100
        print(f"Evaluation Success Rate: {success_rate:.2f}% ({int(success_count)} / {total_episodes} episodes)")
        return success_rate

if __name__ == '__main__':
    # 1. Train
    print("Starting Training...")
    run(15000, is_training=True, render=False)

    # 2. Evaluate
    print("\nStarting Evaluation...")
    run(1000, is_training=False, render=False)
