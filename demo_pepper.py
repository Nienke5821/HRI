# Import custom modules and standard libraries
import nao_2_1_1 as nao                   # Custom module containing helper functions for Nao robot
import time                               # Standard Python time module for delays
import behaviour_based_navigation_nao_2 as bh  # Custom behavior-based navigation module
import qi                                 # NAOqi framework module for connecting to the robot
from naoqi import ALProxy                 # Used to access robot modules (proxies)
import demo_movements as movements        # Custom module with Pepper's movement functions
import demo_conversations as conversations # Custom module with conversation dialogs
import math                               # Standard math module (used here for rotations in radians)

# Connect to either the virtual or actual Pepper robot
# ip = "127.0.0.1"  # Uncomment for virtual robot
ip = "192.168.0.119"  # IP address of the actual robot
port = 9559           # Default port for NAOqi communication

# Initialize proxies (interfaces to robot modules)
motion = ALProxy("ALMotion", ip, port)             # Controls movement and posture
life = ALProxy("ALAutonomousLife", ip, port)       # Controls autonomous behavior (e.g. idle postures)
navigation = ALProxy("ALNavigation", ip, port)     # Controls navigation
life.setState("disabled")                          # Disable autonomous behavior for manual control
memoryProxy = ALProxy("ALMemory", ip, port)        # Memory proxy used to retrieve sensor data
landmarkProxy = ALProxy("ALLandMarkDetection", ip, port)  # Used to detect NAO marks
landmarkProxy.subscribe("landmarkTest")            # Subscribe to landmark detection
leds = ALProxy("ALLeds", ip, port)                 # Control robot LEDs (not used directly in this script)
eye_leds = "FaceLeds"                              # Alias for facial LEDs


def findTarget():
    """
    Let Pepper locate the next target. It does this by turning 90 degrees left, turning its head also 90 degrees left,
    moving 30 centimeters forward, and looking for a target. If it is not found, it rotates its body another 90 degrees left,
    such that it is facing the wall. It moves its head 90 degrees right such that it looks forward. If it is not detected, it
    turns 90 degrees right, and its head 90 degrees left, and it once again moves 30 centimeters forward. This process is
    repeated untill the target is found. Once located, Pepper moves such that it is facing which its back towards the target,
    such that it is looking at the crowd.

    Returns:
        int: the number of the landmark it has detected.
    """
    detected = False  # Initially, no landmark is detected

    # Start scanning: rotate body 90 degrees left and head to the left
    motion.moveTo(0, 0, math.pi / 2)
    motion.setAngles("HeadYaw", 1.2, 0.2)  # Turn head left
    time.sleep(1)  # Wait for stabilization

    while not detected:
        direction = "correct"  # Assume parallel to the wall
        navigation.navigateTo(0.3, 0)  # Move 30 cm forward
        time.sleep(2)  # Wait for the move to complete

        # Try to detect a landmark
        detected, _, landmarkinfo = nao.DetectLandMark()
        if detected:
            break

        # If not detected, rotate to face the wall
        motion.setAngles("HeadYaw", 0, 0.2)  # Look straight
        motion.moveTo(0, 0, math.pi / 2)     # Turn 90° left to face the wall
        direction = "wall"

        if detected:
            break

        # Adjust to be parallel again and scan again
        motion.setAngles("HeadYaw", 1.2, 0.2)  # Look left
        motion.moveTo(0, 0, -math.pi / 2)      # Turn 90° right to become parallel again
        direction = "correct"


    # Resubscribe the proxies just in case
    memoryProxy = ALProxy("ALMemory", ip, 9559)
    landmarkProxy = ALProxy("ALLandMarkDetection", ip, 9559)
    landmarkProxy.subscribe("landmarkTest")

    # Poll until the landmark is available in memory
    markData = memoryProxy.getData("LandmarkDetected")
    while len(markData) == 0:
        markData = memoryProxy.getData("LandmarkDetected")
    
    # Reorient Pepper to face the audience (turn away from the landmark)
    if direction == "wall":
        motion.setAngles("HeadYaw", 0, 0.2)
        motion.moveTo(0, 0, -math.pi)  # Rotate 180° if facing wall
    else:
        motion.setAngles("HeadYaw", 0, 0.2)
        motion.moveTo(0, 0, -math.pi / 2)  # Rotate 90° if parallel

    return landmarkinfo[0][0]  # Return the ID of the detected landmark

# Main program loop
if __name__ == "__main__":
    # Connect to the robot using helper method
    nao.InitProxy(ip, [0], port)
    
    # Wake up the robot (activates motors)
    motion.wakeUp()

    landmarkNumber = 0  # Start of the tour, no landmark detected yet

    while True:
        # Enable face tracking while Pepper talks
        nao.Tracker()

        # Execute different behavior based on the current landmark
        if landmarkNumber == 0: # First conversation
            nao.Say("Welcome everybody! I am Pepper, I will be your tour guide for today! Are you ready to start the tour?")
            movements.wave(ip, port) # Gather attention, welcome people by waving
            conversations.have_one_dialog(ip, port, 0)
        elif landmarkNumber == 64:
            movements.gather_around(ip, port)
            nao.Say("Gather around. You are in for a ride! We are going to have so much fun together! Dont you think?")
            time.sleep(5)
            conversations.have_one_dialog(ip, port, 1)
            movements.hide_eyes(ip, port)
        elif landmarkNumber == 80:
            movements.gather_around(ip, port)
            nao.Say("Gather around. Atlas hosts a lot of fun activities don't you think?")
            time.sleep(4)
            conversations.have_one_dialog(ip, port, 2)
        elif landmarkNumber == 85:
            nao.Say("We just passed the PhD defense room. Did you see it?")
            movements.point_to(ip, port)
            conversations.have_one_dialog(ip, port, 3)
            nao.Say("Now it is time to give me a big round of applause.")
            movements.bow(ip, port)
            break # End the loop after final landmark
        else:
            # If an unknown landmark is detected
            movements.hide_eyes(ip, port)
            nao.Say("Unfortunately I do not have any information about this location.")

        # Turn off face tracking before searching for next landmark
        nao.Tracker(0)

         # Locate the next landmark
        movements.join_turn(ip, port) 
        landmarkNumber = findTarget()
        print("landmark detected", landmarkNumber)
    
    # After tour ends, wait a bit and crouch down
    time.sleep(5)
    nao.Crouch()






