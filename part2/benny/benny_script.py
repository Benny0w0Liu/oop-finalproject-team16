import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle


def print_success_rate(rewards_per_episode):
    """Calculate and print the success rate of the agent."""
    total_episodes = len(rewards_per_episode)
    success_count = np.sum(rewards_per_episode)
    success_rate = (success_count / total_episodes) * 100
    print(f"Success Rate: {success_rate:.2f}% ({int(success_count)} / {total_episodes} episodes)")
    return success_rate

def run(episodes, is_training=True, render=False):

    env = gym.make('FrozenLake-v1', map_name="8x8", is_slippery=True, render_mode='human' if render else None)

    if(is_training):
        q = np.zeros((env.observation_space.n, env.action_space.n)) # init a 64 x 4 array
    else:
        f = open('frozen_lake8x8.pkl', 'rb')
        q = pickle.load(f)
        f.close()

    learning_rate_a = 0.7 # alpha or learning rate
    discount_factor_g = 0.95 # gamma or discount rate. Near 0: more weight/reward placed on immediate state. Near 1: more on future state.
    epsilon = 1         # 1 = 100% random actions
    min_exploration_rate = 0.01       # minimum exploration rate
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
                q[state,action] = q[state,action] + learning_rate_a * (
                    reward + discount_factor_g * np.max(q[new_state,:]) - q[state,action]
                )

            state = new_state

        # Linear decay over 80% of episodes
        epsilon = max(min_exploration_rate, 1.0 - (i / (episodes * 0.8)))

        if (i + 1) % 1000 == 0 and is_training:
            print(f"Episode {i + 1}: Epsilon = {epsilon:.4f}")

        if reward == 1:
            rewards_per_episode[i] = 1

    env.close()
    
    # Moving average calculation
    window_size = 100
    sum_rewards = np.zeros(episodes)
    for t in range(episodes):
        start_idx = max(0, t - window_size + 1)
        sum_rewards[t] = np.sum(rewards_per_episode[start_idx:(t+1)]) / (t - start_idx + 1)
    
    if is_training:
        print_success_rate(rewards_per_episode)
        
        plt.figure(figsize=(10, 6))
        plt.plot(sum_rewards, label='Success Rate (Moving Avg)')
        plt.title('Frozen Lake 8x8 Learning Curve')
        plt.xlabel('Episodes')
        plt.ylabel('Success Rate')
        plt.legend()
        plt.grid(True)
        plt.savefig('frozen_lake8x8.png')
        print("Training finished. Model saved to frozen_lake8x8.pkl")
        print("Learning curve saved to frozen_lake8x8.png")
    
    if not is_training:
        print_success_rate(rewards_per_episode)

    if is_training:
        f = open("frozen_lake8x8.pkl","wb")
        pickle.dump(q, f)
        f.close()

if __name__ == '__main__':
    # Train
    print("Training...")
    run(25000, is_training=True, render=False)
    
    # Evaluate
    print("Evaluating...")
    run(1000, is_training=False, render=False)
