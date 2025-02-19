#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
from pylsl import StreamInlet, resolve_byprop

# EEGストリームを解決する
print("Looking for an EEG stream...")
streams = resolve_byprop('type', 'EEG', timeout=5)

if len(streams) == 0:
    print("No EEG stream found.")
    exit()

# ストリームからデータを取得するためのinletを作成する
inlet = StreamInlet(streams[0])

print("Start receiving data...")
while True:
    # サンプルを受信する
    sample, timestamp = inlet.pull_sample()
    print(f"Timestamp: {timestamp}, Sample: {sample}")
    time.sleep(0.1)  # 短い遅延を入れてCPU使用率を抑える