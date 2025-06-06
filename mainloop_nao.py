import nao_2_1_1 as nao
import time
import behaviour_based_navigation_nao_2 as bh

def testwalking():
    print "Test basic walking ... ",
    try:
        nao.InitSonar(True)
        nao.InitPose()
        nao.Move(1,0,0.2)
        [SL, SR]=nao.ReadSonar()
        print "sonar"
        print SL
        time.sleep(3)
        nao.Move(0,0,0)
        nao.Walk(-0.3, 0, -0.2)
        nao.Crouch()
        succeeded=True
        print "succeeded."
        nao.InitSonar(False)
    except:
        succeeded=False
        print "failed."

def testSonar():
    nao.InitSonar(True)
    moment = time.time()
    nao.InitPose()
    # nao.InitProxy()
    # nao.InitVideo(2)
    nao.InitLandMark(True)
    nao.InitTrack()
    while True:
        # [SL, SR]=nao.ReadSonar()
        # # print SR
        # vel = bh.compute_velocity(SL, SR)
        # tr = bh.compute_turnrate()
        detected, _, landmarkinfo = nao.DetectLandMark()
        print(detected)
        # # print(detected)
        # print marinfo
        # # nao.Move(vel, 0, 0)
        moment2 = time.time()
        if moment2 - moment >= 30:
            break
        if detected:
            data = nao.Tracker(switch=1, targetName='LandMark', targetParam=[0.09, landmarkinfo[0]])
            print "data"
            print(data)
            print "end data"
            yaw = nao.GetYaw()
    nao.InitSonar(False)
    # nao.InitProxy(False)
    nao.InitLandMark(False)
    nao.Crouch()
    nao.EndTrack()

import math
from naoqi import ALProxy
import almath



def initialize():
    
    
    
    nao.InitProxy(ip,[0],port)
    nao.InitSonar(True)
    moment = time.time()
    nao.InitPose()
    # nao.InitProxy()
    # nao.InitVideo(2)
    nao.InitLandMark(True)
    nao.InitTrack()

def detectTheLM():
    detected = False
    while not detected:
        nao.Move(0, 0, 0.5, 1)
        time.sleep(3)
        nao.Move(0,0,0,1)
        time.sleep(1)
        detected, _, landmarkinfo = nao.DetectLandMark()
        print(detected)
        return detected, landmarkinfo

if __name__=="__main__":
    try:
        ip="192.168.0.102"
        port=9559
        initialize()
        
        # detected, landmarkinfo = detectTheLM()
        detected = False
        while not detected:
            nao.Move(0, 0, 0.5, 1)
            time.sleep(2)
            nao.Move(0,0,0,1)
            time.sleep(1)
            detected, _, landmarkinfo = nao.DetectLandMark()
            print(detected)


        # distance to target
        #calculate distance target
        landmarkTheoreticalSize = 0.092
        memoryProxy = ALProxy("ALMemory", ip, 9559)
        landmarkProxy = ALProxy("ALLandMarkDetection", ip, 9559)
        landmarkProxy.subscribe("landmarkTest")
        markData = memoryProxy.getData("LandmarkDetected")
        
        while (len(markData) == 0):
            markData = memoryProxy.getData("LandMarkDetected")
        print(landmarkinfo)
        angularSize = markData[1][0][0][3]
        distanceFromCameraToLandmark = landmarkTheoreticalSize / ( 2 * math.tan( angularSize / 2))
        


        turnrate = 0
        #move towards target
        while distanceFromCameraToLandmark > 0.2:
            detected, _, landmarkinfo = nao.DetectLandMark()
            while not detected:
                if turnrate >= 0:
                    nao.Move(0, 0, -0.3, 1)
                else:
                    nao.Move(0,0,0.3,1)
                time.sleep(1)
                nao.Move(0,0,0,1)
                time.sleep(1)
                detected, _, landmarkinfo = nao.DetectLandMark()
                print(detected)
            print("start while loop")
            memoryProxy = ALProxy("ALMemory", ip, 9559)
            markData = memoryProxy.getData("LandmarkDetected")
        
            while (len(markData) == 0):
                markData = memoryProxy.getData("LandMarkDetected")
            print(landmarkinfo)
            angularSize = markData[1][0][0][3]
            distanceFromCameraToLandmark = landmarkTheoreticalSize / ( 2 * math.tan( angularSize / 2))
            print(distanceFromCameraToLandmark)


            #move
            [SL, SR]=nao.ReadSonar()
            print("sonar", SL, SR)
            velocity = bh.compute_velocity(SL, SR)
            print("velocity", velocity)
            yaw = nao.GetYaw()
            turnrate = bh.compute_turnrate(distanceFromCameraToLandmark, yaw[0], SL, SR, 0)
            print("turnrate", turnrate)
            # turnrate = 0
            nao.Move(velocity, 0, turnrate, 1)
            time.sleep(3)
            # detected, _, landmarkinfo = nao.DetectLandMark()
            # while not detected:
            #     print("detecting 148")
            #     detected, _, landmarkinfo = nao.DetectLandMark()
            # print("detected 145", detected)
            # nao.Tracker(switch=1, targetName='LandMark', targetParam=[0.09, landmarkinfo[0]])
            # time.sleep(2)
            nao.Move()
            time.sleep(1)
            # detected, _, landmarkinfo = nao.DetectLandMark()
            # while not detected:
            #     print("detecting 156", detected)
            #     detected, _, landmarkinfo = nao.DetectLandMark()
            # print("detectd", detected)
    except Exception as e:
        print("There is an error")
        print(e)
    finally:
        nao.InitSonar(False)
        # nao.InitProxy(False)
        nao.InitLandMark(False)
        nao.Crouch()
        nao.EndTrack()



        
    

    


"""
stap 1: vind je doel
	loop: draai rond met hoofd 
    functie: MoveHead(yaw_val=0, pitch_val=0, isAbsolute=True, post=True, timeLists= [[1],[1]])

stap 2: verplaats lichaam richting hoofd
    functie: Move(dx=0, dy=0, dtheta=0, freq=1)

stap 3: verplaats naar doel
    functie: compute_turnrate(target_dist, target_angle, sonar_distance_left, sonar_distance_right, robot_phi) and compute_velocity(SL, SR)
    als lichaam naar links draait hoofd naar rechts draaien

    http://doc.aldebaran.com/1-14/dev/python/examples/vision/landmark.html
    distanceFromCameraToLandmark = landmarkTheoreticalSize / ( 2 * math.tan( angularSize / 2))



#later aanpassen
afstand tot target vergroten wanneer je loop uitgaat
tijdens lopen turnrate omlaag
"""