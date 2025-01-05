# MicroHEAT

A 2d heat diffusion simuation wrapped in a Web API

![img/heat_diffusion.mp4](img/heat_diffusion.mp4)

Useful for:

- Home Assistant Testing
- Heat strategies using sensors and thermostats
- Logging and python program development

**Quickstart:**

```sh
# (optional) create a virtual env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# (optional) test model
python3 ./simulation.py

# run aiohttp webserver
python3 ./server.py
# server running at http://localhost:8080
```

## API endpoints

- http://localhost:8080/reset - reset sim
- http://localhost:8080/sensor - read sensor value
- http://localhost:8080/heat-source/on - switch heat source on
- http://localhost:8080/heat-source/off - switch heat source off
- http://localhost:8080/heat-source/temp/{temp} - set heat source temperature
