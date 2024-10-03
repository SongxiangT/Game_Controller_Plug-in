# Game Control Plug-in

## Overview

This plug-in allows you to control your game using body poses detected via your webcam. It translates specific poses into in-game commands such as moving forward, left, right, backward, jumping, and firing.

## Features

- **Real-time Pose Detection**: Uses Mediapipe and OpenCV to detect full-body poses.
- **Keyboard and Mouse Input Simulation**: Sends keyboard and mouse inputs based on detected poses using `pynput`.
- **Game Monitoring**: Automatically activates controls when the game is running.
- **Gesture-Based Actions**: Includes a "waving fist" gesture to perform a left-click action (fire).
- **Seamless Integration**: Runs alongside the game without interrupting its execution.

## Project Structure
```text
game_control_plugin/
│
├── main.py
├── game_launcher.py
├── pose_detection.py
├── control_logic.py
├── input_simulator.py
├── game_monitor.py
├── requirements.txt
└── README.md
```

### Module Descriptions

1. **`main.py`**: The entry point of the application that coordinates all other modules.
2. **`game_launcher.py`**: Handles launching the game and managing window focus.
3. **`pose_detection.py`**: Manages webcam access and pose detection.
4. **`control_logic.py`**: Translates detected poses into game commands.
5. **`input_simulator.py`**: Simulates keyboard and mouse inputs based on the control logic.
6. **`game_monitor.py`**: Monitors the game's running state and manages the activation of the control system.
7. **`requirements.txt`**: Lists all Python dependencies.
8. **`README.md`**: Provides project documentation and setup instructions.

## Setup Instructions

### Prerequisites

- **Python 3.7+**: Ensure Python is installed on your system. Download from [python.org](https://www.python.org/downloads/).
- **Webcam**: Required for pose detection.
- **Git**: To clone the repository (optional).

### Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/yourusername/game_control_plugin.git
    cd game_control_plugin
    ```

    *Replace `yourusername` with your actual GitHub username.*

2. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure Game Path and Window Title**:

    - Open `main.py` in a text editor.
    - Set the `game_path` variable to the full path of your game executable. Example:

        ```python
        game_path = r"C:\Games\Tomb Raider\tomb3.exe"
        ```

    - Set the `window_title` variable to the exact title of the game window (as it appears in the taskbar or window). You can use tools like [Window Spy](https://www.autohotkey.com/docs/Scripts/WindowSpy.htm) to find the exact title.

        ```python
        window_title = "Tomb Raider"  # Replace with your game's exact window title
        ```

4. **Run the Plug-in**:

    ```bash
    python main.py
    ```

    The plug-in will launch the game and start monitoring for pose-based controls.

### Packaging as an Executable (Optional)

To create a standalone executable using PyInstaller:

1. **Install PyInstaller**:

    ```bash
    pip install pyinstaller
    ```

2. **Create the Executable**:

    ```bash
    pyinstaller --onefile main.py
    ```

    The executable will be located in the `dist/` directory.

## Usage

- **Launching**: Run `main.py` or the packaged executable.
- **Controls**:
    - **Move Forward**: Raise both wrists above shoulder level.
    - **Move Left**: Raise your left wrist above shoulder level while keeping the right wrist at shoulder level.
    - **Move Right**: Raise your right wrist above shoulder level while keeping the left wrist at shoulder level.
    - **Move Backward**: Lower both wrists below shoulder level.
    - **Jump**: Simultaneously raise both wrists and shoulders slightly above their previous positions.
    - **Fire (Left Click)**: Perform a "waving fist" gesture by moving your right fist left and right rapidly.
- **Exiting**: Press the `ESC` key in the video feed window to exit the plug-in.

## Important Considerations

- **Window Title Accuracy**: Ensure that the `window_title` in `main.py` matches the game window exactly.
- **Performance**: Running the plug-in alongside the game may impact performance. Ensure your system meets the requirements.
- **Game Compatibility**: Ensure the game accepts simulated keyboard and mouse inputs and does not have anti-cheat mechanisms that might flag this behavior.
- **Security**: Use responsibly and ensure compliance with the game's terms of service.

## Troubleshooting

- **Game Window Not Found**: Verify the `window_title` matches exactly. Use tools like [Window Spy](https://www.autohotkey.com/docs/Scripts/WindowSpy.htm) to find the exact title.
- **Webcam Issues**: Ensure your webcam is properly connected and not being used by another application.
- **Dependencies Errors**: Ensure all dependencies are installed correctly using `pip install -r requirements.txt`.
- **Gesture Detection Issues**: If gestures are not being detected reliably, adjust the thresholds in `control_logic.py` and ensure proper lighting and camera positioning.

## Enhancements and Best Practices

1. **Configuration File**:  
   Use a configuration file (e.g., `config.json`) to store settings like game path, window title, and control thresholds. This makes it easier to adjust settings without modifying the code.

2. **GUI Interface**:  
   Develop a simple graphical user interface to manage settings, start/stop the plug-in, and display status messages.

3. **Logging**:  
   Implement logging to keep track of the plug-in's actions, errors, and performance metrics. Python's `logging` module can be useful for this.

4. **Advanced Control Logic**:  
   Expand the control logic to recognize more complex poses or gestures for additional in-game actions. Implement smoothing algorithms to reduce jitter in pose detection and improve control accuracy.

5. **Security and Compliance**:  
   Ensure that the plug-in does not violate the game's terms of service. Be cautious with input simulation, as some games have anti-cheat systems that might flag automated inputs.

6. **Performance Optimization**:  
   Optimize the pose detection loop for better performance, potentially using threading or multiprocessing to handle heavy computations.

## License

MIT License

## Acknowledgements

- [Mediapipe](https://mediapipe.dev/)
- [OpenCV](https://opencv.org/)
- [Pynput](https://pypi.org/project/pynput/)
- [psutil](https://psutil.readthedocs.io/)
- [pywin32](https://github.com/mhammond/pywin32)

---
