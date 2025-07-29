import json
import os
import tkinter as tk
from tkinter import filedialog

fileJSON = os.path.join(os.path.abspath("configs/intFiles"), "User.json")


def get_user_pfp():
    if os.path.exists(fileJSON):
        with open(fileJSON, "r") as file:
            userProf = json.load(file)
        if userProf["pfp_path"] == "":
            return False
        else:
            return userProf["pfp_path"]


def find_pfp():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfile(
        title="Select a picture",
        filetypes=[("JPG", ".jpg"), ("PNG", ".png"), ("JPEG", ".jpeg")],
    )
    if add_pfp(file_path.name) == True:
        return True


def add_pfp(path: str):
    if os.path.exists(path):
        if path.endswith(".jpg" or ".png" or ".jpeg"):
            with open(fileJSON, "r") as file:
                userConf = json.load(file)

            userConf["pfp_path"] = path
            with open(fileJSON, "w") as file:
                json.dump(userConf, file, indent=4)
            return True
        return "Invalid type of file. (Only accepts .jpg, .png and .jpeg)"
    return "The path given does not exists."


def getUserName():
    try:
        with open(fileJSON, "r") as file:
            user = json.load(file)

        return user["name"]
    except Exception as e:
        return f"Error: {e}"


def setUserName(name: str):
    try:
        with open(fileJSON, "r") as file:
            user = json.load(file)

        user["name"] = name

        with open(fileJSON, "w") as file:
            json.dump(user, file, indent=4)
    except Exception as e:
        return f"Error: {e}"


def getEmail():
    try:
        with open(fileJSON, "r") as file:
            user = json.load(file)

        return user["email"]
    except Exception as e:
        return f"Error: {e}"


def setEmail(email: str):
    try:
        with open(fileJSON, "r") as file:
            user = json.load(file)

        if not user["email"].endswith(".com"):
            user["email"] = email + "@gmail.com"
        else:
            user["email"] = email

        with open(fileJSON, "w") as file:
            json.dump(user, file, indent=4)
    except Exception as e:
        return f"Error: {e}"


def getBackupPath():
    try:
        with open(fileJSON, "r") as file:
            conf = json.load(file)

        return conf["backup_path"]
    except Exception as e:
        return e


def setBackupPath(path: str):
    try:
        with open(fileJSON, "r") as file:
            user = json.load(file)

        user["backup_path"] = path

        with open(fileJSON, "w") as file:
            json.dump(user, file, indent=4)
    except Exception as e:
        return f"Error: {e}"
