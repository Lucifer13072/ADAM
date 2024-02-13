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

    w = page.width
    h = page.height

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
            page.window_maximized = True
            fullscreen_b.data == False
            page.update()
        elif fullscreen_b.data == False:
            page.width = w
            page.height = h
            fullscreen_b.data == True
            page.update()
        

    def minm(e):
        page.window_minimized = True
        page.update()

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
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
    
    vi = ft.Image("client/images/like.jpg")
    page.add(
        ft.Row(controls=[
            ft.Text("EVA Alfa0.0.1", expand=True, weight=900),
            theme_b,
            ft.IconButton(ft.icons.MINIMIZE, on_click=minm),
            fullscreen_b,
            ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close())]),

        ft.Row(controls=[
            ft.Container(
                content=chat,
                border=ft.border.all(2, ft.colors.OUTLINE),
                border_radius=10,
                padding=10,
                width=300,
                height=900), 
            ft.Container(content=vi,
                border_radius=10,
                height=900,)    
            ],tight=True),

        ft.Row([
                new_task,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=enter_massage,
                ),], width=300),)

 
ft.app(target=main)

