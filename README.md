# Final Project of 114-1 CSE3002 Object-Oriented Programming
group member: 
* [B123245013 劉邦均](https://github.com/Benny0w0Liu)
* [B123045009 陳予涵](https://github.com/Johnnnnnnnnnnnnnnnnnnn)
* [B123040027 林昱辰](https://github.com/ufirstfloor)


# Part 2
## Project overview
> **Goal**: Revise the sample code to achieve a consistent success rate > 0.70 on without
changing `num_episodes`and `max_steps_per_episode`

For this part, In short, our approach combines:
* Tabular Q-learning
* Optimistic initialization
* Epsilon-greedy exploration with decay
* Learning-rate scheduling
* Reward shaping

This is our implementation details:

### Pseudocode

```
Initialize environment (FrozenLake 8x8, slippery or non-slippery)

Initialize Q-table Q[s, a] with optimistic values (e.g., 5.0)

Set hyperparameters:
    alpha <- initial learning rate
    alpha_min <- minimum learning rate
    alpha_decay <- learning rate decay factor
    gamma <- discount factor
    epsilon <- initial exploration rate
    epsilon_min <- minimum exploration rate
    epsilon_decay <- exploration decay factor

For episode = 1 to N_episodes:

    Reset environment
    state <- initial state
    terminated <- false
    truncated <- false

    While not terminated and not truncated:

        With probability epsilon:
            action <- random action
        Else:
            action <- argmax_a Q[state, a]

        Execute action
        new_state, env_reward, terminated, truncated <- environment step

        // Reward shaping
        If terminated and env_reward == 1:
            reward <- +5.0          // reached goal
        Else if terminated and env_reward == 0:
            reward <- -5.0          // fell into hole
        Else:
            reward <- -0.01         // step penalty

        // Q-learning update
        best_next_q <- max_a Q[new_state, a]
        td_target <- reward + gamma × best_next_q
        td_error <- td_target - Q[state, action]
        Q[state, action] <- Q[state, action] + alpha × td_error

        state <- new_state

    If env_reward == 1:
        mark episode as success

    // Decay parameters
    alpha <- max(alpha_min, alpha × alpha_decay)
    epsilon <- max(epsilon_min, epsilon × epsilon_decay)

Save Q-table to disk
```
### Typical changes from the original

1. *Optimistic Initialization*

    The Q-table is initialized with a **positive value (5.0)** for all state–action pairs.

    **Purpose:**

    * Encourages exploration early in training.
    * Actions that have not been tried appear attractive, reducing premature convergence to suboptimal policies.

    This is especially important in FrozenLake, where rewards are sparse.


2. *Epsilon-Greedy Exploration with Decay*

    The agent follows an **epsilon-greedy policy**:

    * With probability `epsilon`, it explores (random action).
    * Otherwise, it exploits the best-known action.

    **Decay strategy:**

    * `epsilon` starts at 1.0 (pure exploration).
    * Gradually decays to 0.1.
    * Ensures sufficient exploration early and stable exploitation later.

    This balances the exploration–exploitation trade-off over long training (15,000 episodes).

3. *Learning Rate Decay*

    The learning rate `alpha` also decays over time:

    * Starts relatively high (0.3) for fast early learning.
    * Gradually decreases to 0.05 for stability.

    **Rationale:**

    * Large updates early help discover good policies.
    * Smaller updates later prevent oscillations and overfitting to noise.

4. *Reward Shaping*

    The original FrozenLake reward is sparse (only +1 at the goal). You introduce **reward shaping**:

    | Situation      | Reward |
    | -------------- | ------ |
    | Reach goal     | +5.0   |
    | Fall into hole | -5.0   |
    | Normal step    | -0.01  |

    **Benefits:**

    * Strong signal differentiating success vs. failure.
    * Step penalty encourages shorter paths.
    * Improves convergence speed in large (8×8) maps.

    This shaping preserves the optimal policy while making learning more efficient.

5. *High Discount Factor*

    The discount factor ( $\gamma$ = 0.99 ) emphasizes long-term rewards.

    **Reasoning:**

    * The goal may be many steps away.
    * Encourages planning ahead rather than greedy local moves.
### Result
1. Terminal output:
    ```
    Success Rate: 63.10% (631 / 1000 episodes)
    ```
2. frozen_lake8x8_train.png
    ![frozen_lake8x8_train.png](./part2/john/frozen_lake8x8_train.png)
3. frozen_lake8x8_eval.png:
    ![frozen_lake8x8_eval.png](./part2/john/frozen_lake8x8_eval.png)
## How to run
```
cd part2\john
python john_version.py
```

## Dependencies

## Contribution list

# Part 3
## Project overview
> **Goal**: Revise the sample code to achieve a consistent success rate > 0.70 on without
changing `num_episodes`and `max_steps_per_episode`

For this part, we try to achieve the goal with two different strategy.

1. Adjust 
2. 

## How to run
## Dependencies
## Contribution list