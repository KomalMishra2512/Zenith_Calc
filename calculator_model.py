import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple, Union, Optional


Number = Union[int, float]


@dataclass
class CalculatorResult:
    value: Optional[Number] = None
    error: Optional[str] = None

    @property
    def is_error(self) -> bool:
        return self.error is not None


@dataclass
class CalculatorModel:
    """
    Logic / data layer for the calculator.
    Handles expression evaluation, memory, history, and angle mode.
    """

    memory: float = 0.0
    angle_mode: str = "deg"  # "deg" or "rad"
    history: List[Tuple[str, str]] = field(default_factory=list)

    def clear_memory(self) -> None:
        self.memory = 0.0
        # Also clear stored history when memory is cleared
        self.history.clear()

    def recall_memory(self) -> float:
        return self.memory

    def add_to_memory(self, value: Number) -> None:
        self.memory += float(value)

    def subtract_from_memory(self, value: Number) -> None:
        self.memory -= float(value)

    def toggle_angle_mode(self) -> str:
        self.angle_mode = "rad" if self.angle_mode == "deg" else "deg"
        return self.angle_mode

    # --- Expression evaluation -------------------------------------------------

    def evaluate(self, expression: str) -> CalculatorResult:
        expression = expression.strip()
        if not expression:
            return CalculatorResult(value=0.0)

        # Replace common calculator symbols with Python equivalents
        processed = (
            expression.replace("×", "*")
            .replace("÷", "/")
            .replace("^", "**")
        )

        try:
            result = self._safe_eval(processed)
        except ZeroDivisionError:
            return CalculatorResult(error="Divide by zero")
        except OverflowError:
            return CalculatorResult(error="Overflow")
        except ValueError:
            return CalculatorResult(error="Math error")
        except Exception:
            return CalculatorResult(error="Invalid input")

        # Normalise floats like 1.0 -> 1 where possible
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        # Store in history
        self.history.append((expression, str(result)))

        return CalculatorResult(value=result)

    # --- Internal helpers ------------------------------------------------------

    def _safe_eval(self, expression: str) -> Any:
        """
        Safely evaluate a mathematical expression using a restricted namespace.
        Supports arithmetic, power, roots, trig, logs, factorial, etc.
        """
        # Prepare namespace
        ns: Dict[str, Any] = {
            # Constants
            "pi": math.pi,
            "e": math.e,
            # Basic functions
            "abs": abs,
            "round": round,
            # Trigonometric in current angle mode
            "sin": self._wrap_trig(math.sin),
            "cos": self._wrap_trig(math.cos),
            "tan": self._wrap_trig(math.tan),
            "asin": self._wrap_inverse_trig(math.asin),
            "acos": self._wrap_inverse_trig(math.acos),
            "atan": self._wrap_inverse_trig(math.atan),
            # Logs
            "log10": math.log10,
            "log": math.log,  # natural log
            "ln": math.log,
            # Powers / roots
            "sqrt": math.sqrt,
            "cbrt": lambda x: math.copysign(abs(x) ** (1.0 / 3.0), x),
            "exp": math.exp,
            "pow": pow,
            "fact": math.factorial,
            "factorial": math.factorial,
            "memory": lambda: self.memory,
            # Exponentials
            "ten_pow": lambda x: 10 ** x,
        }

        # Disallow builtins
        return eval(expression, {"__builtins__": {}}, ns)

    def _wrap_trig(self, func):
        def wrapper(x: Number) -> float:
            if self.angle_mode == "deg":
                x = math.radians(x)
            return func(x)

        return wrapper

    def _wrap_inverse_trig(self, func):
        def wrapper(x: Number) -> float:
            v = func(x)
            if self.angle_mode == "deg":
                return math.degrees(v)
            return v

        return wrapper

