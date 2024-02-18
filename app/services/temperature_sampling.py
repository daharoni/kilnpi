# app/services/temperature_sampling.py
import asyncio
from fastapi import WebSocket
import json
from datetime import datetime
from app.services.websocket_manager import broadcast
from app.utils.global_state import last_temperature, temperature_lock, firingStartTime

async def poll_temperature_sensor():
    new_temp = 100
    while True:
        new_temp += 1
        flags = "some_flag"
        timestamp = datetime.now()
        timeSinceFiringStart = timestamp - firingStartTime
        async with temperature_lock:
            last_temperature = {"temperature": new_temp, "flags": flags, "timestamp": timestamp.isoformat(), "timeSinceFiringStart": timeSinceFiringStart.total_seconds()/(60 * 60)}
            await broadcast(json.dumps(last_temperature))
            # print(new_temp)
        await asyncio.sleep(3)