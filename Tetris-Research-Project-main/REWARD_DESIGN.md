# Reward Function

## Goal
The agent will be trained to generate the highest score possible. This can be done through living longer, breaking more lines at once, ect.

## Decisions

### 1. What counts as successs?
We want our game to maximize total score.
Why? Living as long as posisble in the game is important but it is not a needed goal. In order to beat other players generating the most score is trivial.

### 2. Line clear reward

NES Table Score Rewards


### 3. Survival Reward

Score should be generated per lines cleared as we as survival i.e gaining a new piece to plice will be a reward aswell. 

### 4. Game-over Penality

Big loss we want to heavily prioritize staying alive. 


### 5. Feature Shaping

Features values will be shaped through the neural network.

### 6. Scale

Smallest reward would be for completing a row larget reward would be completing 4 row break.

## Final reward Function
reward per placement = TBD place holder 10
game over = TBD Place holder -100

## Variants to compare
1. Initial
2. after training
3. Fine Tuning
4. RL



