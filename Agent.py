
#
# This Agent demonstrates use of a Keras centred Q-network estimating the Q[S,A] Function from a few basic Features
#
# This DQN Agent Software is Based upon the following  Jaromir Janisch  source:
# https://jaromiru.com/2016/10/03/lets-make-a-dqn-implementation/
# as employed against OpenAI  Gym Cart Pole examples
#  requires keras [and hence Tensorflow or Theono backend]
# ==============================================================================

# DQN pong Agent
# Model-Free
# keras 기반
# 
'''
score: 합산한 타일 수의 총합 ex) 2, 2 합쳐 4를 만들면 score += 4
죽을 때까지 score 최대로 하는 것이 목표
'''

import random, numpy, math, pickle, keras
#
import keras.callbacks
from keras.models import load_model
from keras.layers import *
from keras.optimizers import *
import numpy as np
import Agent_constants as ac

#%% ==========================================================================
'''
<DQN Agent와 Environment 상호작용>

1. 상태에 따른 행동 선택
2. 선택한 행동으로 환경에서 한 타임스텝을 진행
3. 환경으로부터 다음 상태와 보상을 받음
4. 샘플(s, a, r, s')을 리플레이 메모리에 저장
5. 리플레이 메모리에서 무작위 추출한 샘플로 학습
6. 에피소드마다 타깃 모델 업데이트
'''

#  Keras based Neural net Based Brain Class
class Brain:
        def __init__(self, NbrStates, NbrActions):
                self.NbrStates = NbrStates
                self.NbrActions = NbrActions

                self.model = self._createModel()
                self.tbCallBack = keras.callbacks.TensorBoard(log_dir='./logs', histogram_freq=0, batch_size=ac.P_BATCH_SIZE, write_graph=True, write_grads=False, write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None, embeddings_data=None)
                # TensorBoard 사용 코드

        def _createModel(self):
                model = keras.models.Sequential() #계층을 선형으로 쌓은 것

                # Simple Model with Three Hidden Layers and a Linear Output Layer. The Input layer is simply the State input.
                # model.add(Conv1D(filters = 32, kernel_size = 3, strides = 1))
                # 모델 계츨 쌓음
                model.add(Dense(units=32, activation='relu', input_dim=self.NbrStates))
                model.add(Dense(units=32, activation='relu')) #Hidden layer
                # model.add(Dense(units=32, activation='relu'))
                model.add(Dense(units=self.NbrActions, activation='linear'))                            # Linear Output Layer as we are estimating a Function Q[S,A]
                model.summary()
                '''
                model.add(Dense(units=64, activation='relu', input_dim=self.NbrStates, kernel_initializer='he_uniform'))
                1. 입력이 상태, 출력이 큐함수이므로 input_dim에 상태의 크기가 들어가고 마지막 model.add(Dense())를 더할 때 크기를 행동의 크기로 설정
                2. kernel_initalizer: 인공신경망의 각 가중치의 초깃값을 어떻게 설정하는지 중요
                3. model.summary(): 케라스에서는 모델의 정보를 정리해 실행 창에 보여주는 함수 제공
                '''
                # 학습 과정 구성
                model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=ac.LEARNING_RATE))     # use adam as an alternative optimsiuer as per comment
                #loss function: mse
                # optimizer: 최적화기
                return model
        def train(self, x, y, epoch=1, verbose=0):
                self.model.fit(x, y, batch_size=ac.BATCH_SIZE, epochs=epoch, verbose=verbose, initial_epoch = epoch-1)#, callbacks = [self.tbCallBack],validation_split = 0.2)

        # epoch: 주어진 배치를 학습에 몇 번 사용할 것인가를 나타내는 변수, 강화학습에서는 1로 설정

        # fit(): 학습시키는 함수
        # x: numpy array of training data or list of arrays
        # y: numpy array of target(label) data or list of arrays
        def predict(self, s): #예측
                return self.model.predict(s)

        def predictOne(self, s):
                return self.predict(s.reshape(1, self.NbrStates)).flatten()

# =======================================================================================
# A simple Experience Replay memory
#  DQN Reinforcement learning performs best by taking a batch of training samples across a wide set of [S,A,R, S'] expereiences
#

# DQN에서 배치 데이터를 만들어 학습
class ExpReplay:   # stored as ( s, a, r, s_ )
        samples = []

        def __init__(self, capacity):
                self.capacity = capacity

        def add(self, sample):
                self.samples.append(sample)

                if len(self.samples) > self.capacity:
                        self.samples.pop(0)

        def sample(self, n):
                n = min(n, len(self.samples))
                return random.sample(self.samples, n)

