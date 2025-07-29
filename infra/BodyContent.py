import os.path
import flet as ft
import tkinter as tk
from tkinter import filedialog

import configs.MusicConfig as musicConfig

background_color = "#121212"
card_color = "#1E1E1E"
text_primary = "#FFFFFF"
text_secondary = "#C7C7C7"
button_hover = "#2C2C2C"
border_color = "#404040"
icon_color = "#E0E0E0"
equalizer_bar = "#6C6C6C"
foreground_color = "#141414"


def change_hover(e):
    e.control.bgcolor = button_hover if e.data == "true" else foreground_color
    e.control.update()


def AllSongs(page: ft.Page):
    ytLink = ft.TextField()

    modal = ft.AlertDialog(
        modal=True,
        open=False,
        title=ft.Text("Paste yt link here:"),
        content=ytLink,
        actions=[
            ft.ElevatedButton(text="Ok", on_click=lambda e: {page.close(modal)}),
            ft.ElevatedButton(text="Cancel", on_click=lambda e: {page.close(modal)}),
        ],
    )

    page.add(modal)

    def add_msc(e):
        try:
            tki = tk.Tk()
            tki.withdraw()
            tki.attributes("-topmost", True)

            file_path = filedialog.askopenfiles(
                title="Select a music", filetypes=[("MP3 Files", ".mp3")]
            )
            for file in file_path:
                musicConfig.addMusic(file.name)

            allSongsContainer.controls.clear()
            insert_all_songs()

            imagePlaylist.src = musicConfig.getPathByIndex(0).replace(".mp3", ".jpg")
            imagePlaylist.update()
            durTot.value = "Duração: " + musicConfig.getDuration()

            durTot.update()
            page.update()
        except Exception as ex:
            return

    def change_checkBox_visibility(e):
        checkBox.visible = not checkBox.visible
        confirmButton.visible = not confirmButton.visible
        checkBox.value = False
        for cb in music_checkboxes:
            cb.visible = not cb.visible
        page.update()

    def changeAllCheckBox(e):
        for cb in music_checkboxes:
            cb.value = True if e.data == "true" else False
            if e.data == "true":
                for path in musicConfig.get_all_musics():
                    allCheckedSongs.append(path)
        if e.data == "false":
            allCheckedSongs.clear()
        page.update()

    def excludeSongs(e):
        if len(allCheckedSongs) >= 0:
            for path in allCheckedSongs:
                musicConfig.deleteByIndex(musicConfig.getIndexByPath(path))
        checkBox.visible = False
        confirmButton.visible = False
        for cb in music_checkboxes:
            cb.visible = False
            cb.value = False

        allSongsContainer.clean()
        insert_all_songs()
        imagePlaylist.src = musicConfig.getPathByIndex(0).replace(".mp3", ".jpg")

        durTot.value = "Duração: " + musicConfig.getDuration()
        durTot.update()
        imagePlaylist.update()
        allSongsContainer.update()
        allSongs.update()
        page.update()

    def getArtist(name):
        try:
            return name[: name.index(" -")]
        except Exception as e:
            return "Unknown Artist"

    def insert_all_songs():

        allPaths = musicConfig.get_all_musics()
        for path in allPaths:
            nowId = musicConfig.getIndexByPath(path)

            # Trimming path for visibility
            basename = os.path.basename(path)
            name = basename

            try:
                if os.path.basename(path).count("-") > 1:
                    name = basename.replace(
                        basename[0 : basename.index("-") + 2], "", 1
                    )
                if os.path.basename(path).count("(") >= 1:
                    name = basename.replace(
                        basename[basename.index("(") : len(basename)], ""
                    )
                    if name.count("mp3"):
                        name = basename.replace(".mp3", "")
            except Exception as e:
                name = ""

            music_checkbox = ft.Checkbox(
                visible=False,
                width=20,
                height=20,
                on_change=lambda e, p=path: (
                    allCheckedSongs.append(p)
                    if e.data == "true" and p not in allCheckedSongs
                    else (
                        allCheckedSongs.remove(p)
                        if e.data == "false" and p in allCheckedSongs
                        else None
                    )
                ),
            )
            music_checkboxes.append(music_checkbox)

            playlistImage = ft.Image(
                src=path.replace(".mp3", ".jpg"),
                width=50,
                height=50,
                fit=ft.ImageFit.COVER,
            )

            allSongsContainer.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Row(
                                [
                                    music_checkbox,
                                    ft.ElevatedButton(
                                        width=30,
                                        content=ft.Icon(
                                            ft.Icons.PLAY_ARROW, color="white", size=20
                                        ),
                                        style=ft.ButtonStyle(
                                            bgcolor={
                                                ft.ControlState.HOVERED: "transparent",
                                                ft.ControlState.FOCUSED: "transparent",
                                                ft.ControlState.PRESSED: "transparent",
                                                ft.ControlState.DEFAULT: "transparent",
                                            },
                                            overlay_color={
                                                ft.ControlState.HOVERED: "transparent",
                                                ft.ControlState.FOCUSED: "transparent",
                                                ft.ControlState.PRESSED: "transparent",
                                            },
                                            elevation={"hovered": 0, "default": 0},
                                            padding=ft.Padding(
                                                top=0, left=0, right=5, bottom=0
                                            ),
                                        ),
                                    ),
                                    # Foto Musica
                                    playlistImage,
                                    ft.Column(
                                        [
                                            # Nome Musica
                                            ft.Text(
                                                str(nowId + 1)
                                                + ". "
                                                + name.replace(" .mp3", "")
                                            ),
                                            # Artista
                                            ft.Text("by " + getArtist(name)),
                                        ]
                                    ),
                                ],
                                width=400,
                            ),
                            # Duração Musica
                            ft.Text(musicConfig.getIndividualDuration(path), width=40),
                            ft.ElevatedButton(
                                content=ft.Icon(
                                    ft.Icons.EXPAND_MORE_OUTLINED,
                                    color="white",
                                    size=20,
                                ),
                                width=40,
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: "transparent",
                                        ft.ControlState.FOCUSED: "transparent",
                                        ft.ControlState.PRESSED: "transparent",
                                        ft.ControlState.DEFAULT: "transparent",
                                    },
                                    overlay_color={
                                        ft.ControlState.HOVERED: "transparent",
                                        ft.ControlState.FOCUSED: "transparent",
                                        ft.ControlState.PRESSED: "transparent",
                                    },
                                    elevation={"hovered": 0, "default": 0},
                                ),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    on_hover=change_hover,
                    bgcolor=foreground_color,
                    height=70,
                    padding=10,
                    border_radius=5,
                )
            )

    allCheckedSongs = []

    allSongsContainer = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

    music_checkboxes = []

    checkBox = ft.Checkbox(
        value=True,
        width=20,
        height=20,
        visible=False,
        on_change=lambda e: changeAllCheckBox(e),
    )

    confirmButton = ft.ElevatedButton(
        content=ft.Icon(ft.Icons.DELETE, color="white"),
        bgcolor="red",
        width=20,
        height=20,
        visible=False,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=2),
            padding=ft.Padding(top=0, right=3, left=0, bottom=0),
        ),
        on_click=excludeSongs,
    )

    insert_all_songs()

    ft.Container(
        content=allSongsContainer,
        padding=10,
    )

    durTot = ft.Text("Duração: " + musicConfig.getDuration())
    currentPlaylistTitle = ft.Text(
        "Todas as Musicas:", size=34, weight=ft.FontWeight.W_500
    )

    configPlaylistButton = ft.PopupMenuButton(
        content=ft.Container(
            content=ft.Row(
                [ft.Icon(ft.Icons.SETTINGS_OUTLINED, color="white", size=20)]
            ),
            bgcolor=background_color,
            border_radius=3,
            padding=5,
        ),
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=3)),
        width=30,
        height=30,
        items=[
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.EDIT, color="white"),
                        ft.Text("Editar Nome Playlist"),
                    ]
                ),
            ),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ADD, color="white"),
                        ft.Text("Adicionar Musica", color="white"),
                    ]
                ),
                on_click=add_msc,
            ),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.DOWNLOAD, color="white"),
                        ft.Text("Baixar Músicas"),
                    ]
                ),
                on_click=lambda e: page.open(modal),
            ),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.FOLDER_DELETE, color="white"),
                        ft.Text("Excluir Playlist"),
                    ]
                ),
                on_click=lambda e: page.open(modal),
            ),
            ft.PopupMenuItem(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.DELETE, color="white"),
                        ft.Text("Deletar Musicas", color="white"),
                    ]
                ),
                on_click=lambda e: change_checkBox_visibility(e),
            ),
        ],
    )

    imagePlaylist = ft.Image(
        src=musicConfig.getPathByIndex(0).replace(".mp3", ".jpg"),
        width=100,
        height=100,
        fit=ft.ImageFit.COVER,
    )
    allSongs = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Row(
                            [
                                ft.Container(content=imagePlaylist),
                                ft.Column(
                                    [
                                        currentPlaylistTitle,
                                        durTot,
                                    ]
                                ),
                            ]
                        ),
                        ft.Row(
                            [
                                configPlaylistButton,
                                ft.ElevatedButton(
                                    content=ft.Icon(
                                        ft.Icons.PLAY_ARROW, color="black", size=25
                                    ),
                                    bgcolor="#27e91d",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=50)
                                    ),
                                    width=50,
                                    height=50,
                                ),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Column(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Row(
                                        [
                                            ft.Row(
                                                [
                                                    checkBox,
                                                    confirmButton,
                                                ]
                                            ),
                                            ft.Text(
                                                "Nome",
                                                width=200,
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                        ],
                                        width=250,
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    ),
                                    ft.Text("Duração", text_align=ft.TextAlign.CENTER),
                                    ft.Text(""),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            padding=ft.Padding(top=10, left=0, bottom=0, right=-100),
                            bgcolor=background_color,
                            margin=ft.Margin(top=20, left=0, right=0, bottom=0),
                        )
                    ]
                ),
                allSongsContainer,
            ]
        ),
        padding=20,
        margin=ft.Margin(top=20, left=10, right=0, bottom=0),
        bgcolor=card_color,
        border_radius=10,
        expand=True,
    )

    return allSongs
