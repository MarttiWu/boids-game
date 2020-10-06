# Boids Game

Boids is an artificial life program, developed by Craig Reynolds in 1986. 
It simulates the flocking behaviour of birds.

Reference:  [Boids](https://en.wikipedia.org/wiki/Boids)

This Boids Game is implemented in python which simulates the flocking behavior of birds and also the reaction when bumping into obstacles.

# Usage

Open terminal

        python3 Boids.py
        
# Behaviors

## Alignment
Steer towards the average heading of local flockmates.

Reference:  [Boids](https://en.wikipedia.org/wiki/Boids)
![alt text](results/alignment.png)

## Cohension
Steer to move towards the average position of local flockmates.

Reference:  [Boids](https://en.wikipedia.org/wiki/Boids)
![alt text](results/cohension.png)

## Separation
Steer to avoid crowding local flockmates.

Reference:  [Boids](https://en.wikipedia.org/wiki/Boids)
![alt text](results/separation.png)

## Obstacles

![alt text](results/obstacle.png)

