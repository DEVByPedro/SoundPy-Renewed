import configs.PlaylistConfig as playlistConfig

import subprocess
import os
import platform
import urllib.request
import zipfile
import shutil


def download_mp3(e, video_url, idPlaylist):

    if not os.path.exists("sysConf/ffmpeg-2025-03-31-git-35c091f4b7-essentials_build"):
        so = platform.system()
        if so == "Windows":
            destino = os.path.abspath(
                "sysConf/ffmpeg-2025-03-31-git-35c091f4b7-essentials_build/bin"
            )
            print("Instalando arquivos")
            url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
            zip_path = "sysConf/ffmpeg.zip"

            urllib.request.urlretrieve(url, zip_path)

            print("Extraindo arquivos")
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(destino)

            pastas = os.listdir(destino)
            for pasta in pastas:
                bin_path = os.path.join(destino, pasta, "bin")
                if os.path.exists(bin_path):
                    for arquivo in os.listdir(bin_path):
                        shutil.move(
                            os.path.join(bin_path, arquivo),
                            os.path.join(destino, arquivo),
                        )
                    break

            shutil.rmtree(os.path.join(destino, pasta))
            os.remove(zip_path)
        elif so == "Linux":
            print("Instalando FFmpeg no Linux")
            subprocess.run(["sudo", "apt", "update"])
            subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"])

        elif so == "Darwin":
            print("Instalando FFmpeg no macOS")
            subprocess.run(["brew", "install", "ffmpeg"])

    yt_dlp_path = os.path.abspath(r"sysConf\yt-dlp_x86.exe")
    ffmpegpath = os.path.abspath(
        r"sysConf\ffmpeg-2025-03-31-git-35c091f4b7-essentials_build\bin"
    )

    output_template = os.path.abspath("arquives") + "\\%(uploader)s - %(title)s.%(ext)s"

    command = [
        yt_dlp_path,
        "-x",
        "--audio-format",
        "mp3",
        "--restrict-filenames",
        "--write-thumbnail",
        "--convert-thumbnails",
        "jpg",
        "--ffmpeg-location",
        ffmpegpath,
        "-o",
        output_template,
        "--print",
        "after_move:filepath",
        video_url,
    ]

    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        all_musics = []
        for line in process.stdout:
            if line.strip().endswith(".mp3"):
                all_musics.append(line.strip())

        process.wait()
        if process.returncode == 0:
            for music in all_musics:
                if not playlistConfig.containsMusic(idPlaylist, music):
                    new_name = music.replace("_", " ")
                    new_path = os.path.join(os.path.dirname(music), os.path.basename(new_name))

                    os.rename(music, new_path)

                    photo_old_path = music.replace(".mp3", ".jpg")
                    photo_new_name = new_name.replace(".mp3", ".jpg")
                    photo_new_path = os.path.join(os.path.dirname(photo_old_path), os.path.basename(photo_new_name))

                    if os.path.exists(photo_old_path):
                        os.rename(photo_old_path, photo_new_path)

                    playlistConfig.addMusic(idPlaylist, new_path)
            return True
        else:
            return False
    except Exception as e:
        print("Erro ao executar o comando:", e)
        return False
