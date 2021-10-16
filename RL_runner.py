from agent import Agent
import numpy as np
from constants import *

if __name__ == '__main__':
    agent = Agent(train=True, targetUpdateWait=TARGET_UPDATE_WAIT, gamma=GAMMA, epsilon=EPSILON, epsilonDecay= EPSILON_DECAY, epsilonMin=EPSILON_MIN, maxScore = MAX_SCORE)

    for i in range(MIN_EXPERIENCES):
        action = np.random.choice(NUM_ACTIONS)
        frame, reward, done= agent.env.update(action)
        agent.replayBuffer.add_experience(frame, action, reward, done)

    print("now training")
    for i in range(NUM_EPISODES):
        agent.play_one_episode()
        print(i+1)

        if i % MODEL_SAVE_RATE == 0:
            agent.save("model2_ep"+str(i+1)+".h5", "model2_ep"+str(i+1)+"_scores.csv")

    if agent.train == True:
        agent.save("model2.h5", "model2_scores.csv")

    agent.plot()