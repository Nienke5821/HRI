import nao_2_1_1 as nao
import time
import behaviour_based_navigation_nao_2 as bh
import qi
from naoqi import ALProxy
import demo_movements as movements
import demo_conversations as conversations
# import beckon
# import movement


# ip="127.0.0.1" #Virtual Robot ip
ip="192.168.0.119" #Actual Robot ip
port = 9559

# Voor ons: eerste keer 1x wake up en autonomousoff


motion = ALProxy("ALMotion", ip, port)
life = ALProxy("ALAutonomousLife", ip, port)
navigation = ALProxy("ALNavigation", ip, port)
# posture = ALProxy("ALRobotPosture", ip, port)
# posture = ALProxy("ALRobotPostureProxy", ip, port)
life.setState("disabled")
# 
memoryProxy = ALProxy("ALMemory", ip, 9559)
landmarkProxy = ALProxy("ALLandMarkDetection", ip, 9559)
landmarkProxy.subscribe("landmarkTest")
leds = ALProxy("ALLeds", ip, port)
eye_leds = "FaceLeds"
# life = ALProxy("ALAutonomousLife", ip, port)
# life.setState("disabled")
# def findTarget():
#     motion.setAngles("HeadYaw", -1, 0.2) # look left
#     detected = False
#     navigation.navigateTo(0.5, 0)
#     while not detected:
#         markData = memoryProxy.getData("LandmarkDetected")
#         nao.Say("I am starting to detect")
#         while (len(markData) == 0):
#             markData = memoryProxy.getData("LandMarkDetected")
#         print(markData)
#         detected = True
#         # leds.fadeRGB("FaceLeds", 0x0000FF, 0.1)
#         # detected, _, landmarkinfo = nao.DetectLandMark()
#         print(detected)
#         # time.sleep(2)
#         # print(detected)
#         # leds.fadeRGB("FaceLeds", 0x000000, 0.5)
#         # navigation.navigateTo(0.5, 0) # move one meter forwards
#         # print(detected)
#         # time.sleep(1)
#     nao.Say("I have detected the landmark")
#     # print(landmarkinfo)
#     # # nao.Say("detected")
#     # # print(landmarkinfo[0][0])
#     # landmarkNumber = landmarkinfo[0][0]
#     # return landmarkNumber
#     return 5

import math
def findTarget():
    detected = False
    motion.moveTo(0, 0, math.pi / 2)
    motion.setAngles("HeadYaw", 1.2, 0.2) # look left
    # detected = False
    # nao.Say("start while loop one")
    time.sleep(1)
    while not detected:
        direction = "correct"
        navigation.navigateTo(0.3, 0)
        time.sleep(2)
        detected, _, landmarkinfo = nao.DetectLandMark()
        print(detected)
        if detected:
            # nao.Say("detected")
            break
        motion.setAngles("HeadYaw", 0, 0.2)
        motion.moveTo(0, 0, math.pi/2)
        direction = "wall"
        if detected:
            # nao.Say("detected")
            break
        motion.setAngles("HeadYaw", 1.2, 0.2)
        motion.moveTo(0, 0,  - math.pi/2)
        direction = "correct"


        # distance to target
        #calculate distance target
    # nao.Say("exited while loop one")
    landmarkTheoreticalSize = 0.092
    memoryProxy = ALProxy("ALMemory", ip, 9559)
    landmarkProxy = ALProxy("ALLandMarkDetection", ip, 9559)
    landmarkProxy.subscribe("landmarkTest")
    markData = memoryProxy.getData("LandmarkDetected")
    
    while (len(markData) == 0):
        markData = memoryProxy.getData("LandMarkDetected")
    # nao.Say("detected")
    print(landmarkinfo)
    print(landmarkinfo[0][0])
    if direction == "wall":
        motion.setAngles("HeadYaw", 0, 0.2)
        motion.moveTo(0, 0, - math.pi)
    else: # correct
        motion.setAngles("HeadYaw", 0, 0.2)
        motion.moveTo(0, 0, - math.pi / 2)
    
    return landmarkinfo[0][0]


if __name__ == "__main__":
    nao.InitProxy(ip,[0],port)
    motion.wakeUp()
    #nao.Say("Come join, the tour is about to start!")
    # movements.wave()
    # conversations.start_dialog(ip, port)
     # start implementeren
    time.sleep(1)

    # introduction tekst
    # look for target and tell information
    conversations_had = 0
    landmarkNumber = 0
    while True:
        if conversations_had == 0:
            movements.wave(ip, port)
        elif landmarkNumber == 64 or landmarkNumber == 80:
            nao.Say("Gather around.")
            movements.gather_around(ip, port)
        elif landmarkNumber == 85:
            movements.point_to(ip, port)
        else:
             movements.hide_eyes(ip, port)
        # conversations.have_one_dialog(ip, port, landmarkNumber)
        nao.Tracker()
        if landmarkNumber == 0:
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
        nao.Tracker(0)
        print(landmarkNumber)
        conversations_had += 1
        if landmarkNumber == 64:
             movements.hide_eyes(ip, port)
             time.sleep(1)
        if conversations_had == 4:
            time.sleep(2)
            nao.Say("Now it is time to give me a big round of applause.")
            movements.bow(ip, port)
            time.sleep(5)
            break
        time.sleep(2)
        movements.join_turn
        time.sleep(1)
        landmarkNumber = findTarget()
        time.sleep(2)
        print("landmark detected", landmarkNumber)
        

    time.sleep(5)
    nao.Crouch()






