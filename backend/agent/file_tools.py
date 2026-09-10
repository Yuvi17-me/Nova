import os
from pathlib import Path


class FileTools:

    def __init__(self):

        self.home = Path.home()

        self.common_folders = {
            "downloads": self.home / "Downloads",
            "documents": self.home / "Documents",
            "desktop": self.home / "Desktop",
        }

    # ========================================================
    # OPEN DOWNLOADS
    # ========================================================

    def open_downloads(self):

        folder = self.common_folders["downloads"]

        try:

            if not folder.exists():
                return (
                    False,
                    "I couldn't find your Downloads folder."
                )

            os.startfile(str(folder))

            return (
                True,
                "Opening your Downloads folder."
            )

        except Exception as e:

            return (
                False,
                f"I couldn't open Downloads: {e}"
            )

    # ========================================================
    # SEARCH FILES
    # ========================================================

    def search_files(self, filename):

        filename = filename.strip()

        if not filename:
            return (
                False,
                "Please tell me what file you're looking for."
            )

        results = []

        for folder in self.common_folders.values():

            if not folder.exists():
                continue

            try:

                for path in folder.rglob("*"):

                    if not path.is_file():
                        continue

                    if filename.lower() in path.name.lower():

                        results.append(path)

                        if len(results) >= 20:
                            break

            except (PermissionError, OSError):
                continue

        if not results:

            return (
                True,
                f"I couldn't find any files matching '{filename}'."
            )

        response = (
            f"I found {len(results)} file"
            f"{'s' if len(results) != 1 else ''}:\n\n"
        )

        for path in results:
            response += f"• {path}\n"

        return (
            True,
            response.rstrip()
        )

    # ========================================================
    # FIND PDF FILES
    # ========================================================

    def find_pdfs(self):

        results = []

        downloads = self.common_folders["downloads"]

        if not downloads.exists():
            return (
                False,
                "I couldn't find your Downloads folder."
            )

        try:

            for path in downloads.rglob("*.pdf"):

                if path.is_file():
                    results.append(path)

                if len(results) >= 20:
                    break

        except (PermissionError, OSError):
            pass

        if not results:
            return (
                True,
                "I couldn't find any PDF files in Downloads."
            )

        response = (
            f"I found {len(results)} PDF"
            f"{'s' if len(results) != 1 else ''} "
            "in Downloads:\n\n"
        )

        for path in results:
            response += f"• {path}\n"

        return (
            True,
            response.rstrip()
        )

    # ========================================================
    # SEARCH AND OPEN FILE
    # ========================================================

    def search_and_open(self, filename):

        filename = filename.strip()

        if not filename:

            return (
                False,
                "Please tell me which file you want me to open."
            )

        results = []

        for folder in self.common_folders.values():

            if not folder.exists():
                continue

            try:

                for path in folder.rglob("*"):

                    if not path.is_file():
                        continue

                    if filename.lower() in path.name.lower():

                        results.append(path)

                        if len(results) >= 20:
                            break

            except (PermissionError, OSError):
                continue

        # ----------------------------------------------------
        # No result
        # ----------------------------------------------------

        if not results:

            return (
                False,
                f"I couldn't find a file matching '{filename}'."
            )

        # ----------------------------------------------------
        # Multiple results
        # ----------------------------------------------------

        if len(results) > 1:

            response = (
                f"I found multiple files matching "
                f"'{filename}'. Please be more specific:\n\n"
            )

            for path in results[:10]:

                response += f"• {path}\n"

            return (
                False,
                response.rstrip()
            )

        # ----------------------------------------------------
        # Exactly one result
        # ----------------------------------------------------

        file_path = results[0]

        try:

            os.startfile(str(file_path))

            return (
                True,
                f"Opening {file_path.name}."
            )

        except Exception as e:

            return (
                False,
                f"I found the file, but couldn't open it: {e}"
            )

    # ========================================================
    # OPEN FILE
    # ========================================================

    def open_file(self, file_path):

        try:

            path = Path(file_path)

            if not path.exists():

                return (
                    False,
                    "That file no longer exists."
                )

            if not path.is_file():

                return (
                    False,
                    "That path is not a file."
                )

            os.startfile(str(path))

            return (
                True,
                f"Opening {path.name}."
            )

        except Exception as e:

            return (
                False,
                f"I couldn't open the file: {e}"
            )