import random

import flet as ft

import configs.Colors as colors
import configs.PlaylistConfig as playlistConfig
import configs.InfraConfigs as infraConfig


def body(
    page: ft.Page,
    body,
    crnt_msc,
    crnt_artist,
    crnt_img,
    slider,
    crnt_pos,
    crnt_max,
    main_button,
):

    currentId = random.randint(1, len(playlistConfig.get_all_playlist_ids()))

    def go_to_playlist(e, playlist_id):
        playlistConfig.getPlaylistMusicsById(
            e,
            currentId,
            body,
            page,
            crnt_msc,
            crnt_artist,
            crnt_img,
            slider,
            crnt_pos,
            crnt_max,
            main_button,
        )

    def close_playlist_rec(e):
        playlist_recomendada.visible = False
        page.update()

    musica_recomendada = ft.Container(
        width=40 // 100 * page.width,
        height=30 // 100 * page.height,
        bgcolor="red",
        content=ft.Text("Olá"),
    )

    minhas_playlists = ft.Container(
        content=ft.Column([musica_recomendada]),
        bgcolor=colors.card_color,
        expand=True,
        alignment=ft.alignment.top_left,
    )

    playlist_recomendada_contents = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Sugestão de Playlist:", weight=ft.FontWeight.W_500, size=20
                        ),
                        ft.ElevatedButton(
                            content=ft.Icon(ft.Icons.CLOSE_SHARP, color="white"),
                            bgcolor=colors.card_color,
                            on_click=close_playlist_rec,
                        ),
                    ],
                    height=50,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=ft.Image(
                        src=(
                            playlistConfig.getMusicByIndex(currentId, 0).replace(
                                ".mp3", ".jpg"
                            )
                            if len(
                                playlistConfig.getMusicByIndex(currentId, 0).replace(
                                    ".mp3", ".jpg"
                                )
                            )
                            > 0
                            else "la/la"
                        ),
                        fit=ft.ImageFit.COVER,
                    ),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                playlistConfig.getPlaylistNameByIndex(currentId),
                                size=25,
                                weight=ft.FontWeight.W_500,
                            ),
                            ft.Text(
                                "Duração: " + playlistConfig.getDuration(currentId),
                                size=17,
                                weight=ft.FontWeight.W_200,
                                color="grey",
                            ),
                        ]
                    ),
                    margin=ft.Margin(top=0, left=0, right=0, bottom=50),
                ),
                ft.ElevatedButton(
                    bgcolor="white",
                    color="black",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
                    height=50,
                    text="Ir para Playlist",
                    width=int(page.width * (40 / 100)),
                    on_click=lambda e, playlist_id=currentId: go_to_playlist(
                        e, playlist_id
                    ),
                ),
            ],
            spacing=20,
        ),
        padding=10,
        width=int(page.width * (40 / 100)),
        border_radius=20,
    )

    playlist_recomendada = ft.Container(
        content=playlist_recomendada_contents, bgcolor=colors.card_color, width=500
    )

    layout = ft.Container(
        content=(
            ft.Row([minhas_playlists, playlist_recomendada])
            if infraConfig.getValue() == True
            else ft.Row([minhas_playlists])
        )
    )

    return ft.Container(
        content=layout,
        alignment=ft.alignment.top_center,
        expand=True,
        bgcolor=colors.background_color,
    )
