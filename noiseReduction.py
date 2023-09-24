import csv
from typing import List, Tuple
from noiseReductionHelper import SpeedHelper


def read_csv(filename: str) -> List[Tuple[float, float]]:
    data_list: List[Tuple[float, float]] = []

    # CSVファイルを読み取り
    with open(filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        # 各行を処理
        for row in csvreader:
            # 文字列を浮動小数点数に変換し、タプルに格納
            float_tuple: tuple[float, float] = float(row[0]), float(row[1])
            data_list.append(float_tuple)

    return data_list


def process_speed(arg: List[Tuple[float, float]]) -> List[Tuple[int, float]]:
    # 距離の処理をしてから速度の処理をする
    # dpテーブル用意
    dp: List[int] = []
    for i in range(len(arg)):
        dp.append(0)

    # dpする
    for i in range(len(arg)):
        j = i+1
        while j < len(arg):
            if arg[i][0] > arg[j][0] and dp[j] < dp[i]+1:
                dp[j] = dp[i]+1
            j += 1

    # バックトラック準備
    res0: List[Tuple[int, float]] = []
    start_idx: int = 0
    dp_tmp: int = dp[0]
    for i in range(len(arg)):
        if (dp_tmp < dp[i]):
            start_idx = i

    # バックトラック
    i = start_idx
    dp_prv: int = dp[start_idx]+1
    elem_tmp = int(arg[start_idx-1][0]), arg[start_idx-1][1]
    while i >= 0:
        if dp[i] == dp_prv-1:
            dp_prv = dp[i]
            elem_tmp = int(arg[i][0]), arg[i][1]
            res0.append(elem_tmp)
        i -= 1
    res0.reverse()

    # ここから速度の処理
    res: List[Tuple[int, float]] = []
    speed_prv: 0 = res0[0][1]
    for elem in res0:
        if abs(elem[1]-speed_prv) < 20:
            res.append(elem)
            speed_prv = elem[1]
    return res


def process_limit(arg: List[Tuple[float, float]]) -> List[Tuple[int, int]]:
    res: List[Tuple[int, int]] = []
    dist: int = -1
    limit: int = -1
    for row in arg:
        if (dist == -1 and limit == -1) or (0 < row[0] - dist < 5 and abs(limit - row[1]) < 1 and limit % 5 == 0):
            dist = int(row[0])
            limit = int(row[1])
            tmp: tuple[int, int] = dist, limit
            res.append(tmp)
            continue
    return res


def main():
    speed_list: List[Tuple[float, float]] = read_csv('speed.csv')
    # limit_list: List[Tuple[float, float]] = read_csv('limit.csv')
    speed_list_processed: List[Tuple[int, float]] = process_speed(speed_list)
    # limit_list_processed: List[Tuple[int, int]] = process_limit(limit_list)
    for row in speed_list_processed:
        print(row)


if __name__ == "__main__":
    main()
