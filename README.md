# Python MVC Scientific Calculator

This is a desktop calculator application written in Python using the MVC pattern and Tkinter.

It includes:

- Basic arithmetic operations (`+`, `-`, `*`, `/`, `%`)
- Scientific functions (trigonometric, logarithmic, power, roots, factorial, etc.)
- Expression evaluation with parentheses
- Memory operations (MC, MR, M+, M-)
- Calculation history panel
- Basic / Scientific mode switching
- Light / Dark theme switching
- Keyboard support for numbers, operators, `Enter` (=) and `Backspace`

## Requirements

- Python 3.9+ (Tkinter is included with most standard Python installations)

Optional (if you prefer to track dependencies explicitly):

```bash
pip install -r requirements.txt
```

## Running the App

From the project folder:

```bash
python main.py
```

The main window will open showing:

- Display field (top)
- Angle mode / info label
- History area
- Basic buttons
- Toggle buttons for **Scientific Mode** and **Theme**

## Features Overview

- **Basic Mode**
  - Digits `0`–`9`, decimal point `.`
  - Operators: `+`, `-`, `*`, `/`, `%`
  - `=` calculate result
  - `C` clear all, `CE` clear entry, `⌫` backspace
  - `±` negate current number

- **Scientific Mode**
  - Trig: `sin`, `cos`, `tan`, `asin`, `acos`, `atan`
  - Logs: `log10`, `ln` (`log`)
  - Powers / roots: `x²`, `x³`, `xʸ`, `√x`, `³√x`, `10ˣ`
  - Factorial: `n!`
  - Constants: `π` (`pi`), `e`
  - Parentheses: `(`, `)`
  - Angle mode toggle: `deg/rad`

- **Memory**
  - `MC` clear memory
  - `MR` recall memory
  - `M+` add current value to memory
  - `M-` subtract current value from memory

- **History**
  - Each successful calculation appends `"expression = result"` to the history panel.

## Deployment

This is a standard Python desktop app. Common options for deployment:

- **Direct Run**: Ship the source code and run with `python main.py`.
- **Executable (Windows)**: Use a tool like `pyinstaller`:

  ```bash
  pip install pyinstaller
  pyinstaller --name "MVC_Calculator" --onefile main.py
  ```

  The resulting executable in the `dist` folder can be distributed to end users.

