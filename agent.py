from replay_buffer import ReplayBuffer
from constants import *
from tensorflow.keras import Input
from tensorflow.keras.layers import Conv2D, Flatten, Dense
from tensorflow.keras.models import Model, clone_model, load_model, save_model
import matplotlib.pyplot as plt

from game import RLEnv
import numpy as np
import tensorflow as tf
import csv

class Agent():
    def __init__(self, train:bool, targetUpdateWait, gamma, epsilon, epsilonDecay, epsilonMin, maxScore):
        self.env = RLEnv(FPS=2000)
        
        i = Input(shape = (HISTORY_LENGTH, SCREEN_SIZE[1], SCREEN_SIZE[0]))
        x = Conv2D(32, (8,8), strides=4, padding='same', activation='relu')(i)
        x = Conv2D(64, (4,4), strides=2, padding='same', activation='relu')(x)
        x = Conv2D(64, (3,3), strides=1, padding='same', activation='relu')(x)

        x = Flatten()(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(512, activation='relu')(x)
        x = Dense(NUM_ACTIONS)(x)

        self.model = Model(i, x)
        self.model.compile(loss= 'mse', optimizer='adam')
        self.targetModel = clone_model(self.model)
        self.targetModel.set_weights(self.model.get_weights())

        self.train = train
        self.currentFrame = 0
        self.targetUpdateWait = targetUpdateWait
        
        self.replayBuffer = ReplayBuffer(frameHeight=SCREEN_SIZE[1], frameWidth=SCREEN_SIZE[0], 
                            maxSize=MAX_EXPERIENCES, historyLength=HISTORY_LENGTH, batchSize=32)
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilonDecay = epsilonDecay
        self.epsilonMin = epsilonMin
        self.maxScore = maxScore

        self.scores = []

    def get_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(NUM_ACTIONS)
        else:
            QVals = self.targetModel.predict(tf.expand_dims(state, axis=0))
            return np.argmax(QVals[0])

    def trainReplay(self):

        if self.replayBuffer.currentSize < self.replayBuffer.batchSize:
            return
        else:
            states, actions, rewards, nextStates, dones = self.replayBuffer.sample_batch()

            nextQs = self.targetModel.predict(nextStates)
            nextQ = np.amax(nextQs, axis=1)
            targets = rewards + np.invert(dones).astype(np.float32) * self.gamma * nextQ
            
            targets_full = self.targetModel.predict(states)
            targets_full[np.arange(self.replayBuffer.batchSize), actions] = targets

            if self.train:
                self.model.train_on_batch(states, targets)

            if self.epsilon > self.epsilonMin:
                self.epsilon *= self.epsilonDecay


    def update_state(self, state, frame):
        return np.append(state[1:,:,:], np.expand_dims(frame, 0), axis=0)

    def play_one_episode(self):
        frame = self.env.restart()
        state = np.stack([frame] * 4, axis=0)
        done = False
        score = 0

        while not done:

            action = self.get_action(state)
            nextFrame, reward, done = self.env.update(action)
            nextState = self.update_state(state, nextFrame)

            if reward == 1:
                score += 1
                if score > self.maxScore - 1:
                    done = True

            if self.currentFrame % self.targetUpdateWait == 0:
                self.targetModel.set_weights(self.model.get_weights())
                print("target model updated")

            if self.train:
                self.replayBuffer.add_experience(nextFrame, action, reward, done)
                if self.currentFrame % 2 == 0:
                    self.trainReplay()

            state = nextState
            self.currentFrame += 1
        
        self.scores.append(score)

    def load(self, modelDir):
        self.model = load_model(modelDir)

    def save(self, modelDir, scoreDir):
        self.model.save(modelDir)
        with open(scoreDir, 'w') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(self.scores)

    def plot(self):
        episodes = [i for i in range(len(self.scores))]
        plt.plot(episodes, self.scores)
        plt.title("scores per episode")
        plt.xlabel('episodes')
        plt.ylabel('score')
        plt.show()

        



        
