import aiohttp
from aiohttp import web
import asyncio
import random
from simulation import AsyncSimulation


sim = AsyncSimulation()


async def get_simulation_value(request):
    return web.json_response({"value": sim.sensor_value})


async def start_background_tasks(app):
    app["simulation_task"] = asyncio.create_task(sim.run())


async def cleanup_background_tasks(app):
    sim.running = False
    await app["simulation_task"]


async def plot(request):
    await asyncio.to_thread(sim.plot())
    return web.json_response({"success": True})


async def reset(request):
    await sim.reset()
    return web.json_response({"success": True})


async def set_heat_source_on(request):
    sim.heat_source_is_on = True
    return web.json_response({"success": True})


async def set_heat_source_off(request):
    sim.heat_source_is_on = False
    return web.json_response({"success": True})


async def set_heat_source_temperature(request):
    temp = request.match_info["temp"]
    sim.heat_source_temperature = float(temp)
    return web.json_response({"success": True})


async def get_thermostat(request):
    return web.json_response({"value": sim.sensor_thermostat})


async def index(request):
    return aiohttp.web.FileResponse(
        "static/index.html", headers={"Content-Type": "text/html"}
    )


app = web.Application()
# app.router.add_static("/", path="static", name="static")
app.router.add_get("/", index)
app.router.add_get("/reset", reset)
app.router.add_get("/sensor", get_simulation_value)
app.router.add_get("/thermostat", set_heat_source_on)
app.router.add_get("/heat-source/on", set_heat_source_on)
app.router.add_get("/heat-source/off", set_heat_source_off)
app.router.add_get("/heat-source/temp/{temp}", set_heat_source_temperature)

app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)

if __name__ == "__main__":
    web.run_app(app, port=8080)
