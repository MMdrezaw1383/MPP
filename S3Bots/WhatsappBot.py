import pyautogui as pg 
# http://pyautogui.readthedocs.io
from time import sleep
from random import choice

# print(pg.position())
# pg.moveTo(0,0)
# pg.moveTo(1176,465)
# pg.doubleClick()
# pg.doubleClick()

lst= ["hello!", "hi", "i am robot", "reza"]
for i in range(4):
    sleep(1)
    pg.click(410, 986)
    pg.write(choice(lst), interval=0.1)
    pg.hotkey('shift', 'enter')

pg.press("enter")