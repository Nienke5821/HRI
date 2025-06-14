from naoqi import ALProxy
import time


def have_one_dialog(ip, port, landmark):
    topic_paths = [
        "/home/nao/group_04/Introduction_enu.top",
        "/home/nao/group_04/Entrance_enu.top",
        "/home/nao/group_04/Middlefloor_enu.top",
        "/home/nao/group_04/Elevators_enu.top"
    ]

    try:
        dialog = ALProxy("ALDialog", ip, port)
        tts = ALProxy("ALTextToSpeech", ip, port)
        memory = ALProxy("ALMemory", ip, port)

        dialog.setLanguage("English")
        tts.say("Starting dialog sequence.")
        topics = dialog.getLoadedTopics("English")
        print("topics")
        print(topics)
        topic_name_E = dialog.loadTopic("/home/nao/group_04/Entrance_enu.top")
        topic_name_I = dialog.loadTopic("/home/nao/group_04/Introduction_enu.top")
        # subscription_name = "dialog_sequence_{}".format(i)
        # dialog.unsubscribe("dialog_sequence_{}".format(0))
        dialog.deactivateTopic(topic_name_I)
        dialog.unloadTopic(topic_name_I)

        # dialog.unsubscribe("dialog_sequence_{}".format(1))
        dialog.deactivateTopic(topic_name_E)
        dialog.unloadTopic(topic_name_E)
        if landmark == 0: # set the correct conversation corresponding with the landmark it is standing infront of.
            print("introduction")
            i = 0
                
        elif landmark == 64:
                i = 1
        elif landmark == 80:
                i = 2
        elif landmark == 85:
                i = 3
        else:
             print("landmark not recognized")
        topics = dialog.getLoadedTopics("English")
        print("topics")
        print(topics)
        subscription_name = "dialog_sequence_{}".format(i)
        topic_name = dialog.loadTopic(topic_paths[i])
        dialog.activateTopic(topic_name)
        dialog.subscribe(subscription_name)
        dialog.forceInput("onStart")

        # Reset memory signal before dialog
        memory.insertData("my_dialog/finished", 0)

        # Wait until dialog writes to memory (with timeout)
        max_wait = 40  # seconds
        waited = 0
        while memory.getData("my_dialog/finished") != 1 and waited < max_wait:
            time.sleep(0.5)
            waited += 0.5

        if waited >= max_wait:
            tts.say("Timeout waiting for dialog to finish.")

        # Clean up
        dialog.unsubscribe(subscription_name)
        dialog.deactivateTopic(topic_name)
        dialog.unloadTopic(topic_name)

        # tts.say("All dialogs completed.")

    except Exception as e:
        print("Error running dialogs:")
        print(e)

