import flet as ft
from db import init_db, load_forecasts
from jma_api import fetch_and_save_forecast


def main(page: ft.Page):
    page.title = "天気予報（DB版）"
    page.theme_mode = ft.ThemeMode.DARK

    init_db()

    area_code = "130000"  # 東京（テスト用）

    def load_weather(e):
        # API → DB
        fetch_and_save_forecast(area_code)

        # DB → UI
        rows = load_forecasts(area_code)
        result.controls.clear()

        for date, weather, low, high in rows:
            result.controls.append(
                ft.Text(f"{date} : {weather} {low}/{high}℃")
            )

        page.update()

    result = ft.Column()

    page.add(
        ft.ElevatedButton("天気取得", on_click=load_weather),
        result
    )


ft.app(target=main)
