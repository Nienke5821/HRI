import math
import random

degree = math.pi/180.0 # radians per degree

def FTarget(target_angle, robot_phi):
    """
    Computes attractor dynamics to target as mentioned in Thesis Elena Torta equation 3.3

    Args:
        target_angle (float): angle to the target with respect to the world frame
        robot_phi (float): current orientation of the robot

    Returns:
        float: attractor dynamics to target
    """
    Ftar = -math.sin(robot_phi - target_angle) 
    return Ftar

def FObstacle(obs_distance, obs_angle, robot_phi):
    """
    Computes repulsive dynamics to obstacles as mentioned in Thesis Elena Torta equation 3.4

    Args:
        obs_distance (numpy.float64): distance of obstacle
        obs_angle (float): angle to the obstacle
        robot_phi (float): current orientation of the robot

    Returns:
        float: repulsive dynamic to obstacles
    """
    too_far=10 #cm
    sigma_obs = 1 # angular range at which the repulsion strenght acts
    beta_2 = 1 # radial range at which the repulsion strenght acts
    if obs_distance < too_far: # only obstacle avoidance when close to object
        term_A = math.exp(-(robot_phi-obs_angle)**2 / (2*sigma_obs**2))*(robot_phi-obs_angle) 
        term_B = math.exp(-obs_distance / beta_2)
        Fobs = term_A * term_B
    else:
        Fobs = 0

    return Fobs

def FStochastic():
    """
    FStochastic adds noise to the turnrate force. This is just to make the simulation more realistic by adding some noie something useful here.
    
    Returns:
        float: noise value
    """
    Kstoch=0.03
    
    Fstoch = Kstoch*random.randint(1,100)/100.0

    return Fstoch

def FOrienting(target_distance, target_angle, robot_phi):
    """
    Computes attractor dynamics to desired final orientation as mentioned in Thesis Elena Torta equation 3.5

    Args:
        target_distance (numpy.float64): distance to the target
        target_angle (float): angle to the target with respect to the world frame
        robot_phi (float): current orientation of the robot 

    Returns:
        float: attractor dynamics to desired final orientation
    """
    Forient = -math.exp(-target_distance)*math.sin(robot_phi - target_angle)

    return Forient

def compute_velocity(sonar_distance_left, sonar_distance_right, target_angle, robot_phi):
    """
    Computes the velocity of the robot as mentioned in Thesis Elena Torta equation 3.6

    Args:
        sonar_distance_left (numpy.float64): distance to object from the left sonar sensor
        sonar_distance_right (numpy.float64): distance to object from the right sonar sensor
        target_angle (float): angle to the target with respect to the world frame
        robot_phi (float): current orientation of the robot 
    
    Returns:
        float: velocity of the robot
    """
    max_velocity = 0.3 #1.0
    epsilon = 1e-10 # small value term to avoid division by zero

    min_distance_obs = min(sonar_distance_left, sonar_distance_right)
    obs_term = math.exp(-1 / min_distance_obs + epsilon)
    
    heading_angle = math.exp(-abs(robot_phi - target_angle))

    velocity = min(obs_term, heading_angle) * max_velocity

    return velocity

def compute_turnrate(target_dist, target_angle, sonar_distance_left, sonar_distance_right, robot_phi):
    """
    Computes turnrate of the robot as mentioned in Thesis Elena Torta equation 3.1 and 3.2

    Args:
        target_distance (numpy.float64): distance to the target
        target_angle (float): angle to the target with respect to the world frame
        sonar_distance_left (numpy.float64): distance to object from the left sonar sensor
        sonar_distance_right (numpy.float64): distance to object from the right sonar sensor
        robot_phi (float): current orientation of the robot 
    
    Returns:
        float: turnrate of the robot
    """
    max_turnrate = 0.19 #0.349 #rad/s # may need adjustment!
    delta_t = 0.6 # may need adjustment!`
    sonar_angle_left = 30 * degree
    sonar_angle_right = -30 * degree
    
    Fobs_left = FObstacle(sonar_distance_left, sonar_angle_left, robot_phi)
    Fobs_right = FObstacle(sonar_distance_right, sonar_angle_right, robot_phi)

    # Weights of the forces
    weight_obs = 10
    weight_orient = 10
    weight_tar = 10 if (weight_obs * (Fobs_right - Fobs_left) < 0.01) else 0 # only make target force bigger when not close to object

    # Equation 3.2 in Thesis Elena Torta
    FTotal = weight_tar * FTarget(target_angle, robot_phi) + \
             weight_obs * (Fobs_right + Fobs_left) + \
             weight_orient * FOrienting(target_dist, target_angle, robot_phi) + \
             FStochastic()

    # Equation 3.1 in Thesis Elena Torta    
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
