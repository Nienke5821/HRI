import nao_2_1_1 as nao
import time
import behaviour_based_navigation_nao_2 as bh
import qi
from naoqi import ALProxy
import demo_movements as movements
import demo_conversations as conversations
import math


# ip="127.0.0.1" #Virtual Robot ip
ip="192.168.0.119" #Actual Robot ip
port = 9559


# Initalize all the proxies we need
motion = ALProxy("ALMotion", ip, port)
life = ALProxy("ALAutonomousLife", ip, port)
navigation = ALProxy("ALNavigation", ip, port)
life.setState("disabled") # we turn autonomous mode off
memoryProxy = ALProxy("ALMemory", ip, 9559)
landmarkProxy = ALProxy("ALLandMarkDetection", ip, 9559)
landmarkProxy.subscribe("landmarkTest")
leds = ALProxy("ALLeds", ip, port)
eye_leds = "FaceLeds"


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
    detected = False # not detected
    motion.moveTo(0, 0, math.pi / 2) # rotate 90 degrees left
    motion.setAngles("HeadYaw", 1.2, 0.2) # look left
    time.sleep(1)
    while not detected:
        direction = "correct" # standing parallel with the wall
        navigation.navigateTo(0.3, 0) # move 30 centimeters forward
        time.sleep(2)
        detected, _, landmarkinfo = nao.DetectLandMark() # try to detect the landmark
        if detected: # the landmark has been found, so we discontinue the loop
            break
        # the landmark is not detected
        motion.setAngles("HeadYaw", 0, 0.2) # look forward
        motion.moveTo(0, 0, math.pi/2) # standing facing the wall
        direction = "wall"
        if detected:# landmark has been found, discontinue the loop
            break
        motion.setAngles("HeadYaw", 1.2, 0.2) # look left
        motion.moveTo(0, 0,  - math.pi/2) # move right such that pepper is parallel with the wall
        direction = "correct" # standing parallel with the wall


    # get the proxies we need
    memoryProxy = ALProxy("ALMemory", ip, 9559)
    landmarkProxy = ALProxy("ALLandMarkDetection", ip, 9559)
    landmarkProxy.subscribe("landmarkTest")
    markData = memoryProxy.getData("LandmarkDetected")
    
    while (len(markData) == 0): # the landmark is not detected
        markData = memoryProxy.getData("LandMarkDetected") # detect the landmark
    print(landmarkinfo[0][0]) # we can see whether it detects the correct landmark
    if direction == "wall": # faced towards wall, has to rotate 180 degrees
        motion.setAngles("HeadYaw", 0, 0.2) # look forward
        motion.moveTo(0, 0, - math.pi) # rotate body 180 degrees
    else: # positioned parallel with wall, has to rotate 90 degrees right
        motion.setAngles("HeadYaw", 0, 0.2) # look forward
        motion.moveTo(0, 0, - math.pi / 2) # rotate body 90 degrees to the right
    
    return landmarkinfo[0][0] # return the landmarknumber


if __name__ == "__main__":
    nao.InitProxy(ip,[0],port) # connect to Pepper
    motion.wakeUp() # make Pepper "alive" with autonomous mode turned off
    time.sleep(1)
    conversations_had = 0
    landmarkNumber = 0 # initial value, starting point of tour, no landmark is detected yet so we set this to 0
    while True: # endless loop
        # first have the conversation matching the landmark
        if conversations_had == 0: 
            movements.wave(ip, port) # gather attention, welcome people by waving
        elif landmarkNumber == 64 or landmarkNumber == 80: # want people to know pepper wants to say someting
            nao.Say("Gather around.")
            movements.gather_around(ip, port)
        elif landmarkNumber == 85: # Pepper talks about something it just passed, so it points to it
            movements.point_to(ip, port)
        else: # Pepper does not have any text for this landmark, so it covers its eyes
             movements.hide_eyes(ip, port)
        # conversations.have_one_dialog(ip, port, landmarkNumber) # normally we do this and in this function it selects the
        # corresponding conversation, however, the implementation does not work so we have implemented something else that
        # shows the conversations and what is said in there
        nao.Tracker() # track faces while pepper is talking
        if landmarkNumber == 0: # first conversation
            nao.Say("Here I welcome you to my tour. This is the first conversation.")
        elif landmarkNumber == 64:
                nao.Say("Here you can find the restaurant Brownies and Downies. This is the second conversation. I make a joke that I hope I don't fall of the stairs.")
        elif landmarkNumber == 80:
                nao.Say("Atlas organises a lot of activities. This is the third conversation.")
        elif landmarkNumber == 85:
                nao.Say("We just passed the PhD defense room. Here I tell you something about intermate. This is the fourth conversation. ")
        else:
             nao.Say("Unfortunately I do not have any information about this location.")
        time.sleep(3)
        nao.Tracker(0) # turn face tracker off such that it can focus on finding the next landmark
        print(landmarkNumber)
        conversations_had += 1
        if landmarkNumber == 64: # nao makes a joke, and it makes a corresponding movement
             movements.hide_eyes(ip, port)
             time.sleep(1)
        if conversations_had == 4: # all conversations have been had
            time.sleep(2)
            nao.Say("Now it is time to give me a big round of applause.")
            movements.bow(ip, port)
            time.sleep(5)
            break # quit the loop
        time.sleep(2)
        movements.join_turn
        time.sleep(1)
        landmarkNumber = findTarget() # move to the next target
        time.sleep(2)
        print("landmark detected", landmarkNumber)
        

    time.sleep(5)
    nao.Crouch()






