import flet as ft
import asyncio
import time
from core.engine import TypingEngine


async def main(page: ft.Page):
    engine = TypingEngine()
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.title = "Typing Racer Pro"
    page.padding = 30

    # UI Components
    mode_dropdown = ft.Dropdown(options=[ft.dropdown.Option(m) for m in engine.modes.keys()], value="Small", width=300)
    time_dropdown = ft.Dropdown(options=[ft.dropdown.Option(t) for t in ["5", "8", "10", "15", "20", "No Limit"]],
                                value="5", width=300)
    timer_text = ft.Text(size=25, color=ft.Colors.YELLOW)
    is_running = False

    def show_menu():
        page.clean()
        page.add(ft.Container(content=ft.Column([
            ft.Text("Typing Racer Pro", size=40, weight="bold", color=ft.Colors.CYAN_ACCENT),
            mode_dropdown, time_dropdown,
            ft.ElevatedButton("Start Game", on_click=lambda e: asyncio.create_task(
                start_game(mode_dropdown.value, time_dropdown.value)))
        ], alignment=ft.MainAxisAlignment.CENTER), alignment=ft.Alignment.CENTER, padding=20))
        page.update()

    async def start_game(mode, time_limit_str):
        nonlocal is_running
        is_running = True
        page.clean()
        text_to_type = engine.start_game(mode)
        start_time = time.time()

        input_field = ft.TextField(multiline=True, min_lines=5, autofocus=True, border_color=ft.Colors.CYAN_ACCENT)

        async def run_timer():
            limit_sec = int(time_limit_str) * 60 if time_limit_str != "No Limit" else 999999
            for i in range(limit_sec if time_limit_str != "No Limit" else 0,
                           -1 if time_limit_str != "No Limit" else 999999, -1 if time_limit_str != "No Limit" else 1):
                if not is_running: break
                if time_limit_str != "No Limit":
                    timer_text.value = f"Time Remaining: {i // 60:02}:{i % 60:02}"
                else:
                    timer_text.value = f"Time Elapsed: {int(time.time() - start_time)}s"
                page.update()
                if time_limit_str != "No Limit" and i == 0: finish_game(None)
                await asyncio.sleep(1)

        def finish_game(e):
            nonlocal is_running
            is_running = False
            time_taken = round(time.time() - start_time, 2)
            errors = engine.calculate_results(input_field.value)
            page.clean()
            page.add(ft.Column([
                ft.Text("Game Completed!", size=35, color=ft.Colors.GREEN_ACCENT),
                ft.Text(f"Time: {time_taken}s", color=ft.Colors.WHITE),
                ft.Text(f"Errors: {errors}", color=ft.Colors.RED_ACCENT),
                ft.ElevatedButton("Back to Menu", on_click=lambda e: show_menu())
            ], alignment=ft.MainAxisAlignment.CENTER))
            page.update()

        page.add(timer_text, ft.Text(text_to_type, size=18, color=ft.Colors.WHITE), input_field,
                 ft.ElevatedButton("Completed", on_click=finish_game))
        asyncio.create_task(run_timer())
        page.update()

    show_menu()


ft.app(target=main)