from __future__ import annotations

from dataclasses import dataclass

from calculator_model import CalculatorModel
from calculator_view import CalculatorView


@dataclass
class CalculatorController:
    """
    Controller that wires the view and the model together.
    Handles button clicks, keyboard input, and updates the view.
    """

    model: CalculatorModel
    view: CalculatorView

    def __post_init__(self) -> None:
        # Attach callbacks
        self.view.on_button_press = self.handle_symbol
        self.view.on_command = self.handle_command
        # Show initial angle mode
        self.view.set_angle_mode_label(self.model.angle_mode)

    # ---------------------------------------------------------------- symbols
    def handle_symbol(self, symbol: str) -> None:
        current = self.view.get_display()
        self.view.set_display(current + symbol)
        self.view.show_info("")

    # ---------------------------------------------------------------- commands
    def handle_command(self, command: str) -> None:
        if command == "equals":
            self._equals()
        elif command == "C":
            self.view.clear_display()
            self.view.show_info("")
        elif command == "CE":
            self.view.clear_display()
        elif command == "backspace":
            self._backspace()
        elif command == "MC":
            self.model.clear_memory()
            # Clear on-screen history as well when memory is cleared
            self.view.clear_history()
            self.view.show_info("Memory & history cleared")
        elif command == "MR":
            self._recall_memory()
        elif command == "M+":
            self._memory_add()
        elif command == "M-":
            self._memory_subtract()
        elif command == "negate":
            self._negate()
        elif command == "toggle_angle":
            mode = self.model.toggle_angle_mode()
            self.view.set_angle_mode_label(mode)
        elif command == "x²":
            self._apply_power(2)
        elif command == "x³":
            self._apply_power(3)
        elif command == "xʸ":
            self.view.set_display(self.view.get_display() + "**")
        elif command == "√x":
            self._wrap_function("sqrt")
        elif command == "³√x":
            self._wrap_function("cbrt")
        elif command == "10ˣ":
            self._wrap_function("ten_pow")
        elif command == "n!":
            self._wrap_function("factorial")
        elif command in {"sin", "cos", "tan", "asin", "acos", "atan", "log10", "ln", "exp"}:
            # scientific functions operate on the current expression / value
            self._wrap_function(command)

    # --------------------------------------------------------- command helpers
    def _equals(self) -> None:
        expr = self.view.get_display()
        result = self.model.evaluate(expr)
        if result.is_error:
            self.view.show_info(result.error or "Error")
        else:
            # Show result
            self.view.set_display(str(result.value))
            # Also store last result into memory for easy recall
            try:
                self.model.memory = float(result.value) if result.value is not None else 0.0
            except (TypeError, ValueError):
                self.model.memory = 0.0
            self.view.show_info("")
            self.view.add_history_line(expr, str(result.value))

    def _backspace(self) -> None:
        text = self.view.get_display()
        if text:
            self.view.set_display(text[:-1])

    def _current_value_or_zero(self) -> float:
        text = self.view.get_display()
        if not text:
            return 0.0
        # Try direct numeric conversion first
        try:
            return float(text)
        except ValueError:
            # Fall back to full expression evaluation
            res = self.model.evaluate(text)
            if res.is_error or res.value is None:
                # Surface the error to the user and avoid changing memory
                self.view.show_info(res.error or "Invalid input")
                return 0.0
            return float(res.value)

    def _memory_add(self) -> None:
        v = self._current_value_or_zero()
        self.model.add_to_memory(v)
        self.view.show_info(f"Memory = {self.model.memory}")

    def _memory_subtract(self) -> None:
        v = self._current_value_or_zero()
        self.model.subtract_from_memory(v)
        self.view.show_info(f"Memory = {self.model.memory}")

    def _recall_memory(self) -> None:
        v = self.model.recall_memory()
        current = self.view.get_display()
        # If display is empty or just "0", replace it with memory value.
        # Otherwise, append memory value so it can be used in a larger expression.
        if not current or current == "0":
            self.view.set_display(str(v))
        else:
            self.view.set_display(current + str(v))
        self.view.show_info(f"Memory recalled: {v}")

    def _negate(self) -> None:
        text = self.view.get_display()
        if not text:
            return
        if text.startswith("-"):
            self.view.set_display(text[1:])
        else:
            self.view.set_display("-" + text)

    def _apply_power(self, power: int) -> None:
        text = self.view.get_display()
        if not text:
            return
        self.view.set_display(f"({text})**{power}")

    def _wrap_function(self, func_name: str) -> None:
        text = self.view.get_display()
        if not text:
            # start a function call if nothing is entered yet
            self.view.set_display(f"{func_name}(")
        else:
            self.view.set_display(f"{func_name}({text})")

