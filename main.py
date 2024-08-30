import pygame
import pyautogui
import pywinauto
import win32api
import webbrowser
import os
from pygame.locals import *

# This is the list of all the buttons that will simulate being presed on the keyboard when you press them on your controller
def alt_tab():
    pywinauto.keyboard.send_keys("{VK_MENU down}{TAB}{VK_MENU up}")

def open_youtube():
    webbrowser.open("https://www.youtube.com")

def close_tab():
    pyautogui.hotkey('ctrl', 'w')

def open_new_tab():
    pyautogui.hotkey('ctrl', 't')

def switch_to_next_tab():
    pyautogui.hotkey('ctrl', 'tab')

def switch_to_previous_tab():
    pyautogui.hotkey('ctrl', 'shift', 'tab')

def switch_to_next_window():
    pyautogui.hotkey('ctrl', 'winright', 'right')

def switch_to_previous_window():
    pyautogui.hotkey('ctrl', 'winright', 'left')

def take_screenshot():
    pyautogui.hotkey('winleft', 'prtsc')

def paste_text():
    pyautogui.hotkey('ctrl', 'v')

def copy_text():
    pyautogui.hotkey('ctrl', 'c')

def backspace():
    pyautogui.hotkey('backspace')

def change_window():
    pyautogui.hotkey('winleft', 'tab')

pygame.init()

# Making sure you have an adequate controller connected
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

if joystick_count == 0:
    print("No joystick found. Please connect a controller.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# Mapping ALL THE buttons on the controller
left_joystick_x_axis = 0
left_joystick_y_axis = 1
right_joystick_x_axis = 2
right_joystick_y_axis = 3
right_joystick_button = 8
left_shoulder_button = 9
right_shoulder_button = 10
ZR = 11
ZL = 12
y_button = 3
b_button = 1
minus_button = 4
plus_button = 6
d_pad_right = 14
d_pad_left = 13
home_button = 15
windows_button = 7
a_button = 0
x_button = 2

dead_zone = 0.1

cooldown_duration = 500
reset_mouse_cooldown = 5000
reset_distance_threshold = 10
last_action_time = 0
last_reset_time = 0

left_shoulder_button_pressed = False

clock = pygame.time.Clock()
frame_rate = 60

running = True

while running:
    clock.tick(frame_rate)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

# Left stick to control the cursor, once the stick is moved past a certain zone the cursor will begin moving.
        if event.type == JOYAXISMOTION:
            if event.axis == left_joystick_x_axis or event.axis == left_joystick_y_axis:
                if abs(joystick.get_axis(left_joystick_x_axis)) > dead_zone or abs(joystick.get_axis(left_joystick_y_axis)) > dead_zone:
                    mouse_x = int(joystick.get_axis(left_joystick_x_axis) * 10)
                    mouse_y = int(joystick.get_axis(left_joystick_y_axis) * 10)
                    win32api.SetCursorPos((pyautogui.position()[0] + mouse_x, pyautogui.position()[1] + mouse_y))

        elif event.type == JOYBUTTONDOWN:
            current_time = pygame.time.get_ticks()
            print(event.button)

            # When the program runs, call the functions from above depending on what button is pressed based on what we mapped to that hotkey

            if current_time - last_action_time >= cooldown_duration:
                if event.button == left_shoulder_button:
                    left_shoulder_button_pressed = True
                    pyautogui.mouseDown()

                elif event.button == right_shoulder_button:
                    pyautogui.rightClick()

                elif event.button == y_button:
                    open_youtube()

                elif event.button == minus_button:
                    close_tab()

                elif event.button == plus_button:
                    open_new_tab()

                elif event.button == ZR:
                    switch_to_next_window()

                elif event.button == ZL:
                    switch_to_previous_window()

                elif event.button == windows_button:
                    alt_tab()

                elif event.button == d_pad_right:
                    switch_to_next_tab()

                elif event.button == d_pad_left:
                    switch_to_previous_tab()

                elif event.button == home_button:
                    take_screenshot()

                elif event.button == x_button:
                    paste_text()

                elif event.button == a_button:
                    copy_text()

                elif event.button == b_button:
                    backspace()

                elif event.button == right_joystick_button:
                    change_window()

                last_action_time = current_time

# LMB is left shoulder button
        elif event.type == JOYBUTTONUP:
            if event.button == left_shoulder_button:
                left_shoulder_button_pressed = False
                pyautogui.mouseUp()

    current_time = pygame.time.get_ticks()
    if current_time - last_reset_time >= reset_mouse_cooldown:
        screen_width, screen_height = pyautogui.size()
        mouse_x, mouse_y = pyautogui.position()

# The cursor cant go off the screen or else it will be reset
        if mouse_x < reset_distance_threshold or mouse_x > screen_width - reset_distance_threshold or \
           mouse_y < reset_distance_threshold or mouse_y > screen_height - reset_distance_threshold:
            pyautogui.moveTo(screen_width / 2, screen_height / 2)
            last_reset_time = current_time

pygame.quit()
