import csv
from typing import List, Tuple, Union

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
    ret: List[Tuple[int, float]] = create_dp(arg)

    # ここから速度の処理
    res: List[Tuple[int, float]] = []
    speed_prv: float = arg[0][1]
    for elem in ret:
        if abs(elem[1]-speed_prv) < 20:
            res.append(elem)
            speed_prv = elem[1]
    return res

def process_limit(arg: List[Tuple[float, float]]) -> List[Tuple[int, int]]:
    ret: List[Tuple[int, float]] = create_dp(arg)

    # ここから制限の処理
    res: List[Tuple[int, int]] = []
    for elem in ret:
        if elem[1] % 5 == 0 and 20 <= elem[1] <= 130:
            tmp = elem[0], int(elem[1])
            res.append(tmp)
    return res

def create_dp(arg: List[Tuple[float, float]]) -> List[Tuple[int, float]]:
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
    res: List[Tuple[int, float]] = []
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
            res.append(elem_tmp)
        i -= 1
    res.reverse()

    return res

def write_csv(arg: Union[List[Tuple[int, int]], List[Tuple[int, float]]], file_name: str):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(arg)

def main():
    speed_list: List[Tuple[float, float]] = read_csv('speed.csv')
    limit_list: List[Tuple[float, float]] = read_csv('limit.csv')
    speed_list_processed: List[Tuple[int, float]] = process_speed(speed_list)
    limit_list_processed: List[Tuple[int, int]] = process_limit(limit_list)
    write_csv(speed_list_processed, 'speed2.csv')
    write_csv(limit_list_processed, 'limit2.csv')

if __name__ == "__main__":
    main()
