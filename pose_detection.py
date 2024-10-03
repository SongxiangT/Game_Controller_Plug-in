# pose_detection.py
import cv2
import mediapipe as mp

class PoseDetector:
    """
    Detects human poses using Mediapipe.
    """

    def __init__(self, static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            enable_segmentation=enable_segmentation,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_pose(self, frame):
        """
        Detects pose landmarks in the given frame.

        :param frame: BGR image frame from OpenCV.
        :return: Mediapipe Pose object with landmarks.
        """
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        return results

    def draw_landmarks(self, frame, landmarks):
        """
        Draws pose landmarks on the given frame.

        :param frame: BGR image frame from OpenCV.
        :param landmarks: Pose landmarks detected by Mediapipe.
        """
        self.mp_drawing.draw_landmarks(
            frame,
            landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2),
            self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )
