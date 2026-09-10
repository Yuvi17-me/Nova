import ctypes


class SystemTools:

    # ========================================================
    # WINDOWS MEDIA KEY
    # ========================================================

    def _press_media_key(self, key_code):

        KEYEVENTF_KEYUP = 0x0002

        # Key down
        ctypes.windll.user32.keybd_event(
            key_code,
            0,
            0,
            0
        )

        # Key up
        ctypes.windll.user32.keybd_event(
            key_code,
            0,
            KEYEVENTF_KEYUP,
            0
        )

    # ========================================================
    # LOCK COMPUTER
    # ========================================================

    def lock_computer(self):

        try:

            ctypes.windll.user32.LockWorkStation()

            return (
                True,
                "Locking your computer."
            )

        except Exception as e:

            return (
                False,
                f"I couldn't lock the computer: {e}"
            )

    # ========================================================
    # VOLUME UP
    # ========================================================

    def volume_up(self):

        try:

            # VK_VOLUME_UP = 0xAF

            self._press_media_key(
                0xAF
            )

            return (
                True,
                "Volume increased."
            )

        except Exception as e:

            return (
                False,
                f"I couldn't increase the volume: {e}"
            )

    # ========================================================
    # VOLUME DOWN
    # ========================================================

    def volume_down(self):

        try:

            # VK_VOLUME_DOWN = 0xAE

            self._press_media_key(
                0xAE
            )

            return (
                True,
                "Volume decreased."
            )

        except Exception as e:

            return (
                False,
                f"I couldn't decrease the volume: {e}"
            )

    # ========================================================
    # MUTE / UNMUTE
    # ========================================================

    def toggle_mute(self):

        try:

            # VK_VOLUME_MUTE = 0xAD

            self._press_media_key(
                0xAD
            )

            return (
                True,
                "Audio mute toggled."
            )

        except Exception as e:

            return (
                False,
                f"I couldn't change the mute state: {e}"
            )

    # ========================================================
    # PLAY / PAUSE MEDIA
    # ========================================================

    def play_pause(self):

        try:

            # VK_MEDIA_PLAY_PAUSE = 0xB3

            self._press_media_key(
                0xB3
            )

            return (
                True,
                "Play/pause toggled."
            )

        except Exception as e:

            return (
                False,
                f"I couldn't control media playback: {e}"
            )

    # ========================================================
    # NEXT TRACK
    # ========================================================

    def next_track(self):

        try:

            # VK_MEDIA_NEXT_TRACK = 0xB0

            self._press_media_key(
                0xB0
            )

            return (
                True,
                "Skipped to the next track."
            )

        except Exception as e:

            return (
                False,
                f"I couldn't skip to the next track: {e}"
            )

    # ========================================================
    # PREVIOUS TRACK
    # ========================================================

    def previous_track(self):

        try:

            # VK_MEDIA_PREV_TRACK = 0xB1

            self._press_media_key(
                0xB1
            )

            return (
                True,
                "Went back to the previous track."
            )

        except Exception as e:

            return (
                False,
                f"I couldn't go to the previous track: {e}"
            )