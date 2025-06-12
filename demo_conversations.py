from naoqi import ALProxy
import time

def start_dialog(ip, port):
    topic_paths = [
        "/home/nao/dialogs/Introduction_enu.top",
        "/home/nao/dialogs/Entrance_enu.top",
        "/home/nao/dialogs/Middlefloor_enu.top",
        "/home/nao/dialogs/Elevators_enu.top"
    ]

    try:
        dialog = ALProxy("ALDialog", ip, port)
        tts = ALProxy("ALTextToSpeech", ip, port)
        memory = ALProxy("ALMemory", ip, port)

        dialog.setLanguage("English")
        tts.say("Starting dialog sequence.")
        
        for i, path in enumerate(topic_paths):
            subscription_name = "dialog_sequence_{}".format(i)
            topic_name = dialog.loadTopic(path)
            dialog.activateTopic(topic_name)
            dialog.subscribe(subscription_name)

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

        tts.say("All dialogs completed.")

    except Exception as e:
        print("Error running dialogs:")
        print(e)
