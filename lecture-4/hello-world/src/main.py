import flet as ft
import math


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, expand=1, on_click=None):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = on_click


class DigitButton(CalcButton):
    def __init__(self, text, expand=1, on_click=None):
        super().__init__(text, expand, on_click)
        self.bgcolor = ft.Colors.WHITE24
        self.color = ft.Colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, on_click=None):
        super().__init__(text, on_click=on_click)
        self.bgcolor = ft.Colors.ORANGE
        self.color = ft.Colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, on_click=None):
        super().__init__(text, on_click=on_click)
        self.bgcolor = ft.Colors.BLUE_GREY_100
        self.color = ft.Colors.BLACK


class ScientificButton(CalcButton):
    def __init__(self, text, on_click=None):
        super().__init__(text, on_click=on_click)
        self.bgcolor = ft.Colors.GREEN_400
        self.color = ft.Colors.BLACK


def main(page: ft.Page):
    page.title = "Scientific Calculator"

    current_value = "0"
    stored_value = None
    current_operator = None
    new_input = True
    is_scientific = False

    result = ft.Text(value=current_value, color=ft.Colors.WHITE, size=32)

    sci_rows = ft.Column(visible=False)

    def safe_calc(func):
        nonlocal current_value, new_input
        try:
            current_value = str(func(float(current_value)))
            new_input = True
        except:
            current_value = "Error"
            new_input = True

    def on_button_click(e):
        nonlocal current_value, stored_value, current_operator, new_input, is_scientific

        t = e.control.text

        # 数字
        if t in "0123456789.":
            if new_input:
                current_value = ""
                new_input = False
            if t == "." and "." in current_value:
                return
            current_value += t

        # AC
        elif t == "AC":
            current_value = "0"
            stored_value = None
            current_operator = None
            new_input = True

        # 符号反転
        elif t == "+/-":
            safe_calc(lambda x: -x)

        # %
        elif t == "%":
            safe_calc(lambda x: x / 100)

        # 演算子
        elif t in "+-*/":
            stored_value = float(current_value)
            current_operator = t
            new_input = True

        # =
        elif t == "=" and current_operator:
            try:
                new_value = float(current_value)
                if current_operator == "+":
                    current_value = str(stored_value + new_value)
                elif current_operator == "-":
                    current_value = str(stored_value - new_value)
                elif current_operator == "*":
                    current_value = str(stored_value * new_value)
                elif current_operator == "/":
                    current_value = str(stored_value / new_value)
            except:
                current_value = "Error"

            current_operator = None
            new_input = True

        # SCI モード切替
        elif t == "SCI":
            is_scientific = not is_scientific
            sci_rows.visible = is_scientific

        # 科学計算
        elif t == "√":
            safe_calc(math.sqrt)

        elif t == "x²":
            safe_calc(lambda x: x ** 2)

        elif t == "sin":
            safe_calc(lambda x: math.sin(math.radians(x)))

        elif t == "cos":
            safe_calc(lambda x: math.cos(math.radians(x)))

        elif t == "tan":
            safe_calc(lambda x: math.tan(math.radians(x)))

        elif t == "log":
            safe_calc(math.log10)

        elif t == "ln":
            safe_calc(math.log)

        elif t == "π":
            current_value = str(math.pi)
            new_input = True

        result.value = current_value
        page.update()

    sci_rows.controls = [
        ft.Row(
            controls=[
                ScientificButton("√", on_click=on_button_click),
                ScientificButton("x²", on_click=on_button_click),
                ScientificButton("sin", on_click=on_button_click),
                ScientificButton("cos", on_click=on_button_click),
            ]
        ),
        ft.Row(
            controls=[
                ScientificButton("tan", on_click=on_button_click),
                ScientificButton("log", on_click=on_button_click),
                ScientificButton("ln", on_click=on_button_click),
                ScientificButton("π", on_click=on_button_click),
            ]
        ),
    ]

    page.add(
        ft.Container(
            width=380,
            bgcolor=ft.Colors.BLACK,
            border_radius=20,
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            result,
                            ExtraActionButton("SCI", on_click=on_button_click),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    sci_rows,
                    ft.Row(
                        controls=[
                            ExtraActionButton("AC", on_click=on_button_click),
                            ExtraActionButton("+/-", on_click=on_button_click),
                            ExtraActionButton("%", on_click=on_button_click),
                            ActionButton("/", on_click=on_button_click),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("7", on_click=on_button_click),
                            DigitButton("8", on_click=on_button_click),
                            DigitButton("9", on_click=on_button_click),
                            ActionButton("*", on_click=on_button_click),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("4", on_click=on_button_click),
                            DigitButton("5", on_click=on_button_click),
                            DigitButton("6", on_click=on_button_click),
                            ActionButton("-", on_click=on_button_click),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("1", on_click=on_button_click),
                            DigitButton("2", on_click=on_button_click),
                            DigitButton("3", on_click=on_button_click),
                            ActionButton("+", on_click=on_button_click),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("0", expand=2, on_click=on_button_click),
                            DigitButton(".", on_click=on_button_click),
                            ActionButton("=", on_click=on_button_click),
                        ]
                    ),
                ]
            ),
        )
    )


ft.app(main)
