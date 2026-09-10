import re
import webbrowser
import subprocess
import shutil

from backend.agent.system_tools import SystemTools
from backend.agent.file_tools import FileTools


class AgentCore:

    def __init__(self):

        self.system_tools = SystemTools()
        self.file_tools = FileTools()

        self.applications = {
            "chrome": "chrome",
            "google chrome": "chrome",

            "edge": "msedge",
            "microsoft edge": "msedge",

            "notepad": "notepad",
            "calculator": "calc",
            "calc": "calc",

            "explorer": "explorer",
            "file explorer": "explorer",

            "vscode": "code",
            "vs code": "code",
            "visual studio code": "code",
        }

    # ========================================================
    # MAIN ENTRY
    # ========================================================

    def process(self, message):

        message_lower = message.lower().strip()

    # ====================================================
    # FILE ACTIONS
    # ====================================================

        file_action = self.detect_file_action(
            message_lower
        )

        if file_action:

            return self.execute_file_action(
                file_action
            )

    # ====================================================
    # SYSTEM ACTIONS
    # ====================================================

        system_action = self.detect_system_action(
            message_lower
        )

        if system_action:

            return self.execute_system_action(
                system_action
            )

    # ====================================================
    # WEBSITE
    # ====================================================

        website = self.detect_website(
            message_lower
        )

        if website:

            return self.open_website(
                website
            )

    # ====================================================
    # APPLICATION
    # ====================================================

        application = self.detect_application(
            message_lower
        )

        if application:

            return self.open_application(
                application
            )

    # ====================================================
    # NORMAL AI QUERY
    # ====================================================

        return None

    # ========================================================
    # WEBSITE DETECTION
    # ========================================================

    def detect_website(self, message):

        website_patterns = [

            r"open\s+(?:the\s+)?youtube",
            r"go\s+to\s+(?:the\s+)?youtube",

            r"open\s+(?:the\s+)?google",
            r"go\s+to\s+(?:the\s+)?google",

            r"open\s+(?:the\s+)?github",
            r"go\s+to\s+(?:the\s+)?github",

            r"open\s+(?:the\s+)?instagram",
            r"go\s+to\s+(?:the\s+)?instagram",

            r"open\s+(?:the\s+)?chatgpt",
            r"go\s+to\s+(?:the\s+)?chatgpt",
        ]

        websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://github.com",
            "instagram": "https://www.instagram.com",
            "chatgpt": "https://chatgpt.com",
        }

        for pattern in website_patterns:

            match = re.search(
                pattern,
                message
            )

            if match:

                for name in websites:

                    if name in message:

                        return name

        return None

    # ========================================================
    # APPLICATION DETECTION
    # ========================================================

    def detect_application(self, message):

        task_words = [
            "open",
            "launch",
            "start",
            "run"
        ]

        if not any(
            word in message
            for word in task_words
        ):

            return None

        for name in self.applications:

            if name in message:

                return name

        return None

    # ========================================================
    # OPEN APPLICATION
    # ========================================================

    def open_application(self, application):

        executable = self.applications.get(
            application
        )

        if not executable:

            return (
                False,
                f"I don't know how to open {application}."
            )

        try:

            path = shutil.which(
                executable
            )

            if path:

                subprocess.Popen(
                    [path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            else:

                subprocess.Popen(
                    [
                        "cmd",
                        "/c",
                        "start",
                        "",
                        executable
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            return (
                True,
                f"Opening {application}."
            )

        except Exception as e:

            return (
                False,
                f"I couldn't open {application}: {e}"
            )

    # ========================================================
    # OPEN WEBSITE
    # ========================================================

    def open_website(self, website):

        urls = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://github.com",
            "instagram": "https://www.instagram.com",
            "chatgpt": "https://chatgpt.com",
        }

        url = urls.get(
            website
        )

        if not url:

            return (
                False,
                "I don't know that website yet."
            )

        try:

            webbrowser.open(
                url
            )

            return (
                True,
                f"Opening {website}."
            )

        except Exception as e:

            return (
                False,
                f"I couldn't open {website}: {e}"
            )

    # ========================================================
    # SYSTEM ACTION DETECTION
    # ========================================================

    def detect_system_action(self, message):

        # ----------------------------------------------------
        # LOCK
        # ----------------------------------------------------

        lock_phrases = [
            "lock my pc",
            "lock my computer",
            "lock the pc",
            "lock the computer",
            "lock computer",
            "lock pc"
        ]

        if any(
            phrase in message
            for phrase in lock_phrases
        ):

            return "lock"

        # ----------------------------------------------------
        # VOLUME UP
        # ----------------------------------------------------

        volume_up_phrases = [
            "increase volume",
            "increase the volume",
            "volume up",
            "turn the volume up",
            "make it louder",
            "make the volume louder"
        ]

        if any(
            phrase in message
            for phrase in volume_up_phrases
        ):

            return "volume_up"

        # ----------------------------------------------------
        # VOLUME DOWN
        # ----------------------------------------------------

        volume_down_phrases = [
            "decrease volume",
            "decrease the volume",
            "volume down",
            "turn the volume down",
            "make it quieter",
            "lower the volume"
        ]

        if any(
            phrase in message
            for phrase in volume_down_phrases
        ):

            return "volume_down"

        # ----------------------------------------------------
        # MUTE
        # ----------------------------------------------------

        mute_phrases = [
            "mute",
            "mute my computer",
            "mute the computer",
            "mute audio",
            "mute sound"
        ]

        if any(
            phrase in message
            for phrase in mute_phrases
        ):

            return "mute"

        # ----------------------------------------------------
        # PLAY / PAUSE
        # ----------------------------------------------------

        play_pause_phrases = [
            "play music",
            "pause music",
            "play the music",
            "pause the music",
            "play",
            "pause",
            "play pause",
            "pause play",
            "resume music",
            "resume playback",
            "resume"
        ]

        if any(
            phrase in message
            for phrase in play_pause_phrases
        ):

            return "play_pause"

        # ----------------------------------------------------
        # NEXT TRACK
        # ----------------------------------------------------

        next_track_phrases = [
            "next song",
            "next track",
            "skip song",
            "skip this song",
            "skip track",
            "play next song",
            "play next track"
        ]

        if any(
            phrase in message
            for phrase in next_track_phrases
        ):

            return "next_track"

        # ----------------------------------------------------
        # PREVIOUS TRACK
        # ----------------------------------------------------

        previous_track_phrases = [
            "previous song",
            "previous track",
            "previous",
            "go back song",
            "go to previous song",
            "play previous song"
        ]

        if any(
            phrase in message
            for phrase in previous_track_phrases
        ):

            return "previous_track"

        return None

    # ========================================================
    # EXECUTE SYSTEM ACTION
    # ========================================================

    def execute_system_action(self, action):

        if action == "lock":

            return self.system_tools.lock_computer()

        if action == "volume_up":

            return self.system_tools.volume_up()

        if action == "volume_down":

            return self.system_tools.volume_down()

        if action == "mute":

            return self.system_tools.toggle_mute()

        if action == "play_pause":

            return self.system_tools.play_pause()

        if action == "next_track":

            return self.system_tools.next_track()

        if action == "previous_track":

            return self.system_tools.previous_track()

        return (
            False,
            "I don't know how to perform that system action."
        )

    # ========================================================
    # EXECUTE FILE ACTION
    # ========================================================

    def execute_file_action(self, file_action):

        action, value = file_action

        # ----------------------------------------------------
        # OPEN DOWNLOADS
        # ----------------------------------------------------

        if action == "open_downloads":

            return self.file_tools.open_downloads()

        # ----------------------------------------------------
        # FIND PDFS
        # ----------------------------------------------------

        if action == "find_pdfs":

            return self.file_tools.find_pdfs()

        # ----------------------------------------------------
        # SEARCH FILE
        # ----------------------------------------------------

        if action == "search_file":

            return self.file_tools.search_files(
                value
            )

        # ----------------------------------------------------
        # SEARCH AND OPEN
        # ----------------------------------------------------

        if action == "search_and_open":

            return self.file_tools.search_and_open(
                value
            )

        return (
            False,
            "I don't know how to perform that file action."
        )

    # ========================================================
    # FILE ACTION DETECTION
    # ========================================================

    def detect_file_action(self, message):

        # ----------------------------------------------------
        # OPEN DOWNLOADS
        # ----------------------------------------------------

        downloads_phrases = [
            "open downloads",
            "open my downloads",
            "show downloads",
            "show my downloads",
            "open downloads folder",
            "open my downloads folder"
        ]

        if any(
            phrase in message
            for phrase in downloads_phrases
        ):

            return (
                "open_downloads",
                None
            )

        # ----------------------------------------------------
        # FIND PDFS
        # ----------------------------------------------------

        pdf_phrases = [
            "find pdf",
            "find pdfs",
            "find my pdf",
            "find my pdfs",
            "search for pdf",
            "search for pdfs"
        ]

        if any(
            phrase in message
            for phrase in pdf_phrases
        ):

            return (
                "find_pdfs",
                None
            )

        # ----------------------------------------------------
        # FIND AND OPEN FILE
        # ----------------------------------------------------

        open_file_phrases = [
            "find and open ",
            "open my ",
            "open the ",
            "open "
        ]

        for phrase in open_file_phrases:

            if message.startswith(phrase):

                filename = message[
                    len(phrase):
                ].strip()

                # Do not treat Downloads as a file.

                if filename in [
                    "downloads",
                    "downloads folder"
                ]:

                    continue

                if filename:

                    return (
                        "search_and_open",
                        filename
                    )

        # ----------------------------------------------------
        # FIND FILE
        # ----------------------------------------------------

        find_patterns = [
            "find ",
            "search for ",
            "look for ",
            "locate "
        ]

        for phrase in find_patterns:

            if message.startswith(phrase):

                filename = message[
                    len(phrase):
                ].strip()

                if filename:

                    return (
                        "search_file",
                        filename
                    )

        # ----------------------------------------------------
        # NO FILE ACTION
        # ----------------------------------------------------

        return None