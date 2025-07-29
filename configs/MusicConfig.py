import json
import time
import threading

from mutagen.mp3 import MP3
import os
import pygame
import flet as ft
import configs.Colors as Colors
import configs.PlaylistConfig as playConf

fileJSON = os.path.join(os.path.abspath("configs/intFiles"), "Song.json")
status = {"is_paused": False, "is_playing": False, "current_index": None}
pygame.init()
mixer = pygame.mixer
position_seconds = [0]
thread_started = False
MUSIC_END = pygame.USEREVENT + 1
playlist_id = {"id": 0}


def addMusic(path: str):

    if len(path) > 0:
        with open(fileJSON, "r") as file:
            song = json.load(file)
    else:
        return "No valid path given"
    try:
        index_of_song = song["paths"].index(path)
        if index_of_song >= 0:
            return "The path given already exist"
    except Exception as e:
        if path.endswith(".mp3"):
            song["paths"].append(path)

            with open(fileJSON, "w") as file:
                json.dump(song, file, indent=4)
            getDuration()

            return True


def getPathByIndex(index: int):
    try:
        with open(fileJSON, "r") as file:
            sngPaths = json.load(file)

        return sngPaths["paths"][index]

    except Exception as e:
        return "No path found on index: " + str(index)


def deleteByIndex(index: int):
    try:
        with open(fileJSON, "r") as file:
            sngPaths = json.load(file)

        sngPaths["duration"] -= MP3(sngPaths["paths"][index]).info.length
        sngPaths["paths"].pop(index)

        with open(fileJSON, "w") as file:
            json.dump(sngPaths, file, indent=4)

        return True
    except Exception as e:
        return "No paths excluded."


def get_all_musics():
    try:
        with open(fileJSON, "r") as file:
            songs = json.load(file)
        allPaths = []

        for path in songs["paths"]:
            allPaths.append(path)

        return allPaths
    except Exception as e:
        return "Error: " + str(e)


def getDuration():
    try:
        with open(fileJSON, "r") as file:
            songs = json.load(file)

        songs["duration"] = 0
        total = 0
        for path in songs["paths"]:
            total += MP3(path).info.length

        seconds = total
        minutes = 0
        hours = 0

        while seconds > 59:
            seconds -= 60
            minutes += 1
        while minutes > 59:
            minutes -= 60
            hours += 1

        songs["duration"] = round(float(total))
        with open(fileJSON, "w") as file:
            json.dump(songs, file, indent=4)
        return f"{round(hours):02d}:{round(minutes):02d}:{round(seconds):02d}"

    except Exception as e:
        return "00:00:00"


def format_time(time):
    second = time
    minute = 0

    while second > 59:
        second -= 60
        minute += 1

    return f"{round(minute):02d}:{round(second):02d}"


def update_slider(e, slider, page, crnt_pos, crnt_max):
    while True:
        if status["is_playing"] and mixer.music.get_busy():
            position_seconds[0] += 1
            crnt_pos.value = format_time(position_seconds[0])
            crnt_max.value = format_time(slider.max)
            slider.value = position_seconds[0]
            page.update()
            if position_seconds[0] >= slider.max - 1:
                status["is_playing"] = False
                status["is_paused"] = False
                position_seconds[0] = 0
                slider.value = 0
        time.sleep(1)


def getIndividualDuration(path: str):
    if os.path.exists(path):
        if path.endswith(".mp3"):
            total = MP3(path).info.length
            seconds = total
            minutes = 0

            while seconds > 59:
                seconds -= 60
                minutes += 1

            return f"{round(minutes):02d}:{round(seconds):02d}"
        return "Please, select a .mp3 file."
    return "Path given does not exists"


def on_slider_change(e, page):
    if mixer.music.get_busy():
        mixer.music.set_pos(e.control.value)
        position_seconds[0] = int(e.control.value)
        page.update()


def getIndexByPath(path: str):
    try:
        with open(fileJSON, "r") as file:
            songs = json.load(file)

        for pathIndex in range(len(songs["paths"])):
            if songs["paths"][pathIndex] == path:
                return pathIndex

    except Exception as e:
        return f"Error: {e}"


