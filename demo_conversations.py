from naoqi import ALProxy  # Import ALProxy to connect to Pepper's modules
import time  # Time module for adding delays

def have_one_dialog(ip, port, i):
    """
    Executes a single dialog interaction based on the given index.
    Loads a .top file, activates it, and waits until the dialog finishes (as flagged in memory).

    Args:
        ip (str): IP address of the robot.
        port (int): Port number (usually 9559).
        i (int): Index to choose which dialog topic to run.
    """

    # List of predefined dialog topic files for different tour locations
    topic_paths = [
        "/home/nao/group_04/Introduction_enu.top",     # Index 0 - Introduction
        "/home/nao/group_04/Entrance_enu.top",         # Index 1 - Entrance area
        "/home/nao/group_04/Middlefloor_enu.top",      # Index 2 - Middle of the floor
        "/home/nao/group_04/Elevators_enu.top"         # Index 3 - Near the elevators
    ]

    try:
        # Create proxies to the Dialog and Memory modules
        dialog = ALProxy("ALDialog", ip, port)
        memory = ALProxy("ALMemory", ip, port)

        # Set dialog language to English
        dialog.setLanguage("English")

        # Generate a unique subscription name for this dialog instance
        subscription_name = "dialog_sequence_{}".format(i)

        # Load the corresponding dialog topic (.top file)
        topic_name = dialog.loadTopic(topic_paths[i])

        # Activate the loaded topic so it's ready to run
        dialog.activateTopic(topic_name)

        # Subscribe to start the dialog interaction
        dialog.subscribe(subscription_name)

        # Before starting, make sure the 'finished' flag is reset
        memory.insertData("my_dialog/finished", 0)

        # Wait until the dialog finishes; the .top file must include a script to set this flag
        while memory.getData("my_dialog/finished") != 1:
            time.sleep(0.5)  # Poll every half second

        # Once finished, clean up:
        dialog.unsubscribe(subscription_name)     # Stop dialog subscription
        dialog.deactivateTopic(topic_name)        # Deactivate the topic
        dialog.unloadTopic(topic_name)            # Unload the topic from memory

    except Exception as e:
        # If any error occurs during dialog setup or execution, print it
        print("Error running dialogs:")
        print(e)
