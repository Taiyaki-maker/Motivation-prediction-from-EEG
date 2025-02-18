#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
from bleak import BleakClient

address = "5EC5EB41-CADB-F642-47B8-5B61188681BE"  # MuseデバイスのMACアドレス

async def print_services(address):
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid}")

loop = asyncio.get_event_loop()
loop.run_until_complete(print_services(address))
