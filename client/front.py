import flet as ft
import load as ld

def main(page):
    page.title = 'EVA v0.0.1'
    page.theme_mode = ft.ThemeMode.DARK
    page.fullscreen_dialog = True
    chat = ft.Column()
    def enter_massage(e):
        chat.controls.append(ft.Text(new_task.value))
        chat.controls.append(ft.Text(ld.answer(new_task.value)))
        new_task.value = ""
        page.update()

    chat = ft.Column(width=200, height=300)
    new_task = ft.TextField(hint_text="Сообщение:", width=200)

    page.add(
        chat,
        ft.Row(controls=[new_task, ft.ElevatedButton("Enter:", on_click=enter_massage)])
        )

ft.app(target=main)

