#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import numpy as np
from pylsl import StreamInlet, resolve_byprop
from scipy.signal import welch
import matplotlib.pyplot as plt

data_length = 100
x = []
y = []
count = 0

# 周波数帯域の定義
BANDS = {
    'Delta': (0.5, 4),
    'Theta': (4, 8),
    'Alpha': (8, 12),
    'Beta': (12, 30),
    'Gamma': (30, 45)
}

# EEGストリームを解決する
print("Looking for an EEG stream...")
streams = resolve_byprop('type', 'EEG', timeout=5)

if len(streams) == 0:
    print("No EEG stream found.")
    exit()

# ストリームからデータを取得するためのinletを作成する
inlet = StreamInlet(streams[0])

print("Start receiving data...")

# サンプリング周波数を取得
fs = int(inlet.info().nominal_srate())

# ウィンドウサイズの設定（例えば1秒間のデータを使用）
window_size = fs  # 1秒分のデータ
data_buffer = np.zeros((window_size, inlet.info().channel_count()))  # ゼロで初期化されたバッファ
buffer_index = 0

# 初期バッファの充填
print("Filling buffer...")
while buffer_index < window_size:
    sample, timestamp = inlet.pull_sample()
    data_buffer[buffer_index, :] = sample
    buffer_index += 1

print("Buffer filled, starting data processing...")

plt.ion()  # インタラクティブモードオン
fig, ax = plt.subplots()

while True:
    count += 1
    # サンプルを受信する
    sample, timestamp = inlet.pull_sample()
    data_buffer = np.roll(data_buffer, -1, axis=0)
    data_buffer[-1, :] = sample

    # 各チャネルごとに周波数帯域の成分を計算
    band_powers = {}
    for channel in range(data_buffer.shape[1]):
        freqs, psd = welch(data_buffer[:, channel], fs, nperseg=window_size)
        for band, (low, high) in BANDS.items():
            idx_band = np.logical_and(freqs >= low, freqs <= high)
            band_power = np.mean(psd[idx_band])
            if band not in band_powers:
                band_powers[band] = []
            band_powers[band].append(band_power)

    # 各帯域の平均パワーを計算
    for band in BANDS.keys():
        band_powers[band] = np.mean(band_powers[band])

    x.append(count)
    y.append(band_powers['Delta'])

    if len(x) > 100:
        del x[0]
        del y[0]

    ax.clear()
    ax.plot(x, y)
    ax.set_ylim(0, 100)  # y軸の範囲を設定
    ax.set_title("Delta Band Power Over Time")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Delta Band Power")

    plt.pause(0.1)

    # データをリアルタイムで表示
    print(f"Timestamp: {timestamp}, Band Powers: {band_powers}")

    time.sleep(1.0)  # 1秒ごとにデータを処理