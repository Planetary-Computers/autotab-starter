import threading

import cv2
import numpy as np

from server.server import run_server
from utils.driver import get_mirror


def open_application_window(width: int, height: int):
    # Create a named window
    cv2.namedWindow("Autotab Mirror", cv2.WINDOW_NORMAL)
    # Resize the window
    cv2.resizeWindow("Autotab Mirror", width, height)
    return "Autotab Mirror"


def stream_video(driver, window):
    while True:
        # Capture frame-by-frame from the browser
        frame = driver.get_screenshot_as_png()
        # Convert the PNG binary data to an image array
        frame_arr = np.frombuffer(frame, np.uint8)
        img_arr = cv2.imdecode(frame_arr, cv2.IMREAD_COLOR)
        # Convert the image from BGR to RGB color space
        # img = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
        # Display the resulting frame in the application window
        cv2.imshow(window, img_arr)
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


def mirror(
    # driver: AutotabChromeDriver
    width: int = 200,
    height: int = 50,
):
    driver = get_mirror(width=200, height=50)
    window = open_application_window(200, 50)
    server_thread = threading.Thread(target=run_server, args=(driver,))
    server_thread.start()
    stream_video(driver, window)


def close():
    cv2.destroyAllWindows()
