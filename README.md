# Metalworking: The Game

This is the realistic 2D simulator of mechanical cutting process. Simulates cutting tool itself, eccentricity axis and cut path.

![v0_1](https://user-images.githubusercontent.com/36193247/230894403-85afeedb-1923-4da7-817b-bbe13739738b.png)

# How to play it

- Download and install the latest Python 3.x from https://www.python.org/downloads/
    - During installation process install Python downloading tool that called `pip`. Or manually install it later by using this commad:
        - in Windows:
            `py get-pip.py`
        - in Linux:
            `python get-pip.py`
        - in MacOS:
            `python get-pip.py`
    - Get some modules by using `pip`, required by this app:
        `pip install pygame`
- Once you have installed Python and `pip`, launch the file named `main.py` in app directory.
- The goal is simple: cut as many steel as you can. If the cutting tool hits far beyond the screen, the stage will be restarted.
- Use these control keys to change conditions:
    - `ESC` - quit game;
    - `ENTER` - reset game stage;
    - `CTRL` - stop/unstop rotation;
    - `ALT` - reverse rotation direction;
    - `SPACE` - stop/unstop movement;
    - `ARROW LEFT`, `ARROW RIGHT`, `ARROW UP`, `ARROW DOWN` - change direction of tool movement, even if the movement is stopped;
    - `/` - decrease movement speed;
    - `*` - increase movement speed;
    - `-` - decrease rotation speed;
    - `+` - increase rotation speed.
- Change constants in the file `constants.py`, e.g. game FPS, window resolution, and so on.
