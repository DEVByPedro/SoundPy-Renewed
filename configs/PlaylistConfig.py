import json
import os
from mutagen.mp3 import MP3
from PIL import Image

import configs.MusicConfig as musicConfig
import infra.BodyContent as bodyContent
import infra.PlaylistContent as playlistContent
from configs.MusicConfig import mixer
import flet as ft

fileJSON = os.path.join(os.path.abspath("configs/intFiles"), "Playlist.json")


def add_playlist(name: str):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    maxId = 1
    for id, nameOfPlay in playlist["playlistNames"]:
        if nameOfPlay == name:
            return "Already inserted"
        if id >= maxId:
            maxId = id + 1
    playlist["playlistNames"].append([maxId, name])
    playlist["playlistMusics"].append([maxId, []])
    with open(fileJSON, "w") as file:
        json.dump(playlist, file, indent=4)

def addMusic(idPlaylist, path):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for play in playlist["playlistMusics"]:
        if play[0] == idPlaylist:
            if play[1] == "all":
                return
            play[1].append(path)
    with open(fileJSON, "w") as file:
        json.dump(playlist, file, indent=4)
    return "Added"

def remove_playlist_by_name(name: str):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    idx = None
    for i, pl in enumerate(playlist["playlistNames"]):
        if pl[1] == name:
            idx = i
            break
    if idx is not None:
        playlist["playlistNames"].pop(idx)
        playlist["playlistMusics"].pop(idx)

        for play in playlist["playlistNames"]:
            if play[0] > idx:
                play[0] -= 1

        for play in playlist["playlistMusics"]:
            if play[0] > idx:
                play[0] -= 1

    with open(fileJSON, "w") as file:
        json.dump(playlist, file, indent=4)

def get_all_playlists():
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    return playlist["playlistNames"]

def get_all_playlist_ids():
    with open(fileJSON, "r") as file:
        playlist = json.load(file)

    all_ids = []
    for row in playlist["playlistMusics"]:
        all_ids.append(row[1])
    return all_ids

def getPlaylistNameByIndex(index):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for pl in playlist["playlistNames"]:
        if pl[0] == index:
            return pl[1]
    return ""

def getDuration(id):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for playlistId in playlist["playlistMusics"]:
        if playlistId[0] == id:
            if playlistId[1] == "all":
                return musicConfig.getDuration()
            total = 0
            for path in playlistId[1]:
                try:
                    total += MP3(path).info.length
                except Exception:
                    continue
            seconds = int(total)
            minutes = seconds // 60
            hours = minutes // 60
            seconds = seconds % 60
            minutes = minutes % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return "00:00:00"

def getPlaylistMusicsById(
    e,
    id,
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
):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for playlists in playlist["playlistNames"]:
        if playlists[0] == id:
            body.content.controls.clear()
            body.content.controls.append(
                playlistContent.AllPlaylistSongs(
                    page,
                    id,
                    crnt_msc,
                    crnt_artist,
                    crnt_img,
                    slider,
                    crnt_pos,
                    crnt_max,
                    main_button,
                    current_vol,
                )
            )
            break
    body.content.update()
    body.update()
    page.update()

def setContent(
    e,
    id,
    path,
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
):

    body_column.controls.clear()
    body_column.controls.append(
        playlistContent.AllPlaylistSongs(
            page,
            id,
            crnt_msc,
            crnt_artist,
            crnt_img,
            slider,
            crnt_pos,
            crnt_max,
            main_button,
            current_vol,
        )
    )

    musicConfig.playMusic(
        e,
        path,
        getIndexByPath(id, path),
        slider,
        page,
        id,
        crnt_msc,
        crnt_artist,
        crnt_img,
        main_button,
        current_vol,
    )

    body_column.update()
    page.update()

