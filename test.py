#システムの利用を宣言する
import os
import sys

#PyOCRを読み込む
from PIL import Image
import pyocr

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

#画像の読み込み
img = Image.open("2.png")

#文字を読み取る
builder = pyocr.builders.TextBuilder(tesseract_layout=6)
result = tool.image_to_string(img,lang="eng",builder=builder)

#結果を出力
print(result)