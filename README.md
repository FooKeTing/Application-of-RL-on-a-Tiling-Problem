# User Manual
The figure below provides instructions outlining the pre-execution steps required for the Python files, namely _env_playerCode.py_ and _trainPlayerCode.py_. Users can arrive at a conclusion by following these instructions and analyzing the generated output files. It should be noted that the process indicated by the green dotted box requires manual execution.

![User Manual Flowchart](https://github.com/FooKeTing/Application-of-RL-on-a-Tiling-Problem/assets/134204900/15fb208c-d1d8-4190-a9b8-a236811b57ac)

The information regarding the input and output files is documented below. These tables provide valuable insights into the contents and specifications of the files, allowing users to gain a better understanding.

![image](https://github.com/FooKeTing/Application-of-RL-on-a-Tiling-Problem/assets/134204900/c0add9df-6344-4af7-9f57-fa3496cee0fa)

![image](https://github.com/FooKeTing/Application-of-RL-on-a-Tiling-Problem/assets/134204900/8be0028c-4dac-4b04-97e8-532dfc4d8045)


**Main Flow Chart for Developed Framework**

The figure below shows how the developed reinforcement learning framework works on training an agent to fill up all empty grids.

![Main Program Flowchart](https://github.com/FooKeTing/Application-of-RL-on-a-Tiling-Problem/assets/134204900/4fa9e254-4b95-4b81-b4fd-0587b0a1f2bc)

The framework developed for this project comprises a reinforcement learning algorithm and two classes: _playernum_ and _squarestate_. The derived class _squarestate_ inherits from both the abstract class_ gym.Env_ and the base class _playernum_.

The base class _playernum_ includes six methods: ___init__()_, _show_menuOrientation()_, _drawWall()_, _get_lastNCols()_, _get_LastNRows()_, and _get_firstLastNCols()_. The _playernum_ class randomly places the player within a grid with user-specified values for the number of players (_NUM_PLAYER_) and player orientation (_PLAYER_ORIENTATION_), based on a specified number of rows (_BOARD_ROWS_) and columns (_BOARD_COLS_).

The derived class _squarestate_ utilizes the **OpenAI Gym** environment and consists of six methods: ___init__()_, _render()_, _step()_, _positionNum()_, _availablePosition()_, and _reset()_. Note that the _positionNum()_ and _availablePosition()_ methods are executed within the _step()_ method and are not explicitly shown in the last figure. The _squarestate_ class sends information, including rewards, states, and actions, to the reinforcement learning algorithm.

The framework utilizes the **Stable Baselines3** library to train the RL agent. During the training process, the framework creates a temporary file called "_stepFile_" to store the current state of the agent, represented as a 1-dimensional numpy array. This file can be deleted once the training process is completed. The training continues until the agent successfully fills all empty grid spaces, and the relevant information is stored in a file named "_modelFile_x.txt_". This training and storage process repeats automatically for a specified number of iterations defined as _MAX_REPEATNUM_.

If the _trainingTime_ limit is reached or the agent fails to fill all empty grid spaces, a "_bufferFile_" is created. This file stores the training experiences, and the user must manually initiate the training process again if the _bufferFile_ is present. It is important to note that if the agent fails to fill all empty grid spaces, the user may need to adjust parameters, such as _hyperparameters_(e.g., learning_rate, clip_range, gamme, etc.), _TOTAL_TIMESTEP_ and _trainingTime_, as these parameters significantly impact the agent's training.

This methodology ensures a systematic and iterative training process for the RL agent in the tiling problem, allowing for fine-tuning and adjustments to enhance the agent's performance.

**Important!!** The _env_playerCode_v2.py_ file is the second version of the _env_playerCode.py_ as the new version allows the player to step one or two-step at each time while the old version only allows the player to step one step at each time. 
