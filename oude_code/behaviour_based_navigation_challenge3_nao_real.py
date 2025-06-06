import math
import random

degree = math.pi/180.0 # radians per degree

def FTarget(target_distance, target_angle, robot_phi):
    #do something useful here
    # Ftar = -math.sin(robot_phi - target_angle) 
    print("target distance", target_distance)
    print("robot phi", robot_phi)
    print("target angle", target_angle)
    Ftar = -math.exp(-target_distance) * math.sin(robot_phi - target_angle) 
    return Ftar

def FObstacle(obs_distance, obs_angle, robot_phi):
    too_far=10 #cm
    sigma_obs = 1
    beta_2 = 1

    # only obstacle avoidance when close
    if obs_distance < too_far:
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
    #do something useful here
    Forient = -math.exp(-target_distance)*math.sin(robot_phi - target_angle)
    # Forient = -math.sin(robot_phi - target_angle)
    return Forient

def compute_velocity(sonar_distance_left, sonar_distance_right):
    max_velocity = 1.0
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
    max_turnrate = 0.349 #rad/s # may need adjustment!

    delta_t = 0.8 # may need adjustment!`
    weight_1 = max(100000, 999999999999 * math.exp(-min(sonar_distance_left, sonar_distance_right)))
    weight_2 = max(4, 10 * math.exp(-target_dist)) 
    weight_3 = 2

    sonar_angle_left = 30 * degree
    sonar_angle_right = -30 * degree
    
    Fobs_left = FObstacle(sonar_distance_left, sonar_angle_left, robot_phi)
    Fobs_right = FObstacle(sonar_distance_right, sonar_angle_right, robot_phi)

    # FTotal = weight_1 * FTarget(target_dist, target_angle, robot_phi) + \
    #          weight_2 * (Fobs_left + Fobs_right) + \
    #          weight_3 * FOrienting(target_dist, target_angle, robot_phi) + \
    #          FStochastic()
    
    print "FTarget ", (weight_1*FTarget(target_dist, target_angle, robot_phi)), "Fobs ", (weight_2 * (Fobs_right - Fobs_left))

    FTotal = weight_1 * FTarget(target_dist, target_angle, robot_phi) + \
             weight_2 * (Fobs_right - Fobs_left) + \
             weight_3 * FOrienting(target_dist, target_angle, robot_phi) + \
             FStochastic()
             
    # turnrate: d phi(t) / dt = sum( forces ) 
    turnrate =  FTotal*delta_t
    
    # normalise turnrate value
    turnrate=turnrate/max_turnrate
    if turnrate>max_turnrate:
        turnrate=1.0
    elif turnrate<-max_turnrate:
        turnrate=-1.0

    return turnrate

if __name__=="__main__":
    pass
