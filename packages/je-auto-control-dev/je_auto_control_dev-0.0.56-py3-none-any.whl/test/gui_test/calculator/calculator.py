import subprocess
from time import sleep

from je_auto_control import locate_and_click

# 開啟windows 計算機
# 並累加1至9
# open windows calc.exe
# and calculate 1 + 2 .... + 9

subprocess.Popen("calc", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
sleep(3)

locate_and_click(
    "../../test_source/1.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/plus.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)

locate_and_click(
    "../../test_source/2.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)

locate_and_click(
    "../../test_source/equal.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/plus.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/3.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/plus.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/4.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/plus.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/5.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/plus.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/6.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/plus.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/7.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/plus.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/8.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/plus.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/9.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
locate_and_click(
    "../../test_source/equal.png",
    mouse_keycode="mouse_left",
    detect_threshold=0.9,
    draw_image=False
)
