from vpython import *
from time import *
import random

c = 2
randm = 1
Force = 30
radius = 0.01
speed = 5
Damp_const = 0.99
Force_const = 100
num_particles = 6
Normalisation_factor = 0.2
Seconds_To_Run = 100
rate_pre = 100
particles = []
velocities = []
Forces = []
positions = []
Centr_Atom = sphere(pos=vector(0, 0, 0), radius=0.5, color=color.white)
cylinders = []



first_positions = []
for i in range(num_particles):
    new_position = norm(vector(random.uniform(-randm, randm), random.uniform(-randm, randm), random.uniform(-randm, randm)))*c
    first_positions.append(new_position)

positions.append(first_positions)
    

for i in range(num_particles):
    new_particle = sphere(pos=positions[0][i], radius=0.25, color=color.green)
    new_particle.pos = norm(new_particle.pos) * c
    particles.append(new_particle)

for i in range(num_particles):
    new_velocity = vector(random.uniform(-speed, speed), random.uniform(-speed, speed), random.uniform(-speed, speed))
    velocities.append(new_velocity)


for i in range(num_particles):
    cylinder_first = []
    for j in range(num_particles):
    
        if i != j:
            new_cylinder = cylinder(pos = positions[-1][i], axis = positions[-1][j]-positions[-1][i], length = mag(positions[-1][j]-positions[-1][i]), radius = 0.1, color = color.white, visible = False)
            cylinder_first.append(new_cylinder)
        else:
            new_cylinder = None
            cylinder_first.append(new_cylinder)
    cylinders.append(cylinder_first)



a = 0

while a <= (Seconds_To_Run*60):
    for i in range(num_particles):
        final_force = vector(0, 0, 0)
        for j in range(num_particles):
            if i != j:
                dist = mag(positions[-1][i] - positions[-1][j])
                force_magnitude = Force**2 / dist**2
                direction = norm(positions[-1][i] - positions[-1][j])
                force = force_magnitude * direction
                final_force += force
        final_force *= Force_const
        Forces.append(final_force)
    
    Predictions = []

    for i in range(num_particles):
        Predicted_coords = positions[-1][i] + (velocities[i] * 1/60) + (Forces[i]*1/7200)
        Final_Pos = Predicted_coords + (c - mag(Predicted_coords))*norm(Predicted_coords)*Normalisation_factor
        Predictions.append(Final_Pos)
        velocities[i] += Forces[i]*1/60
        velocities[i] *= Damp_const
        
    positions.append(Predictions)
    
    Forces = []
    
    
    a+=1
    
