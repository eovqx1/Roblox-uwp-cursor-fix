import sys
import win32gui
import win32con
import pyautogui
from pynput.mouse import Listener, Button, Controller
from pynput import keyboard
import time

def is_uwp_app_focused():
    active_window = win32gui.GetForegroundWindow()
    if win32gui.GetWindowLong(active_window, win32con.GWL_STYLE) & win32con.WS_VISIBLE:
        class_name = win32gui.GetClassName(active_window)
        return "ApplicationFrameWindow" in class_name
    return False

locked = False
mouseX, mouseY = 0, 0
isfocused = False

def lock_cursor():
    global locked, mouseX, mouseY
    mouseX, mouseY = pyautogui.position().x, pyautogui.position().y
    locked = True
    if isfocused:
        print(f"[DEBUG] Locking cursor")

def unlock_cursor():
    global locked
    if locked and isfocused:
        pyautogui.moveTo(mouseX, mouseY)
    locked = False
    if isfocused:
        print(f"[DEBUG] Unlocking cursor")

def on_click(x, y, button, pressed):
    if button == Button.right:
        if pressed:
            lock_cursor()
        else:
            unlock_cursor()

mlistener = Listener(on_click=on_click)
mlistener.start()

gInterval = 0.05

running = True
def on_release(key):
    global running, gInterval
    if key == keyboard.Key.insert:
        mlistener.stop()
        running = False
        return False
    elif key == keyboard.Key.delete:
        if not locked: gInterval = 0.025; lock_cursor()
        else: gInterval = 0.05; unlock_cursor()

listener = keyboard.Listener(on_release=on_release)
listener.start()

print("""[DEBUG] Started
### UWP Roblox Cursor Fix ###
Written by eovqx. on discord.
Instructions:
 
To manually lock/unlock your cursor, press DEL on your keyboard.
 press INS on your keyboard to exit
""")

wasfocused = False
while running:
    isfocused = is_uwp_app_focused()
    if locked and isfocused:
        if not wasfocused:
            print("[DEBUG] Window focused")
            wasfocused = True
        pyautogui.moveTo(mouseX, mouseY)
    if wasfocused and not isfocused:
        print("[DEBUG] Lost focus")
        wasfocused = False
    time.sleep(gInterval)
