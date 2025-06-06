import math
import random

degree = math.pi/180.0 # radians per degree

def FTarget(target_distance, target_angle, robot_phi):
    # Ftar = -math.sin(robot_phi - target_angle) 
    Ftar = -math.exp(-target_distance) * math.sin(robot_phi - target_angle) 
    return Ftar

def FObstacle(obs_distance, obs_angle, robot_phi):
    too_far=10 #cm
    sigma_obs = 1
    beta_2 = 1

    if obs_distance < too_far: # only obstacle avoidance when close to object
        #do something useful here
        term_A = math.exp(-(robot_phi-obs_angle)**2 / (2*sigma_obs**2))*(robot_phi-obs_angle) 
        term_B = math.exp(-obs_distance / beta_2)
        # Fobs = term_A * term_B
        Fobs = abs(term_A * term_B)
    else:
        Fobs = 0
    return Fobs

def FStochastic():
    """FStochastic adds noise to the turnrate force. This is just to make the simulation more realistic by adding some noie something useful here"""
    Kstoch=0.03
    
    Fstoch = Kstoch*random.randint(1,100)/100.0

    return Fstoch

def FOrienting(target_distance, target_angle, robot_phi):
    Forient = -math.exp(-target_distance)*math.sin(robot_phi - target_angle)
    # Forient = -math.sin(robot_phi - target_angle)
    return Forient

def compute_velocity(sonar_distance_left, sonar_distance_right):
    max_velocity = 0.3#1.0
    max_distance = 0.8 #m
    min_distance = 0.4 #m

    if sonar_distance_left>max_distance and sonar_distance_right > max_distance:
        velocity = max_velocity
    elif sonar_distance_left<min_distance or sonar_distance_right < min_distance:
        velocity = 0.0
    elif sonar_distance_left<sonar_distance_right:
        velocity = max_velocity*sonar_distance_left/max_distance
    else:
        velocity = max_velocity*sonar_distance_right/max_distance

    
    return velocity

def compute_turnrate(target_dist, target_angle, sonar_distance_left, sonar_distance_right, robot_phi):
    max_turnrate = 0.19#0.349 #rad/s # may need adjustment!

    delta_t = 0.8 # may need adjustment!`
    sonar_angle_left = 30 * degree
    sonar_angle_right = -30 * degree
    
    Fobs_left = FObstacle(sonar_distance_left, sonar_angle_left, robot_phi)
    Fobs_right = FObstacle(sonar_distance_right, sonar_angle_right, robot_phi)

    # FTotal = weight_1 * FTarget(target_dist, target_angle, robot_phi) + \
    #          weight_2 * (Fobs_left + Fobs_right) + \
    #          weight_3 * FOrienting(target_dist, target_angle, robot_phi) + \
    #          FStochastic()


    # Weights of the forces
    weight_2 = 10#100
    weight_3 = 10#100
    weight_1 = 10 if (weight_2 * (Fobs_right - Fobs_left) < 0.05) else 0 #100000000000 only make target force bigger when not close to object

    # Force right - left, so robot turns right when Fobs positive and left when Fobs negative, (Fobs left and Fobs right always positive since absolute is used)
    FTotal = weight_1 * FTarget(target_dist, target_angle, robot_phi) + \
             weight_2 * (Fobs_right - Fobs_left) + \
             weight_3 * FOrienting(target_dist, target_angle, robot_phi) + \
             FStochastic()
             
    # turnrate: d phi(t) / dt = sum( forces ) 
    turnrate =  FTotal*delta_t
    
    # normalise turnrate value
    turnrate=turnrate/max_turnrate
    if turnrate>max_turnrate:
        turnrate=max_turnrate#1.0
    elif turnrate<-max_turnrate:
        turnrate=-max_turnrate#-1.0

    return turnrate

if __name__=="__main__":
    pass
