<p align="center"><img src="http://i0.kym-cdn.com/photos/images/original/001/185/731/ed3.png" height="164"></p>

# Sneks openAI gym environment
Sneks is an openAI gym environment similar to the classic game Snake. It contains both a single-player version (Snek) and a multi-player version(Sneks). The different environemnts are described below.

## Installation
The environment can be installed using pip

> pip install -e .

## Requirements
- numpy
- gym
- opencv2

## Supported platforms
We only support Python3. Environments are actively tested on Ubuntu and MACOS. Currently there are some issues with Ubuntu renderer.

## Observations and actions
At its core, the game state is represented by a matrix of a given size (depends on the various environments). Every different object is associated with different sets of IDs, allowing expansions for new objects and multi-players.

The observation returned by the environment can be of different types:
- **raw**: returns directly the game matrix, IDs are integer encoded in the range 0-255.
- **rgb**: returns a color-coded image (0-255), using the color scheme defined in the render object.
- **rgb5**: returns a color-coded image (0-255) but enlarged in size by a factor of 5. Other scales can be added in the registration file (init file).
- **layered**: each object is returned in a different channel of an image. This could be better in multi-agent settings (EXPERIMENTAL).

The size of the environment can be set directly choosing between [16, 32, 64], the grid will always be a square.

Actions are discrete, encoded by integers in the range [0,3] representing [UP, RIGHT, DOWN, LEFT]<br>
In multi-agent environments actions are provided as vectors. The step function returns a vector of rewards and done-flags (observation is the same for every player).

## Environments and versions
Given the many possible configurations for observations and sizes, we adopt a modular naming strategy similar to the OpenAI gym Atari environments. Each environment is of the form:
> <env_type>-<observation_type>-<size\>-v1

The various environment types are described below.

### babysnek
![babysnek][babysnek] <br>
First simple environment, only one snake and one goal (food). The episode terminates once the snake eats the food or dies (eats himself or go outside map limits). Just a basic setting to test things out.<br>
Rewards:
- Reach goal (eats): +1
- Move: 0
- Dies: -1

Example environment: *babysnek-raw-16-v1*

[babysnek]: src/babysnek.gif?raw=true

### snek-v1
![snek][snek] <br>
Environment in a 16x16 grid, only one snake and one goal (food). The episode terminates when it reaches the step limit (default: 1000) or if the snake goes outside bounds or eats itself.<br>
Rewards:
- Reach goal (eats): +1
- Move: 0
- Dies: -1
<br>

Above a GIF of the environment played by vanilla DQN.

Example environment: *snek-rgb-16-v1*

[snek]: src/snek.gif?raw=true

### hungrysnek-v1

Similar to *snek-v1*, but the snek also has a dynamic step limit which resets after eating, as a progressively increasing hunger.

Example environment: *hungysnek-raw-32-v1*

## TODO
- Define various multiagent environments:
  - Snakes can eat each other (who wins?).
  - Eat or starve, snakes cannot eat each other but food is limited.

## Ideas
- Cooperation game: snakes can eat only if they reach the same food together
- More walls? (Maze-like?) Other block types with different behaviour?
