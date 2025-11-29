import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle


def print_success_rate(rewards_per_episode):
    """Calculate and print the success rate of the agent."""
    total_episodes = len(rewards_per_episode)
    success_count = int(np.sum(rewards_per_episode))
    success_rate = (success_count / total_episodes) * 100.0
    print(f"Success Rate: {success_rate:.2f}% ({success_count} / {total_episodes} episodes)")


def run(episodes,
        is_training=True,
        render=False,
        slippery=True,
        epsilon_eval=0.0):

    env = gym.make(
        'FrozenLake-v1',
        map_name="8x8",
        is_slippery=slippery,
        render_mode='ansi' if render else None
    )

    n_states = env.observation_space.n
    n_actions = env.action_space.n

    if is_training:
        # 樂觀初始化 Q-table：全部先給一個正值，鼓勵探索
        q = np.ones((n_states, n_actions)) * 5.0
    else:
        with open('frozen_lake8x8.pkl', 'rb') as f:
            q = pickle.load(f)

    # ===== Hyperparameters =====
    # 學習率：從 0.3 慢慢降到 0.05
    alpha = 0.3
    alpha_min = 0.05
    alpha_decay = 0.9997   # 每個 episode 乘一次

    gamma = 0.99           # discount factor

    # 訓練時的 epsilon：1.0 -> 0.1
    epsilon = 1.0
    epsilon_min = 0.1
    epsilon_decay = 0.9993

    rng = np.random.default_rng()

    rewards_per_episode = np.zeros(episodes)

    for ep in range(episodes):
        state, _ = env.reset()
        terminated = False
        truncated = False

        while not terminated and not truncated:

            if is_training:
                # 訓練：epsilon-greedy
                if rng.random() < epsilon:
                    action = env.action_space.sample()
                else:
                    action = int(np.argmax(q[state, :]))
            else:
                # 評估：可選擇保留一點探索（epsilon_eval）
                if rng.random() < epsilon_eval:
                    action = env.action_space.sample()
                else:
                    action = int(np.argmax(q[state, :]))

            new_state, env_reward, terminated, truncated, _ = env.step(action)

            if is_training:
                # ---- reward shaping ----
                if terminated and env_reward == 1:
                    reward = 5.0        # 成功到終點
                elif terminated and env_reward == 0:
                    reward = -5.0       # 掉進洞
                else:
                    reward = -0.01      # 一般走一步

                best_next_q = np.max(q[new_state, :])
                td_target = reward + gamma * best_next_q
                td_error = td_target - q[state, action]
                q[state, action] += alpha * td_error

            state = new_state

        # 用環境的 reward==1 當「成功一次」
        if env_reward == 1:
            rewards_per_episode[ep] = 1

        # 訓練：衰減 alpha / epsilon
        if is_training:
            alpha = max(alpha_min, alpha * alpha_decay)
            epsilon = max(epsilon_min, epsilon * epsilon_decay)

    env.close()

    # ===== moving average 圖 =====
    window = 100
    moving_avg = np.zeros(episodes)
    for t in range(episodes):
        moving_avg[t] = np.mean(rewards_per_episode[max(0, t - window):t + 1])

    plt.clf()
    plt.plot(moving_avg)
    plt.xlabel("Episode")
    plt.ylabel(f"Moving Avg Reward (window={window})")
    title_mode = "Training" if is_training else "Evaluation"
    slip_str = "slippery" if slippery else "non-slippery"
    plt.title(f"FrozenLake 8x8 Q-learning - {title_mode} ({slip_str})")

    if is_training:
        plt.savefig('frozen_lake8x8_train.png')
    else:
        plt.savefig('frozen_lake8x8_eval.png')

    # 測試時印成功率
    if not is_training:
        print_success_rate(rewards_per_episode)

    # 訓練時把 Q-table 存檔
    if is_training:
        with open("frozen_lake8x8.pkl", "wb") as f:
            pickle.dump(q, f)


if __name__ == '__main__':
    run(15000, is_training=True,  render=False, slippery=True)
    run(1000,  is_training=False, render=False, slippery=True, epsilon_eval=0.0)

