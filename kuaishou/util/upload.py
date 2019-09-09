import pyautogui


def upload():


    # 获取当前屏幕分辨率
    screenWidth, screenHeight = pyautogui.size()

    # 获取当前鼠标位置
    currentMouseX, currentMouseY = pyautogui.position()

    # 2秒钟鼠标移动坐标为100,100位置  绝对移动
    # pyautogui.moveTo(100, 100,2)
    pyautogui.moveTo(x=100, y=100, duration=2, tween=pyautogui.linear)

    # 鼠标移到屏幕中央。
    pyautogui.moveTo(screenWidth / 2, screenHeight / 2)
