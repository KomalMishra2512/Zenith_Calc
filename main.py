from calculator_model import CalculatorModel
from calculator_view import CalculatorView
from controller import CalculatorController


def main() -> None:
    model = CalculatorModel()
    view = CalculatorView()
    CalculatorController(model=model, view=view)
    view.mainloop()


if __name__ == "__main__":
    main()

