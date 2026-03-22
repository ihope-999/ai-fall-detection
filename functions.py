import cv2
import os
import time
import pywhatkit as kit
import pyautogui
import urllib
import settings


def check_model_availabity():
    model_path = 'pose_landmarker_lite.task'
    if not os.path.exists(model_path):
        print("Downloading pose model.")
        url = 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task'
        urllib.request.urlretrieve(url, model_path)
        print("Model downloaded.")
    return model_path

def take_fall_picture(frame, now):
    os.makedirs(settings.save_folder, exist_ok=True)
    formatted_time = now.strftime("%H-%M-%S")
    filepath = f"{settings.save_folder}/FALL-{formatted_time}.jpg"
    success = cv2.imwrite(filepath, frame)
    print(f"Picture saved: {success} -> {filepath}")
    return filepath


def create_fall_log(now, fall_count):
    os.makedirs(settings.save_folder, exist_ok=True)
    log_path = f"{settings.save_folder}/fall_log.txt"
    with open(log_path, "a") as f:
        f.write(f"Fall #{fall_count} at {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"Log updated: {log_path}")


def send_WP_message(fall_count, img_path):
    modified_msg = settings.msg + str(fall_count)
    kit.sendwhatmsg_instantly(settings.phone_number, modified_msg, settings.WAIT_WP_OPEN_TIME, close_time=20, tab_close=True)
    time.sleep(settings.WAIT_WP_OPEN_TIME - 5)
    pyautogui.press("tab")
    pyautogui.press("enter")
    print("WP text sent!")

    kit.sendwhats_image(settings.phone_number, img_path, caption=f"Fall #{fall_count}", wait_time=2, close_time=20, tab_close=True)
    time.sleep(2)
    pyautogui.press("enter")
    print("WP image sent!")