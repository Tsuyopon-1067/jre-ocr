# システムの利用を宣言する
import os
import sys

# PyOCRを読み込む
from PIL import Image
import pyocr

# open cv
import cv2

def main():
    tool = initialize()
    #画像の読み込み
    img = Image.open("2.png")
    runmovie(tool, "movie.mp4")


def initialize():
    #Tesseractのインストール場所
    tesseract_path = "C:\Program Files\Tesseract-OCR"
    if tesseract_path not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + tesseract_path

    #OCRエンジンを取得
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("OCRエンジンが指定されていません")
        sys.exit(1)
    else:
        tool = tools[0]
    return tool

def runmovie(tool, video_path):
    cap = cv2.VideoCapture(video_path)
    last_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if not cap.isOpened():
        return

    for i in range(0, last_frame, 12):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            frame = frame[146:293, 1750:1884]
            readtext(tool, cv_to_pil(frame))
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
    #文字を読み取る
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    result = tool.image_to_string(img,lang="eng",builder=builder)

    #結果を出力
    print(result)


if __name__ == "__main__":
    main()