import asyncio
import json
import psutil
from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, HTMLResponse
from app.utils import minify_html

html = str

router = APIRouter(prefix="/sys", tags=["sys"], include_in_schema=False)

templates = Jinja2Templates(directory="app/templates")
templates.env.trim_blocks = True
templates.env.lstrip_blocks = True


# Fungsi generator untuk streaming data ke client
async def sys_event_stream():
    labels = ["" for _ in range(30)]
    values_cpu = [None for _ in range(30)]
    values_memory = [None for _ in range(30)]
    while True:
        data = {
            "cpu": {"labels": labels, "values": values_cpu},
            "memory": {"labels": labels, "values": values_memory},
        }

        yield f"event: resource-chart-update\ndata: {json.dumps(data)}\n\n"  # send data to client

        # get cpu dta
        cpu_percent = psutil.cpu_percent()
        values_cpu.append(cpu_percent)

        # get memory data
        memory_percent = psutil.virtual_memory().percent
        values_memory.append(memory_percent)

        # get datetime
        labels.append(datetime.now().isoformat())

        # remove the first element if the length is more than 30
        if len(labels) > 30:
            values_cpu.pop(0)
            values_memory.pop(0)
            labels.pop(0)

        await asyncio.sleep(3)  # send data every 3 seconds


@router.get("/sse")
async def get_sys_event_stream():
    return StreamingResponse(sys_event_stream(), media_type="text/event-stream")


@router.get("/")
async def view_root(request: Request):
    _tamplate = "sys/index.jinja"
    res = templates.TemplateResponse(
        _tamplate, {"request": request, "title": "System Info"}
    )
    minify = await minify_html(res)
    return minify


@router.get("/battery")
async def get_sys_battery() -> HTMLResponse:
    class BatteryIcon:
        EMPTY = "battery"
        HALF = "battery-half"
        FULL = "battery-full"
        CHARGING = "battery-charging"

    battery = psutil.sensors_battery()
    if not battery:
        return HTMLResponse(content="<h1>No battery detected</h1>", status_code=404)

    icon = (
        BatteryIcon.CHARGING
        if battery.power_plugged
        else (
            BatteryIcon.FULL
            if battery.percent > 50
            else BatteryIcon.HALF if battery.percent > 20 else BatteryIcon.EMPTY
        )
    )

    html_content: html = (
        f"""<span><i class="bi bi-{icon}"></i> {battery.percent:.2f}%</span>"""
    )
    return HTMLResponse(content=html_content, status_code=200)
