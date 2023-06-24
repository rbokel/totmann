import tkinter as tk
from playsound import playsound

_COUNTDOWN_LENGTH = 3*60
_TIMEOUT_LENGTH = 15*60

_countdown_timer = None

# Create a window
window = tk.Tk()
window.title("Totmann")
window.geometry("400x400")
# add a label
label = tk.Label(text="Totmann", font=("Arial", 32))
label.pack()

# add a button
def handle_click():
    global _countdown_timer
    
    window.iconify()
    if _countdown_timer is None:
        window.after(_TIMEOUT_LENGTH*1000, update_time)
        return
    
    window.after_cancel(_countdown_timer)
    _countdown_timer = None



button = tk.Button(text="Click me!",command=handle_click, font=("Arial", 32))
button.pack(fill=tk.BOTH, expand=True)

# run a timer every second
def lift_window(window):
    window.deiconify()
    window.attributes('-topmost', True)
    window.update_idletasks()  # get window on top
    # window.attributes('-topmost', False)  # prevent permanent focus 
    # window.focus_force()  # focus to the window

def countdown(count):
    global _countdown_timer

    # change text in label        
    label['text'] = count

    if count > 0:
        # call countdown again after 1000ms (1s)
        _countdown_timer= window.after(1000, countdown, count-1)
        if count == 120 or count == 60 :
            playsound('beep-08b.mp3')
    else:
        print("do alarm")
        playsound('beep-08b.mp3')
        # playsound('alarm.mp3')



def update_time():
    print("update_time")
    lift_window(window)
    countdown(_COUNTDOWN_LENGTH)


update_time()

# Run the main window loop
window.mainloop()
