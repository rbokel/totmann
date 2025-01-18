# lib
import os
from os import path
import tkinter as tk
import json

# 3rd party
from playsound import playsound
from platformdirs import user_data_dir

# local
from strings import STRINGS



def app_path(localPath):
    return path.join(path.dirname(__file__), localPath)


def app_data_path(localPath):
    return path.join(user_data_dir("Totmann", "org.qlod"), localPath)


class Model:
    STATE_INIT = "init"
    STATE_WAITING_FOR_TIMEOUT = "waiting-for-timeout"
    STATE_COUNTING_DOWN = "counting-down"
    STATE_ALARMING = "alarming"

    def __init__(self):
        self.state = Model.STATE_INIT
        self.countdown = 0
        self.on_change_state = None
        self.on_change_countdown = None
        self.alarm_length = 60
        self.countdown_length = 5 * 60
        self.timeout_length = 15 * 60
        self.lang = "en"
        self.load_settings()

    def set_state(self, state):
        self.state = state
        self.on_change_state()

    def set_countdown(self, countdown):
        self.countdown = countdown
        self.on_change_countdown()

    def decrement_countdown(self):
        self.set_countdown(self.countdown - 1)

    def switch_to_alarm(self):
        self.set_state(Model.STATE_ALARMING)
        self.set_countdown(self.alarm_length)

    def switch_to_countdown(self):
        self.set_state(Model.STATE_COUNTING_DOWN)
        self.set_countdown(self.countdown_length)

    def switch_to_timeout(self):
        self.set_state(Model.STATE_WAITING_FOR_TIMEOUT)
        self.set_countdown(self.timeout_length)

    def is_init(self):
        return self.state == Model.STATE_INIT

    def is_counting_down(self):
        return self.state == Model.STATE_COUNTING_DOWN

    def is_waiting_for_timeout(self):
        return self.state == Model.STATE_WAITING_FOR_TIMEOUT

    def is_alarming(self):
        return self.state == Model.STATE_ALARMING

    def is_timeout(self):
        return self.countdown == 0

    def repeat_alarm(self):
        self.switch_to_alarm()

    def update_time(self):
        self.decrement_countdown()

        if self.is_timeout():
            if self.is_waiting_for_timeout():
                self.switch_to_countdown()
            elif self.is_counting_down():
                self.switch_to_alarm()
            elif self.is_alarming():
                self.repeat_alarm()
            elif self.is_init():
                self.switch_to_timeout()

    def save_settings(self):
        settings = {
            "alarm_length": self.alarm_length,
            "countdown_length": self.countdown_length,
            "timeout_length": self.timeout_length,
            "lang": self.lang,
        }
        settings_file_path = app_data_path("settings.json")
        os.makedirs(os.path.dirname(settings_file_path), exist_ok=True)

        with open(settings_file_path, "w") as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open(app_data_path("settings.json"), "r") as f:
                settings = json.load(f)
                self.alarm_length = settings.get("alarm_length", 60)
                self.countdown_length = settings.get("countdown_length", 5 * 60)
                self.timeout_length = settings.get("timeout_length", 15 * 60)
                self.lang = settings.get("lang", "en")
        except FileNotFoundError:
            pass


