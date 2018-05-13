<p align="center"><img src="http://i0.kym-cdn.com/photos/images/original/001/185/731/ed3.png" height="164"></p>

# Sneks openAI gym environment
Sneks is an openAI gym environment similar to the classic game Snake. It contains both a single-player version (Snek) and a multi-player version(Sneks). The different environemnts are described below.

## Installation
The environment can be installed using pip

> pip install -e .

## Requirements
- numpy
- gym

## Supported platforms
We only support Python3. Environments are actively tested on Ubuntu and MACOS. Currently there are some issues with Ubuntu renderer.

## Observations and actions
The environment outputs as an observation a matrix representing the game map (as an image with pixels). The observation size depends on the map size. Every different object is associated with different numbers in the grid (0-255).<br>
We provide two different observation mode:
- *raw*: returns the game matrix directly.
- *rgb*: returns a render of the game matrix as an rgb image, with a possible zoom factor.

Actions are integers in [0,3] representing [UP, RIGHT, DOWN, LEFT]<br>
In multi-agent environments actions are provided as vectors. The step function returns a vector of rewards and done-flags (observation is the same for every player).

## Environments and versions

### babysnek-v1
![babysnek][babysnek] <br>
First simple enviroment (16x16 grid), only one snake and one goal (food). The episode terminates once the snake eats the food or dies (eats himself or go outside map limits). Just a basic setting to test things out.<br>
Rewards:
- Reach goal (eats): +1
- Move: 0
- Dies: -1

[babysnek]: src/babysnek.gif?raw=true

### snek-v1
![snek][snek] <br>
Enviroment in a 16x16 grid, only one snake and one goal (food). The episode terminates when it reaches the step limit (default: 1000) or if the snake goes outside bounds or eats itself.<br>
Rewards:
- Reach goal (eats): +1
- Move: 0
- Dies: -1
<br>

Above a GIF of the environment played by vanilla DQN. All the solutions and implementations on the environment can be found in the corresponding [github repo](https://github.com/nicomon24/Sneks-solutions), that contains more detailed explanation on solutions

[snek]: src/snek.gif?raw=true

### snek-rgb-v1

The same as *snek-v1* but with observations in RGB mode.

### hungrysnek-v1

Similar to *snek-v1*, but the snek also has a dynamic step limit which resets after eating, as a progressively increasing hunger.

## TODO
- Larger single-agent environment (32x32 and 64x64)
- Define various multiagent environments:
  - Snakes can eat each other
  - Eat or starve, snakes cannot eat each other but food is limited

## Ideas
- Cooperation game: snakes can eat only if they reach the same food together
- More walls? (Maze-like?) Other block types with different behaviour?
