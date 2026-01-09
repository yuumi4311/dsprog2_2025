import flet as ft
import requests
from datetime import datetime

AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json"


# -------------------------
# 地方 → 都道府県 階層取得
# -------------------------
def get_area_hierarchy():
    res = requests.get(AREA_URL, timeout=5).json()
    centers = res["centers"]
    offices = res["offices"]

    region_order = [
        "北海道", "東北", "関東甲信", "北陸",
        "東海", "近畿", "中国", "四国", "九州", "沖縄"
    ]

    hierarchy = {}
    for r in region_order:
        for c in centers.values():
            if r in c["name"]:
                hierarchy[c["name"]] = {}

    for code, info in offices.items():
        parent = info.get("parent")
        if parent in centers:
            region = centers[parent]["name"]
            if region in hierarchy:
                hierarchy[region][info["name"]] = code

    return hierarchy


# -------------------------
# 天気文 正規化
# -------------------------
def normalize_weather(text):
    return (
        text.replace("　", "")
            .replace("時々", "、時々")
            .replace("所により", "、所により")
            .replace("後", "のち")
    )


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
    page.title = "気象庁 天気予報"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#121212"

    hierarchy = get_area_hierarchy()

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
        region = region_dd.value
        pref = pref_dd.value
        code = hierarchy[region][pref]

        res = requests.get(FORECAST_URL.format(code)).json()
        short = res[0]["timeSeries"][0]
        temps = res[0]["timeSeries"][2]["areas"][0]["temps"]

        dates = short["timeDefines"]
        weathers = short["areas"][0]["weathers"]

        content_area.controls.clear()
        content_area.controls.append(
            ft.Text(f"{pref} の天気予報", size=26, weight="bold")
        )

        cards = ft.Row(wrap=True, spacing=16)

        for i in range(min(5, len(dates))):
            date = datetime.fromisoformat(dates[i]).strftime("%m/%d")
            raw = weathers[i]
            weather = normalize_weather(raw)
            icon = weather_icon(raw)

            low = temps[i * 2] if i * 2 < len(temps) else "-"
            high = temps[i * 2 + 1] if i * 2 + 1 < len(temps) else "-"

            cards.controls.append(
                ft.Container(
                    width=150,
                    padding=16,
                    bgcolor="#1E1E1E",
                    border_radius=14,
                    shadow=ft.BoxShadow(
                        blur_radius=10,
                        spread_radius=1,
                        color="#000000AA",
                    ),
                    content=ft.Column(
                        [
                            ft.Text(date, weight="bold", color="#BBBBBB"),
                            ft.Text(icon, size=44),
                            ft.Text(
                                weather,
                                size=11,
                                text_align="center",
                                color="#DDDDDD",
                            ),
                            ft.Row(
                                [
                                    ft.Text(f"{low}℃", color="#64B5F6"),
                                    ft.Text("/", color="#888888"),
                                    ft.Text(f"{high}℃", color="#EF9A9A"),
                                ],
                                alignment="center",
                            ),
                        ],
                        horizontal_alignment="center",
                        spacing=6,
                    ),
                )
            )

        content_area.controls.append(cards)
        page.update()

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

    nav = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        bgcolor="#1A1A1A",
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.WB_SUNNY_OUTLINED,
                selected_icon=ft.Icons.WB_SUNNY,
                label="天気",
            )
        ],
    )

    # -------- レイアウト --------
    page.add(
        ft.Row(
            [
                nav,
                ft.VerticalDivider(width=1, color="#333333"),
                ft.Container(
                    expand=True,
                    padding=28,
                    content=ft.Column(
                        [
                            ft.Text(
                                "🌙 Weather Dashboard",
                                size=28,
                                weight="bold",
                            ),
                            ft.Row(
                                [region_dd, pref_dd],
                                spacing=20,
                            ),
                            ft.Divider(color="#333333"),
                            content_area,
                        ],
                        spacing=18,
                    ),
                ),
            ],
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)
