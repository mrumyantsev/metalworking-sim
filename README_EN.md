# Milling Simulator

**Milling Simulator** is a graphical desktop application that simulates the metalworking process through a milling operation.

The simulation shows the basic mechanics of the process: a rotating cutting tool (mill), the center of which is located at a certain distance relative to its center of rotation (runout), passes through the material being processed (relatively metal). The actual center of the tool discards the path.

![Milling](./millsim.png "Milling process")\
*Milling process displayed on screen*

## Controls

Press keys on the keyboard to control the processing.

* Stop/resume feeding - *Space* key.
* Stop/resume rotation - *Ctrl* key.
* Expand the direction of rotation - *Alt* key.
* Change the direction of movement of the tool - keys *left*, *right*, *up*, *down*.
* Reduce feed speed - */* key.
* Increase feed speed - *\** key.
* Reduce rotation speed - key *-*.
* Increase rotation speed - *+* key.
* Restarting the material and the initial position of the tool - *Enter* key.
* Exit the program - *Esc* key.

## Configuration

Open and edit the configuration file to change tool runout, number of teeth, cutting conditions, and other settings.

```
vim ./configs/config.yml
```

## System requirements

**Operating system:**

- Windows / macOS / Linux/UNIX.

**Software:**

- Python programming language >=3.6.
- pip package manager for Python.
- make utility.

## Installation and launch

Download and install the packages required for this application.

```
pip install pyyaml pygame
```

Launch the program.

```
make fast-run
```

Launch the program (short command).

```
make
```