while True:
    rate(rate_pre)
    for j in range(len(positions)):
        rate(rate_pre)
        for i in range(num_particles):
            particles[i].pos = positions[j][i]
        
        for i in range(len(cylinders)):
            lowest_dist = 10000
            
            for k in range(num_particles):
                if i == k:
                    continue
                if (mag(positions[j][k]-positions[j][i]) < lowest_dist):
                    lowest_dist = mag(positions[j][k]-positions[j][i])
            
            for k in range(num_particles):
                if i == k:
                    continue
                if (mag(positions[j][k]-positions[j][i]) > lowest_dist*0.9 and mag(positions[j][k]-positions[j][i]) < lowest_dist*1.1):
                    cylinders[i][k].pos = positions[j][i]
                    cylinders[i][k].axis = positions[j][k]-positions[j][i]
                    cylinders[i][k].length = mag(positions[j][k]-positions[j][i])
                    cylinders[i][k].visible = True
                else:
                    cylinders[i][k].visible = False
                    
                
    
    
        
        
        
                    
                
           
        
        
    
    
    '''rate(30)
    distH1H2 = mag(H1.pos - H2.pos)
    ForceH1H2 = Force**2 / distH1H2**2 
    directionH1H2 = norm(H1.pos - H2.pos)
    FinalForceH1H2 = ForceH1H2 * directionH1H2
    
    distH1H3 = mag(H1.pos - H3.pos)
    ForceH1H3 = Force**2 / distH1H3**2
    directionH1H3 = norm(H1.pos - H3.pos)
    FinalForceH1H3 = ForceH1H3 * directionH1H3

    distH1H4 = mag(H1.pos - H4.pos)
    ForceH1H4 = Force**2 / distH1H4**2
    directionH1H4 = norm(H1.pos - H4.pos)
    FinalForceH1H4 = ForceH1H4 * directionH1H4
    
    distH1H5 = mag(H1.pos - H5.pos)
    ForceH1H5 = Force**2 / distH1H5**2 
    directionH1H5 = norm(H1.pos - H5.pos)
    FinalForceH1H5 = ForceH1H5 * directionH1H5
    
    distH1H6 = mag(H1.pos - H6.pos)
    ForceH1H6 = Force**2 / distH1H6**2
    directionH1H6 = norm(H1.pos - H6.pos)
    FinalForceH1H6 = ForceH1H6 * directionH1H6

    FinalForceH1 = (FinalForceH1H2 + FinalForceH1H3 + FinalForceH1H4 + FinalForceH1H5 + FinalForceH1H6) * Force_const
    PredictedCoordH1 = H1.pos + (V1*(1/60)) +  (FinalForceH1 * (1/7200))
    FinalCoordH1 = PredictedCoordH1 + (norm(PredictedCoordH1) * (c - mag(PredictedCoordH1))*0.3)
    V1 += FinalForceH1 * (1/60)
    V1 *= Damp_const



    
    
    distH2H3 = mag(H2.pos - H3.pos)
    ForceH2H3 = Force**2 / distH2H3**2
    directionH2H3 = norm(H2.pos - H3.pos)
    FinalForceH2H3 = ForceH2H3 * directionH2H3

    distH2H4 = mag(H2.pos - H4.pos)
    ForceH2H4 = Force**2 / distH2H4**2
    directionH2H4 = norm(H2.pos - H4.pos)
    FinalForceH2H4 = ForceH2H4 * directionH2H4
    
    distH2H5 = mag(H2.pos - H5.pos)
    ForceH2H5 = Force**2 / distH2H5**2
    directionH2H5 = norm(H2.pos - H5.pos)
    FinalForceH2H5 = ForceH2H5 * directionH2H5
    
    distH2H6 = mag(H2.pos - H6.pos)
    ForceH2H6 = Force**2 / distH2H6**2
    directionH2H6 = norm(H2.pos - H6.pos)
    FinalForceH2H6 = ForceH2H6 * directionH2H6

    FinalForceH2 = ((-FinalForceH1H2) + FinalForceH2H3 + FinalForceH2H4 + FinalForceH2H5 + FinalForceH2H6) * Force_const
    PredictedCoordH2 = H2.pos + (V2*(1/60)) + (FinalForceH2 * (1/7200))
    FinalCoordH2 = PredictedCoordH2 + (norm(PredictedCoordH2) * (c - mag(PredictedCoordH2))*0.3)
    V2 += FinalForceH2 * (1/60)
    V2 *= Damp_const

    

    distH3H4 = mag(H3.pos - H4.pos)
    ForceH3H4 = Force**2 / distH3H4**2
    directionH3H4 = norm(H3.pos - H4.pos)
    FinalForceH3H4 = ForceH3H4 * directionH3H4
    
    distH3H5 = mag(H3.pos - H5.pos)
    ForceH3H5 = Force**2 / distH3H5**2
    directionH3H5 = norm(H3.pos - H5.pos)
    FinalForceH3H5 = ForceH3H5 * directionH3H5
    
    distH3H6 = mag(H3.pos - H6.pos)
    ForceH3H6 = Force**2 / distH3H6**2
    directionH3H6 = norm(H3.pos - H6.pos)
    FinalForceH3H6 = ForceH3H6 * directionH3H6

    FinalForceH3 = ((-FinalForceH1H3) + (-FinalForceH2H3) + FinalForceH3H4 + FinalForceH3H5 + FinalForceH3H6) * Force_const
    PredictedCoordH3 = H3.pos + (V3*(1/60)) + (FinalForceH3 * (1/7200))
    FinalCoordH3 = PredictedCoordH3 + (norm(PredictedCoordH3) * (c - mag(PredictedCoordH3))*0.3)
    V3 += FinalForceH3 * (1/60)
    V3 *= Damp_const



    
    
    
    
    distH4H5 = mag(H4.pos - H5.pos)
    ForceH4H5 = Force**2 / distH4H5**2
    directionH4H5 = norm(H4.pos - H5.pos)
    FinalForceH4H5 = ForceH4H5 * directionH4H5
    
    distH4H6 = mag(H4.pos - H6.pos)
    ForceH4H6 = Force**2 / distH4H6**2
    directionH4H6 = norm(H4.pos - H6.pos)
    FinalForceH4H6 = ForceH4H6 * directionH4H6

    FinalForceH4 = ((-FinalForceH1H4) + (-FinalForceH2H4) + (-FinalForceH3H4) + FinalForceH4H5 + FinalForceH4H6) * Force_const
    PredictedCoordH4 = H4.pos + (V4*(1/60)) + (FinalForceH4 * (1/7200))
    FinalCoordH4 = PredictedCoordH4 + (norm(PredictedCoordH4) * (c - mag(PredictedCoordH4))*0.3)
    V4 += FinalForceH4 * (1/60)
    V4 *= Damp_const


    distH5H6 = mag(H5.pos - H6.pos)
    ForceH5H6 = Force**2 / distH5H6**2
    directionH5H6 = norm(H5.pos - H6.pos)
    FinalForceH5H6 = ForceH5H6 * directionH5H6

    FinalForceH5 = ((-FinalForceH1H5) + (-FinalForceH2H5) + (-FinalForceH3H5) + (-FinalForceH4H5) + FinalForceH5H6) * Force_const
    PredictedCoordH5 = H5.pos + (V5*(1/60)) + (FinalForceH5 * (1/7200))
    FinalCoordH5 = PredictedCoordH5 + (norm(PredictedCoordH5) * (c - mag(PredictedCoordH5))*0.3)
    V5 += FinalForceH5 * (1/60)
    V5 *= Damp_const



    FinalForceH6 = ((-FinalForceH1H6) + (-FinalForceH2H6) + (-FinalForceH3H6) + (-FinalForceH4H6) + (-FinalForceH5H6)) * Force_const
    PredictedCoordH6 = H6.pos + (V6*(1/60)) + (FinalForceH6 * (1/7200))
    FinalCoordH6 = PredictedCoordH6 + (norm(PredictedCoordH6) * (c - mag(PredictedCoordH6))*0.3)
    V6 += FinalForceH6 * (1/60)
    V6 *= Damp_const



    


    H1.pos = FinalCoordH1
    H2.pos = FinalCoordH2
    H3.pos = FinalCoordH3
    H4.pos = FinalCoordH4
    H5.pos = FinalCoordH5
    H6.pos = FinalCoordH6
    
    
    C1.pos = H1.pos
    C1.axis = H2.pos - H1.pos
    C1.length = mag(H2.pos - H1.pos)
    C2.pos = H1.pos
    C2.axis = H3.pos - H1.pos
    C2.length = mag(H3.pos - H1.pos)
    C3.pos = H1.pos
    C3.axis = H4.pos - H1.pos
    C3.length = mag(H4.pos - H1.pos)
    C4.pos = H1.pos
    C4.axis = H5.pos - H1.pos
    C4.length = mag(H5.pos - H1.pos)
    C5.pos = H1.pos
    C5.axis = H6.pos - H1.pos
    C5.length = mag(H6.pos - H1.pos)
    
    C6.pos = H2.pos
    C6.axis = H3.pos - H2.pos
    C6.length = mag(H3.pos - H2.pos)
    C7.pos = H2.pos
    C7.axis = H4.pos - H2.pos
    C7.length = mag(H4.pos - H2.pos)
    C8.pos = H2.pos
    C8.axis = H5.pos - H2.pos
    C8.length = mag(H5.pos - H2.pos)
    C9.pos = H2.pos
    C9.axis = H6.pos - H2.pos
    C9.length = mag(H6.pos - H2.pos)
    
    C10.pos = H3.pos
    C10.axis = H4.pos - H3.pos
    C10.length = mag(H4.pos - H3.pos)
    C11.pos = H3.pos
    C11.axis = H5.pos - H3.pos
    C11.length = mag(H5.pos - H3.pos)
    C12.pos = H3.pos
    C12.axis = H6.pos - H3.pos
    C12.length = mag(H6.pos - H3.pos)
    
    C13.pos = H4.pos
    C13.axis = H5.pos - H4.pos
    C13.length = mag(H5.pos - H4.pos)
    C14.pos = H4.pos
    C14.axis = H6.pos - H4.pos
    C14.length = mag(H6.pos - H4.pos)
    
    C15.pos = H5.pos
    C15.axis = H6.pos - H5.pos
    C15.length = mag(H6.pos - H5.pos)'''
