# main.py
import threading
import time
import cv2
import logging
import tkinter as tk
from tkinter import filedialog, messagebox
from game_launcher import open_game
from game_monitor import is_game_running, get_window_handle
from pose_detection import PoseDetector
from control_logic import ControlLogic
from input_simulator import InputSimulator
import win32gui

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO to log only applied actions
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("game_control.log"),
        logging.StreamHandler()
    ]
)

class GameControlUI:
    def __init__(self, master):
        self.master = master
        master.title("Game Control Plug-in")

        # Initialize variables
        self.game_path = tk.StringVar()
        self.key_map = {
            'Move Forward': tk.StringVar(value='w'),
            'Move Left': tk.StringVar(value='a'),
            'Move Right': tk.StringVar(value='d'),
            'Move Backward': tk.StringVar(value='s'),
            'Jump': tk.StringVar(value='space'),
            'Attack': tk.StringVar(value='left_click')  # Special handling for mouse clicks
        }

        # Variable to track which action is being configured
        self.current_mapping_action = None

        # Create UI components
        self.create_widgets()

        # Control loop thread
        self.control_thread = None
        self.control_active = False

    def create_widgets(self):
        # Game Path Selection
        path_frame = tk.Frame(self.master)
        path_frame.pack(padx=10, pady=5, fill='x')

        path_label = tk.Label(path_frame, text="Game Executable Path:")
        path_label.pack(side='left')

        path_entry = tk.Entry(path_frame, textvariable=self.game_path, width=50)
        path_entry.pack(side='left', padx=5)

        browse_button = tk.Button(path_frame, text="Browse", command=self.browse_game_path)
        browse_button.pack(side='left')

        # Key Mappings
        mapping_frame = tk.Frame(self.master)
        mapping_frame.pack(padx=10, pady=5, fill='x')

        tk.Label(mapping_frame, text="Key Mappings:", font=('Arial', 12, 'bold')).pack(anchor='w')

        self.mapping_buttons = {}
        for action, var in self.key_map.items():
            row = tk.Frame(mapping_frame)
            row.pack(fill='x', pady=2)

            label = tk.Label(row, text=action, width=20, anchor='w')
            label.pack(side='left')

            # Display the current key/mouse binding
            binding_display = tk.Label(row, textvariable=var, relief='sunken', width=20, anchor='w')
            binding_display.pack(side='left', padx=5)

            # Button to capture new key/mouse binding
            capture_button = tk.Button(row, text="Capture", command=lambda a=action: self.capture_binding(a))
            capture_button.pack(side='left', padx=5)

            self.mapping_buttons[action] = {
                'display': binding_display,
                'button': capture_button
            }

        # Launch Button
        launch_button = tk.Button(self.master, text="Launch Game", command=self.launch_game)
        launch_button.pack(pady=10)

        # Status Display
        self.status_label = tk.Label(self.master, text="Status: Idle", fg='blue')
        self.status_label.pack(pady=5)

    def browse_game_path(self):
        filepath = filedialog.askopenfilename(
            title="Select Game Executable",
            filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")]
        )
        if filepath:
            self.game_path.set(filepath)

    def capture_binding(self, action):
        """
        Initiates the binding capture process for a specific action.
        """
        self.current_mapping_action = action
        self.update_status(f"Press the desired key or mouse button for '{action}'...")
        logging.info(f"Awaiting input for action: {action}")
        # Bind the key and mouse events
        self.master.bind("<Key>", self.on_key_press)
        self.master.bind("<Button>", self.on_mouse_click)

    def on_key_press(self, event):
        """
        Captures the key press and updates the corresponding action binding.
        """
        if self.current_mapping_action:
            key = event.keysym.lower()
            self.key_map[self.current_mapping_action].set(key)
            self.update_status(f"Mapped '{self.current_mapping_action}' to key: {key}")
            logging.info(f"Action '{self.current_mapping_action}' mapped to key: {key}")
            self.current_mapping_action = None
            # Unbind the events after capturing
            self.master.unbind("<Key>")
            self.master.unbind("<Button>")

    def on_mouse_click(self, event):
        """
        Captures the mouse click and updates the corresponding action binding.
        """
        if self.current_mapping_action:
            # Map mouse buttons to strings
            mouse_buttons = {
                1: 'left_click',
                2: 'middle_click',
                3: 'right_click'
            }
            button = mouse_buttons.get(event.num, f"button{event.num}")
            self.key_map[self.current_mapping_action].set(button)
            self.update_status(f"Mapped '{self.current_mapping_action}' to mouse button: {button}")
            logging.info(f"Action '{self.current_mapping_action}' mapped to mouse button: {button}")
            self.current_mapping_action = None
            # Unbind the events after capturing
            self.master.unbind("<Key>")
            self.master.unbind("<Button>")

    def launch_game(self):
        # Validate inputs
        if not self.game_path.get():
            messagebox.showerror("Input Error", "Please select the game executable path.")
            return

        # Extract key mappings
        key_mappings = {}
        for action, var in self.key_map.items():
            key = var.get().strip()
            if not key:
                messagebox.showerror("Input Error", f"Please map a key for '{action}'.")
                return
            key_mappings[action] = key

        # Confirm Launch
        confirm = messagebox.askyesno("Launch Game", "Are you sure you want to launch the game with the current settings?")
        if not confirm:
            return

        # Disable UI elements to prevent re-entry
        self.disable_ui()

        # Update status
        self.update_status("Launching game...")

        # Start the game launcher in a separate thread
        launcher_thread = threading.Thread(target=self.start_game, args=(self.game_path.get(), key_mappings), daemon=True)
        launcher_thread.start()

    def start_game(self, game_path, key_mappings):
        window_title_keyword = r"Unturned.*"  # Update based on actual window title
        game_name = "Unturned.exe"  # Update based on actual process name

        logging.info(f"Starting game launcher for {game_path} with window pattern '{window_title_keyword}'")

        try:
            open_game(game_path, window_title_keyword, game_name, max_wait=60)
            logging.info("Game launcher executed successfully.")
        except Exception as e:
            logging.error(f"Exception while launching game: {e}")
            self.update_status("Error launching game.")
            self.enable_ui()
            return

        # Bring the game window to the foreground
        window_handle = get_window_handle(window_title_keyword)
        if window_handle:
            try:
                win32gui.SetForegroundWindow(window_handle)
                logging.info("Game window brought to the foreground.")
            except Exception as e:
                logging.warning(f"Failed to bring game window to foreground: {e}")
        else:
            logging.warning("Game window handle not found despite process running.")

        # Activate controls
        logging.info("Game is running. Activating controls.")
        self.update_status("Game is running. Activating controls.")
        self.control_active = True

        # Start the control loop
        self.control_thread = threading.Thread(target=self.control_loop, args=(game_name, window_title_keyword, key_mappings), daemon=True)
        self.control_thread.start()

    def control_loop(self, game_name, window_title_keyword, key_mappings):
        pose_detector = PoseDetector()
        control_logic = ControlLogic()
        input_sim = InputSimulator()

        # Update InputSimulator with key mappings
        input_sim.update_key_mappings(key_mappings)

        logging.info("Control loop started.")
        self.update_status("Control loop started.")

        try:
            cap = cv2.VideoCapture(0)  # Open the webcam
            if not cap.isOpened():
                logging.error("Cannot open webcam.")
                self.update_status("Cannot open webcam.")
                self.control_active = False
                self.enable_ui()
                return

            while self.control_active:
                if is_game_running(game_name, window_title_keyword):
                    success, frame = cap.read()
                    if not success:
                        logging.warning("Failed to read frame from webcam.")
                        continue

                    # Flip the image to create a mirror effect
                    frame = cv2.flip(frame, 1)

                    # Detect pose
                    results = pose_detector.detect_pose(frame)

                    if results.pose_landmarks and results.pose_landmarks.landmark:
                        # Draw pose landmarks on the video frame
                        pose_detector.draw_landmarks(frame, results.pose_landmarks)

                        # Analyze pose to get commands
                        commands = control_logic.analyze_pose(results.pose_landmarks.landmark)

                        # Execute movement commands
                        input_sim.handle_movement(commands)

                        # If jump is detected, disable mouse movement by not processing mouse commands
                        if commands.get('jump', False):
                            logging.info("Jump;")
                        else:
                            # Execute head movement for camera rotation only if not jumping
                            mouse_movement_x = commands.get('head_movement_x', 0)
                            mouse_movement_y = commands.get('head_movement_y', 0)
                            if mouse_movement_x != 0 or mouse_movement_y != 0:
                                input_sim.move_mouse(mouse_movement_x, mouse_movement_y)

                    else:
                        logging.warning("No pose landmarks detected.")
                        input_sim.release_all_keys()
                        self.update_status("No pose detected.")
                        continue  # Skip to the next frame

                    # Show the video feed with pose landmarks
                    cv2.imshow('Full-Body Pose Detection', frame)

                    # Press ESC to exit
                    if cv2.waitKey(5) & 0xFF == 27:
                        logging.info("ESC pressed. Exiting control loop.")
                        self.control_active = False
                        break
                else:
                    # If the game is not running, release all keys and wait
                    input_sim.release_all_keys()
                    self.update_status("Game is not running.")
                    logging.info("Game is not running.")
                    time.sleep(2)

        except Exception as e:
            logging.error(f"Error in control loop: {e}")
            self.update_status(f"Error in control loop: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.update_status("Controls deactivated.")
            logging.info("Control loop terminated.")
            self.enable_ui()

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")
        # Only log info messages to keep the log clean
        if message.startswith("Mapped") or message.endswith("controls started.") or message == "Jump;" or message in ["Idle", "Controls deactivated.", "Error launching game.", "Error in control loop:"] :
            logging.info(message)

    def disable_ui(self):
        for child in self.master.winfo_children():
            if isinstance(child, (tk.Button, tk.Entry)):
                child.configure(state='disabled')
            elif isinstance(child, tk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, (tk.Button, tk.Entry)):
                        subchild.configure(state='disabled')

    def enable_ui(self):
        for child in self.master.winfo_children():
            if isinstance(child, (tk.Button, tk.Entry)):
                child.configure(state='normal')
            elif isinstance(child, tk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, (tk.Button, tk.Entry)):
                        subchild.configure(state='normal')
        self.update_status("Idle")

def main():
    root = tk.Tk()
    app = GameControlUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
