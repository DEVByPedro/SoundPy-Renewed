import setup.bin.InstallDependencies as insDep
import setup.bin.CreateJSONS as createJSONs

insDep.installDependencies()
createJSONs.createJsonSetup()

import pygame
import flet as ft
import threading
import infra.Home as homePage
import time
import os
import configs.Configurations as config
import configs.Colors as colors
import configs.MusicConfig as musicConfig
import configs.PlaylistConfig as playlistConfig
import configs.UserConfig as userConfig

crnt_msc = ft.Text("", size=16, color="white")
crnt_artist = ft.Text("", size=12, color="grey")
crnt_img = ft.Image(src="na/na", fit=ft.ImageFit.COVER)
crnt_pos = ft.Text("00:00", size=14, color="white")
crnt_max = ft.Text("00:00", size=14, color="white")
current_vol = [0.5]

def main(page: ft.Page):
    page.padding = 0
    page.bgcolor = colors.background_color
    page.theme_mode = ft.ThemeMode.DARK
    page.window_fav_icon = os.path.abspath("Icon.jpg")
    page.title = "Sound Py - DEMO"

    playlistConfig.reload_musics()

    def selectAndCloseSideBar(
        e, playlist_id, body, page, crnt_msc, crnt_artist, crnt_img
    ):
        playlistConfig.getPlaylistMusicsById(
            e,
            playlist_id,
            body,
            page,
            crnt_msc,
            crnt_artist,
            crnt_img,
            slider,
            crnt_pos,
            crnt_max,
            main_button,
            current_vol,
        )
        toggle_sidebar(e)
        page.update()

    def upgrade_playlist():
        playlists_buttons.clear()
        criarPlaylistButton.visible = True
        criarPlaylistButton.opacity = 1.0
        playlists_buttons.append(criarPlaylistButton)
        for idx, playlist in enumerate(playlistConfig.get_all_playlists()):
            button = ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Container(
                            width=35,
                            height=35,
                            content=ft.Image(
                                src=playlistConfig.getMusicByIndex(idx + 1, 0).replace(
                                    ".mp3", ".jpg"
                                ),
                                fit=ft.ImageFit.COVER,
                                height=35,
                                width=35,
                            ),
                            border_radius=50,
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    value=playlist[1],
                                    size=13,
                                    weight=ft.FontWeight.W_500,
                                ),
                                ft.Text(
                                    playlistConfig.getDuration(playlist[0]),
                                    size=11,
                                    color="grey",
                                ),
                            ],
                            spacing=0,
                            height=40,
                        ),
                    ]
                ),
                color="white",
                bgcolor=colors.foreground_color,
                height=50,
                width=250,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2)),
                on_click=lambda e, playlist_id=playlist[0]: selectAndCloseSideBar(
                    e, playlist_id, body, page, crnt_msc, crnt_artist, crnt_img
                ),
            )
            playlists_buttons.append(button)
        criarPlaylistButton.visible = True
        submenu.controls = playlists_buttons
        page.update()

    def open_sidebar(e):
        nonlocal expandedSidebar
        expandedSidebar = not expandedSidebar
        if expandedSidebar:
            sidebar.bgcolor = colors.foreground_color
            for txt in text_refs:
                txt.opacity = 1
                txt.offset = ft.Offset(0, 0)
            for btn in buttons:
                btn.width = 180
            sidebar.width = 200

    def toggle_sidebar(e):
        nonlocal expandedSidebar
        nonlocal expanded
        expandedSidebar = not expandedSidebar
        if expandedSidebar:
            sidebar.bgcolor = colors.foreground_color
            for txt in text_refs:
                txt.opacity = 1
                txt.offset = ft.Offset(0, 0)
            for btn in buttons:
                btn.width = 180
            sidebar.width = 200
        else:
            expandedSidebar = False
            expanded = False
            submenu.visible = False
            for btn in submenu.controls:
                btn.opacity = 0.0
            sidebar.bgcolor = colors.foreground_color
            for btn in buttons:
                btn.width = 40
            for txt in text_refs:
                txt.opacity = 0
                txt.offset = ft.Offset(-0.3, 0)
            sidebar.width = 60

        page.update()

    def toggle_menu(e):
        nonlocal expanded
        expanded = not expanded
        if expanded:
            open_sidebar(e)
            upgrade_playlist()
            submenu.visible = True
            criarPlaylistButton.visible = True
            for btn in submenu.controls:
                btn.visible = True
            submenu.opacity = 1.0
        else:
            submenu.opacity = 0.0
            for btn in submenu.controls:
                btn.visible = False
                btn.opacity = 0.0
        page.update()

    def show_all_fav(e):
        body_column.controls.clear()
        body_column.controls.append(
            ft.Container(
                content=ft.Text(
                    "Favoritos ainda não implementado.",
                    color=colors.text_secondary,
                    size=20,
                ),
                alignment=ft.alignment.center,
                expand=True,
                bgcolor=colors.background_color,
            )
        )
        body_column.update()

        page.update()

    def show_mainMenu(e):
        body_column.controls.clear()
        body_column.controls.append(
            homePage.body(
                page,
                body,
                crnt_msc,
                crnt_artist,
                crnt_img,
                slider,
                crnt_pos,
                crnt_max,
                main_button,
            )
        )
        body_column.update()

        page.update()

    def set_user_pfp():
        response = userConfig.get_user_pfp()
        if response:
            return ft.Image(
                src=response,
                width=50,
                height=50,
                border_radius=50,
                fit=ft.ImageFit.COVER,
            )
        return ft.Icon(ft.Icons.PERSON_OUTLINE, color="white")

    def renew_user_pfp(e):
        if userConfig.find_pfp():
            new_image = set_user_pfp()
            userProfile.content = new_image

            new_userProfileButton = ft.Stack(
                [new_image, changeButton], width=30, height=30
            )

            userProfile.items[0].content.controls[1] = new_userProfileButton

            page.update()

    def change_opacity(e):
        changeButton.opacity = 0.7 if e.data == "true" else 0
        changeButton.update()

    def volume_change(e):
        current_vol[0] = e.control.value
        pygame.mixer.music.set_volume(current_vol[0])

    def openModals(param):

        playlist_modal = ft.AlertDialog(
            open=False,
            modal=True,
            title=ft.Text("Criar Playlist:"),
            content=ft.TextField(
                hint_text="Nome da Playlist",
                border_color=colors.text_primary,
                autofocus=True,
                on_submit=lambda e: [
                    playlistConfig.add_playlist(playlist_modal.content.value),
                    page.close(playlist_modal),
                    upgrade_playlist(),
                ],
            ),
            bgcolor=colors.card_color,
            actions=[
                ft.ElevatedButton(
                    text="Criar",
                    bgcolor="white",
                    color="black",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2)),
                    on_click=lambda e: [
                        playlistConfig.add_playlist(playlist_modal.content.value),
                        page.close(playlist_modal),
                        upgrade_playlist(),
                    ],
                ),
                ft.ElevatedButton(
                    "Cancelar",
                    color="white",
                    on_click=lambda e: page.close(playlist_modal),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2)),
                ),
            ],
        )

        if param == "playlist":
            return page.open(playlist_modal)

    def toggle_play_pause(e):
        pause = playlistConfig.pause_or_unpause(e)
        if pause == 1:
            main_button.content = ft.Icon(ft.Icons.PLAY_ARROW_SHARP, color="black")
        else:
            main_button.content = ft.Icon(ft.Icons.PAUSE_SHARP, color="black")

        page.update()

    def getMusicName(path: str):
        count = path.count("-")
        while count > 0:
            indexOfTrace = path.index("-")
            path = path[indexOfTrace + 2 :]
            count -= 1
        return path

    def getArtist(name):
        return name.split("-")[0] if "-" in name else "Unknown Artist"

    def search_musics(e):
        related_musics.clear()
        all_ids = playlistConfig.get_all_playlist_ids()

        buttons = []

        for playlist in all_ids:
            for music in playlist:
                path = music
                music_name = os.path.basename(music).replace(".mp3", "")
                final_name = getArtist(music_name) + " - " + getMusicName(music_name)

                if final_name.lower().strip().__contains__(e.data.lower().strip()):
                    related_musics.append((final_name, path))

        for music_related, path in related_musics:
            buttons.append(
                ft.ElevatedButton(
                    content=ft.Container(
                        ft.Row(
                            [
                                ft.Container(
                                    width=50,
                                    height=50,
                                    content=ft.Image(
                                        src=path.replace(".mp3", ".jpg"),
                                        width=50,
                                        height=50,
                                        fit=ft.ImageFit.COVER,
                                    ),
                                ),
                                ft.Column(
                                    [
                                        ft.Text(
                                            getMusicName(music_related),
                                            color="white",
                                            size=15,
                                        ),
                                        ft.Text(
                                            getArtist(music_related),
                                            color="grey",
                                            size=13,
                                        ),
                                        ft.Text(
                                            musicConfig.getIndividualDuration(path),
                                            color="grey",
                                            size=10,
                                        ),
                                    ],
                                    spacing=0,
                                ),
                            ]
                        ),
                        padding=5,
                        alignment=ft.alignment.center_left,
                    ),
                    expand=True,
                    height=70,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                    on_click=lambda e, p=path: {
                        playlistConfig.setContent(
                            e,
                            playlistConfig.getPlaylistIdByMusicPath(p),
                            p,
                            body_column,
                            page,
                            crnt_msc,
                            crnt_artist,
                            crnt_img,
                            slider,
                            crnt_pos,
                            crnt_max,
                            main_button,
                            current_vol,
                        ),
                        on_blur(e),
                    },
                    bgcolor=colors.card_color,
                )
            )

        floating_window.content = ft.Column(
            controls=buttons,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        floating_window.visible = True
        floating_window.opacity = 1
        page.update()

    related_musics = []
    buttons = []
    text_refs = []
    playlists_buttons = []
    submenu = ft.Column(controls=playlists_buttons, opacity=1.0, animate_opacity=300)
    expanded = False
    expandedSidebar = False
    clicking_result = [False]

    # Modal para criar playlist
    criarPlaylistButton = ft.ElevatedButton(
        text="Criar Nova Playlist",
        bgcolor=colors.card_color,
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=2)),
        height=40,
        width=250,
        on_click=lambda e: openModals("playlist"),
    )

    # Body central
    body_column = ft.Column([], expand=True)
    body = ft.Container(
        bgcolor=colors.background_color,
        content=body_column,
        padding=10,
        margin=ft.Margin(top=-10, bottom=0, left=-10, right=0),
        expand=True,
        alignment=ft.alignment.top_left,
    )

    menu_items = [
        ("Menu", ft.Icons.MENU_SHARP, toggle_sidebar),
        ("Home", ft.Icons.HOME, show_mainMenu),
        ("Fav. Songs", ft.Icons.BOOKMARK_ADD_SHARP, show_all_fav),
        ("Playlists", ft.Icons.PLAYLIST_PLAY_SHARP, toggle_menu),
    ]

    for label, icon_name, action in menu_items:
        text = ft.Text(
            value=label,
            size=15,
            weight=ft.FontWeight.W_400,
            color=colors.text_primary,
            opacity=0,
            offset=ft.Offset(-0.3, 0),
            animate_opacity=100,
            animate_offset=200,
        )
        text_refs.append(text)

        icon = ft.Icon(icon_name, size=20, color="white")

        buttons.append(
            ft.ElevatedButton(
                content=ft.Container(
                    content=ft.Row([icon, text]),
                    alignment=ft.alignment.center_left,
                    expand=True,
                ),
                style=ft.ButtonStyle(
                    bgcolor=colors.foreground_color,
                    shape=ft.RoundedRectangleBorder(radius=5),
                    overlay_color=colors.button_hover,
                ),
                width=40,
                height=40,
                animate_scale=200,
                on_click=action,
            )
        )
    buttons.append(submenu)

    sidebar = ft.Container(
        content=ft.Column(buttons, scroll="auto", expand=True),
        bgcolor=colors.foreground_color,
        width=60,
        alignment=ft.alignment.top_left,
        padding=ft.Padding(top=10, right=5, left=10, bottom=10),
        animate=ft.Animation(200, "easeInOut"),
        margin=ft.Margin(top=-10, bottom=0, left=0, right=0),
        expand=False,
    )

    changeButton = ft.ElevatedButton(
        content=ft.Icon(ft.Icons.EDIT, color="white"),
        width=50,
        height=50,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=50)),
        opacity=0,
        on_click=renew_user_pfp,
        on_hover=change_opacity,
    )

    userProfileButton = ft.Stack(
        [set_user_pfp(), changeButton],
        width=30,
        height=30,
        alignment=ft.alignment.center,
    )

    userProfile = ft.PopupMenuButton(
        width=50,
        height=50,
        content=set_user_pfp(),
        items=[
            ft.PopupMenuItem(
                content=ft.Row(
                    [ft.Text(f"Olá, {userConfig.getUserName()}!"), userProfileButton],
                    width=300,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                mouse_cursor=ft.MouseCursor.BASIC,
            ),
            ft.PopupMenuItem(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.SETTINGS_SHARP, color="white"),
                            ft.Text("Configurações"),
                        ]
                    )
                ),
                on_click=lambda e: config.open_settings(e, page),
            ),
        ],
    )

    floating_window = ft.Container(
        bgcolor=colors.background_color,
        border_radius=ft.BorderRadius(0, 0, 25, 25),
        padding=20,
        width=552,
        visible=False,
        animate_opacity=200,
        opacity=0,
        left=page.width // 2 + 68,
        top=65,
        height=400,
    )

    def on_focus(e):
        floating_window.visible = True if e.data != None else False
        floating_window.opacity = 1
        page.update()

    def on_blur(e):
        time.sleep(0.1)
        floating_window.visible = False
        floating_window.opacity = 0
        page.update()

    topbar_textfield = ft.TextField(
        border_color=colors.text_secondary,
        width=551,
        hint_text=ft.Text("Procurar Musica", size=15, color="white").value,
        prefix_icon=ft.Icon(
            ft.Icons.SEARCH_OUTLINED, color=colors.text_secondary, size=18
        ),
        color="white",
        on_change=search_musics,
        on_focus=on_focus,
        on_blur=on_blur,
    )

    # Top Bar
    topbar = ft.Container(
        content=ft.Row(
            [
                ft.Text(width=80),
                topbar_textfield,
                userProfile,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=colors.foreground_color,
        height=70,
        padding=10,
        margin=ft.Margin(top=0, bottom=0, left=0, right=0),
        animate=ft.Animation(200, "easeInOut"),
        expand=False,
    )

    slider = ft.Slider(
        width=500,
        height=5,
        active_color="white",
        inactive_color=colors.card_color
    )
    icon_ref = ft.Ref[ft.Icon]()
    main_button = ft.ElevatedButton(
        content=ft.Icon(ft.Icons.PLAY_ARROW_SHARP, color="black"),
        bgcolor="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=50)),
        on_click=lambda e: {toggle_play_pause(e)},
    )
    bottomContents = ft.Row(
        controls=[
            ft.Container(
                width=page.width * 0.25,
                alignment=ft.alignment.center_left,
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=70,
                            height=70,
                            bgcolor="#0A0A0A",
                            content=crnt_img,
                            border_radius=15,
                        ),
                        ft.Column(
                            controls=[crnt_msc, crnt_artist],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=3,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                width=page.width * 0.5,
                alignment=ft.alignment.center,
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Icon(
                                        ft.Icons.SKIP_PREVIOUS_SHARP, color="white"
                                    ),
                                    bgcolor=colors.card_color,
                                    color="white",
                                    on_click=lambda e: musicConfig.playPrevious(
                                        e,
                                        playlistConfig.getIndexByPath(
                                            playlistConfig.getPlaylistIdByMusicPath(
                                                playlistConfig.getPathByName(
                                                    crnt_msc.value
                                                )
                                            ),
                                            playlistConfig.getPathByName(
                                                crnt_msc.value
                                            ),
                                        ),
                                        playlistConfig.getPlaylistIdByMusicPath(
                                            playlistConfig.getPathByName(crnt_msc.value)
                                        ),
                                        slider,
                                        page,
                                        crnt_msc,
                                        crnt_artist,
                                        crnt_img,
                                        main_button,
                                        current_vol,
                                    ),
                                ),
                                main_button,
                                ft.ElevatedButton(
                                    content=ft.Icon(
                                        ft.Icons.SKIP_NEXT_SHARP, color="white"
                                    ),
                                    bgcolor=colors.card_color,
                                    color="white",
                                    on_click=lambda e: musicConfig.playNext(
                                        e,
                                        playlistConfig.getIndexByPath(
                                            playlistConfig.getPlaylistIdByMusicPath(
                                                playlistConfig.getPathByName(
                                                    crnt_msc.value
                                                )
                                            ),
                                            playlistConfig.getPathByName(
                                                crnt_msc.value
                                            ),
                                        ),
                                        playlistConfig.getPlaylistIdByMusicPath(
                                            playlistConfig.getPathByName(crnt_msc.value)
                                        ),
                                        slider,
                                        page,
                                        crnt_msc,
                                        crnt_artist,
                                        crnt_img,
                                        main_button,
                                        current_vol,
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        ft.Row(
                            controls=[crnt_pos, slider, crnt_max],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ),
            ft.Container(
                width=page.width * 0.25,
                alignment=ft.alignment.center_right,
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            name=ft.Icons.VOLUME_UP,
                            color="white",
                            size=20,
                        ),
                        ft.Slider(
                            height=5,
                            min=0,
                            max=1,
                            value=0.5,
                            active_color="white",
                            inactive_color=colors.card_color,
                            thumb_color="white",
                            on_change=volume_change,
                            tooltip="Volume",
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.END,
                ),
                padding=ft.padding.only(right=20),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        height=100,
    )

    bottombar = ft.Container(
        height=int(15 / 100 * page.height),
        bgcolor="#0A0A0A",
        content=bottomContents,
        padding=10,
    )

    layout = ft.Row(
        controls=[sidebar, body],
        expand=True,
    )

    main_column = ft.Column(
        controls=[topbar, ft.Column(controls=[layout, bottombar], expand=True)],
        expand=True,
    )

    body_column.controls.clear()
    body_column.controls.append(
        homePage.body(
            page,
            body,
            crnt_msc,
            crnt_artist,
            crnt_img,
            slider,
            crnt_pos,
            crnt_max,
            main_button,
        )
    )
    page.window.maximized = True
    page.add(ft.Stack(controls=[main_column, floating_window], expand=True))

    threading.Thread(
	    target=lambda: musicConfig.update_slider(None, slider, page, crnt_pos, crnt_max),
	    daemon=True,
    ).start()

ft.app(target=main)
