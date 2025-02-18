#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
from bleak import BleakClient

address = "5EC5EB41-CADB-F642-47B8-5B61188681BE"  # MuseデバイスのMACアドレス

async def stream_data(address):
    async with BleakClient(address) as client:
        async def handle_data(sender, data):
            print(f"Received data from {sender}: {data}")

        # 特性UUIDを使用
        await client.start_notify('273e0003-4c4d-454d-96be-f03bac821358', handle_data)
        print("Notification started")
        await asyncio.sleep(30)  # 30秒間データを取得
        await client.stop_notify('273e0003-4c4d-454d-96be-f03bac821358')
        print("Notification stopped")

loop = asyncio.get_event_loop()
loop.run_until_complete(stream_data(address))