# control_logic.py
import logging

class ControlLogic:
    """
    Analyzes pose landmarks to determine game commands based on player's gestures.
    """
    HEAD_MOVEMENT_THRESHOLD_X = 0.02  # Threshold for horizontal head movement
    HEAD_MOVEMENT_THRESHOLD_Y = 0.02  # Threshold for vertical head movement
    HEAD_MOVEMENT_SENSITIVITY_X = 10  # Sensitivity factor for horizontal mouse movement
    HEAD_MOVEMENT_SENSITIVITY_Y = 10  # Sensitivity factor for vertical mouse movement
    JUMP_THRESHOLD = 0.05  # Threshold to detect a sudden jump

    def __init__(self):
        # Initialize previous head positions
        self.prev_head_position_x = None
        self.prev_head_position_y = None
        self.prev_average_y = None
        self.jump_detected = False

    def analyze_pose(self, landmarks):
        """
        Analyzes pose landmarks to extract movement commands.

        :param landmarks: List of landmark objects from Mediapipe.
        :return: Dictionary of commands.
        """
        commands = {
            'jump': False,
            'go_forward': False,
            'go_backward': False,
            'move_left': False,
            'move_right': False,
            'attack': False,
            'head_movement_x': 0,
            'head_movement_y': 0,
            'mouse_move_up': False,
            'mouse_move_down': False,
            'mouse_move_left': False,
            'mouse_move_right': False
        }

        # Extract relevant landmarks
        nose = landmarks[0]           # Nose landmark
        left_wrist = landmarks[15]    # Left wrist
        right_wrist = landmarks[16]   # Right wrist
        left_elbow = landmarks[13]    # Left elbow
        right_elbow = landmarks[14]   # Right elbow
        left_shoulder = landmarks[11] # Left shoulder
        right_shoulder = landmarks[12]# Right shoulder

        # Calculate average y position to detect jump
        average_y = sum([lm.y for lm in landmarks]) / len(landmarks)

        if self.prev_average_y is not None:
            delta_y = average_y - self.prev_average_y
            if delta_y < -self.JUMP_THRESHOLD:
                # Significant upward movement detected
                commands['jump'] = True
                self.jump_detected = True
                logging.debug("Jump detected.")
        self.prev_average_y = average_y

        # Head Movement Detection for Mouse Rotation
        current_head_position_x = nose.x  # Using nose's x position as reference
        current_head_position_y = nose.y  # Using nose's y position as reference
        head_movement_x = 0
        head_movement_y = 0

        if self.prev_head_position_x is not None and self.prev_head_position_y is not None and not self.jump_detected:
            # Calculate movement differences
            delta_x = current_head_position_x - self.prev_head_position_x
            delta_y = current_head_position_y - self.prev_head_position_y

            # Horizontal Movement (Left and Right)
            if abs(delta_x) > self.HEAD_MOVEMENT_THRESHOLD_X:
                head_movement_x = delta_x * self.HEAD_MOVEMENT_SENSITIVITY_X
                if delta_x > 0:
                    commands['mouse_move_right'] = True
                else:
                    commands['mouse_move_left'] = True

            # Vertical Movement (Up and Down)
            if abs(delta_y) > self.HEAD_MOVEMENT_THRESHOLD_Y:
                head_movement_y = delta_y * self.HEAD_MOVEMENT_SENSITIVITY_Y
                if delta_y > 0:
                    commands['mouse_move_down'] = True
                else:
                    commands['mouse_move_up'] = True

        # Update previous head positions
        self.prev_head_position_x = current_head_position_x
        self.prev_head_position_y = current_head_position_y

        # Assign head movements to commands
        commands['head_movement_x'] = head_movement_x
        commands['head_movement_y'] = head_movement_y

        # Define functions to determine hand states
        def is_hand_raised(wrist, elbow, shoulder):
            """
            Determines if a hand is raised based on wrist, elbow, and shoulder positions.

            :param wrist: Wrist landmark.
            :param elbow: Elbow landmark.
            :param shoulder: Shoulder landmark.
            :return: True if hand is raised, False otherwise.
            """
            return wrist.y < elbow.y < shoulder.y

        def is_hand_lowered(wrist, elbow, shoulder):
            """
            Determines if a hand is lowered based on wrist, elbow, and shoulder positions.

            :param wrist: Wrist landmark.
            :param elbow: Elbow landmark.
            :param shoulder: Shoulder landmark.
            :return: True if hand is lowered, False otherwise.
            """
            return wrist.y > elbow.y > shoulder.y

        # Gesture Controls

        # Jump: Player jumps (already detected above)
        # No additional action needed here

        # Go Forward: Both hands raised vertically
        if is_hand_raised(left_wrist, left_elbow, left_shoulder) and is_hand_raised(right_wrist, right_elbow, right_shoulder):
            commands['go_forward'] = True

        # Go Backward: Both hands lowered and all landmarks detected
        if is_hand_lowered(left_wrist, left_elbow, left_shoulder) and is_hand_lowered(right_wrist, right_elbow, right_shoulder):
            # Ensure all landmarks are detected
            if all([nose, left_wrist, right_wrist, left_elbow, right_elbow, left_shoulder, right_shoulder]):
                commands['go_backward'] = True

        # Move Left: Only left hand raised
        if is_hand_raised(left_wrist, left_elbow, left_shoulder) and not is_hand_raised(right_wrist, right_elbow, right_shoulder):
            commands['move_right'] = True

        # Move Right: Only right hand raised
        if is_hand_raised(right_wrist, right_elbow, right_shoulder) and not is_hand_raised(left_wrist, left_elbow, left_shoulder):
            commands['move_left'] = True

        # Attack: Both hands raised parallel to each other forward
        if (abs(left_wrist.y - right_wrist.y) < 0.5 and
            abs(left_elbow.y - right_elbow.y) < 0.5 and
            abs(left_shoulder.y - right_shoulder.y) < 0.5 and
            is_hand_raised(left_wrist, left_elbow, left_shoulder) and
            is_hand_raised(right_wrist, right_elbow, right_shoulder)):
            commands['attack'] = True

        return commands
