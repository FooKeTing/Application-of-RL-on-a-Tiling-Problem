from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import BaseCallback
import time
import os
from env_playerCode_v2 import *
#from env_playerCode import *

# user define value 
trainingTime = 3600 # in second
TOTAL_TIMESTEP = 100000
MAX_REPEATNUM = 10
# file name that stored each step taken by the players
stepFile = 'stepFile_2_4x4_Vertical.txt' 
# file name that stored the previous experience from a stopped training session
bufferFile = 'loseModel.zip' 

class EpisodeCountandWinStopCallback(BaseCallback):
    def __init__(self, trainingTime, verbose=0):
        super(EpisodeCountandWinStopCallback, self).__init__(verbose)
        # initialize the number of episode that the agent taken during training
        self.num_episodes = 0
        self.time_limit = trainingTime
        # initialize the number of repetition when the agent get win result
        self.repeatNum = 0

    def _on_training_start(self) -> None:
        # activate the timer when the training is started
        self.start_time = time.time()   
        return self.start_time
        
    def _on_step(self) -> bool:
        # when the agent trained over the maximum training time
        if self.start_time is not None and time.time() - self.start_time > self.time_limit:
            self._on_training_end()
            return False

        # convert the numpy array of the environment state that agent taken to list
        currentState = self.locals['obs_tensor'][0]
        self.currentState = currentState.tolist()
        nextState = self.locals['infos'][0]['next_state']
        self.nextState = nextState.tolist()
        
        # save the environment state taken by agent as dictionary
        InitialstateData = {
            'current_state' : self.currentState
            }
        finalStateData = {
            'final_state' : self.nextState
            }
        # save the environment state taken by agent for each step into a text file
        with open(stepFile,'a') as file:
            file.write(str(InitialstateData)+ '\n')

        # check if the episode has ended
        if self.locals['dones']:
            # calculate the episode taken by the agent to reach first win when training
            self.num_episodes += 1
            print(f'Cumulative number of episodes played: {self.num_episodes}')

            # assign firstWin as cumulative reward that collected by the agent during training process
            self.firstWin = self.locals['infos'][0]['cumulative_reward']
            self.NumOutBoundary = self.locals['infos'][0]['number_outBoundary']
            
            # stop the training process when the agent get win result
            if self.firstWin >= 1:
                # deactivate the timer 
                end_time = time.time()
                # calculate the time taken by the training agent to get the first win result
                elapsed_time = end_time - self.start_time
                print(f'Training took {elapsed_time:.2f} seconds.')

                # print the hyperparameter that the training agent to get first win result
                best_params = {'learning_rate': lr, 'clip_range': clip_range,'n_steps': n_steps, 'batch_size': batch_size, 'gamma': gamma, 'gae_lambda':gae_lambda, 'ent_coef': ent_coef}
                print('Best hyperparameters:', best_params)
                
                # get the last few lines from the text file that save all step taken by the agent
                with open(stepFile,'r') as file:
                    lines = file.readlines()
                    last_few_lines = lines [-(int((((BOARD_COLS * BOARD_ROWS) / NUM_PLAYER) - 1 ) + self.NumOutBoundary)):]

                # save the hyperparameter, time taken, episode, cumulative reward, and step taken by the trained agent to get first win into a text file
                with open(f"modelFile_{self.repeatNum}.txt", 'w') as file:
                    file.write('Here are the hyperparameter for an agent to get first win:' + '\n')
                    file.write(str(best_params) + '\n')
                    file.write('The total episode to get the first win: ')
                    file.write(str(self.num_episodes) + ' episode.\n')
                    file.write('Time taken for this training: ')
                    file.write(str('%.2f' % elapsed_time) + ' second.\n')
                    file.write('Cumulative reward received by the agent: ')
                    file.write(str('%.2f' % self.firstWin) + '\n')
                    file.write('Cumulative number of out-of-boundary: ')
                    file.write(str('%.2f' % self.NumOutBoundary) + '\n')
                    file.write('Below are the steps to get first win'+ '\n')
                    file.writelines(last_few_lines)
                    file.write(str(finalStateData)+ '\n')

                # reset the episode count and start time for the next training
                self.num_episodes = 0
                self.start_time = time.time()

                self.repeatNum += 1

                if self.repeatNum >= MAX_REPEATNUM: 
                    print('Have reached the maximum number of repetition!')
                    # exit the training process
                    exit()
        return True

    def _on_training_end(self) -> None:
        model.save(bufferFile)
        print('Training stopped at ', self.time_limit, ' second.')
        print(currentParam)
        # exit the training process
        exit()
"""
# range of hyperparameters to train different grid size 
hyperparams = {
    'learning_rate': [3e-4, 1e-4, 3e-3, 1e-3, 3e-2, 1e-2],
    'clip_range': [0.1, 0.2, 0.3, 0.4],
    'n_steps':[8, 16, 32, 64, 128, 256, 512, 1024, 2048],
    'batch_size':[8, 16, 32, 64, 128, 256, 512, 1024, 2048],
    'gamma' :[0, 0.3, 0.5, 0.7, 0.9, 0.95, 0.999],
    'gae_lambda' : [0.9, 0.95, 0.99], 
    'ent_coef': [0.00, 0.003, 0.005, 0.007, 0.009, 0.01]
}"""

# define the hyperparameter for training the agent
hyperparams = {
    'learning_rate': [3e-4],
    'clip_range': [0.1],
    'n_steps':[8],
    'batch_size':[8],
    'gamma' :[0.7],
    'gae_lambda' : [0.9], 
    'ent_coef': [0.009]
}

# create a single environment instance
env = squarestate()

# create and wrap the environment with the Monitor wrapper 
env = Monitor(env, filename=None, allow_early_resets=True)

# wrap a single environment in a vectorized environment to allow parallel execution of multiple environment
env = DummyVecEnv([lambda: env])

# initialize the hyperparameter used to train an agent
best_params = None

# use grid search
# loop over all hyperparameter combinations
for lr in hyperparams['learning_rate']:
    for clip_range in hyperparams['clip_range']:
        for n_steps in hyperparams['n_steps']:
            for batch_size in hyperparams['batch_size']:
                for gamma in hyperparams['gamma']:
                    for gae_lambda in hyperparams['gae_lambda']:
                        for ent_coef in hyperparams['ent_coef']:
                            
                            # check the existence of file that save the previous training experience
                            # to load the previous training experience
                            if os.path.exists(bufferFile):
                                model = PPO.load(bufferFile, env = env)
                                print('Loading the file.')
                            else:
                                # create the PPO agent with the current hyperparameters
                                model = PPO ('MlpPolicy', env, learning_rate=lr, clip_range=clip_range, n_steps=n_steps, batch_size=batch_size, gamma=gamma, gae_lambda=gae_lambda, ent_coef=ent_coef, verbose=1)

                            currentParam = {'learning_rate': lr, 'clip_range': clip_range,'n_steps': n_steps, 'batch_size': batch_size, 'gamma': gamma, 'gae_lambda':gae_lambda, 'ent_coef': ent_coef}
                            print(currentParam)

                            callback = EpisodeCountandWinStopCallback(trainingTime)
                            # train the agent on the training set based on the user define total timestep
                            model.learn(total_timesteps = TOTAL_TIMESTEP, reset_num_timesteps = False, callback = callback)
