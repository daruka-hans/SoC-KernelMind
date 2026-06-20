import numpy as np
import matplotlib.pyplot as plt

from env import ProbeEnv
from agent import ProbeAgent

def train(episodes=20000):
    env=ProbeEnv()
    agent=ProbeAgent()

    rewards=[]
    outcomes=[]

    for i in range(episodes):
        raw_state=env.reset()
        state=agent.discretize_state(raw_state)

        total_reward=0.0
        done=False
        success=0

        while not done:
            action=agent.choose_action(state)
            raw_next,reward,done=env.step(action)
            next_state=agent.discretize_state(raw_next)

            agent.learn(state,action,reward,next_state,done)

            state=next_state
            total_reward+=reward

            if done and env.h<=0 and env.v>=-3.0:
                success=1
            
        rewards.append(total_reward)
        outcomes.append(success)
        
        #print progress every 2000 episodes
        if(i+1)%2000==0:
            recent_reward=np.mean(rewards[-2000:])
            recent_outcome=np.mean(outcomes[-2000:])
            print(f"Episode {i+1:5d} | "
                  f"Avg Reward: {recent_reward:7.1f} | "
                  f"Success Rate: {recent_outcome*100:5.1f}% | "
                  f"Epsilon: {agent.epsilon:.3f}")
            
    return agent,rewards,outcomes

def plot_results(rewards,outcomes,window=500):
    fig,(ax1,ax2)=plt.subplots(2,1,figsize=(12,8))
    fig.suptitle("Project Hail Mary: Adrian Descent Training")

    def moving_avg(data,w):
        return np.convolve(data, np.ones(w)/w, mode='valid')

    episodes = range(len(moving_avg(rewards, window)))

    ax1.plot(episodes, moving_avg(rewards, window), color='cyan')
    ax1.set_title(f"Episode Reward (moving avg, window={window})")
    ax1.set_xlabel("Episode")
    ax1.set_ylabel("Total Reward")
    ax1.axhline(y=0, color='white', linestyle='--', alpha=0.3)
    ax1.grid(True, alpha=0.3)

    success_pct = [x * 100 for x in outcomes]
    ax2.plot(episodes, moving_avg(success_pct, window), color='lime')
    ax2.set_title(f"Landing Success Rate % (moving avg, window={window})")
    ax2.set_xlabel("Episode")
    ax2.set_ylabel("Success %")
    ax2.set_ylim(0, 100)
    ax2.axhline(y=50, color='white', linestyle='--', alpha=0.3)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("learning_curve.png", dpi=150)
    plt.show()
    print("Saved → learning_curve.png")


if __name__ == "__main__":
    agent,rewards,outcomes = train(episodes=20000)
    plot_results(rewards,outcomes)

    np.save("q_table.npy", agent.qtable)
    print("Q-table saved → q_table.npy")