def get_all_playlist_musics(id, limit):
    def getPlaylistLen(id):
        with open(fileJSON, "r") as file:
            playlist = json.load(file)
        return len(playlist["playlistMusics"][id - 1][1])

    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    musics = []
    try:
        for pl in playlist["playlistMusics"]:
            if pl[0] == id:
                if len(pl[1]) == 0:
                    return []
                if limit == "all":
                    limit = getPlaylistLen(id)
                else:
                    limit = int(limit)
                if pl[1] == "all":
                    allMsc = musicConfig.get_all_musics()
                    for i in range(limit):
                        if i <= len(allMsc):
                            musics.append(allMsc[i])
                else:
                    for i in range(limit):
                        musics.append(pl[1][i])
                return musics
    except IndexError as e:
        return musics

def deleteByIndex(idPlaylist, index):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for play in playlist["playlistMusics"]:
        if play[0] == idPlaylist:
            if play[1] == "all":
                all = musicConfig.get_all_musics()
                if index < 0 or index >= len(all):
                    return -1
                musicConfig.deleteByIndex(index)
                return 1
            if 0 <= index < len(play[1]):
                play[1].pop(index)
                with open(fileJSON, "w") as file:
                    json.dump(playlist, file, indent=4)
                return 1
    return -1

def getIndexByPath(idPlaylist, path):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for play in playlist["playlistMusics"]:
        if play[0] == idPlaylist:
            if play[1] == "all":
                all = musicConfig.get_all_musics()
                for row in all:
                    if row == path:
                        return all.index(row)
            if path in play[1]:
                return play[1].index(path)
    return 0

def editPlaylistName(idPlaylist, newName):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for pl in playlist["playlistNames"]:
        if pl[0] == idPlaylist:
            pl[1] = newName
            break
    with open(fileJSON, "w") as file:
        json.dump(playlist, file, indent=4)
    return "Edited"

def containsMusic(id, path):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)
    for music in playlist["playlistMusics"]:
        if music[0] == id:
            if path in music[1]:
                return True
    return False

def getPhotoImage(path: str):
    if os.path.exists(path):
        if path.endswith(".mp3"):
            new_path = os.path.abspath(path.replace(".mp3", ".jpg"))
            if os.path.exists(new_path):
                imagem = Image.open(new_path).convert("RGB")
                imagem = imagem.resize((100, 100))
                cores = imagem.getcolors(10000)
                cor_mais_comum = max(cores, key=lambda item: item[0])[1]
                return "#%02x%02x%02x" % cor_mais_comum
        return "No Image Found"
    return "#0A0A0A"

def getMusicByIndex(idPlaylist, index):
    with open(fileJSON, "r") as file:
        playlist = json.load(file)

    try:
        for play in playlist["playlistMusics"]:
            if play[0] == idPlaylist:
                return play[1][index]
    except Exception as e:
        return ""

def pause_or_unpause(e):
    if mixer.music.get_busy():
        pause(e)
        return 1
    else:
        unpause(e)
        return 0

def pause(e):
    return mixer.music.pause()

def unpause(e):
    return mixer.music.unpause()

def get_all_playlists_musics():
    all_songs = []
    all_ids = get_all_playlist_ids()

    for playlist in all_ids:
        for music in playlist:
            all_songs.append(music)

    return all_songs

def getPlaylistIdByMusicPath(path: str):
    all_ids = get_all_playlist_ids()

    for id, playlist in enumerate(all_ids):
        for music in playlist:
            if music == path:
                return id + 1

def getPathByName(name: str):
    all_musics = get_all_playlists_musics()

    for music in all_musics:
        if music.__contains__(name):
            return music

def reload_musics():
    for i in range(len(get_all_playlist_ids())):
        i += 1

        all_new_musics = []

        with open(fileJSON, "r") as file:
            playlist = json.load(file)

        for musicPath in playlist["playlistMusics"][i-1][1]:
            all_new_musics.append(os.path.abspath("arquives\\"+os.path.basename(musicPath)))

        for j in range(len(all_new_musics)):
            playlist["playlistMusics"][i-1][1][j] = all_new_musics[j]

        with open(fileJSON, "w") as file:
            json.dump(playlist, file, indent=4)