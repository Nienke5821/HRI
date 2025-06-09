import nao_2_1_1 as nao
import time
import behaviour_based_navigation_nao_2 as bh
import qi
from naoqi import ALProxy
import demo_movements as movements
import demo_conversations as conversations
# import beckon
# import movement


ip="127.0.0.1" #Virtual Robot ip
#ip="192.168.0.119" #Actual Robot ip
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


def findTarget():
    detected = False
    motion.setAngles("HeadYaw", -1, 0.2) # look left
    # detected = False
    nao.Say("start while loop one")
    time.sleep(1)
    while not detected:
        navigation.navigateTo(0.3, 0)
        time.sleep(2)
        detected, _, landmarkinfo = nao.DetectLandMark()
        print(detected)


        # distance to target
        #calculate distance target
    nao.Say("exited while loop one")
    landmarkTheoreticalSize = 0.092
    memoryProxy = ALProxy("ALMemory", ip, 9559)
    landmarkProxy = ALProxy("ALLandMarkDetection", ip, 9559)
    landmarkProxy.subscribe("landmarkTest")
    markData = memoryProxy.getData("LandmarkDetected")
    
    while (len(markData) == 0):
        markData = memoryProxy.getData("LandMarkDetected")
    nao.Say("detected")
    print(landmarkinfo)
    print(landmarkinfo[0][0])


if __name__ == "__main__":
    nao.InitProxy(ip,[0],port)
    motion.wakeUp()
    #nao.Say("Come join, the tour is about to start!")
    # movements.wave()
    conversations.start_dialog(ip, port)
     # start implementeren
    target_found = False
    time.sleep(5)

    # introduction tekst
    # look for target and tell information
    # while True:
    # landmarkNumber = findTarget()

    time.sleep(5)
    nao.Crouch()






