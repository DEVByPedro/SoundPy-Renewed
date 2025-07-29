import os.path

import flet as ft
import shutil
import configs.Colors as colors
import configs.UserConfig as userConfig
import configs.InfraConfigs as infraConf
import tkinter as tk
from tkinter import filedialog
import configs.Notifications as notifications
import time


def open_settings(e, page):

    all_settings_pages = [
        ft.Container(
            content=ft.Container(
                expand=True,
                content=ft.Column(
                    [
                        ft.Container(
                            padding=10,
                            content=ft.Text(
                                "Conta e Segurança", size=20, color="white"
                            ),
                        ),
                        ft.Container(
                            padding=10,
                            content=ft.Column(
                                [
                                    ft.Text("Nome de exibição", size=17, color="white"),
                                    ft.TextField(
                                        hint_text=userConfig.getUserName(),
                                        on_submit=lambda e: userConfig.setUserName(
                                            e.control.value
                                        ),
                                        border_radius=8,
                                        border_color=colors.text_primary,
                                        width=400,
                                    ),
                                ]
                            ),
                        ),
                    ],
                    spacing=10,
                ),
                alignment=ft.alignment.top_left,
            )
        ),
        ft.Container(
            content=ft.Container(
                expand=True,
                content=ft.Column(
                    [
                        ft.Container(
                            padding=10,
                            content=ft.Text("Aplicativo", size=20, color="white"),
                        ),
                        ft.Container(
                            padding=10,
                            content=ft.Row(
                                [
                                    ft.Text(
                                        "Sugestão de Playlist", size=17, color="white"
                                    ),
                                    ft.Switch(
                                        value=infraConf.getValue(),
                                        on_change=lambda e: infraConf.changeVal(e),
                                    ),
                                ],
                                expand=True,
                            ),
                        ),
                        ft.Container(
                            padding=10,
                            content=ft.Row(
                                [
                                    ft.Text(
                                        "Receber Notificações?", size=17, color="white"
                                    ),
                                    ft.Switch(
                                        value=infraConf.getNotifValue(),
                                        on_change=lambda e: infraConf.changeNotifVal(e),
                                    ),
                                ],
                                expand=True,
                            ),
                        ),
                        ft.Container(
                            padding=10,
                            content=ft.Column(
                                [
                                    ft.Text("Fazer Backup", size=17, color="white"),
                                    ft.Container(
                                        ft.Row(
                                            [
                                                ft.TextField(
                                                    hint_text=userConfig.getBackupPath(),
                                                    on_submit=lambda e: userConfig.setBackupPath(
                                                        e.control.value
                                                    ),
                                                    border_color=ft.Colors.TRANSPARENT,
                                                ),
                                                ft.ElevatedButton(
                                                    bgcolor=colors.card_color,
                                                    content=ft.Icon(
                                                        ft.Icons.ATTACH_FILE,
                                                        color="white",
                                                        size=15,
                                                    ),
                                                    on_click=set_upload_configs,
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        ),
                                        border_radius=8,
                                        border=ft.Border(
                                            ft.BorderSide(1, "white"),
                                            ft.BorderSide(1, "white"),
                                            ft.BorderSide(1, "white"),
                                            ft.BorderSide(1, "white"),
                                        ),
                                        width=400,
                                    ),
                                    ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Criar Backup",
                                                color="black",
                                                bgcolor="white",
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(8)
                                                ),
                                                on_click=lambda e: make_backup(e, page),
                                            ),
                                            ft.ElevatedButton(
                                                "Importar Backup",
                                                color="black",
                                                bgcolor="white",
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(8)
                                                ),
                                                on_click=lambda e: import_backup(
                                                    e, page
                                                ),
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ),
                    ],
                    spacing=10,
                ),
                alignment=ft.alignment.top_left,
            )
        ),
        ft.Container(
            content=ft.Container(
                expand=True,
                content=ft.Column(
                    [
                        ft.Container(
                            padding=10,
                            content=ft.Text("Utilizagem", size=20, color="white"),
                        )
                    ],
                    spacing=10,
                ),
                alignment=ft.alignment.top_left,
            )
        ),
    ]

    settings_content = ft.Container(content=all_settings_pages[0], expand=True)

    def change_page(e, id):
        settings_content.content = all_settings_pages[id]
        settings_content.update()

    settings_modal = ft.AlertDialog(
        modal=True,
        open=False,
        title=ft.Text("Configurações", size=20),
        bgcolor=colors.card_color,
        content=ft.Row(
            [
                # main container
                ft.Container(
                    content=ft.Row(
                        [
                            # Left container
                            ft.Container(
                                content=ft.Column(
                                    [
                                        # User Settings
                                        ft.ElevatedButton(
                                            content=ft.Row(
                                                [
                                                    ft.Icon(
                                                        ft.Icons.PERSON,
                                                        color="white",
                                                        size=15,
                                                    ),
                                                    ft.Text(
                                                        "Pessoal",
                                                        color="white",
                                                        size=15,
                                                    ),
                                                ],
                                                spacing=10,
                                            ),
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=8
                                                ),
                                                overlay_color=colors.button_hover,
                                            ),
                                            bgcolor=colors.foreground_color,
                                            height=50,
                                            on_click=lambda e: change_page(e, 0),
                                        ),
                                        ft.ElevatedButton(
                                            content=ft.Row(
                                                [
                                                    ft.Icon(
                                                        ft.Icons.APPS,
                                                        color="white",
                                                        size=15,
                                                    ),
                                                    ft.Text(
                                                        "Aplicativo",
                                                        color="white",
                                                        size=15,
                                                    ),
                                                ],
                                                spacing=10,
                                            ),
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=8
                                                ),
                                                overlay_color=colors.button_hover,
                                            ),
                                            bgcolor=colors.foreground_color,
                                            height=50,
                                            on_click=lambda e: change_page(e, 1),
                                        ),
                                        ft.ElevatedButton(
                                            content=ft.Row(
                                                [
                                                    ft.Icon(
                                                        ft.Icons.PERSON,
                                                        color="white",
                                                        size=15,
                                                    ),
                                                    ft.Text(
                                                        "Histórico",
                                                        color="white",
                                                        size=15,
                                                    ),
                                                ],
                                                spacing=10,
                                            ),
                                            style=ft.ButtonStyle(
                                                shape=ft.RoundedRectangleBorder(
                                                    radius=8
                                                ),
                                                overlay_color=colors.button_hover,
                                            ),
                                            bgcolor=colors.foreground_color,
                                            height=50,
                                            on_click=lambda e: change_page(e, 2),
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                width=(25 / 100) * 900,
                                alignment=ft.alignment.top_center,
                            ),
                            settings_content,
                        ]
                    ),
                    width=900,
                    height=500,
                )
            ]
        ),
        actions=[
            ft.ElevatedButton(
                bgcolor="white",
                color="black",
                text="Ok",
                on_click=lambda e: {page.close(settings_modal)},
            )
        ],
    )

    page.open(settings_modal)


def set_upload_configs(e):
    try:
        tki = tk.Tk()
        tki.withdraw()
        tki.attributes("-topmost", True)
        file_path = filedialog.askdirectory(title="Selecione a pasta para backup:")
        userConfig.setBackupPath(file_path.title())
    except Exception as e:
        return e


def make_backup(e, page):
    modal = ft.AlertDialog(
        modal=True,
        open=False,
        title=ft.Text("Criando Backup", size=25),
        content=ft.Column(
            [ft.Text("Aguarde um momento"), ft.ProgressBar(color="white")], tight=True
        ),
    )

    page.dialog = modal
    page.open(modal)
    page.update()

    time.sleep(1)

    backup_base = userConfig.getBackupPath()

    if not backup_base:
        set_upload_configs(e)
        backup_base = userConfig.getBackupPath()

    if not backup_base:
        modal.open = False
        page.update()
        return False

    src_configs = os.path.abspath("configs/intFiles")
    src_arquives = os.path.abspath("arquives")
    dst = os.path.join(backup_base, "SoundPyBKP")

    dst_configs = os.path.join(dst, "intFiles")
    dst_arquives = os.path.join(dst, "arquives")

    if os.path.exists(dst):
        shutil.rmtree(dst)

    try:
        os.makedirs(dst_configs, exist_ok=True)
        os.makedirs(dst_arquives, exist_ok=True)

        for root, dirs, files in os.walk(src_configs):
            for file in files:
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, src_configs)
                dst_file = os.path.join(dst_configs, rel_path)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)

        for root, dirs, files in os.walk(src_arquives):
            for file in files:
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, src_arquives)
                dst_file = os.path.join(dst_arquives, rel_path)
                os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                shutil.copy2(src_file, dst_file)

        modal.open = False
        page.update()
        notifications.spawnNotification(
            "Backup Criado", "Seu backup foi criado no caminho escolhido!"
        )
        return True

    except Exception as err:
        modal.open = False
        page.update()
        notifications.spawnNotification(
            "Erro ao criar backup", f"Ocorreu um erro: {err}"
        )
        return False


