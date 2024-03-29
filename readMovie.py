# システムの利用を宣言する
import os
import sys
import time

# PyOCRを読み込む
from PIL import Image
import pyocr

# open cv
import cv2

# データ構造用クラス
from FrameData import FrameData

# データ書き込み用クラス
from Writer import FrameDataWriter


class ClipingPoint:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height


def read_movie(MOVIE_FILE: str, RESOLUTION: int, clpnt: ClipingPoint):
    tool = initialize()
    fdw = FrameDataWriter()
    runmovie(tool, MOVIE_FILE, fdw, RESOLUTION, clpnt)


def initialize():
    # Tesseractのインストール場所
    tesseract_path = "C:\Program Files\Tesseract-OCR"
    if tesseract_path not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + tesseract_path

    # OCRエンジンを取得
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("OCRエンジンが指定されていません")
        sys.exit(1)
    else:
        tool = tools[0]
    return tool


def runmovie(tool, video_path, fdw, RESOLUTION, clpnt):
    cap = cv2.VideoCapture(video_path)
    last_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if not cap.isOpened():
        return

    for i in range(0, last_frame, RESOLUTION):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            frame = frame[clpnt.y1:clpnt.y2, clpnt.x1:clpnt.x2]
            fd = readtext(tool, cv_to_pil(frame))
            fdw.write(fd)
            print_progress_bar(i, last_frame)
        else:
            return


def cv_to_pil(image):
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def readtext(tool, img):
    # 文字を読み取る
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    result = tool.image_to_string(img, lang="eng", builder=builder)

    # 結果を出力
    fd = FrameData(result)
    # print(fd.to_string())
    return fd


def print_progress_bar(now, max):
    rate = 50.0 / max
    done = int(rate * now)
    bar_end = int(rate * max)
    bar = "="*done + (">" if done < bar_end-1 else "=") + " "*(bar_end-done-1)
    print("\r[{}] {}/{}".format(bar, now+1, max), end="")
