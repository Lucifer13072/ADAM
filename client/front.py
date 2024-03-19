import flet as ft
import load as ld
import time
import webbrowser


def main(page):
    page.title = 'Eva v0.0.2'
    page.theme_mode = ft.ThemeMode.DARK
    page.fullscreen_dialog = True
    page.window_title_bar_hidden = True
    page.window_title_bar_buttons_hidden = True
    page.window_width = 1080
    page.window_height = 700

    def enter_massage(e):
        if name_task.value == "":
            chat.controls.append(ft.Text(f"Пользователь: " + new_task.value, size=11))
        else:
            chat.controls.append(ft.Text(f"{name_task.value}:" + new_task.value, size=11))

        chat.controls.append(ft.Text("Eva: " + ld.answer(new_task.value), size=11))
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
        else:
            page.window_width = 1080
            page.window_heightt = 700
            fullscreen_b.data == True
            page.update()
    
    def settings(e):
        page.dialog = settings_modal
        settings_modal.open = True
        page.update()

    def close_settings(e):
        settings_modal.open = False
        page.update()

    def minm(e):
        page.window_minimized = True
        page.update()

    def language_repl(e):
        if lang_b.data == True: #RU
            lang_b.data = False
            lang_b.text = "Русский"
            new_task.hint_text = "Сообщение: "
            model_button_login_dl.text= "Сохранить"
            model_button_main_dl.text = "Сохранить"
            settings_text.value = "Настройки"
            repl_theme_text.value = "Изменить тему: "
            repl_lang_text.value = "Изменить язык: "
            login_title_text.value = "Профиль"
            login_text.value = "Введите ваше имя: " 
            key_text.value = "Введите ключ: " 

        else: #ENG
            lang_b.data = True
            lang_b.text = "English"
            new_task.hint_text = "Messenge: "
            model_button_login_dl.text = "Save"
            model_button_main_dl.text = "Save"
            settings_text.value = "Settings"
            repl_theme_text.value = "Replace Theme: "
            repl_lang_text.value = "Replace language: "
            login_title_text.value = "Profile" 
            login_text.value = "Enter your name: "
            key_text.value = "Enter key: " 
        page.update()

    def login_form_open(e):
        page.dialog = login_modal
        login_modal.open = True
        page.update()


    def login_form_close(e):
        page.dialog = settings_modal
        settings_modal.open = True
        page.update()


    def help(e):
        webbrowser.open("http://localhost")
        page.update()

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    #tasks
    new_task = ft.TextField(
        hint_text="Сообщение: ",
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        on_submit=enter_massage)
    name_task = ft.TextField(max_lines=1, shift_enter=True, expand=True)
    key_task = ft.TextField(max_lines=1, shift_enter=True, expand=True)


    # buttons
    theme_b = ft.IconButton(icon=ft.icons.DARK_MODE, on_click=theme_replace, data=False,) 
    fullscreen_b = ft.IconButton(ft.icons.FULLSCREEN, on_click=fsc, data=True)
    lang_b = ft.TextButton(text="Русский", on_click=language_repl, data=False)
    model_button_main_dl = ft.TextButton(text="Сохранить", on_click=close_settings)
    model_button_login_dl = ft.TextButton(text="Сохранить", on_click=login_form_close)
    login_form_b = ft.IconButton(ft.icons.KEY, on_click=login_form_open)

    #Texts
    settings_text = ft.Text("Настройки")
    repl_lang_text = ft.Text("Изменить язык: ")
    repl_theme_text = ft.Text("Изменить тему: ")
    login_title_text = ft.Text("Профиль")
    key_text = ft.Text("Введите ключ: ")
    login_text = ft.Text("Введите ваше имя: ")

    settings_modal = ft.AlertDialog(
        modal=True,
        title=settings_text,
        content=ft.Column(
                [ft.Row([repl_theme_text, theme_b]),
                 ft.Row([repl_lang_text, lang_b])],
                spacing=10,
                height=200,),
        actions=[
            ft.IconButton(ft.icons.HELP, on_click=help),
            login_form_b,
            model_button_main_dl,
        ],
        actions_alignment=ft.MainAxisAlignment.START
    )

    login_modal = ft.AlertDialog(
        modal = True,
        title=login_title_text,
        content=ft.Column(
                [ft.Row([login_text, name_task]),
                 ft.Row([]),
                 ft.Row([key_text, key_task])],
                spacing=10,
                height=200,
                width=400),
        actions=[model_button_login_dl],
    )
    
    settings_b = ft.IconButton(ft.icons.SETTINGS, on_click=settings)

    vi = ft.Image("images/like.jpg")
    page.add(

        ft.Row(controls=[ft.WindowDragArea(
            ft.Text("Eva"+" Alfa0.0.1", weight=900), expand=True),
            settings_b,
            ft.IconButton(ft.icons.MINIMIZE, on_click=minm),
            fullscreen_b,
            ft.IconButton(ft.icons.CLOSE, on_click=lambda _: page.window_close())]),
        
        ft.Divider(),

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

