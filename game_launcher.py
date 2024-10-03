# game_launcher.py
import subprocess
import time
import logging
from game_monitor import is_game_running  # Importing the function

def open_game(game_path, window_title_keyword, game_name, max_wait=60):
    """
    Launch the game executable and wait until the game window appears.

    :param game_path: Path to the game executable.
    :param window_title_keyword: Regex pattern to identify the game window.
    :param game_name: The exact process name of the game executable.
    :param max_wait: Maximum time to wait for the game window to appear.
    """
    try:
        subprocess.Popen([game_path])
        logging.info(f"Game launched: {game_path}")
    except Exception as e:
        logging.error(f"Failed to launch game: {e}")
        raise e

    # Wait until the game is detected as running
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if is_game_running(game_name, window_title_keyword):  # Pass both arguments
            logging.info("Game window detected.")
            return
        time.sleep(1)

    logging.warning("Game window not detected within the wait period.")
    raise TimeoutError("Failed to detect game launch within the specified time.")
