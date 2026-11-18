# Traffic Flow Simulation

A 2D traffic-flow simulation built with **Python** and **Pygame**. The application visualizes vehicle movement through a four-approach road intersection, with traffic lights, lane markings, vehicle spawning, and basic vehicle-stopping behavior.

## Overview

The simulation represents an intersection containing four traffic approaches:

- **H1:** Upper horizontal lane, with vehicles moving from left to right.
- **H2:** Lower horizontal lane, with vehicles moving from right to left.
- **V1:** Upper vertical approach.
- **V2:** Lower vertical approach.

Vehicles are generated automatically and move through the intersection according to their assigned direction. Traffic lights and nearby vehicles influence whether a vehicle can continue moving.

## Application Screenshots

The following screenshots demonstrate the traffic simulation during execution, including vehicle movement, traffic signals, road markings, and live vehicle statistics.

### Simulation Output – 1

![Traffic Flow Simulation Output 1](screenshots/traffic-flow-simulation-01.png)

### Simulation Output – 2

![Traffic Flow Simulation Output 2](screenshots/traffic-flow-simulation-02.png)

## Features

- **Four-lane intersection:** Visualizes two horizontal and two vertical traffic approaches.
- **Traffic light visualization:** Displays red and green traffic signals with a countdown timer.
- **Automatic vehicle generation:** Creates vehicles at regular time intervals.
- **Randomized vehicle speed:** Assigns each vehicle a random speed.
- **Basic traffic stopping behavior:** Vehicles stop when they encounter applicable red traffic lights or another vehicle too close ahead.
- **Intersection road markings:** Includes lane boundaries, dashed lane markings, pedestrian-crossing markings, and directional arrows.
- **Live simulation statistics:** Displays the number of vehicles currently in the simulation and their average recorded waiting time.
- **Real-time rendering:** Updates vehicle positions and the intersection display using the Pygame game loop.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3 | Application programming language |
| Pygame | 2D graphics, rendering, events, and simulation loop |
| Random | Random vehicle generation and speed assignment |
| Time | Timing vehicle generation and traffic-light transitions |

## Project Structure

```text
traffic-flow-simulation-/
│
├── main.py
├── README.md
│
└── screenshots/
    ├── traffic-flow-simulation-01.png
    └── traffic-flow-simulation-02.png

```

The current implementation is contained in a single Python source file.

## Prerequisites

Install the following before running the application:

- Python 3.9 or newer
- pip (Python package installer)
- Pygame

Check your Python installation:

```bash
python3 --version
```

Check pip:

```bash
python3 -m pip --version
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Aakashsah247/traffic-flow-simulation-.git
```

### 2. Open the project directory

```bash
cd traffic-flow-simulation-
```

### 3. Create a virtual environment

**macOS / Linux:**

```bash
python3 -m venv .venv
```

**Windows:**

```powershell
py -m venv .venv
```

### 4. Activate the virtual environment

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**

```cmd
.venv\Scripts\activate.bat
```

### 5. Install Pygame

```bash
python -m pip install --upgrade pip
python -m pip install pygame
```

### 6. Run the application

```bash
python main.py
```

A Pygame window should open displaying the traffic intersection and the running simulation.

To close the application, close the simulation window.

## Simulation Configuration

The simulation uses configurable constants defined near the beginning of `main.py`.

| Configuration | Default value | Description |
|---|---:|---|
| Screen width | 1200 pixels | Simulation window width |
| Screen height | 600 pixels | Simulation window height |
| Lane height | 50 pixels | Horizontal lane height |
| Car length | 40 pixels | Vehicle length |
| Car width | 20 pixels | Vehicle width |
| Vertical lane width | 60 pixels | Vertical road width |
| Vehicle spawn interval | 2 seconds | Minimum interval between vehicle-generation checks |
| Traffic light interval | 10 seconds | Traffic-light switching interval |

Vehicle speeds are randomly selected between 80 and 120 km/h and converted to pixels per second for movement calculations.

## How the Simulation Works

### 1. Vehicle generation

The application checks the vehicle-generation interval and randomly selects a vehicle approach:

- 40% probability: vehicle enters from the left.
- 40% probability: vehicle enters from the right.
- 10% probability: vehicle enters from the top.
- 10% probability: vehicle enters from the bottom.

### 2. Vehicle movement

Each vehicle receives a direction, starting position, and randomized speed.

Vehicle movement is updated continuously using the elapsed frame time, allowing movement to be adjusted according to the simulation's frame rate.

### 3. Traffic lights

Traffic signals are represented by red and green circles. A timer is displayed beside each signal.

The current implementation includes traffic-light state synchronization for the horizontal approaches and separate vertical traffic-light objects.

### 4. Vehicle stopping behavior

Vehicles check their surroundings before moving.

A vehicle can stop when:

- An applicable traffic light is red.
- Another vehicle is too close ahead in the same lane.

This provides a basic representation of traffic queues and traffic-light-controlled movement.

### 5. Simulation statistics

The simulation displays:

- Number of vehicles currently in the simulation.
- Average recorded vehicle waiting time.

## Troubleshooting

### Pygame is not installed

If you receive:

```text
ModuleNotFoundError: No module named 'pygame'
```

Install Pygame:

```bash
python -m pip install pygame
```

### Python command is not recognized

Try:

```bash
python3 main.py
```

On Windows, try:

```powershell
py main.py
```

### Pygame window does not open

Check that:

- Python is installed correctly.
- Pygame is installed in the active virtual environment.
- You are running the command from the project directory.
- Your operating system supports opening a graphical Pygame window.

## Current Implementation Scope

This repository contains a basic graphical traffic simulation. It demonstrates vehicle generation, directional movement, traffic-light visualization, basic stopping conditions, and intersection rendering.

It should not be considered a validated real-world traffic-control system. The current implementation does not include advanced traffic optimization, sensor integration, real traffic data, collision physics, or a validated adaptive signal-control algorithm.

The displayed average waiting-time statistic is not yet calculated from accumulated vehicle waiting durations in the current implementation.

## Author

**Aakash Sah**

- GitHub: [Aakashsah247](https://github.com/Aakashsah247)

## License

No license is currently specified in the supplied project source. Add a `LICENSE` file if you intend to distribute the project under a particular open-source license.
