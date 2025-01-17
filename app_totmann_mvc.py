from os import path
import tkinter as tk
from playsound import playsound


class Model:
    COUNTDOWN_LENGTH = 5 * 60
    TIMEOUT_LENGTH = 15 * 60
    STATE_INIT = "init"
    STATE_WAITING_FOR_TIMEOUT = "waiting-for-timeout"
    STATE_COUNTING_DOWN = "counting-down"

    def __init__(self):
        self.state = Model.STATE_INIT
        self.countdown = 0
        self.on_change_state = None
        self.on_change_countdown = None

    def update_state(self, value):
        self.state = value
        self.on_change_state()

    def update_countdown(self, value):
        self.countdown = value
        self.on_change_countdown()

    def reset_timeout(self):
        self.update_state(Model.STATE_WAITING_FOR_TIMEOUT)
        self.update_countdown(Model.TIMEOUT_LENGTH)

    def decrement_countdown(self):
        self.update_countdown(self.countdown - 1)

    def is_timeout(self):
        return self.countdown <= 0

    def switch_to_countdown(self):
        self.update_state(Model.STATE_COUNTING_DOWN)
        self.update_countdown(Model.COUNTDOWN_LENGTH)

    def is_init(self):
        return self.state == Model.STATE_INIT

    def is_counting_down(self):
        return self.state == Model.STATE_COUNTING_DOWN

    def is_waiting_for_timeout(self):
        return self.state == Model.STATE_WAITING_FOR_TIMEOUT

    def update_time(self):
        self.decrement_countdown()

        if self.is_timeout():
            if self.is_waiting_for_timeout():
                self.switch_to_countdown()
            elif self.is_counting_down():
                self.switch_to_countdown()
            elif self.is_init():
                self.reset_timeout()


class View:
    BUTTON_PAD = 80

    def init(self, root, controller):
        self.root = root
        self.controller = controller
        self.label = tk.Label(text="Totmann", font=("Arial", 32))
        self.label.pack()
        self.button = tk.Button(
            text="Hier \nberühren !",
            command=self.controller.handle_click,
            font=("Arial", 32),
        )
        self.button.pack(
            fill=tk.BOTH, expand=True, padx=View.BUTTON_PAD, pady=View.BUTTON_PAD
        )

    def update_label(self, text):
        self.label["text"] = text

    def hide_window(self):
        self.root.iconify()

    def show_window(self):
        self.root.deiconify()
        self.root.attributes("-topmost", True)
        self.root.update_idletasks()


class Controller:
    def init(self, model, view):
        self.model = model
        self.view = view

        model.on_change_state = self.handle_change_state
        model.on_change_countdown = self.handle_change_countdown

    def appPath(self, localPath):
        return path.join(path.dirname(__file__), localPath)

    def beep(self):
        print("BEEP!")
        playsound(self.appPath("beep.mp3"))
        playsound(self.appPath("hilfe.mp3"))

    def update_time(self):
        self.model.update_time()
        self.view.root.after(1000, self.update_time)

    def handle_change_countdown(self):
        self.view.update_label(self.model.countdown)

    def handle_change_state(self):
        if self.model.is_waiting_for_timeout():
            self.view.hide_window()
        elif self.model.is_counting_down():
            self.view.show_window()
            self.beep()

    def handle_click(self, event=None):
        self.model.reset_timeout()


if __name__ == "__main__":
    model = Model()
    root = tk.Tk()
    root.title("Totmann")
    root.geometry("400x400")
    controller = Controller(model, None)
    view = View(root, controller)
    controller.view = view
    root.after(1000, controller.update_time)
    root.mainloop()
