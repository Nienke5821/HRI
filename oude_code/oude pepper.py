import nao_2_1_1 as nao
import time
import behaviour_based_navigation_nao_2 as bh
import qi
from naoqi import ALProxy
# Voor ons: eerste keer 1x wake up en autonomousoff

# life = ALProxy("ALAutonomousLife", ip, port)
# life.setState("disabled")
# motion_proxy.wakeUp()
# nao.Say("I have woken up")
# time.sleep(5)

# Navigate to a point (1 meter forward and 0.5 meters to the right)

ip="192.168.0.119"
port=9559

nao.InitProxy(ip,[0],port)


nao.Say("hello")
motion_proxy = ALProxy("ALMotion", ip, port)
# motion_proxy.wakeUp()
# nao.Say("I have woken up")
# time.sleep(5)
# motion_proxy.moveTo(0.2, 0, 0)
# nao.Say("I am done")

# nao.Say("I am detecting a landmark")
# time.sleep(1)
# nao.InitLandMark(True)
# detected, _, landmarkinfo = nao.DetectLandMark()
# while not detected:
#     detected, _, landmarkinfo = nao.DetectLandMark()
# nao.Say("detected")

# if detected:
#             data = nao.Tracker(switch=1, targetName='LandMark', targetParam=[0.09, landmarkinfo[0]])

life = ALProxy("ALAutonomousLife", ip, port)
life.setState("disabled")

motion_proxy.wakeUp()
# motion_proxy.setStiffnesses("Body", 1.0)
nao.Say("I have woken up")
time.sleep(5)
# nao.Crouch()
# navigation = ALProxy("ALNavigation", ip, port)
# navigation.navigateTo(1.5, 0)
# time.sleep(20)
            # print "data"
            # print(data)
            # print "end data"
            # yaw = nao.GetYaw()
# nao.Say(str(detected))
# navigation = ALProxy("ALNavigation", ip, port)
# navigation.navigateTo(0.2, 0.0)
# nao.Move(1,0,0) # stop moving
# nao.sleep(1)
#laserfindfunctie
# nao.Move(0,0,0)


# nao.InitSonar(True)
# moment = time.time()
# nao.InitPose()
# # nao.InitProxy()
# # nao.InitVideo(2)
# nao.InitLandMark(True)
# nao.InitTrack()