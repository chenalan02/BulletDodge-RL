from agent import Agent
import numpy as np
from constants import *

if __name__ == '__main__':
    agent = Agent(train=True, targetUpdateWait=TARGET_UPDATE_WAIT, gamma=GAMMA, epsilon=EPSILON, epsilonDecayConst= EPSILON_DECAY_CONST, epsilonMin=EPSILON_MIN, maxScore = MAX_SCORE, replayRate = REPLAY_RATE)

    for i in range(MIN_EXPERIENCES):
        action = np.random.choice(NUM_ACTIONS)
        frame, reward, done= agent.env.update(action)
        agent.replayBuffer.add_experience(frame, action, reward, done)

    print("now training")
    for i in range(NUM_EPISODES):
        agent.play_one_episode()
        print(i+1)

        if i % MODEL_SAVE_RATE == 0:
            agent.save("model4_ep"+str(i+1)+".h5", "model4_ep"+str(i+1)+"_scores.csv")

    if agent.train == True:
        agent.save("model4.h5", "model4_scores.csv")

    agent.plot()