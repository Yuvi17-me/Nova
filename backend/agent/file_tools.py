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

        # Stores the results of the most recent file search.
        # This allows commands such as:
        #
        # Find resume
        # Open 1st one
        #
        self.last_search_results = []

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

        # Support CV / curriculum vitae synonym search for resume
        search_terms = [filename.lower()]
        if filename.lower() in [
            "resume",
            "my resume",
            "cv",
            "curriculum vitae"
        ]:
            search_terms = ["resume", "cv", "curriculum vitae"]

        results = []

        for folder in self.common_folders.values():

            if not folder.exists():
                continue

            try:

                for path in folder.rglob("*"):

                    if not path.is_file():
                        continue

                    path_name_lower = path.name.lower()

                    if any(
                        term in path_name_lower
                        for term in search_terms
                    ):

                        results.append(path)

                        if len(results) >= 20:
                            break

            except (PermissionError, OSError):

                continue

        # Rank results: exact matches first, then shallower folders, then newest
        def rank_result(p):
            stem = p.stem.lower()
            exact = 0 if stem in [
                "resume",
                "my resume",
                "cv",
                filename.lower()
            ] else 1
            depth = len(p.parts)
            try:
                mtime = -p.stat().st_mtime
            except Exception:
                mtime = 0
            return (exact, depth, mtime)

        results.sort(key=rank_result)

        # Save search results for contextual commands.

        self.last_search_results = results.copy()

        # ----------------------------------------------------
        # No results
        # ----------------------------------------------------

        if not results:

            return (
                True,
                f"I couldn't find any files matching '{filename}'."
            )

        # ----------------------------------------------------
        # Build response
        # ----------------------------------------------------

        response = (
            f"I found {len(results)} file"
            f"{'s' if len(results) != 1 else ''}:\n\n"
        )

        for index, path in enumerate(results, start=1):

            response += f"{index}. {path}\n"

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

        # Save PDF results as the latest search results.

        self.last_search_results = results.copy()

        # ----------------------------------------------------
        # No results
        # ----------------------------------------------------

        if not results:

            return (
                True,
                "I couldn't find any PDF files in Downloads."
            )

        # ----------------------------------------------------
        # Build response
        # ----------------------------------------------------

        response = (
            f"I found {len(results)} PDF"
            f"{'s' if len(results) != 1 else ''} "
            "in Downloads:\n\n"
        )

        for index, path in enumerate(results, start=1):

            response += f"{index}. {path}\n"

        return (
            True,
            response.rstrip()
        )

    # ========================================================
    # OPEN SEARCH RESULT BY NUMBER
    # ========================================================

    def open_search_result(self, index):

        # Make sure we have previous results.

        if not self.last_search_results:

            return (
                False,
                "I don't have any recent file search results. "
                "Please search for a file first."
            )

        # Convert to zero-based index.

        zero_index = index - 1

        # Check range.

        if zero_index < 0 or zero_index >= len(
            self.last_search_results
        ):

            return (
                False,
                f"I only have {len(self.last_search_results)} "
                "recent search result"
                f"{'s' if len(self.last_search_results) != 1 else ''}."
            )

        file_path = self.last_search_results[zero_index]

        return self.open_file(
            file_path
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

        # Support CV / curriculum vitae synonym search for resume
        search_terms = [filename.lower()]
        if filename.lower() in [
            "resume",
            "my resume",
            "cv",
            "curriculum vitae"
        ]:
            search_terms = ["resume", "cv", "curriculum vitae"]

        results = []

        for folder in self.common_folders.values():

            if not folder.exists():
                continue

            try:

                for path in folder.rglob("*"):

                    if not path.is_file():
                        continue

                    path_name_lower = path.name.lower()

                    if any(
                        term in path_name_lower
                        for term in search_terms
                    ):

                        results.append(path)

                        if len(results) >= 20:
                            break

            except (PermissionError, OSError):

                continue

        # Rank results: exact matches first, then shallower folders, then newest
        def rank_result(p):
            stem = p.stem.lower()
            exact = 0 if stem in [
                "resume",
                "my resume",
                "cv",
                filename.lower()
            ] else 1
            depth = len(p.parts)
            try:
                mtime = -p.stat().st_mtime
            except Exception:
                mtime = 0
            return (exact, depth, mtime)

        results.sort(key=rank_result)

        # Save these results too.

        self.last_search_results = results.copy()

        # ----------------------------------------------------
        # No result
        # ----------------------------------------------------

        if not results:

            return (
                False,
                f"I couldn't find a file matching '{filename}'."
            )

        # ----------------------------------------------------
        # Single exact match among multiple results
        # (e.g. user's direct "My resume.txt" vs sample files)
        # ----------------------------------------------------

        exact_matches = [
            p for p in results
            if p.stem.lower() in [
                "resume",
                "my resume",
                "cv",
                filename.lower()
            ]
        ]

        if len(exact_matches) == 1:

            return self.open_file(
                exact_matches[0]
            )

        # ----------------------------------------------------
        # Multiple results
        # ----------------------------------------------------

        if len(results) > 1:

            response = (
                f"I found multiple files matching "
                f"'{filename}'. Please be more specific:\n\n"
            )

            for index, path in enumerate(
                results[:10],
                start=1
            ):

                response += f"{index}. {path}\n"

            return (
                False,
                response.rstrip()
            )

        # ----------------------------------------------------
        # Exactly one result
        # ----------------------------------------------------

        return self.open_file(
            results[0]
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