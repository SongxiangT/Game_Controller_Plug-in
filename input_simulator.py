# input_simulator.py
from pynput.keyboard import Controller, Key
from pynput.mouse import Button, Controller as MouseController
import logging

class InputSimulator:
    """
    Simulates keyboard and mouse inputs based on detected commands.
    """

    def __init__(self):
        self.keyboard = Controller()
        self.mouse = MouseController()
        self.keys_pressed = {}
        self.key_map = {
            'Move Forward': 'w',
            'Move Left': 'a',
            'Move Right': 'd',
            'Move Backward': 's',
            'Jump': 'space'
        }
        self.attack_key = 'left_click'  # Default attack action

    def update_key_mappings(self, key_mappings):
        """
        Updates the key mappings based on user input.

        :param key_mappings: Dictionary containing action-key mappings.
        """
        for action in self.key_map.keys():
            if action in key_mappings:
                self.key_map[action] = key_mappings[action].lower()

        if 'Attack' in key_mappings:
            self.attack_key = key_mappings['Attack'].lower()

    def handle_movement(self, commands):
        """
        Handles movement commands by pressing or releasing keys.

        :param commands: Dictionary of detected movement commands.
        """
        actions = ['Move Forward', 'Move Left', 'Move Right', 'Move Backward']
        applied_actions = []

        for action in actions:
            key = self.key_map.get(action, None)
            if key:
                if commands.get(action.lower().replace(' ', '_'), False):
                    self.press_key(key)
                    applied_actions.append(action)
                else:
                    self.release_key(key)

        # Handle Jump
        if commands.get('jump', False):
            self.press_jump()
            applied_actions.append('Jump')

        # Handle Attack
        if commands.get('attack', False):
            self.click_left()
            applied_actions.append('Attack')

        # Handle Mouse Movements
        mouse_actions = []
        if commands.get('mouse_move_up', False):
            mouse_actions.append('Mouse Move Up')
        if commands.get('mouse_move_down', False):
            mouse_actions.append('Mouse Move Down')
        if commands.get('mouse_move_left', False):
            mouse_actions.append('Mouse Move Left')
        if commands.get('mouse_move_right', False):
            mouse_actions.append('Mouse Move Right')

        for action in mouse_actions:
            if action == 'Mouse Move Up':
                self.move_mouse(0, -15)  # Negative y for up
            elif action == 'Mouse Move Down':
                self.move_mouse(0, 15)   # Positive y for down
            elif action == 'Mouse Move Left':
                self.move_mouse(-15, 0)  # Negative x for left
            elif action == 'Mouse Move Right':
                self.move_mouse(15, 0)   # Positive x for right
            applied_actions.append(action)

        # Log only applied actions
        if applied_actions:
            logging.info("; ".join(applied_actions))

    def press_key(self, key):
        """
        Presses a keyboard key if not already pressed.

        :param key: Key to press (e.g., 'w', 'a', 's', 'd').
        """
        try:
            if not self.keys_pressed.get(key, False):
                if key == 'space':
                    self.keyboard.press(Key.space)
                else:
                    self.keyboard.press(key)
                self.keys_pressed[key] = True
        except Exception as e:
            logging.error(f"Error pressing key '{key}': {e}")

    def release_key(self, key):
        """
        Releases a keyboard key if it was pressed.

        :param key: Key to release (e.g., 'w', 'a', 's', 'd').
        """
        try:
            if self.keys_pressed.get(key, False):
                if key == 'space':
                    self.keyboard.release(Key.space)
                else:
                    self.keyboard.release(key)
                self.keys_pressed[key] = False
        except Exception as e:
            logging.error(f"Error releasing key '{key}': {e}")

    def press_jump(self):
        """
        Simulates a spacebar press for jumping.
        """
        try:
            self.press_key('space')
            self.release_key('space')
        except Exception as e:
            logging.error(f"Error during jump action: {e}")

    def click_left(self):
        """
        Simulates a left mouse click for attacking.
        """
        try:
            if self.attack_key == 'left_click':
                self.mouse.click(Button.left, 1)
        except Exception as e:
            logging.error(f"Error during left click: {e}")

    def move_mouse(self, dx, dy):
        """
        Moves the mouse cursor based on head movement for camera rotation.

        :param dx: Horizontal movement amount.
        :param dy: Vertical movement amount.
        """
        try:
            if dx != 0 or dy != 0:
                self.mouse.move(int(dx), int(dy))
        except Exception as e:
            logging.error(f"Error moving mouse: {e}")

    def release_all_keys(self):
        """
        Releases all currently pressed keys.
        """
        try:
            for key in list(self.keys_pressed.keys()):
                self.release_key(key)
        except Exception as e:
            logging.error(f"Error releasing all keys: {e}")
