import numpy as np
import asyncio
import matplotlib.pyplot as plt


def diffuse_heat_fdtd(grid, dx=1.0, dt=1.0, D=0.25):
    """
    Single time step of heat diffusion simulation

    args:
        grid: 2D numpy array of temperatures
        dx: spatial step size
        dt: time step size
        D: diffusion coefficient
    """

    error = D * dt / (dx * dx)
    if error > 0.5:
        raise ValueError(f"Simulation unstable: error = {error}")

    new_grid = grid.copy()

    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):

            new_grid[i, j] = grid[i, j] + D * dt / dx**2 * (
                grid[i + 1, j]
                + grid[i - 1, j]
                + grid[i, j + 1]
                + grid[i, j - 1]
                - 4 * grid[i, j]
            )

    return new_grid


def exponential_function_over_time(t, A=1.0, tau=1.0):
    """Exponential function A * exp(-t/tau)"""
    return A * np.exp(-t / tau)


class AsyncSimulation:
    def __init__(self, width=10, height=10, period=0.1):
        self.running = True
        self.echo = True  # echo to console

        self.width = width
        self.height = height

        self.step = 0
        self.period = period

        self.ambient_temperature = 5.0

        # heat source
        self.center_x = width // 2
        self.center_y = height // 2
        self.heat_source_is_on = True
        self.heat_source_temperature = 60.0

        self.heat_price = 0.2
        self.cost = None

        self.sensor_x = 2
        self.sensor_y = 2
        self.sensor_value = None

        self.sensor_thermostat_state = False  # True if the thermostat is on
        self.sensor_thermostat_temperature = 10.0

        # initialize grid
        # self.grid = np.zeros((self.width, self.height))
        self.grid = np.ones((self.width, self.height)) * self.ambient_temperature

    async def reset(self):
        self.grid = np.ones((self.width, self.height)) * self.ambient_temperature
        self.step = 0

    async def start(self):
        self.running = True

    async def stop(self):
        self.running = False

    async def run(self):
        while self.running:

            if self.heat_source_is_on:

                self.grid[
                    self.center_x - 1 : self.center_x + 1,
                    self.center_y - 1 : self.center_y + 1,
                ] = self.heat_source_temperature

            # do the diffusion
            self.grid = diffuse_heat_fdtd(self.grid)
            # sensor: measure the grid
            self.sensor_value = self.grid[self.sensor_x, self.sensor_y]

            # Reset edges to ambient temperature

            # sensor: check thermostat threshold
            if self.sensor_value > self.sensor_thermostat_temperature:
                self.sensor_thermostat_state = True
            else:
                self.sensor_thermostat_state = False

            if self.step % 10 == 0 and self.echo:
                print(
                    f"Step {self.step}, {self.sensor_value}, {self.sensor_thermostat_state}"
                )

            self.step += 1

            await asyncio.sleep(self.period)


def visualise_heat_diffusion_animated(width=50, height=50, n_steps=100):
    """Visualise heat diffusion in an animated plot"""
    grid = np.zeros((width, width))
    # plt.figure(figsize=(width, width))

    for step in range(n_steps):

        grid[width // 2 - 2 : width // 2 + 2, width // 2 - 2 : width // 2 + 2] = max(
            0, 100
        )

        plt.clf()
        plt.imshow(grid, cmap="hot", vmin=0, vmax=50)
        plt.colorbar()
        plt.title(f"Heat Distribution at step {step}")
        plt.pause(0.1)
        grid = diffuse_heat_fdtd(grid)
        plt.savefig(f"./img/heat_step_{step:04d}.png")


if __name__ == "__main__":
    visualise_heat_diffusion_animated()
