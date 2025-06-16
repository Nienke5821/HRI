from naoqi import ALProxy
import time


def have_one_dialog(ip, port, i):
    topic_paths = [
        "/home/nao/group_04/Introduction_enu.top",
        "/home/nao/group_04/Entrance_enu.top",
        "/home/nao/group_04/Middlefloor_enu.top",
        "/home/nao/group_04/Elevators_enu.top"
    ]

    try:
        dialog = ALProxy("ALDialog", ip, port)
        memory = ALProxy("ALMemory", ip, port)

        dialog.setLanguage("English")

        subscription_name = "dialog_sequence_{}".format(i)
        topic_name = dialog.loadTopic(topic_paths[i])
        dialog.activateTopic(topic_name)
        dialog.subscribe(subscription_name)
        dialog.forceInput("onStart")

        # Reset memory signal before dialog
        memory.insertData("my_dialog/finished", 0)

        # Wait until dialog writes to memory
        while memory.getData("my_dialog/finished") != 1:
            time.sleep(0.5)

        # Clean up
        dialog.unsubscribe(subscription_name)
        dialog.deactivateTopic(topic_name)
        dialog.unloadTopic(topic_name)

    except Exception as e:
        print("Error running dialogs:")
        print(e)

