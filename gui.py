import tkinter as tk
from tkinter import ttk

from calculator import (
    parse_position,
    calculate_distance,
    calculate_bearing,
    get_valid_charges
)

import mission_log

class FireControlApp:

    def __init__(self):

        self.root = tk.Tk()

        self.cards = []

        self.root.title(
            "Iron Nest Fire Control"
        )

        self.root.geometry(
            "700x800"
        )

        self.build_input_area()

        self.build_log_area()

        self.root.bind_all(
            "<MouseWheel>",
            self.on_mousewheel
        )

    def build_input_area(self):

        input_frame = ttk.Frame(
            self.root
        )

        input_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            input_frame,
            text="Gun Position"
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.gun_entry = ttk.Entry(
            input_frame,
            width=25
        )

        self.gun_entry.grid(
            row=0,
            column=1
        )

        ttk.Label(
            input_frame,
            text="Target Position"
        ).grid(
            row=1,
            column=0,
            sticky="w"
        )

        self.target_entry = ttk.Entry(
            input_frame,
            width=25
        )

        self.target_entry.grid(
            row=1,
            column=1
        )

        ttk.Label(
            input_frame,
            text="Starting Mission #"
        ).grid(
            row=2,
            column=0,
            sticky="w"
        )

        self.counter_entry = ttk.Entry(
            input_frame,
            width=25
        )

        self.counter_entry.insert(
            0,
            "1"
        )

        self.counter_entry.grid(
            row=2,
            column=1
        )

        ttk.Button(
            input_frame,
            text="Calculate Fire Mission",
            command=self.calculate
        ).grid(
            row=3,
            column=0,
            pady=10
        )

        ttk.Button(
            input_frame,
            text="Reset Mission Log",
            command=self.clear_log
        ).grid(
            row=3,
            column=1,
            pady=10
        )

        self.error_label = ttk.Label(
            self.root,
            foreground="red"
        )

        self.error_label.pack()

        # Current Fire Mission Area
        self.current_frame = tk.Frame(
            self.root,
            bd=2,
            relief="solid",
            bg="#d9d9d9"
        )

        self.current_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.current_card = tk.Frame(
            self.current_frame,
            bd=2,
            relief="solid",
            bg="#f2f2f2"
        )

        self.current_card.pack(
            fill="x",
            padx=5,
            pady=5
        )

    def build_log_area(self):

        ttk.Label(
            self.root,
            text="MISSION HISTORY",
            font=("Consolas", 12, "bold")
        ).pack(
            anchor="w",
            padx=10,
            pady=(10, 0)
        )
        self.canvas = tk.Canvas(
            self.root
        )

        scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.mission_container = ttk.Frame(
            self.canvas
        )

        self.mission_container.bind(
            "<Configure>",
            lambda e:
            self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.mission_container,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.current_frame = tk.Frame(
            self.root,
            bd=2,
            relief="solid"
        )

        self.current_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

    def on_mousewheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    def clear_log(self):

        for child in (self.mission_container.winfo_children()):
            child.destroy()

        self.cards.clear()

        mission_log.clear_history()

        mission_log.set_counter(int(self.counter_entry.get()))

    def calculate(self):

        try:

            gun_text = (
                self.gun_entry
                .get()
                .strip()
                .upper()
            )

            target_text = (
                self.target_entry
                .get()
                .strip()
                .upper()
            )

            current_mission = (
                gun_text,
                target_text
            )

            gun = parse_position(gun_text)

            target = parse_position(target_text)

            distance = calculate_distance(gun, target)

            bearing = calculate_bearing(gun,target)

            charges = get_valid_charges(distance)

            self.update_current_mission(
                gun_text,
                target_text,
                bearing,
                distance,
                charges
            )

            if not mission_log.mission_exists(current_mission):

                self.create_card(
                    gun_text,
                    target_text,
                    bearing,
                    distance,
                    charges
                )

                mission_log.add_mission(
                    current_mission
                )

                mission_log.increment_counter()

            self.error_label.config(text="")

        except Exception as ex:

            self.error_label.config(text=str(ex))

    def update_current_mission(
        self,
        gun,
        target,
        bearing,
        distance,
        charges
    ):

        # Clear current mission contents
        for widget in self.current_card.winfo_children():
            widget.destroy()

        # Recreate header
        tk.Label(
            self.current_card,
            text=f"Gun: {gun}",
            bg="#d9d9d9"
        ).pack(anchor="w", padx=5)

        tk.Label(
            self.current_card,
            text=f"Target: {target}",
            bg="#d9d9d9"
        ).pack(anchor="w", padx=5)

        tk.Label(
            self.current_card,
            text=f"Bearing: {bearing}°",
            bg="#d9d9d9"
        ).pack(anchor="w", padx=5)

        tk.Label(
            self.current_card,
            text=f"Range: {distance} km",
            bg="#d9d9d9"
        ).pack(anchor="w", padx=5)

        ttk.Separator(
            self.current_card
        ).pack(
            fill="x",
            pady=4
        )

        if not charges:

            tk.Label(
                self.current_card,
                text="NO VALID FIRING SOLUTION",
                fg="red",
                bg="#d9d9d9"
            ).pack(anchor="w", padx=10)

        else:

            for charge, elevation in charges:

                tk.Label(
                    self.current_card,
                    text=
                    f"Charge {charge} → {elevation}°",
                    bg="#d9d9d9"
                ).pack(
                    anchor="w",
                    padx=15
                )

    def create_card(
        self,
        gun,
        target,
        bearing,
        distance,
        charges
    ):

        mission_number = (mission_log.get_counter())

        card = tk.Frame(
            self.mission_container,
            bd=2,
            relief="solid",
            bg="#f2f2f2"
        )

        tk.Label(
            card,
            text=
            f"FIRE MISSION #{mission_number}",
            bg="#f2f2f2",
            font=(
                "Consolas",
                12,
                "bold"
            )
        ).pack(
            anchor="w",
            padx=5
        )

        tk.Label(
            card,
            text=f"Gun: {gun}",
            bg="#f2f2f2"
        ).pack(anchor="w", padx=5)

        tk.Label(
            card,
            text=f"Target: {target}",
            bg="#f2f2f2"
        ).pack(anchor="w", padx=5)

        tk.Label(
            card,
            text=f"Bearing: {bearing}°",
            bg="#f2f2f2"
        ).pack(anchor="w", padx=5)

        tk.Label(
            card,
            text=f"Range: {distance} km",
            bg="#f2f2f2"
        ).pack(anchor="w", padx=5)

        ttk.Separator(card).pack(
            fill="x",
            pady=4
        )

        if not charges:

            tk.Label(
                card,
                text=
                "NO VALID FIRING SOLUTION",
                fg="red",
                bg="#f2f2f2"
            ).pack(
                anchor="w",
                padx=5
            )

        else:

            for charge, elevation in charges:

                tk.Label(
                    card,
                    text=
                    f"Charge {charge} → {elevation}°",
                    bg="#f2f2f2"
                ).pack(
                    anchor="w",
                    padx=15
                )

        self.cards.insert(0, card)

        for widget in self.mission_container.winfo_children():
            widget.pack_forget()

        for widget in self.cards:
            widget.pack(
            fill="x",
            pady=5
            )

        self.canvas.yview_moveto(0)

    def run(self):
        self.root.mainloop()