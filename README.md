# VPython-Particle-Sim

A 3D physics simulation that models how particles arrange themselves on the 
surface of a sphere using repulsive forces — visually demonstrating VSEPR 
theory by taking in a number of peripheral atoms.

## Live Demo
https://glowscript.org/#/user/angadmaster123/folder/MyPrograms/program/AtomSim

No install needed — works in any browser.

## Calculation

Forces between all particle pairs are computed each frame using an inverse-square 
repulsion law, then summed per particle. Position and velocity are updated via 
Euler integration, followed by a partial normalisation step that softly constrains 
each particle to the sphere surface. All frames are pre-computed and stored in a 
2D list before playback begins.

## How to Run Locally 
Just run the HTML file if python one causes error

### Requirements
- Python 3.x
- A modern browser (Chrome, Firefox, Edge)

### Install dependencies
pip install vpython

### Run
python AutoSim.py

A browser tab will open automatically with the 3D simulation.

## How It Works
- Particles start at random positions on a sphere
- Each particle repels every other particle (inverse square law)
- A normalisation force keeps them on the sphere surface
- After simulating 100 seconds of physics, it plays back the animation
- Cylinders draw bonds to each particle's nearest neighbour

## Controls
Use your mouse to rotate, zoom, and pan the 3D view in the browser window.