def playMusic(
    e,
    path: str,
    id,
    slider,
    page,
    idPlaylist,
    crnt_msc,
    crnt_artist,
    crnt_img,
    main_button,
    current_vol,
):

    global thread_started

    def getMusicName(path: str):
        count = path.count("-")
        while count > 0:
            indexOfTrace = path.index("-")
            path = path[indexOfTrace + 2 :]
            count -= 1
        return path

    def getArtist(name):
        return name.split("-")[0] if "-" in name else "Unknown Artist"

    if not os.path.exists(path):
        return "Path given does not exists"

    if not path.endswith(".mp3"):
        return "Please, select a .mp3 file."

    try:
        is_current_music = status["current_index"] == id
        same_playlist = playlist_id["id"] == idPlaylist

        if (
            is_current_music
            and status["is_playing"]
            and not status["is_paused"]
            and same_playlist
        ):
            status["is_paused"] = True
            status["is_playing"] = False
            e.content = ft.Icon(
                ft.Icons.PAUSE_SHARP, color=Colors.current_music_color, size=20
            )
            mixer.music.pause()
            return

        if (
            is_current_music
            and status["is_paused"]
            and not status["is_playing"]
            and same_playlist
        ):
            status["is_paused"] = False
            status["is_playing"] = True
            e.content = ft.Icon(
                ft.Icons.PLAY_ARROW, color=Colors.current_music_color, size=20
            )
            mixer.music.unpause()
            return

        if not is_current_music or not same_playlist:
            mixer.music.load(path)
            mixer.music.play()
            main_button.content = ft.Icon(ft.Icons.PAUSE_SHARP, color="black")
            mixer.music.set_volume(current_vol[0])
            position_seconds[0] = 0
            slider.max = MP3(path).info.length
            slider.min = 0
            slider.on_change = lambda e: on_slider_change(e, page)

            status.update({"is_playing": True, "is_paused": False, "current_index": id})
            playlist_id["id"] = idPlaylist
            mixer.music.set_endevent(MUSIC_END)

            music_name = os.path.basename(path).replace(".mp3", "")
            crnt_msc.value = getMusicName(music_name)
            crnt_artist.value = getArtist(music_name)
            crnt_img.src = path.replace(".mp3", ".jpg")

            crnt_msc.update()
            crnt_artist.update()
            crnt_img.update()

            if not thread_started:
                threading.Thread(
                    target=loop_check_end,
                    args=(
                        e,
                        slider,
                        page,
                        crnt_msc,
                        crnt_artist,
                        crnt_img,
                        main_button,
                        current_vol,
                    ),
                    daemon=True,
                ).start()
                thread_started = True

            e.update()

    except Exception as ex:
        return f"Error playing music: {ex}"


def playNext(
    e,
    id,
    idPlaylist,
    slider,
    page,
    crnt_msc,
    crnt_artist,
    crnt_img,
    main_button,
    current_vol,
):
    if id + 1 == len(playConf.get_all_playlist_musics(idPlaylist, "all")):
        id = -1
    return playMusic(
        e,
        playConf.getMusicByIndex(idPlaylist, id + 1),
        id + 1,
        slider,
        page,
        idPlaylist,
        crnt_msc,
        crnt_artist,
        crnt_img,
        main_button,
        current_vol,
    )


def playPrevious(
    e,
    id,
    idPlaylist,
    slider,
    page,
    crnt_msc,
    crnt_artist,
    crnt_img,
    main_button,
    current_vol,
):
    if id - 1 == 0:
        len(playConf.get_all_playlist_musics(idPlaylist, "all")) + 1
    return playMusic(
        e,
        playConf.getMusicByIndex(idPlaylist, id - 1),
        id - 1,
        slider,
        page,
        idPlaylist,
        crnt_msc,
        crnt_artist,
        crnt_img,
        main_button,
        current_vol,
    )


def stopSong():
    if mixer.get_busy():
        mixer.music.stop()
        return
    return


def check_music_end(
    e, slider, page, crnt_msc, crnt_artist, crnt_img, main_button, current_vol
):
    idPlaylist = playlist_id["id"]
    for event in pygame.event.get():
        if event.type == MUSIC_END:
            next_index = status["current_index"] + 1
            if next_index < len(playConf.get_all_playlist_musics(idPlaylist, "all")):
                playMusic(
                    e,
                    playConf.getMusicByIndex(idPlaylist, next_index),
                    next_index,
                    slider,
                    page,
                    idPlaylist,
                    crnt_msc,
                    crnt_artist,
                    crnt_img,
                    main_button,
                    current_vol,
                )


def loop_check_end(
    e, slider, page, crnt_msc, crnt_artist, crnt_img, main_button, current_vol
):
    while True:
        check_music_end(
            e, slider, page, crnt_msc, crnt_artist, crnt_img, main_button, current_vol
        )
        time.sleep(1)