def import_backup(e, page):
    try:
        tki = tk.Tk()
        tki.withdraw()
        tki.attributes("-topmost", True)
        file_path = filedialog.askdirectory(title="Selecione a pasta de backup")
        tki.destroy()

        if not file_path:
            return

        source_music_dir = os.path.join(file_path, "arquives")
        source_config_dir = os.path.join(file_path, "intFiles")

        music_dir = os.path.abspath("arquives")
        user_config_dir = os.path.abspath("configs/intFiles")

        os.makedirs(user_config_dir, exist_ok=True)
        os.makedirs(music_dir, exist_ok=True)

        def copy_folder(src_dir, dst_dir):
            for root, dirs, files in os.walk(src_dir):
                for file in files:
                    src_file = os.path.join(root, file)
                    rel_path = os.path.relpath(src_file, src_dir)
                    dst_file = os.path.join(dst_dir, rel_path)
                    os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                    shutil.copy2(src_file, dst_file)

        if os.path.exists(source_music_dir):
            copy_folder(source_music_dir, music_dir)
        else:
            print("Pasta 'arquives' não encontrada no backup.")

        if os.path.exists(source_config_dir):
            copy_folder(source_config_dir, user_config_dir)
        else:
            print("Pasta 'intFiles' não encontrada no backup.")

        notifications.spawnNotification(
            "Backup Importado!", "Seu backup foi importado ao sistema"
        )
        page.update()

    except Exception as ex:
        notifications.spawnNotification(
            "Erro ao importar Backup", f"Erro ao importar backup: {ex}"
        )
