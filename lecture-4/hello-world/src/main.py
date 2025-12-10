import flet as ft


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, expand=1, on_click=None):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = on_click


class DigitButton(CalcButton):
    def __init__(self, text, expand=1, on_click=None):
        CalcButton.__init__(self, text, expand, on_click)
        self.bgcolor = ft.Colors.WHITE24
        self.color = ft.Colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, on_click=None):
        CalcButton.__init__(self, text, on_click=on_click)
        self.bgcolor = ft.Colors.ORANGE
        self.color = ft.Colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, on_click=None):
        CalcButton.__init__(self, text, on_click=on_click)
        self.bgcolor = ft.Colors.BLUE_GREY_100
        self.color = ft.Colors.BLACK


def main(page: ft.Page):
    current_value = "0"
    stored_value = None
    current_operator = None
    new_input = True   # ← 追加

    result = ft.Text(value=current_value, color=ft.Colors.WHITE, size=30)

    def on_button_click(e):
        nonlocal current_value, stored_value, current_operator, new_input

        t = e.control.text

        # 数字・小数点
        if t in "0123456789.":
            if new_input:
                current_value = ""   # ← 演算子を押した後の最初の数字入力でクリア
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

        # +/-
        elif t == "+/-":
            current_value = str(float(current_value) * -1)

        # %
        elif t == "%":
            current_value = str(float(current_value) / 100)

        # 演算子
        elif t in "+-*/":
            stored_value = float(current_value)
            current_operator = t
            new_input = True     # ← ここでクリアしない

        # =
        elif t == "=" and current_operator:
            new_value = float(current_value)
            if current_operator == "+":
                current_value = str(stored_value + new_value)
            elif current_operator == "-":
                current_value = str(stored_value - new_value)
            elif current_operator == "*":
                current_value = str(stored_value * new_value)
            elif current_operator == "/":
                current_value = str(stored_value / new_value)

            current_operator = None
            new_input = True

        result.value = current_value
        page.update()


    # UI構築
    page.add(
        ft.Container(
            width=350,
            bgcolor=ft.Colors.BLACK,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[result]),
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
