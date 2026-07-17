from vpython import *
import random
import numpy as np
import time

scene.width = 300
scene.height = 100
scene.range = 20000
scene.background = color.black
scene.center = vector(0, 0, 0)
scene.forward = vector(0, -0.3, -1)
scene.autoscale = False

SHOW_CYLINDERS        = True    
FINAL_CYLINDERS_ONLY  = True   
                                
SHOW_ARROWS           = True   
SHOW_GRID             = False  
FINAL_ONLY            = True    


if SHOW_GRID:
    grid_size = 600
    grid_spacing = 50
    for x in range(-grid_size, grid_size + grid_spacing, grid_spacing):
        curve(pos=[vector(x, -4, -grid_size), vector(x, -4, grid_size)], color=color.white, radius=0.05)
    for z in range(-grid_size, grid_size + grid_spacing, grid_spacing):
        curve(pos=[vector(-grid_size, -4, z), vector(grid_size, -4, z)], color=color.white, radius=0.05)


c                    = 50
Force                = 1000000
speed                = 5
Damp_const           = 0.9
Force_const          = 5000000
num_particles        = 10000
Normalisation_factor = 0.5
Seconds_To_Run       = 5
rate_pre             = 60
arrow_scale          = 0.005
total_steps          = Seconds_To_Run * 60


Centr_Atom = sphere(pos=vector(0, 0, 0), radius=20000, color=color.red)


init = np.random.uniform(-1, 1, (num_particles, 3))  
init = init / np.linalg.norm(init, axis=1, keepdims=True) * c

particles = []
for i in range(num_particles):
    p = sphere(pos=vector(float(init[i,0]), float(init[i,1]), float(init[i,2])), radius=10000, color=color.green)
    particles.append(p)

pos = init.copy()
vel = np.random.uniform(-speed, speed, (num_particles, 3))  


cylinders = []       
bond_cylinders = {} 

if SHOW_CYLINDERS and not FINAL_CYLINDERS_ONLY:
    print("Creating all cylinders upfront...")
    cyl_start = time.time()
    for i in range(num_particles):
        row = []
        for j in range(num_particles):
            if i != j:
                row.append(cylinder(
                    pos=vector(float(pos[i,0]), float(pos[i,1]), float(pos[i,2])),
                    axis=vector(float(pos[j,0]-pos[i,0]), float(pos[j,1]-pos[i,1]), float(pos[j,2]-pos[i,2])),
                    length=float(np.linalg.norm(pos[j]-pos[i])),
                    radius=500, color=color.white, visible=False
                ))
            else:
                row.append(None)
        cylinders.append(row)
        if (i + 1) % 100 == 0:
            print(f"  Cylinders: {i+1}/{num_particles} ({(i+1)/num_particles*100:.0f}%)")
    print(f"Cylinders done in {time.time()-cyl_start:.1f}s!")


arrows_tan = []
arrows_rad = []
if SHOW_ARROWS:
    for i in range(num_particles):
        arrows_tan.append(arrow(pos=vector(float(pos[i,0]), float(pos[i,1]), float(pos[i,2])), axis=vector(0,0.01,0), color=color.red, shaftwidth=0.12))
        arrows_rad.append(arrow(pos=vector(float(pos[i,0]), float(pos[i,1]), float(pos[i,2])), axis=vector(0,0.01,0), color=color.cyan, shaftwidth=0.07, opacity=0.4))


def run_physics(pos, vel, steps):
    forces_hist = []
    pos_hist = [pos.copy()]
    start = time.time()
    for a in range(steps):
        forces = np.zeros((num_particles, 3))
        for i in range(num_particles - 1):
            diff = pos[i] - pos[i+1:]
            dist = np.linalg.norm(diff, axis=1, keepdims=True)
            dist = np.maximum(dist, 1e-10)
            f = (Force**2 / dist**2) * (diff / dist) * Force_const
            forces[i]    += f.sum(axis=0)
            forces[i+1:] -= f

        if SHOW_ARROWS:
            forces_hist.append(forces.copy())

        predicted = pos + vel/60 + forces/7200
        mag_ = np.linalg.norm(predicted, axis=1, keepdims=True)
        mag_ = np.maximum(mag_, 1e-10)
        pos = predicted + (c - mag_) * (predicted / mag_) * Normalisation_factor
        vel = (vel + forces/60) * Damp_const

        if not FINAL_ONLY:
            pos_hist.append(pos.copy())

        if (a + 1) % 60 == 0:
            elapsed = time.time() - start
            seconds_done = (a + 1) // 60
            pct = (a + 1) / steps * 100
            eta = (elapsed / (a + 1)) * (steps - a - 1)
            print(f"  [{pct:5.1f}%] second {seconds_done}/{Seconds_To_Run} — elapsed: {elapsed:.1f}s — ETA: {eta:.1f}s")

    total_time = time.time() - start
    print(f"\nDone in {total_time:.1f}s!")
    return pos, vel, pos_hist, forces_hist


