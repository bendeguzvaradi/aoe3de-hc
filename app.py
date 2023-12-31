import tkinter as tk
import yaml
import keyboard
from pathlib import Path
from helpers import track_mouse_coordinates
from functions import get_rand_cards

# Check the platform
import platform
import pyautogui

if platform.system() == 'Windows':
    import pygetwindow as gw


class App(tk.Tk):

    def __init__(self, debug_mode: bool = False) -> None:
        super().__init__()

        with open(Path(__file__).parent / "ui_config.yaml", "r", encoding="utf-8") as conf:
            self.config = yaml.load(conf, Loader=yaml.FullLoader)
        with open(Path(__file__).parent / "civs_config.yaml", "r", encoding="utf-8") as conf:
            self.civs_config = yaml.load(conf, Loader=yaml.FullLoader)

        self.max_civ_cards = {civ:(21 if civ in ["United States", "Mexicans"] else 25) for civ, _ in self.civs_config.items()}
        
        # App settings
        self.title("AOE3 Random Card Selector")
        self.geometry("512x768")
        self.resizable(True, True)
        self.debug_mode = debug_mode
        if self.debug_mode:
            track_mouse_coordinates()

        self.Lb = None
        self.cards_display=tk.Text(self, width=80, height=15)
        self.cards_display.pack()

        # Add Age Limit option
        self.max_age_var = tk.StringVar()
        self.max_age_var.set("None")

        max_age_label = tk.Label(self, text="Max Age")
        max_age_label.pack()

        max_age_options = [None, "Age 1", "Age 2", "Age 3", "Age 4"]
        self.max_age_dropdown = tk.OptionMenu(self, self.max_age_var, *max_age_options)
        self.max_age_dropdown.pack()

        # Create a Scale widget for adjusting the moveTo duration
        self.duration_slider = tk.Scale(self, from_=0.1, to=2.0, resolution=0.01, orient=tk.HORIZONTAL, label='Speed (s)',
                                            command=self.get_move_duration)
        self.duration_slider.set(0.5)
        self.duration_slider.pack()

        self.res_x = None
        self.res_y = None

        self._setup_ui()
        self.get_clicked_civ()
        self.get_max_age()

    def _get_aoe3(self):
        if platform.system() == 'Windows':
            # Find the window by its title
            print(gw.getAllTitles())
            aoe3_window = gw.getWindowsWithTitle(self.config["aoe3name"])[0]
            if aoe3_window:
                # Maximize the window
                aoe3_window.activate()

                # Get the resolution of the active window
                self.res_x = aoe3_window.width
                self.res_y = aoe3_window.height
            else:
                raise TabError("Age of Empires III De not started!")
        elif platform.system() == 'Linux':
            raise NotImplementedError("Not yet implemented!")
        
    def get_clicked_civ(self) -> str:
        """Returns clicked civ from list."""
        selected_idx = self.Lb.curselection()
        self.after(1000, self.get_clicked_civ)
        if selected_idx:
            selected_element = self.Lb.get(selected_idx[0])
            return selected_element
        
    def get_max_age(self) -> int:
        """Return max age limit."""
        selected_age = self.max_age_var.get()
        self.after(1000, self.get_max_age)
        return self.config["age_options"][selected_age]

    def get_move_duration(self, value) -> float:
        """Return move duration."""
        self.get_move_duration = float(value)

    def _setup_ui(self) -> None:
        """Creates UI list."""
        self.Lb = tk.Listbox(self)
        for idx, key in enumerate(self.civs_config.keys()):
            self.Lb.insert(idx, key)
        self.Lb.pack()

        # Create the "Start Selection" button and disable it initially
        self.start_button = tk.Button(self, text="Start Selection", command=self.click_cards, state=tk.DISABLED)
        self.start_button.pack()

        # Schedule a function to enable/disable the button based on self.get_clicked_civ
        self.update_start_button_state()

    def update_start_button_state(self):
        """Enable the button if self.detect_selected_element is not None, otherwise disable it"""
        if self.get_clicked_civ is not None:
            self.start_button["state"] = tk.NORMAL
        else:
            self.start_button["state"] = tk.DISABLED

    def print_cards_to_ui(self, cards: list):
        """Prints selected random cards."""
        # Clear the current content if there is any
        if self.cards_display.get("1.0", tk.END):
            self.cards_display.delete("1.0", tk.END)
        for key, value in cards:
            self.cards_display.insert(tk.END,  f"Age: {key} Card: {value}\n")

    def click_cards(self):
        """Gets card dict and clicks on them."""

        # Focus to Age of Empires III
        self._get_aoe3()
        finished = False
                        
        automation_running = True

        cards_selected = get_rand_cards(self.max_civ_cards[self.get_clicked_civ()], self.civs_config[self.get_clicked_civ()], age_limit=self.get_max_age())
        self.print_cards_to_ui(cards_selected)

        posconf = self.config
        while automation_running and not finished:
            for idx, card in enumerate(cards_selected):
                age = card[0]
                age_num = f"age{age}"
                row_num = card[1]

                if row_num <= 15:
                    x = posconf["row1_start"][0] + posconf["col_card_distance"] * (row_num - 1)
                    conf_row = f"row1_start"
                elif row_num > 15 and row_num <= 30:
                    x = posconf["row2_start"][0] + posconf["col_card_distance"] * (row_num - 16)
                    conf_row = f"row2_start"
                elif row_num > 30 and row_num <= 45:
                    x = posconf["row3_start"][0] + posconf["col_card_distance"] * (row_num - 31)
                    conf_row = f"row3_start"
                else:
                    raise ValueError("Wrong card cooridnates found!")
                row_pos = (x, posconf[conf_row][1])

                def stop_automation():
                    nonlocal automation_running
                    automation_running = False

                # Listen for the ESC key
                keyboard.add_hotkey('esc', stop_automation)
                if cards_selected[idx-1][0] != cards_selected[idx][0]:
                    # Get Age
                    print(f"Selected Age {age_num}")
                    pyautogui.moveTo(posconf[age_num][0], posconf[age_num][1], duration=self.get_move_duration)
                    pyautogui.click()
                # Get Row
                print(f"Selected card {row_num}")
                pyautogui.moveTo(row_pos[0], row_pos[1], duration=self.get_move_duration)
                pyautogui.click()
            finished = True


def main():
    app = App(debug_mode=False)
    app.mainloop()


if __name__ == "__main__":
    main()
