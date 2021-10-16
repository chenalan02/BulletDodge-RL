import numpy as np
from game import Map

class ReplayBuffer():
    def __init__(self, frameHeight, frameWidth, maxSize, historyLength, batchSize):
        self.historyLength = historyLength
        self.current = 0
        self.currentSize = 0
        self.maxSize = maxSize
        self.batchSize = batchSize
        self.frameHeight = frameHeight
        self.frameWidth = frameWidth

        self.frames = np.zeros((maxSize, self.frameHeight, self.frameWidth), dtype=np.uint8)
        self.actions = np.zeros(maxSize, dtype=np.int32)
        self.rewards = np.zeros(maxSize, dtype=np.int32)
        self.done = np.zeros(maxSize, dtype=np.bool)

        self.states = np.empty((self.batchSize, self.historyLength, 
                            self.frameHeight, self.frameWidth), dtype=np.uint8)
        self.new_states = np.empty((self.batchSize, self.historyLength, 
                                self.frameHeight, self.frameWidth), dtype=np.uint8)
        self.indices = np.empty(self.batchSize, dtype=np.int32)

    def add_experience(self, frame, action, reward, done):
        self.frames[self.current] = frame
        self.actions[self.current] = action
        self.rewards[self.current] = reward
        self.done[self.current] = done

        self.current = (self.current+1) % self.maxSize
        self.currentSize = min(self.currentSize+1, self.maxSize)

    def get_random_index(self):
        while True:
            idx = np.random.randint(self.historyLength, self.currentSize - 1)
            if idx < self.historyLength + 1:
                continue
            if idx >= self.current and idx - self.historyLength <= self.current:
                continue
            if self.done[idx - self.historyLength:idx].any():
                continue
            break
        return idx

    def sample_batch(self):
        if self.currentSize < self.historyLength:
            raise ValueError('Not enough memories to get a minibatch')

        for i in range(self.batchSize):
            idx = self.get_random_index()
            self.indices[i] = idx

        for i, idx in enumerate(self.indices):
            self.states[i] = self.get_state(idx - 1)
            self.new_states[i] = self.get_state(idx)

        return self.states, \
        self.actions[self.indices], \
        self.rewards[self.indices], \
        self.new_states, \
        self.done[self.indices]
        
    def get_state(self, index):
        if index > self.historyLength - 1:
            return self.frames[index - self.historyLength+1:index+1, ...]
        