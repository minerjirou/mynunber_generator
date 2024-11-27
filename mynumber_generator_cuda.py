import numpy as np
from numba import cuda

# CUDAカーネル関数: 検査用数字を計算する
@cuda.jit
def calculate_check_digit(numbers, results):
    idx = cuda.grid(1)

    if idx < numbers.size:
        Pn = cuda.local.array(11, dtype=np.int64)
        Qn = cuda.local.array(11, dtype=np.int64)

        # 入力番号をPnに分割
        num = numbers[idx]
        for i in range(10, -1, -1):
            Pn[i] = num % 10
            num //= 10

        # Qnを計算
        for n in range(1, 12):
            if n <= 6:
                Qn[n - 1] = n + 1
            else:
                Qn[n - 1] = n - 5

        # Σ(Pn * Qn)を計算
        total_sum = 0
        for i in range(11):
            total_sum += Pn[i] * Qn[i]

        # 検査用数字を計算
        remainder = total_sum % 11
        check_digit = 11 - remainder
        if check_digit >= 10:
            check_digit = 0

        # 結果に保存
        results[idx] = check_digit

# メイン関数
def main():
    # 実行時に生成する個数を入力
    try:
        data_size = int(input("生成する12桁の番号の個数を入力してください: "))
    except ValueError:
        print("無効な入力です。整数を入力してください。")
        return

    numbers = np.array([10000000000 + i for i in range(data_size)], dtype=np.int64)
    results = np.zeros(data_size, dtype=np.int64)

    # GPUメモリへの転送
    d_numbers = cuda.to_device(numbers)
    d_results = cuda.to_device(results)

    # CUDAカーネルの実行
    threads_per_block = 256
    blocks_per_grid = (data_size + threads_per_block - 1) // threads_per_block
    calculate_check_digit[blocks_per_grid, threads_per_block](d_numbers, d_results)

    # 結果をCPUに転送
    results = d_results.copy_to_host()

    # ファイルに保存
    with open("generated_numbers.txt", "w") as f:
        for i in range(data_size):
            f.write(f"{numbers[i]}{results[i]}\n")

    # 先頭5行を表示
    with open("generated_numbers.txt", "r") as f:
        for _ in range(5):
            print(f.readline().strip())

if __name__ == "__main__":
    main()
import numpy as np
from numba import cuda

# CUDAカーネル関数: 検査用数字を計算する
@cuda.jit
def calculate_check_digit(numbers, results):
    idx = cuda.grid(1)

    if idx < numbers.size:
        Pn = cuda.local.array(11, dtype=np.int64)
        Qn = cuda.local.array(11, dtype=np.int64)

        # 入力番号をPnに分割
        num = numbers[idx]
        for i in range(10, -1, -1):
            Pn[i] = num % 10
            num //= 10

        # Qnを計算
        for n in range(1, 12):
            if n <= 6:
                Qn[n - 1] = n + 1
            else:
                Qn[n - 1] = n - 5

        # Σ(Pn * Qn)を計算
        total_sum = 0
        for i in range(11):
            total_sum += Pn[i] * Qn[i]

        # 検査用数字を計算
        remainder = total_sum % 11
        check_digit = 11 - remainder
        if check_digit >= 10:
            check_digit = 0

        # 結果に保存
        results[idx] = check_digit

# メイン関数
def main():
    # 実行時に生成する個数を入力
    try:
        data_size = int(input("生成する12桁の番号の個数を入力してください: "))
    except ValueError:
        print("無効な入力です。整数を入力してください。")
        return

    numbers = np.array([i for i in range(data_size)], dtype=np.int64)
    results = np.zeros(data_size, dtype=np.int64)

    # GPUメモリへの転送
    d_numbers = cuda.to_device(numbers)
    d_results = cuda.to_device(results)

    # CUDAカーネルの実行
    threads_per_block = 256
    blocks_per_grid = (data_size + threads_per_block - 1) // threads_per_block
    calculate_check_digit[blocks_per_grid, threads_per_block](d_numbers, d_results)

    # 結果をCPUに転送
    results = d_results.copy_to_host()

    # ファイルに保存
    with open("generated_numbers.txt", "w") as f:
        for i in range(data_size):
            f.write(f"{numbers[i]:011d}{results[i]}\n")

    # 先頭5行を表示
    with open("generated_numbers.txt", "r") as f:
        for _ in range(5):
            print(f.readline().strip())

if __name__ == "__main__":
    main()
