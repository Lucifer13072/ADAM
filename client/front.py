import flet as ft
import load as ld
import time

ru = {"User":"Пользователь: ",
      "Messenge":"Сообщение:",
      "Enter":"Отправить"}

eng = {"User":"User: ",
      "Messenge":"Massenge:",
      "Enter":"Enter"}

def main(page):
    page.title = 'EVA v0.0.1'
    page.theme_mode = ft.ThemeMode.DARK
    page.fullscreen_dialog = True
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True

    def enter_massage(e):
        chat.controls.append(ft.Text("Пользователь: " + new_task.value))
        chat.controls.append(ft.Text("Eva: " + ld.answer(new_task.value)))
        new_task.value = ""
        page.update()


    def theme_replace(e):
        if theme_b.data == True: #Dark
            theme_b.data = False
            page.theme_mode = ft.ThemeMode.DARK
            theme_b.bgcolor=ft.colors.BLACK
            theme_b.color=ft.colors.WHITE
            theme_b.icon = ft.icons.DARK_MODE
        else: #Light 
            theme_b.data = True
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_b.bgcolor=ft.colors.WHITE
            theme_b.color=ft.colors.BLACK
            theme_b.icon = ft.icons.LIGHT_MODE
        page.update()

    def fsc(e):
        if fullscreen_b.data == True:
            page.window_maximizable = True
            fullscreen_b.data == False
            page.update()
        else:
            page.window_maximized = False
            fullscreen_b.data == True
            page.update()
        

    def minm(e):
        page.window_minimized = True
        page.update()

    chat = ft.ListView(
        spacing=4,
        padding=4,
        horizontal=1,
        item_extent=10
    )

    
    new_task = ft.TextField(
        hint_text="Сообщение:",
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        on_submit=enter_massage)


    theme_b = ft.IconButton(icon=ft.icons.LIGHT_MODE, 
            on_click=theme_replace, 
            data=False,)

    fullscreen_b = ft.IconButton(ft.icons.FULLSCREEN, on_click=fsc, data=True)

    ent_block = ft.Row(controls=[new_task, ft.FilledButton("Enter:", on_click=enter_massage,)])
    
    image = ft.Image("client/images/like.jpg")

    page.add(
        ft.Row(controls=[
            ft.Text("EVA Alfa0.0.1", expand = True),
            theme_b,
            ft.IconButton(ft.icons.MINIMIZE, on_click=minm),
            fullscreen_b,
            ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close())]),
        
        ft.Row(controls=[image, ft.Column([chat, ent_block]),]))
 
ft.app(target=main)