#self.numpy.array([ batchitem[0][2] for batchitem in self.ExpReplay.samples[-128:] ])
# ============================================================================================
class Agent:
        def __init__(self, NbrStates, NbrActions):
                self.NbrStates = NbrStates
                self.NbrActions = NbrActions
                self.ExpCount = 0
                self.brain = Brain(NbrStates, NbrActions)
                self.ExpReplay = ExpReplay(ac.ExpReplay_CAPACITY)
                self.steps = 0
                self.epsilon = ac.MAX_EPSILON
        # ============================================
        # 학습 모델 로드
        def Load(self, num):
                self.brain.model = keras.models.load_model("./model_power/2048_Model{}.h5".format(num))
                with open("./model_power/2048_Model{}_steps.txt".format(num),"r") as f:
                        self.steps = int(f.read())
                        print(self.steps)


                with open("./model/2048_Model{}_exp.txt".format(num),"rb") as f:
                        self.ExpReplay.samples = pickle.load(f)

                        
                if self.steps < ac.OBSERVEPERIOD:
                    self.epsilon = 1.0
                else:
                    self.epsilon = ac.MIN_EPSILON + (ac.MAX_EPSILON - ac.MIN_EPSILON) * math.exp(-ac.LAMBDA * (self.steps-ac.OBSERVEPERIOD))
        # ============================================
        # 학습 모델 저장
        def Save(self, num):
                self.brain.model.save("./model_power/2048_Model{}.h5".format(num))
                with open("./model_power/2048_Model{}_steps.txt".format(num),"w") as f:
                        f.write('{}'.format(self.steps))
                        #print("Write!")
                        #print(self.steps)
                        
                with open("./model_power/2048_Model{}_exp.txt".format(num),"wb") as f:
                        pickle.dump(self.ExpReplay.samples, f)
                '''
                테스트용 코드: S, A, R, S' 잘 저장되고 있는지?
                arr = np.array(self.ExpReplay.samples)
                print(arr.shape)
                print(arr)
                '''
        # ============================================
        # Return the Best Action  from a Q[S,A] search.  Depending upon an Epslion Explore/ Exploitaiton decay ratio
        

        # epsilon만큼의 확률로 random한 action을 취함
        # 또는 아직 observeperiod일 때도 random한 action을 취함
        def Act(self, s):
                if (random.random() < self.epsilon or self.steps < ac.OBSERVEPERIOD):
                        return random.randint(0, self.NbrActions-1)                                             # Explore
                else:
                        return numpy.argmax(self.brain.predictOne(s))                                   # Exploit Brain best Prediction
        '''
        입실론-탐욕 정책
        에이전트가 행동을 선택할 때 사용하는 입실론은 처음에는 1을 가짐 -> 무조건 무작위로 행동 선택
        학습이 진행됨에 따라 무작위가 아니라 모델의 예측에 따라 행동을 선택해야 함 -> CaptureSample() 함수에 의해 감소됨
        지속적인 탐험을 위해 최솟값 설정
        '''
        # ============================================
        # 시간에 따라 epsilon 값이 감소 (lambda 값으로 감소 속도 결정)
        def CaptureSample(self, sample):  # in (s, a, r, s_) format
                #print("여기")
                #print(sample)
                self.ExpReplay.add(sample)

                # slowly decrease Epsilon based on our experience
                self.steps += 1
                if(self.steps>ac.OBSERVEPERIOD):
                        self.epsilon = ac.MIN_EPSILON + (ac.MAX_EPSILON - ac.MIN_EPSILON) * math.exp(-ac.LAMBDA * (self.steps-ac.OBSERVEPERIOD))

        # ============================================
        # Perform an Agent Training Cycle Update by processing a set of samples from the Experience Replay memory
        def Process(self):
                self.ExpCount+=1
                if(self.ExpCount%ac.EXP_PROCESS_RATIO!=0):
                        return 0
               
        
                batch = self.ExpReplay.sample(ac.BATCH_SIZE)
                batchLen = len(batch)

                no_state = numpy.zeros(self.NbrStates)
                # print(batch)
                states = numpy.array([ batchitem[0].flatten() for batchitem in batch ])

                # 여기서 flatten하지 말고 input하는 값 즉 NextStates, GameStates? 자체를 flatten하도록 바꿀 예정


                #print(states.shape)
                b = numpy.array(batch)
                #print(b.shape)
                states_ = numpy.array([ (no_state if batchitem[3] is None else batchitem[3]) for batchitem in batch ])

                predictedQ = self.brain.predict(states)                                         # Predict from keras Brain the current state Q Value
                predictedNextQ = self.brain.predict(states_)                            # Predict from keras Brain the next state Q Value

                x = numpy.zeros((batchLen, self.NbrStates))
                y = numpy.zeros((batchLen, self.NbrActions))

                #  Now compile the Mini Batch of [States, TargetQ] to Train an Target estimator of Q[S,A]
                for i in range(batchLen):
                        batchitem = batch[i]
                        state = batchitem[0]; a = batchitem[1]; reward = batchitem[2]; nextstate = batchitem[3]

                        targetQ = predictedQ[i]
                        if nextstate is None:
                                targetQ[a] = reward                                             # An End state Q[S,A]assumption
                        else:
                                targetQ[a] = reward + ac.GAMMA * numpy.amax(predictedNextQ[i])     # The core Q[S,A] Update recursive formula
                                # Q-value (action value function) 아마도?

                        x[i] = state
                        y[i] = targetQ

                self.brain.train(x, y, self.ExpCount)                                          #  Call keras DQN to Train against the Mini Batch set
# =======================================================================
