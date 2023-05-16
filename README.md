# Metalworking Simulator

This is the realistic 2D simulator of mechanical cutting process. It provides life-close demonstration of cutting tool itself, its runout, cut path and trajectory of the center of tool. User can affect the process by pressing control keys.

![v0_1](https://user-images.githubusercontent.com/36193247/230894403-85afeedb-1923-4da7-817b-bbe13739738b.png)

# Control Keys

- `ESC` - quit game.
- `ENTER` - reset game stage.
- `CTRL` - stop/unstop rotation.
- `ALT` - reverse rotation direction.
- `SPACE` - stop/unstop movement.
- `ARROW LEFT`, `ARROW RIGHT`, `ARROW UP`, `ARROW DOWN` - change direction of the tool movement, even if the movement is stopped.
- `/` - decrease movement speed.
- `*` - increase movement speed.
- `-` - decrease rotation speed.
- `+` - increase rotation speed.

# How to play it

- Download and install the latest Python 3.x from https://www.python.org/downloads/
    - During installation process install Python downloading tool that called `pip`. Or manually install it later by using this commad:
        - in Windows:
            `py get-pip.py`
        - in Linux:
            `python get-pip.py`
        - in MacOS:
            `python get-pip.py`
    - Get some modules by using `pip`, required by this application:
        `pip install pygame`
- Once you have installed Python and `pip`, launch the file named `__main__.py` inside the `main` directory.
- The goal is simple: cut as many steel as you can. If the cutting tool hits far beyond the screen, the stage will be restarted.
- Use control keys to change work conditions.
- Change constants in the file `constants.py`, e.g. game FPS, window resolution, and so on.
