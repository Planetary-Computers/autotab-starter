import threading
from typing import Optional, Tuple

import cv2
import numpy as np

from server.server import run_server
from utils.driver import AutotabChromeDriver, get_driver

MIRROR_WINDOW_NAME = "Autotab Bot"


def open_application_window(width: int, height: int, left: int):
    # Create a named window
    cv2.namedWindow(MIRROR_WINDOW_NAME, cv2.WINDOW_NORMAL)
    # Resize the window
    cv2.resizeWindow(MIRROR_WINDOW_NAME, width, height)
    # Position the window
    cv2.moveWindow(MIRROR_WINDOW_NAME, left, 0)
    return MIRROR_WINDOW_NAME


def stream_video(
    driver: AutotabChromeDriver,
    window_name: str,
    driver_width: int,
    scaling_factor: float,
):
    while True:
        try:
            # Capture frame-by-frame from the browser
            frame = driver.get_screenshot_as_png()
            # Convert the PNG binary data to an image array
            frame_arr = np.frombuffer(frame, np.uint8)
            img_arr = cv2.imdecode(frame_arr, cv2.IMREAD_COLOR)
            # Get the pixel width of the image
            pixel_width = img_arr.shape[1]
            rescale_factor = driver_width / pixel_width
            # Resize the image
            scale_percent = scaling_factor * rescale_factor * 100
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
    driver_window_size: Tuple[int, int],
    window_scaling_factor: float,
    left: int = 0,
    params_filepath: Optional[str] = None,
):
    driver = get_driver(
        include_ext=False, headless=True, window_size=driver_window_size
    )

    driver_width, driver_height = driver_window_size
    window = open_application_window(
        int(driver_width * window_scaling_factor),
        int(driver_height * window_scaling_factor),
        left,
    )
    server_thread = threading.Thread(
        target=run_server,
        args=(
            driver,
            params_filepath,
        ),
    )
    server_thread.start()
    stream_video(driver, window, driver_width, window_scaling_factor)


def close():
    cv2.destroyAllWindows()
