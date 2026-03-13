import tkinter as tk
from tkinter import ttk
from typing import Callable, List, Tuple


class CalculatorView(tk.Tk):
    """
    GUI / View layer for the calculator.

    It exposes callbacks that the controller can attach to:
      - on_button_press(symbol: str)
      - on_command(name: str)
      - on_key_press(event)
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("Zenith_Calc")
        # Allow the window to be resized
        self.resizable(True, True)

        # Theme state
        self._theme = "light"

        # Controller callbacks (to be set by controller)
        self.on_button_press: Callable[[str], None] = lambda _s: None
        self.on_command: Callable[[str], None] = lambda _c: None

        self._build_widgets()
        self._apply_theme()

    # --------------------------------------------------------------------- UI
    def _build_widgets(self) -> None:
        # Make root grid resizable
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        main = ttk.Frame(self, padding=8)
        main.grid(row=0, column=0, sticky="nsew")
        # Configure rows/columns in main frame for responsive layout
        for c in range(6):
            main.columnconfigure(c, weight=1)
        # Let history and button area grow
        main.rowconfigure(2, weight=1)
        main.rowconfigure(4, weight=1)
        main.rowconfigure(5, weight=1)

        # Display entry
        self.display_var = tk.StringVar()
        self.display = ttk.Entry(
            main, textvariable=self.display_var, font=("Consolas", 18), justify="right"
        )
        self.display.grid(row=0, column=0, columnspan=6, sticky="ew", pady=(0, 4))
        self.display.focus_set()

        # Info bar (angle mode, error, etc.)
        self.info_var = tk.StringVar(value="")
        self.info_label = ttk.Label(main, textvariable=self.info_var, anchor="e")
        self.info_label.grid(row=1, column=0, columnspan=6, sticky="ew", pady=(0, 4))

        # History area
        history_frame = ttk.Frame(main)
        history_frame.grid(row=2, column=0, columnspan=6, sticky="ew", pady=(0, 4))
        ttk.Label(history_frame, text="History").pack(side="left")
        self.history_text = tk.Text(
            history_frame,
            height=4,
            width=40,
            state="disabled",
            font=("Consolas", 10),
        )
        self.history_text.pack(side="right", fill="both", expand=True)

        # Mode / theme buttons
        toolbar = ttk.Frame(main)
        toolbar.grid(row=3, column=0, columnspan=6, sticky="ew", pady=(0, 4))
        self.mode_button = ttk.Button(toolbar, text="Scientific Mode", command=self._toggle_mode_clicked)
        self.mode_button.pack(side="left")
        self.theme_button = ttk.Button(toolbar, text="Dark Theme", command=self._toggle_theme_clicked)
        self.theme_button.pack(side="right")

        # Frames for basic and scientific buttons
        self.basic_frame = ttk.Frame(main)
        self.basic_frame.grid(row=4, column=0, columnspan=6, sticky="nsew")

        self.sci_frame = ttk.Frame(main)
        self.sci_frame.grid(row=5, column=0, columnspan=6, sticky="nsew")

        # Build button layouts
        self._build_basic_buttons(self.basic_frame)
        self._build_scientific_buttons(self.sci_frame)

        # Start in basic mode (hide scientific frame)
        self.sci_frame.grid_remove()

        # Keyboard bindings: let Entry handle normal typing, we only handle control keys
        self.bind("<Return>", self._on_enter)
        self.bind("<BackSpace>", self._on_backspace)
        self.bind("<Escape>", self._on_clear)

    def _build_basic_buttons(self, frame: ttk.Frame) -> None:
        buttons = [
            ["MC", "MR", "M+", "M-"],
            ["CE", "C", "⌫", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="],
        ]

        for r, row in enumerate(buttons):
            for c, label in enumerate(row):
                if label == "=":
                    cmd = lambda l=label: self._command_clicked("equals")
                elif label in {"C", "CE"}:
                    cmd = lambda l=label: self._command_clicked(l)
                elif label == "⌫":
                    cmd = lambda: self._command_clicked("backspace")
                elif label == "MC":
                    cmd = lambda: self._command_clicked("MC")
                elif label == "MR":
                    cmd = lambda: self._command_clicked("MR")
                elif label == "M+":
                    cmd = lambda: self._command_clicked("M+")
                elif label == "M-":
                    cmd = lambda: self._command_clicked("M-")
                elif label == "±":
                    cmd = lambda: self._command_clicked("negate")
                else:
                    cmd = lambda l=label: self._symbol_clicked(l)

                # Use default ttk styling (no custom colors)
                b = ttk.Button(frame, text=label, width=5, command=cmd)
                b.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

        for i in range(4):
            frame.columnconfigure(i, weight=1)
        for i in range(len(buttons)):
            frame.rowconfigure(i, weight=1)

    def _build_scientific_buttons(self, frame: ttk.Frame) -> None:
        sci_buttons = [
            ["sin", "cos", "tan", "deg/rad"],
            ["asin", "acos", "atan", "("],
            ["log10", "ln", "exp", ")"],
            ["x²", "x³", "xʸ", "√x"],
            ["³√x", "10ˣ", "n!", "π"],
            ["e", "%", "^", ""],
        ]

        for r, row in enumerate(sci_buttons):
            for c, label in enumerate(row):
                if not label:
                    continue
                if label == "deg/rad":
                    cmd = lambda: self._command_clicked("toggle_angle")
                elif label in {"x²", "x³", "xʸ", "√x", "³√x", "10ˣ", "n!"}:
                    cmd = lambda l=label: self._command_clicked(l)
                elif label in {"sin", "cos", "tan", "asin", "acos", "atan", "log10", "ln", "exp"}:
                    # treat scientific functions as operations on the current value
                    cmd = lambda l=label: self._command_clicked(l)
                elif label == "π":
                    cmd = lambda: self._symbol_clicked("pi")
                elif label == "e":
                    cmd = lambda: self._symbol_clicked("e")
                else:
                    cmd = lambda l=label: self._symbol_clicked(l)

                # Use default ttk styling (no custom colors)
                b = ttk.Button(frame, text=label, width=5, command=cmd)
                b.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")

        for i in range(4):
            frame.columnconfigure(i, weight=1)
        for i in range(len(sci_buttons)):
            frame.rowconfigure(i, weight=1)

    # ----------------------------------------------------------------- helpers
    def set_display(self, text: str) -> None:
        self.display_var.set(text)
        self.display.icursor("end")

    def get_display(self) -> str:
        return self.display_var.get()

    def append_to_display(self, text: str) -> None:
        self.display_var.set(self.get_display() + text)
        self.display.icursor("end")

    def clear_display(self) -> None:
        self.display_var.set("")

    def show_info(self, text: str) -> None:
        self.info_var.set(text)

    def set_angle_mode_label(self, mode: str) -> None:
        self.show_info(f"Angle mode: {mode.upper()}")

    def add_history_line(self, expr: str, result: str) -> None:
        self.history_text.configure(state="normal")
        self.history_text.insert("end", f"{expr} = {result}\n")
        self.history_text.see("end")
        self.history_text.configure(state="disabled")

    def clear_history(self) -> None:
        self.history_text.configure(state="normal")
        self.history_text.delete("1.0", "end")
        self.history_text.configure(state="disabled")

    # ----------------------------------------------------------------- themes
    def _apply_theme(self) -> None:
        if self._theme == "dark":
            bg = "#121212"
            fg = "#ffffff"
            entry_bg = "#1f2933"
            accent = "#2563eb"  # blue
            sci_accent = "#059669"  # green
        else:
            bg = "#e5f0ff"
            fg = "#0f172a"
            entry_bg = "#ffffff"
            accent = "#1d4ed8"  # blue
            sci_accent = "#059669"  # green

        style = ttk.Style(self)
        if self._theme == "dark":
            style.theme_use("clam")

        # Window background
        self.configure(bg=bg)

        # Base styles
        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg)
        style.configure("TButton", padding=4)

        # Apply entry / history colors
        self.display.configure(background=entry_bg, foreground=fg)
        self.history_text.configure(background=entry_bg, foreground=fg, insertbackground=fg)

    def _toggle_theme_clicked(self) -> None:
        self._theme = "dark" if self._theme == "light" else "light"
        self.theme_button.configure(text="Light Theme" if self._theme == "dark" else "Dark Theme")
        self._apply_theme()

    # ------------------------------------------------------------- mode toggle
    def _toggle_mode_clicked(self) -> None:
        if self.sci_frame.winfo_ismapped():
            self.sci_frame.grid_remove()
            self.mode_button.configure(text="Scientific Mode")
        else:
            self.sci_frame.grid()
            self.mode_button.configure(text="Basic Mode")

    # ------------------------------------------------------------- events
    def _symbol_clicked(self, symbol: str) -> None:
        self.on_button_press(symbol)

    def _command_clicked(self, command: str) -> None:
        self.on_command(command)

    def _on_key_press(self, event: tk.Event) -> None:
        char = event.char
        if char in "0123456789.+-*/%^()":
            self.on_button_press(char)
        elif char.lower() == "s":
            # quick sin when typing "s"
            self.on_button_press("sin")
        elif char.lower() == "c":
            self.on_button_press("cos")
        elif char.lower() == "t":
            self.on_button_press("tan")

    def _on_enter(self, _event: tk.Event) -> None:
        self.on_command("equals")

    def _on_backspace(self, _event: tk.Event) -> None:
        self.on_command("backspace")

    def _on_clear(self, _event: tk.Event) -> None:
        self.on_command("C")

