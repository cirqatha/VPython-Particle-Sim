# VPython-Particle-Sim

A 3D physics simulation that models how particles arrange themselves on the 
surface of a sphere using repulsive forces — visually demonstrating VSEPR 
theory by taking in a number of peripheral atoms.

No AI was used, it was just calculation stuff to do before working on this simulation project. 

## Live Demo
https://glowscript.org/#/user/angadmaster123/folder/MyPrograms/program/AtomSim

No install needed — works in any browser.

## Calculation

- Every particle exerts an inverse-square repulsive force on every other particle
- All forces on each particle are summed each frame (O(n²) pair calculations)
- Force is used to update velocity, velocity is used to update position 
- A damping constant is applied to velocity each frame to bleed off energy and help the system settle
- After each position update, a partial normalisation nudges particles back toward the sphere surface without snapping them instantly
- All frames are pre-computed and stored in a 2D list before the animation plays back

  
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


## Controls
Use your mouse to rotate, zoom, and pan the 3D view in the browser window.
