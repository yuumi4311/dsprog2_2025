import flet as ft
import requests
from datetime import datetime

from db import init_db, load_forecasts, load_forecast_by_date
from jma_api import fetch_and_store

AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json"


# -------------------------
# 地方 → 都道府県 階層取得
# -------------------------
def get_area_hierarchy():
    res = requests.get(AREA_URL, timeout=5).json()
    centers = res["centers"]
    offices = res["offices"]

    hierarchy = {}
    for c in centers.values():
        hierarchy[c["name"]] = {}

    for code, info in offices.items():
        parent = info.get("parent")
        if parent in centers:
            region = centers[parent]["name"]
            hierarchy[region][info["name"]] = code

    return hierarchy


# -------------------------
# 天気 → アイコン
# -------------------------
def weather_icon(text):
    if "雪" in text:
        return "❄️"
    if "雷" in text:
        return "⛈"
    if "雨" in text:
        return "🌧"
    if "くもり" in text or "曇" in text:
        return "☁️"
    if "晴" in text:
        return "☀️"
    return "🌈"


# -------------------------
# アプリ本体
# -------------------------
def main(page: ft.Page):
    page.title = "気象庁 天気予報（DB版）"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"

    init_db()
    hierarchy = get_area_hierarchy()

    selected_area_code = None
    selected_pref_name = None

    content_area = ft.Column(
        expand=True,
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
    )

    # -------- 地方変更 --------
    def on_region_change(e):
        region = region_dd.value
        pref_dd.options = [
            ft.dropdown.Option(p) for p in hierarchy[region].keys()
        ]
        pref_dd.disabled = False
        pref_dd.value = None
        page.update()

    # -------- 都道府県変更 --------
    def on_pref_change(e):
        nonlocal selected_area_code, selected_pref_name

        region = region_dd.value
        pref = pref_dd.value
        code = hierarchy[region][pref]

        selected_area_code = code
        selected_pref_name = pref

        # API → DB
        fetch_and_store(code)

        # DB → UI
        rows = load_forecasts(code)
        show_forecast_list(pref, rows)

    # -------- 一覧表示 --------
    def show_forecast_list(pref, rows):
        content_area.controls.clear()

        content_area.controls.append(
            ft.Text(f"{pref} の天気予報", size=26, weight="bold")
        )

        cards = ft.Row(wrap=True, spacing=16)

        for date, weather, low, high in rows:
            icon = weather_icon(weather)
            disp_date = datetime.fromisoformat(date).strftime("%m/%d")

            cards.controls.append(
                ft.Container(
                    width=150,
                    padding=16,
                    bgcolor="#1E1E1E",
                    border_radius=14,
                    content=ft.Column(
                        [
                            ft.Text(disp_date, weight="bold"),
                            ft.Text(icon, size=44),
                            ft.Text(
                                weather,
                                size=11,
                                text_align="center",
                            ),
                            ft.Text(f"{low}/{high}℃"),
                        ],
                        horizontal_alignment="center",
                        spacing=6,
                    ),
                )
            )

        content_area.controls.append(cards)
        page.update()

    # -------- DatePicker --------
    def on_date_change(e):
        if not selected_area_code:
            return

        date = e.control.value  # YYYY-MM-DD
        row = load_forecast_by_date(selected_area_code, date)

        content_area.controls.clear()

        if not row:
            content_area.controls.append(
                ft.Text("この日の予報データはありません", color="red")
            )
            page.update()
            return

        date, weather, low, high = row
        icon = weather_icon(weather)

        content_area.controls.append(
            ft.Text(f"{selected_pref_name}（{date}）", size=26, weight="bold")
        )

        content_area.controls.append(
            ft.Container(
                width=200,
                padding=20,
                bgcolor="#1E1E1E",
                border_radius=14,
                content=ft.Column(
                    [
                        ft.Text(icon, size=48),
                        ft.Text(weather, text_align="center"),
                        ft.Text(f"{low}/{high}℃"),
                    ],
                    horizontal_alignment="center",
                    spacing=8,
                ),
            )
        )

        page.update()

    date_picker = ft.DatePicker(
        on_change=on_date_change
    )
    page.overlay.append(date_picker)

    def open_date_picker(e):
        page.open(date_picker)
        
    pick_date_btn = ft.ElevatedButton(
    "日付を選択",
    icon=ft.Icons.CALENDAR_MONTH,
    on_click=open_date_picker,
)

    # -------- UI --------
    region_dd = ft.Dropdown(
        label="地方",
        options=[ft.dropdown.Option(r) for r in hierarchy.keys()],
        on_change=on_region_change,
        width=220,
    )

    pref_dd = ft.Dropdown(
        label="都道府県",
        disabled=True,
        on_change=on_pref_change,
        width=220,
    )

    page.add(
        ft.Column(
            [
                ft.Text("🌙 Weather Dashboard", size=28, weight="bold"),
                ft.Row(
                    [region_dd, pref_dd, pick_date_btn],
                    spacing=20,
                ),
                ft.Divider(color="#333333"),
                content_area,
            ],
            expand=True,
            spacing=18,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
