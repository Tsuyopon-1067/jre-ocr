# システムの利用を宣言する
import os
import sys

# PyOCRを読み込む
from PIL import Image
import pyocr

# open cv
import cv2

# データ構造用クラス
from FrameData import FrameData

from Writer import FrameDataWriter

from typing import List
from multiprocessing import Pool


# データ書き込み用クラス
class ClipingPoint:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.x2 = x + width
        self.y1 = y
        self.y2 = y + height

# 引数をまとめるために使う構造体的クラス


class MovieArg:
    def __init__(self, process_num, video_path, RESOLUTION, clpnt, start, end):
        self.process_num = process_num
        self.video_path = video_path
        self.RESOLUTION = RESOLUTION
        self.clpnt = clpnt
        self.start = start
        self.end = end


def read_movie(MOVIE_FILE: str, RESOLUTION: int, clpnt: ClipingPoint):
    tool = initialize()

    runmovie(MOVIE_FILE, RESOLUTION, clpnt)


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


def runmovie(video_path, RESOLUTION, clpnt) -> None:
    cap = cv2.VideoCapture(video_path)

    split_size: int = 1
    if os.cpu_count != None:
        split_size = os.cpu_count()  # type: ignore

    list_len = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)/RESOLUTION)
    split_len: int = int(list_len/split_size)
    count_remain: int = list_len - split_len*split_size
    frame_lst: List[int] = []
    frame_lst.append(0)
    idx_pointer: int = 0

    for i in range(split_size):
        idx_pointer += split_len
        if count_remain > 0:
            idx_pointer += 1
            count_remain -= 1
        frame_lst.append(idx_pointer*RESOLUTION)

    arg_lst: List[MovieArg] = []
    for i in range(split_size):
        arg_lst.append(MovieArg(i, video_path, RESOLUTION,
                       clpnt, frame_lst[i], frame_lst[i+1]))

    p = Pool(split_size)
    ret = p.map(runmovie_sub, arg_lst)

    fdw = FrameDataWriter()
    for v in ret:
        for w in v:
            fdw.write(w)


def runmovie_sub(arg: MovieArg) -> List[FrameData]:
    video_path = arg.video_path
    RESOLUTION = arg.RESOLUTION
    clpnt = arg.clpnt
    start = arg.start
    end = arg.end
    tool = initialize()

    res: List[FrameData] = []
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return res

    for i in range(start, end, RESOLUTION):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            frame = frame[clpnt.y1:clpnt.y2, clpnt.x1:clpnt.x2]
            fd = readtext(tool, cv_to_pil(frame))
            res.append(fd)
        else:
            return res
    return res


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
