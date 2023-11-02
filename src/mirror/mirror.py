import threading

import cv2
import numpy as np

from server.server import run_server
from utils.driver import AutotabChromeDriver, get_mirror_driver


def open_application_window(width: int, height: int, left: int):
    # Create a named window
    cv2.namedWindow("Autotab Mirror", cv2.WINDOW_NORMAL)
    # Resize the window
    cv2.resizeWindow("Autotab Mirror", width, height)
    # Position the window
    cv2.moveWindow("Autotab Mirror", left, 0)
    return "Autotab Mirror"


def stream_video(driver: AutotabChromeDriver, window_name: str, scaling_factor: float):
    while True:
        try:
            # Capture frame-by-frame from the browser
            frame = driver.get_screenshot_as_png()
            # Convert the PNG binary data to an image array
            frame_arr = np.frombuffer(frame, np.uint8)
            img_arr = cv2.imdecode(frame_arr, cv2.IMREAD_COLOR)

            # Resize the image
            scale_percent = scaling_factor * 100
            width = int(img_arr.shape[1] * scale_percent / 100)
            height = int(img_arr.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(img_arr, dim, interpolation=cv2.INTER_AREA)

            cv2.imshow(window_name, resized)
            cv2.waitKey(1)
        except KeyboardInterrupt:
            return
        except Exception as e:
            if "no such window: target window already closed" in str(e):
                pass
            else:
                print("streaming frame error: {}".format(e))


def mirror(
    driver_width: int,
    driver_height: int,
    window_scaling_factor: float,
    left: int = 0,
):
    driver = get_mirror_driver(width=driver_width, height=driver_height)
    window = open_application_window(
        int(driver_width * window_scaling_factor),
        int(driver_height * window_scaling_factor),
        left,
    )
    server_thread = threading.Thread(target=run_server, args=(driver,))
    server_thread.start()
    stream_video(driver, window, window_scaling_factor)


def close():
    cv2.destroyAllWindows()
