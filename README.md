# VPython-Particle-Sim

A 3D physics simulation that models how particles arrange themselves on the 
surface of a sphere using repulsive forces — visually demonstrating VSEPR 
theory by taking in a number of peripheral atoms.

No AI was used, it was just calculation stuff to do before working on this simulation project. 

## Live Demo

READ THIS FIRST!!!!!!!!!!!!! WAIT 10-20 SECONDS AFTER OPENING THE WEB PROJECT, ITS COMPUTING AROUND 5000 OBJECTS PER FRAME AND STORING THEM BEFORE STARTING THE SIMULATION SO THAT IT CAN BE SMOOTH
https://glowscript.org/#/user/angadmaster123/folder/MyPrograms/program/AtomSim

If you run the Python script, you can go for much larger simulation, like this 10000 particle beast which took 20 minutes just to compute even with numpy calculations

<img width="1895" height="885" alt="Screenshot 2026-07-16 230359" src="https://github.com/user-attachments/assets/4d806c44-64fa-45a6-b5a0-4c5344420950" />



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
