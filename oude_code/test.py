import nao_2_1_1 as nao
import time
import behaviour_based_navigation_nao_2 as bh
import qi
from naoqi import ALProxy
# import beckon
import movement



# motion_proxy.wakeUp()
# nao.Say("I have woken up")
# time.sleep(5)
def hello():
	names = list()
	times = list()
	keys = list()

	names.append("LElbowRoll")
	times.append([1, 1.5, 2, 2.5])
	keys.append([-1.02102, -0.537561, -1.02102, -0.537561])

	names.append("LElbowYaw")
	times.append([1, 2.5])
	keys.append([-0.66497, -0.66497])

	names.append("LHand")
	times.append([2.5])
	keys.append([0.66])

	names.append("LShoulderPitch")
	times.append([1, 2.5])
	keys.append([-0.707571, -0.707571])

	names.append("LShoulderRoll")
	times.append([1, 2.5])
	keys.append([0.558505, 0.558505])

	names.append("LWristYaw")
	times.append([1, 2.5])
	keys.append([-0.0191986, -0.0191986])
	names2=["LElbowRoll","LElbowYaw","LHand","LShoulderPitch","LShoulderRoll","LWristYaw"]
	angles=[-0.479966,-0.561996,0.66,1.30202,0.195477, -0.637045]
	motion = ALProxy("ALMotion", ip, 9559)
	motion.setExternalCollisionProtectionEnabled("Arms", False)
	tts = ALProxy("ALTextToSpeech",ip, port)
	tts.setParameter("speed", 100)
	tts.setLanguage("English")
	motion.angleInterpolation(names, keys, times, True)
	tts.say("Hello")
	motion.setAngles(names2,angles,0.3)
# Navigate to a point (1 meter forward and 0.5 meters to the right)

ip="192.168.0.116"
port=9559



nao.InitProxy(ip,[0],port)

# Voor ons: eerste keer 1x wake up en autonomousoff

nao.Say("hello")
motion = ALProxy("ALMotion", ip, port)
life = ALProxy("ALAutonomousLife", ip, port)
posture = ALProxy("ALRobotPosture", ip, port)
# posture = ALProxy("ALRobotPostureProxy", ip, port)
# life.setState("disabled")
# 
# life = ALProxy("ALAutonomousLife", ip, port)
# life.setState("disabled")
motion.wakeUp()
# nao.InitPose()
time.sleep(5)
nao.Say("I have woken up")

# Wake up the robot
# motion.wakeUp()
movement.beckon()
time.sleep(5)
# beckon()
nao.Say("beckon is done")
time.sleep(1)
movement.welcoming()
time.sleep(5)
nao.Say("welcoming is done")
time.sleep(1)
movement.attentionGesture0()
time.sleep(5)
nao.Say("gesture zero is done")
time.sleep(1)
movement.attentionGesture1()
time.sleep(5)
nao.Say("gesture one is done")
time.sleep(1)
movement.attentionGesture2()
time.sleep(5)
nao.Say("gesture two is done")
time.sleep(1)
movement.attentionGesture3()
time.sleep(5)
nao.Say("gesture three is done")
time.sleep(1)
movement.attentionGesture4()
time.sleep(5)
nao.Say("gesture four is done")
time.sleep(1)
movement.attentionGesture15()
time.sleep(5)
nao.Say("gesture one five is done")
time.sleep(1)
movement.attentionGesture25()
time.sleep(5)
nao.Say("gesture two five is done")
nao.Say("I am finished")
nao.Crouch()

# print(posture.getPostureList())
# nao.InitLandMark(True)
# detected, _, landmarkinfo = nao.DetectLandMark()
# print(landmarkinfo)

# while not detected:
#     detected, _, landmarkinfo = nao.DetectLandMark()
# nao.Say("detected")
# print(landmarkinfo[0][0])
# if detected:
#             data = nao.Tracker(switch=1, targetName='LandMark', targetParam=[0.09, landmarkinfo[0]])


# time.sleep(5)



	








""""
navigation = ALProxy("ALNavigation", ip, port)
navigation.navigateTo(1.5, 0)
time.sleep(20)
"""