class View:
    BUTTON_PAD = 30

    def __init__(self, root, controller, lang="en"):
        self.root = root
        self.controller = controller
        self.set_lang(lang)
        self.root.attributes("-topmost", True)

        self.countdown = tk.IntVar(value=5)
        self.timeout = tk.IntVar(value=15)
        self.alarm = tk.IntVar(value=1)

        self.render_settings_view()

    def set_lang(self, lang):
        self.lang = lang
        self.strings = STRINGS[self.lang]
        root.title(self.strings["TITLE"])

    def render_settings_view(self):
        self.remove_widgets()
        self.stop_timer()
        self.label = tk.Label(text=self.strings["TITLE"], font=("Arial", 32))
        self.label.pack()
        self.timeout_label = tk.Label(
            text=self.strings["TIMEOUT_LABEL_TEXT"], font=("Arial", 16)
        )
        self.timeout_label.pack()
        self.timeout_entry = tk.Entry(textvariable=self.timeout, font=("Arial", 16))
        self.timeout_entry.pack()

        self.countdown_label = tk.Label(
            text=self.strings["COUNTDOWN_LABEL_TEXT"], font=("Arial", 16)
        )
        self.countdown_label.pack()
        self.countdown_entry = tk.Entry(textvariable=self.countdown, font=("Arial", 16))
        self.countdown_entry.pack()

        self.alarm_label = tk.Label(
            text=self.strings["ALARM_LABEL_TEXT"], font=("Arial", 16)
        )
        self.alarm_label.pack()
        self.alarm_entry = tk.Entry(textvariable=self.alarm, font=("Arial", 16))
        self.alarm_entry.pack()

        self.button = tk.Button(
            text=self.strings["START_BUTTON_TEXT"],
            command=self.controller.handle_click_start,
            font=("Arial", 32),
        )
        self.button.pack(
            fill=tk.BOTH, expand=True, padx=View.BUTTON_PAD, pady=View.BUTTON_PAD
        )

    def render_main_view(self):
        self.remove_widgets()
        self.start_timer()
        self.label = tk.Label(text=self.strings["TITLE"], font=("Arial", 32))
        self.label.pack()
        self.button = tk.Button(
            text=self.strings["RESET_BUTTON_TEXT"],
            command=self.controller.handle_click_reset,
            font=("Arial", 32),
        )
        self.button.pack(
            fill=tk.BOTH, expand=True, padx=View.BUTTON_PAD, pady=View.BUTTON_PAD
        )

    def remove_widgets(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def start_timer(self):
        self.root.after(1000, self.controller.update_time)

    def stop_timer(self):
        self.root.after_cancel(self.controller.update_time)

    def update_label(self, time):
        text = self.strings["ALARM_TEXT"].format(minutes=time // 60, seconds=time % 60)
        self.label["text"] = text

    def hide_window(self):
        self.root.iconify()

    def show_window(self):
        self.root.deiconify()
        self.root.attributes("-topmost", True)
        self.root.update_idletasks()


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        model.on_change_state = self.handle_change_state
        model.on_change_countdown = self.handle_change_countdown

    def load_settings(self):
        self.model.load_settings()
        self.view.timeout.set(self.model.timeout_length // 60)
        self.view.countdown.set(self.model.countdown_length // 60)
        self.view.alarm.set(self.model.alarm_length // 60)
        self.view.set_lang(self.model.lang)

    def beep(self):
        print("BEEP!")
        playsound(app_path("beep.mp3"))
        playsound(app_path("hilfe.mp3"))

    def update_time(self):
        self.model.update_time()
        self.view.root.after(1000, self.update_time)

    def handle_change_countdown(self):
        time = self.model.countdown
        if self.model.is_waiting_for_timeout():
            time += self.model.countdown_length
        self.view.update_label(time)

    def handle_change_state(self):
        if self.model.is_waiting_for_timeout():
            self.view.hide_window()
        elif self.model.is_counting_down():
            self.view.show_window()
        elif self.model.is_alarming():
            self.view.show_window()
            self.beep()

    def handle_click_reset(self, event=None):
        self.model.switch_to_timeout()

    def handle_click_start(self, event=None):
        self.model.timeout_length = self.view.timeout.get() * 60
        self.model.countdown_length = self.view.countdown.get() * 60
        self.model.alarm_length = self.view.alarm.get() * 60
        self.model.lang = self.view.lang
        self.model.save_settings()
        self.model.switch_to_timeout()
        self.view.render_main_view()


if __name__ == "__main__":
    model = Model()
    root = tk.Tk()
    root.geometry("400x400")
    controller = Controller(model, None)
    view = View(root, controller)
    controller.view = view
    controller.load_settings()
    root.mainloop()
