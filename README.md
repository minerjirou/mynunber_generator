# 12桁番号生成ツール

## 概要
このツールは、11桁の番号から検査用数字を計算し、12桁の番号を効率的に生成するためのPythonスクリプトを提供します。高速処理のためにCUDAを利用し、大量の番号を生成する際に適しています。

ツールには以下の2つのスクリプトが含まれています。

1. **`mynumber_generator_cpp2py.py`**
   - C++コードをPythonに移植したCUDAによる生成ツール。
2. **`mynumber_generator_cuda.py`**
   - Pythonのみで純粋に書いた高速なCUDAカーネルを用いた生成ツール。

---

## 必要条件

### ソフトウェア要件
- Python 3.8以上
- CUDA対応GPU
- CUDA Toolkit

### 必要なライブラリ
以下のコマンドを使用して必要なライブラリをインストールしてください。

```bash
pip install numpy numba
```

---

## ファイル一覧

- `mynumber_generator_cpp2py.py` - C++から移植された番号生成ツール。
- `mynumber_generator_cuda.py` - 高速なCUDA実装。
- `README.md` - 本ドキュメント。

---

## 出力形式
生成される番号は以下の形式で出力されます。

```
000000000001
000000000012
000000000023
...
```

出力ファイル名はデフォルトで `generated_numbers.txt` です。

---

## 注意事項

1. CUDA対応GPUが必要です。環境にCUDA Toolkitを正しくインストールしてください。
2. 非常に大規模な生成タスクを実行する場合は、十分なディスク容量を確保してください。
3. 出力ファイルは既存のファイルを上書きするため、必要に応じてバックアップを取ってください。

---

## 使用方法

### `mynumber_generator_cpp2py.py`

1. スクリプトを実行します。
   ```bash
   python mynumber_generator_cpp2py.py
   ```
2. 生成する番号の総数を入力します。
3. 結果は`generated_numbers.txt`に保存されます。

### `mynumber_generator_cuda.py`

1. スクリプトを実行します。
   ```bash
   python mynumber_generator_cuda.py
   ```
2. 生成する番号の総数を入力します。
3. 結果は`generated_numbers.txt`に保存されます。

---

## カスタマイズ

- **チャンクサイズの変更**
  デフォルトでは1,000,000の番号を一度に処理します。
  必要に応じて以下のファイルを編集してください。

  - `mynumber_generator_cpp2py.py`
    ```python
    chunk_size = 1000000
    ```

- **出力ファイル名の変更**
  出力ファイル名を変更するには、以下のファイルを編集してください。

  - `mynumber_generator_cpp2py.py`
    ```python
    output_file = "generated_numbers.txt"
    ```

  - `mynumber_generator_cuda.py`
    ```python
    with open("generated_numbers.txt", "w") as f:
    ```