def create_bond_cylinders(pos):
    print("Computing bonds and creating cylinders...")
    bond_start = time.time()
    dists_all = np.linalg.norm(pos[:, np.newaxis, :] - pos[np.newaxis, :, :], axis=2)
    np.fill_diagonal(dists_all, np.inf)
    bc = {}
    count = 0
    for i in range(num_particles):
        lowest_dist = float(np.min(dists_all[i]))
        for k in range(num_particles):
            if i == k:
                continue
            d = float(dists_all[i][k])
            if lowest_dist*0.7 < d < lowest_dist*1.3:
                cyl = cylinder(
                    pos=vector(float(pos[i,0]), float(pos[i,1]), float(pos[i,2])),
                    axis=vector(float(pos[k,0]-pos[i,0]), float(pos[k,1]-pos[i,1]), float(pos[k,2]-pos[i,2])),
                    length=d,
                    radius=500, color=color.white, visible=True
                )
                bc[(i, k)] = cyl
                count += 1
    print(f"Created {count} bond cylinders in {time.time()-bond_start:.1f}s")
    return bc


def update_bond_cylinders(bc, frame):
    for (i, k), cyl in bc.items():
        cyl.pos = vector(float(frame[i,0]), float(frame[i,1]), float(frame[i,2]))
        cyl.axis = vector(
            float(frame[k,0]-frame[i,0]),
            float(frame[k,1]-frame[i,1]),
            float(frame[k,2]-frame[i,2])
        )
        cyl.length = float(np.linalg.norm(frame[k]-frame[i]))


def update_all_cylinders(cylinders, frame):
    for i in range(len(cylinders)):
        dists = np.linalg.norm(frame - frame[i], axis=1)
        dists[i] = np.inf
        lowest_dist = float(np.min(dists))
        for k in range(num_particles):
            if i == k:
                continue
            d = float(dists[k])
            if lowest_dist*0.7 < d < lowest_dist*1.3:
                cylinders[i][k].pos = particles[i].pos
                cylinders[i][k].axis = vector(
                    float(frame[k,0]-frame[i,0]),
                    float(frame[k,1]-frame[i,1]),
                    float(frame[k,2]-frame[i,2])
                )
                cylinders[i][k].length = d
                cylinders[i][k].visible = True
            else:
                cylinders[i][k].visible = False


angle = 0
rotation_speed = 0

if FINAL_ONLY:
    print("Computing final structure...")
    pos, vel, _, _ = run_physics(pos, vel, total_steps)

    for i in range(num_particles):
        particles[i].pos = vector(float(pos[i,0]), float(pos[i,1]), float(pos[i,2]))

    if SHOW_CYLINDERS:
        if FINAL_CYLINDERS_ONLY:
            bond_cylinders = create_bond_cylinders(pos)
        else:
            
            dists_all = np.linalg.norm(pos[:, np.newaxis, :] - pos[np.newaxis, :, :], axis=2)
            np.fill_diagonal(dists_all, np.inf)
            for i in range(num_particles):
                lowest_dist = float(np.min(dists_all[i]))
                for k in range(num_particles):
                    if i == k:
                        continue
                    d = float(dists_all[i][k])
                    if lowest_dist*0.7 < d < lowest_dist*1.3:
                        cylinders[i][k].pos = particles[i].pos
                        cylinders[i][k].axis = vector(float(pos[k,0]-pos[i,0]), float(pos[k,1]-pos[i,1]), float(pos[k,2]-pos[i,2]))
                        cylinders[i][k].length = d
                        cylinders[i][k].visible = True
                    else:
                        cylinders[i][k].visible = False

    print("Showing final structure. Rotating...")
    while True:
        rate(rate_pre)
        angle += rotation_speed
        scene.forward = vector(sin(angle), -0.3, -cos(angle))

else:
    print("Computing all frames...")
    pos, vel, positions_np, forces_history = run_physics(pos, vel, total_steps)

    if SHOW_CYLINDERS and FINAL_CYLINDERS_ONLY:
        bond_cylinders = create_bond_cylinders(pos)

    print("Starting animation...")
    while True:
        rate(rate_pre)
        for j in range(len(positions_np)):
            rate(rate_pre)
            angle += rotation_speed
            scene.forward = vector(sin(angle), -0.3, -cos(angle))

            frame = positions_np[j]
            for i in range(num_particles):
                particles[i].pos = vector(float(frame[i,0]), float(frame[i,1]), float(frame[i,2]))

            if SHOW_ARROWS and j < len(forces_history):
                for i in range(num_particles):
                    r_hat = frame[i] / np.linalg.norm(frame[i])
                    f = forces_history[j][i] * arrow_scale
                    f_rad = np.dot(f, r_hat) * r_hat
                    f_tan = f - f_rad
                    arrows_tan[i].pos = particles[i].pos
                    arrows_tan[i].axis = vector(float(f_tan[0]), float(f_tan[1]), float(f_tan[2]))
                    arrows_rad[i].pos = particles[i].pos
                    arrows_rad[i].axis = vector(float(f_rad[0]*0.4), float(f_rad[1]*0.4), float(f_rad[2]*0.4))

            if SHOW_CYLINDERS:
                if FINAL_CYLINDERS_ONLY:
                    update_bond_cylinders(bond_cylinders, frame)
                else:
                    update_all_cylinders(cylinders, frame)
