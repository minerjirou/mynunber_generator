# https://github.com/yayoimizuha/mynumber_generator のC++コードをPythonに移植。
import numpy as np
from numba import cuda
import math

# 定数
Qn = np.array([6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2], dtype=np.int16)
div_arr = np.array([10**i for i in reversed(range(11))], dtype=np.int64)
snprintf_arr = np.array([10**i for i in reversed(range(12))], dtype=np.int64)

# CUDAカーネル関数
@cuda.jit
def calculate_12digit_numbers(start, chunk, output):
    idx = cuda.grid(1)
    if idx < chunk:
        input_num = start + idx
        acc = 0

        # 検査用数字計算
        for k in range(11):
            acc += Qn[k] * ((input_num // div_arr[k]) % 10)
        acc %= 11
        if acc <= 1:
            acc = 0
        else:
            acc = 11 - acc

        # 12桁の番号計算
        comp_val = input_num * 10 + acc
        for k in range(12):
            output[idx * 13 + k] = ord('0') + (comp_val // snprintf_arr[k]) % 10
        output[idx * 13 + 12] = ord('\n')

# メイン関数
def generate_numbers(output_file, total_numbers, chunk_size):
    threads_per_block = 512  # スレッド数を増加して並列度を向上
    with open(output_file, 'wb') as f:
        for start in range(0, total_numbers, chunk_size):
            current_chunk = min(chunk_size, total_numbers - start)

            # GPUメモリ確保
            output_string = cuda.device_array(current_chunk * 13, dtype=np.uint8)

            # CUDAカーネル実行
            blocks_per_grid = math.ceil(current_chunk / threads_per_block)
            calculate_12digit_numbers[blocks_per_grid, threads_per_block](start, current_chunk, output_string)

            # 結果をホストにコピー
            f.write(output_string.copy_to_host().tobytes())

if __name__ == "__main__":
    total_numbers = int(input("生成する番号の総数を入力してください: "))
    chunk_size = 1000000  # チャンクサイズを拡大してIO頻度を減少
    output_file = "generated_numbers.txt"

    generate_numbers(output_file, total_numbers, chunk_size)
    print(f"{output_file}に番号を生成しました。")