import tkinter as tk
from playsound import playsound

_COUNTDOWN_LENGTH = 1*60
_TIMEOUT_LENGTH = 8 * 60
_REPEAT_LENGTH = 6

state = "waiting-for-timeout"
countdown = _TIMEOUT_LENGTH

def beep():
    print("BEEP!")
    playsound("beep.mp3")

def alert():
    print("ALERT!")
    playsound("alarm.mp3", block=False)

def hideWindow():
    window.iconify()

def showWindow():
    window.deiconify()
    window.attributes('-topmost', True)
    window.update_idletasks() 

def update_label():
    label['text'] = countdown
    
def update_time():
    global state, countdown

    countdown -= 1
    update_label()
    window.after(1000, update_time)

    if state == "waiting-for-timeout":
        hideWindow()
        if countdown <= 0:
            state = "counting-down-1"
            countdown = _COUNTDOWN_LENGTH
    elif state == "counting-down-1":
        showWindow()
        if countdown <= 0:
            beep()
            state = "counting-down-2"
            countdown = _COUNTDOWN_LENGTH
    elif state == "counting-down-2":
        showWindow()
        if countdown <= 0:
            beep()
            state = "counting-down-3"
            countdown = _COUNTDOWN_LENGTH
    elif state == "counting-down-3":
        showWindow()
        if countdown <= 0:
            beep()
            state = "timeout"
            countdown = _COUNTDOWN_LENGTH
    elif state == "timeout":
        if countdown <= 0:
            beep()
            countdown =_REPEAT_LENGTH
    

def handle_click():
    global state, countdown

    state = "waiting-for-timeout"
    countdown = _TIMEOUT_LENGTH    

# Create a window
window = tk.Tk()
window.title("Totmann")
window.geometry("400x400")

label = tk.Label(text="Totmann", font=("Arial", 32))
label.pack()

button = tk.Button(text="Click me!",command=handle_click, font=("Arial", 32))
button.pack(fill=tk.BOTH, expand=True)

window.after(1000, update_time)
window.mainloop()
