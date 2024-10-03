# 🎮 Game Control Plug-in 🕹️

██████╗ █████╗ ██████╗ ███████╗███████╗███████╗██████╗  
> **Disclaimer:** Use this tool responsibly. Ensure you have the rights to modify and control the games you use it with. ⚠️


Welcome to the **Game Control Plug-in** repository! This innovative tool allows you to control your favorite games using intuitive body gestures and head movements. Say goodbye to traditional controllers and embrace a more immersive gaming experience! 🤖💪

## 🛠️ Features

- **Gesture-Based Controls:** Move, jump, and attack using simple hand gestures.
- **Head Movement for Camera Control:** Rotate your in-game camera by moving your head in different directions.
- **Customizable Key Mappings:** Easily map gestures and head movements to your preferred in-game actions.
- **Real-Time Feedback:** Visualize your pose and gestures through the webcam feed.
- **User-Friendly UI:** Intuitive interface for setting up and configuring controls.
- **Lightweight & Efficient:** Minimal lag for a seamless gaming experience.

## 📸 Demo
### Overview
<img width="444" alt="71868e40906146173b07aefcad66074" src="https://github.com/user-attachments/assets/14ed8d4b-b9c8-4860-a1ca-736e588d6948"> <br>

<img width="816" alt="b35dcad2db8601539390f32ea1b60d1" src="https://github.com/user-attachments/assets/83ddc60c-2e07-4303-9e12-7520ab862c47"> <br>

<br>
![Demo Video]!
<br>
*Check out our [YouTube Demo](https://www.youtube.com/) to see the Game Control Plug-in in action!*

## 📥 Installation

### 🖥️ Prerequisites

- **Operating System:** Windows 10 or later
- **Python:** Version 3.7 or higher
- **Webcam:** Required for pose detection

### 🔧 Setup Steps

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/game-control-plugin.git
   cd game-control-plugin
   ```
2. **Create a Virtual Environment:**
```bash
   python -m venv venv
```

3. Activate the Virtual Environment:
   ```bash
   venv\Scripts\activate
   ```

4. Install Dependencies:

```bash
pip install -r requirements.txt
```


5. Run the Application:
```bash
   python main.py
```
## 🎮 How to Use
1. Launch the Application:

After running ```main.py```, a GUI window will appear.

2, Configure Game Executable:

Click the "Browse" button to select your game's executable file (e.g., ```Unturned.exe```).
3. Map Controls:

For each action (Move Forward, Move Left, Move Right, Move Backward, Jump, Attack), click the "Capture" button and press the desired key or mouse button you want to assign.

4. Launch the Game:

Once all mappings are set, click the "Launch Game" button. The application will start the game and begin monitoring your gestures.
5. Control In-Game Actions:

Jump: Perform a sudden upward movement.
Go Forward: Raise both hands vertically.
Go Backward: Lower both hands.
Move Left: Raise only the left hand.
Move Right: Raise only the right hand.
Attack: Raise both hands parallel to each other forward.
Head Movements: Move your head up, down, left, and right to control the in-game camera (disabled during a jump).
6. Exit Control Loop:

Press ESC in the OpenCV window to exit the control loop and deactivate controls.


## 🧩 Configuration
Key Mappings: All key and mouse button mappings are saved in config.json. You can edit this file directly or use the GUI to reconfigure controls.

## 📝 Contributing
We welcome contributions! 🎉 Whether it's reporting bugs, suggesting features, or submitting pull requests, your help is appreciated.

## 🤝 Support
Need help? Reach out to us!

Email: songxiangtang@gmail.com

## 👥 Authors
🎓 Songxiang Tang <br>
Master of Information Systems, University of Melbourne<br>
📧 songxiangt@student.unimelb.edu.au<br>
🎓 Xin Shen<br>
Master of Information Technology, University of Melbourne<br>
📧 xsshen2@student.unimelb.edu.au<br>
🎓 Chun-Hao Chen<br>
Master of Information Systems, University of Melbourne<br>
📧 chunhaoc1@student.unimelb.edu.au<br>

## 🛡️ Security

Ensure that you trust the sources of your dependencies and understand the permissions the application requires. Always run applications like this with caution.

## 💡 Tips & Tricks

- **Optimal Lighting:** For better pose detection, use your application in a well-lit environment.
- **Stable Camera Position:** Mount your webcam at eye level for accurate head movement detection.
- **Calibrate Gestures:** Spend some time adjusting the thresholds and sensitivities in the code (`control_logic.py`) to fit your personal gestures and movements.

## 🐍 Python Dependencies

- **OpenCV:** For video capture and display.
- **Mediapipe:** For pose detection.
- **Pynput:** For simulating keyboard and mouse inputs.
- **psutil:** For monitoring game processes.
- **pywin32:** For window management on Windows.

All dependencies are listed in `requirements.txt`. Install them using `pip install -r requirements.txt`.

## 📢 Stay Connected

Follow us for updates and more exciting projects!

- **GitHub:** [Songxiang Tang](https://github.com/SongxiangT)
- **LinkedIn:** [Songxiang Tang]([https://www.linkedin.com/in/yourprofile](https://www.linkedin.com/in/songxiang-tang-34b752290/))

---

Happy Gaming! 🎉🕹️
