import os
import json

fileJSON = os.path.join(os.path.abspath("configs/intFiles"), "Configurations.json")


def getValue():
    try:
        with open(fileJSON, "r") as file:
            conf = json.load(file)

        return True if conf["playlist_recomendation"] == 1 else False
    except Exception as e:
        return e


def getNotifValue():
    try:
        with open(fileJSON, "r") as file:
            conf = json.load(file)

        return True if conf["notification"] == 1 else False
    except Exception as e:
        return e


def isNOtificationEnabled():
    try:
        with open(fileJSON, "r") as file:
            conf = json.load(file)

        return True if conf["notification"] == 1 else False
    except Exception as e:
        return e


def changeVal(e):
    try:
        with open(fileJSON, "r") as file:
            conf = json.load(file)

        if e.data == "true":
            conf["playlist_recomendation"] = 1
        else:
            conf["playlist_recomendation"] = 0

        with open(fileJSON, "w") as file:
            json.dump(conf, file, indent=4)
    except Exception as e:
        return e


def changeNotifVal(e):
    try:
        with open(fileJSON, "r") as file:
            conf = json.load(file)

        if e.data == "true":
            conf["notification"] = 1
        else:
            conf["notification"] = 0

        with open(fileJSON, "w") as file:
            json.dump(conf, file, indent=4)
    except Exception as e:
        return e
