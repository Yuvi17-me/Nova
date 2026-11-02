import re
import webbrowser
import subprocess
import shutil
from datetime import datetime

from backend.agent.system_tools import SystemTools
from backend.agent.file_tools import FileTools
from backend.memory.memory_manager import MemoryManager


class AgentCore:

    def __init__(self):

        self.system_tools = SystemTools()
        self.file_tools = FileTools()
        self.memory_manager = MemoryManager()

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
        # MEMORY ACTIONS
        # ====================================================

        memory_action = self.detect_memory_action(
            message,
            message_lower
        )

        if memory_action:

            return self.execute_memory_action(
                memory_action
            )

        # ====================================================
        # UTILITY ACTIONS (TIME, DATE, IDENTITY)
        # ====================================================

        utility_action = self.detect_utility_action(
            message_lower
        )

        if utility_action:

            return self.execute_utility_action(
                utility_action
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
        # NORMAL AI QUERY
        # ====================================================

        return None

    # ========================================================
    # WEBSITE DETECTION
    # ========================================================

    def detect_website(self, message):

        websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "github": "https://github.com",
            "instagram": "https://www.instagram.com",
            "chatgpt": "https://chatgpt.com",
        }

        website_patterns = {

            "youtube": [
                r"\bopen\s+(?:the\s+)?youtube\b",
                r"\bgo\s+to\s+(?:the\s+)?youtube\b",
            ],

            "google": [
                r"\bopen\s+(?:the\s+)?google\b",
                r"\bgo\s+to\s+(?:the\s+)?google\b",
            ],

            "github": [
                r"\bopen\s+(?:the\s+)?github\b",
                r"\bgo\s+to\s+(?:the\s+)?github\b",
            ],

            "instagram": [
                r"\bopen\s+(?:the\s+)?instagram\b",
                r"\bgo\s+to\s+(?:the\s+)?instagram\b",
            ],

            "chatgpt": [
                r"\bopen\s+(?:the\s+)?chatgpt\b",
                r"\bgo\s+to\s+(?:the\s+)?chatgpt\b",
            ],
        }

        for website, patterns in website_patterns.items():

            for pattern in patterns:

                if re.search(pattern, message):

                    return website

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

        # Check longer names first.

        application_names = sorted(
            self.applications.keys(),
            key=len,
            reverse=True
        )

        for name in application_names:

            # Prevent matching "chrome" inside another word.

            if re.search(
                rf"\b{re.escape(name)}\b",
                message
            ):

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
        # DISAMBIGUATION: JOB RESUME VS MEDIA RESUME
        # If the user says "find my resume", "open resume",
        # "where is my resume", etc., it refers to their CV/job
        # profile document and MUST NOT trigger media playback.
        # ----------------------------------------------------

        is_job_resume = bool(
            re.search(
                r"\b(?:find|search(?:\s+for)?|look\s+for|locate|where\s+is|show(?:\s+me)?|get|open|view|read|edit|send|email|check|download|print)\b.*\b(?:resume|cv)\b",
                message
            )
            or re.search(
                r"\b(?:my|your|his|her|a|the|job|latest|updated|current|work)\s+resume\b",
                message
            )
            or re.search(
                r"\bresume\s+(?:file|document|doc|pdf|folder|profile)\b",
                message
            )
        )

        # ----------------------------------------------------
        # LOCK
        # ----------------------------------------------------

        lock_patterns = [
            r"\block\s+(?:my\s+|the\s+)?(?:pc|computer|screen|workstation)\b",
            r"^\s*(?:please\s+|can\s+you\s+)?lock(?:\s+screen)?(?:\s+now|\s+please)?\s*$",
        ]

        if any(re.search(pat, message) for pat in lock_patterns):
            if not re.search(r"\bunlock\b", message):
                return "lock"

        # ----------------------------------------------------
        # VOLUME UP
        # ----------------------------------------------------

        volume_up_patterns = [
            r"\b(?:increase|turn\s+up|raise)\s+(?:the\s+)?volume\b",
            r"\bvolume\s+up\b",
            r"\bmake\s+it\s+louder\b",
            r"\bmake\s+the\s+volume\s+louder\b",
            r"^\s*(?:please\s+)?louder(?:\s+please)?\s*$",
        ]

        if any(re.search(pat, message) for pat in volume_up_patterns):
            return "volume_up"

        # ----------------------------------------------------
        # VOLUME DOWN
        # ----------------------------------------------------

        volume_down_patterns = [
            r"\b(?:decrease|turn\s+down|lower|reduce)\s+(?:the\s+)?volume\b",
            r"\bvolume\s+down\b",
            r"\bmake\s+it\s+quieter\b",
            r"\bmake\s+the\s+volume\s+quieter\b",
            r"^\s*(?:please\s+)?quieter(?:\s+please)?\s*$",
        ]

        if any(re.search(pat, message) for pat in volume_down_patterns):
            return "volume_down"

        # ----------------------------------------------------
        # MUTE
        # ----------------------------------------------------

        mute_patterns = [
            r"\bmute\s+(?:the\s+|my\s+)?(?:computer|pc|audio|sound|system|volume)\b",
            r"^\s*(?:please\s+|can\s+you\s+)?mute(?:\s+audio|\s+sound|\s+now|\s+please)?\s*$",
            r"\btoggle\s+mute\b",
        ]

        if any(re.search(pat, message) for pat in mute_patterns):
            if not re.search(r"\bunmute\b", message):
                return "mute"

        # ----------------------------------------------------
        # PLAY / PAUSE / RESUME MEDIA
        # ----------------------------------------------------

        if not is_job_resume:

            media_action_pattern = (
                r"\b(?:play|pause|resume|unpause)\s+(?:the\s+)?"
                r"(?:music|song|songs|video|videos|audio|track|tracks|playback|media|playing)\b"
            )

            media_standalone_pattern = (
                r"^\s*(?:please\s+|can\s+you\s+|could\s+you\s+)?"
                r"(?:play|pause|resume|unpause|play\s+pause|pause\s+play|toggle\s+playback|toggle\s+play)"
                r"(?:\s+now|\s+please)?\s*$"
            )

            if (
                re.search(media_action_pattern, message)
                or re.search(media_standalone_pattern, message)
            ):
                return "play_pause"

        # ----------------------------------------------------
        # NEXT TRACK
        # ----------------------------------------------------

        next_track_patterns = [
            r"\b(?:play\s+)?next\s+(?:song|track)\b",
            r"\bskip\s+(?:this\s+)?(?:song|track)\b",
            r"^\s*(?:please\s+)?(?:skip|next)(?:\s+song|\s+track)?(?:\s+now|\s+please)?\s*$",
        ]

        if any(re.search(pat, message) for pat in next_track_patterns):
            return "next_track"

        # ----------------------------------------------------
        # PREVIOUS TRACK
        # ----------------------------------------------------

        previous_track_patterns = [
            r"\b(?:play\s+)?previous\s+(?:song|track)\b",
            r"\bgo\s+back\s+(?:a\s+|one\s+)?(?:song|track)\b",
            r"^\s*(?:please\s+)?previous\s+(?:song|track)(?:\s+now|\s+please)?\s*$",
            r"^\s*(?:please\s+)?previous(?:\s+now|\s+please)?\s*$",
        ]

        if any(re.search(pat, message) for pat in previous_track_patterns):
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
        # OPEN PREVIOUS SEARCH RESULT
        # ----------------------------------------------------

        if action == "open_search_result":

            return self.file_tools.open_search_result(
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

        # ====================================================
        # RESUME / CV SPECIAL DETECTION
        # Explicitly maps resume/CV requests to search or open.
        # ====================================================

        resume_search_patterns = [
            r"^(?:find|search(?:\s+for)?|locate|look\s+for|where\s+is|show(?:\s+me)?|get)\s+(?:my\s+|the\s+|a\s+)?(?:job\s+)?(?:resume|cv|curriculum\s+vitae)\b",
            r"^(?:my\s+)?(?:job\s+)?(?:resume|cv|curriculum\s+vitae)$",
            r"\bwhere\s+is\s+(?:my\s+|the\s+)?(?:job\s+)?(?:resume|cv)\b",
        ]

        for pattern in resume_search_patterns:
            if re.search(pattern, message):
                return (
                    "search_file",
                    "resume"
                )

        resume_open_patterns = [
            r"^(?:open|launch|view|read|display)\s+(?:my\s+|the\s+|a\s+)?(?:job\s+)?(?:resume|cv|curriculum\s+vitae)\b",
            r"^find\s+and\s+open\s+(?:my\s+|the\s+|a\s+)?(?:job\s+)?(?:resume|cv|curriculum\s+vitae)\b",
        ]

        for pattern in resume_open_patterns:
            if re.search(pattern, message):
                return (
                    "search_and_open",
                    "resume"
                )

        # ====================================================
        # OPEN PREVIOUS SEARCH RESULT
        # ====================================================

        ordinal_patterns = {
            "first": 1,
            "1st": 1,

            "second": 2,
            "2nd": 2,

            "third": 3,
            "3rd": 3,

            "fourth": 4,
            "4th": 4,

            "fifth": 5,
            "5th": 5,
        }

        # ----------------------------------------------------
        # Commands:
        #
        # Open 1st one
        # Open first one
        # Open second one
        # Open #2
        # Open 2
        # ----------------------------------------------------

        if message.startswith("open "):

            target = message[
                len("open "):
            ].strip()

            # Remove "one"

            target = re.sub(
                r"\s+one$",
                "",
                target
            ).strip()

            # Remove "#"

            target = target.replace(
                "#",
                ""
            ).strip()

            # Check ordinal

            if target in ordinal_patterns:

                return (
                    "open_search_result",
                    ordinal_patterns[target]
                )

            # Check numeric

            if target.isdigit():

                index = int(target)

                if index > 0:

                    return (
                        "open_search_result",
                        index
                    )

        # ====================================================
        # OPEN DOWNLOADS
        # ====================================================

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

        # ====================================================
        # FIND PDFS
        # ====================================================

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

        # ====================================================
        # FIND AND OPEN FILE
        # ====================================================

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

                # Clean leading articles/possessives
                clean_filename = re.sub(
                    r"^(?:my|the|a|an)\s+",
                    "",
                    filename
                ).strip()
                if clean_filename:
                    filename = clean_filename

                # Don't treat Downloads as a file.

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

        # ====================================================
        # FIND FILE
        # ====================================================

        find_patterns = [
            "find and show ",
            "find ",
            "search for ",
            "search ",
            "look for ",
            "locate ",
            "where is ",
            "where's ",
            "show me ",
            "show ",
            "get "
        ]

        for phrase in find_patterns:

            if message.startswith(phrase):

                filename = message[
                    len(phrase):
                ].strip()

                # Clean leading articles/possessives
                clean_filename = re.sub(
                    r"^(?:my|the|a|an)\s+",
                    "",
                    filename
                ).strip()
                if clean_filename:
                    filename = clean_filename

                if filename:

                    return (
                        "search_file",
                        filename
                    )

        # ====================================================
        # NO FILE ACTION
        # ====================================================

        return None

    # ========================================================
    # MEMORY ACTION DETECTION
    # ========================================================

    def detect_memory_action(self, message, message_lower):

        # ----------------------------------------------------
        # Querying memory / Identity
        # ----------------------------------------------------
        memory_query_patterns = [
            r"^(?:what\s+do\s+you|what\s+all\s+do\s+you)\s+(?:remember|know)\s+(?:about\s+me)?\??$",
            r"^(?:what\s+are\s+your|show(?:\s+me)?\s+(?:my\s+|the\s+|all\s+)?)memories\??$",
            r"^(?:my\s+memories|saved\s+memories)\??$",
            r"^(?:who\s+am\s+i|what\s+is\s+my\s+name)\??$",
            r"^what\s+do\s+you\s+know\??$",
        ]

        for pat in memory_query_patterns:
            if re.search(pat, message_lower):
                return ("show_memory", None)

        # ----------------------------------------------------
        # Explicit storing / teaching
        # ----------------------------------------------------
        store_patterns = [
            r"^(?:please\s+)?(?:remember\s+that|note\s+that|learn\s+that)\s+(.+)",
            r"^(?:please\s+)?remember\s+([^\?]+)$",
        ]

        for pat in store_patterns:
            match = re.match(pat, message, re.IGNORECASE)
            if match:
                fact = match.group(1).strip()
                # Don't capture questions or "remember to"
                if not fact.lower().startswith("to ") and not fact.lower().startswith("what "):
                    return ("store_memory", fact)

        return None

    # ========================================================
    # EXECUTE MEMORY ACTION
    # ========================================================

    def execute_memory_action(self, memory_action):
        action, value = memory_action

        if action == "show_memory":
            profile = self.memory_manager.get_profile()
            memories = self.memory_manager.get_memories(limit=12)

            user_name = profile.get("user_name", "Yuvraj")
            role = profile.get("developer_role", "Developer")
            pref_langs = profile.get("preferred_languages", "C++, Python")
            os_name = profile.get("primary_os", "Windows 11")

            lines = [
                f"### 🧠 **Nova Memory & User Identity**",
                f"",
                f"**User Profile:**",
                f"- **Recognized User**: {user_name} ({role})",
                f"- **Preferred Stack**: {pref_langs}",
                f"- **System Platform**: {os_name}",
                f"",
            ]

            if memories:
                lines.append(f"**Learned Facts & Preferences ({len(memories)} entries):**")
                for m in memories:
                    cat = m.get("category", "general").capitalize()
                    content = m.get("content", "")
                    lines.append(f"- `[{cat}]` {content}")
            else:
                lines.append("*No explicit memories stored yet. You can teach me by saying:*")
                lines.append("> *\"Remember that I prefer modern C++20 for all algorithms.\"*")

            return (True, "\n".join(lines))

        if action == "store_memory":
            fact = value.strip().rstrip(".?!")
            mem_id = self.memory_manager.add_memory(fact, category="user_instruction", importance=2)
            if mem_id:
                return (
                    True,
                    f"🧠 **Saved to Long-Term Memory**\n\n"
                    f"I've committed that to my persistent knowledge base:\n"
                    f"> *\"{fact}\"*\n\n"
                    f"I'll remember this across all our conversations."
                )
            else:
                return (
                    True,
                    f"🧠 I already have this in my memory:\n> *\"{fact}\"*"
                )

        return (False, "Could not process memory action.")

    # ========================================================
    # UTILITY ACTION DETECTION
    # ========================================================

    def detect_utility_action(self, message_lower):
        # Strip conversational prefixes
        cleaned = re.sub(
            r"^(?:can\s+you\s+|could\s+you\s+|please\s+|tell\s+me\s+)+",
            "",
            message_lower
        ).strip()

        # Date & Year (e.g. "what is the current date & year", "date and year")
        date_year_patterns = [
            r"^(?:what(?:['’]s|\s+is)?\s+)?(?:the\s+)?(?:current\s+)?date\s+(?:&|and)\s+year\??$",
            r"^(?:what(?:['’]s|\s+is)?\s+)?(?:the\s+)?today['’]?s\s+date\s+(?:&|and)\s+year\??$",
            r"^date\s+(?:&|and)\s+year\??$",
        ]
        if any(re.search(pat, cleaned) for pat in date_year_patterns):
            return "date_year"

        # Year (e.g. "what year is it", "what is the current year", "which year are we in")
        year_patterns = [
            r"^(?:what(?:['’]s|\s+is)?\s+)?(?:the\s+)?current\s+year\??$",
            r"^(?:what|which)\s+year\s+(?:is\s+(?:it|this)|are\s+we\s+in)\??$",
            r"^current\s+year\??$",
        ]
        if any(re.search(pat, cleaned) for pat in year_patterns):
            return "year"

        # Date & Time (e.g. "date and time", "current date and time")
        datetime_patterns = [
            r"^(?:what(?:['’]s|\s+is)?\s+)?(?:the\s+)?(?:current\s+)?date\s+(?:&|and)\s+time\??$",
            r"^(?:what(?:['’]s|\s+is)?\s+)?(?:the\s+)?(?:current\s+)?time\s+(?:&|and)\s+date\??$",
            r"^date\s+(?:&|and)\s+time\??$",
        ]
        if any(re.search(pat, cleaned) for pat in datetime_patterns):
            return "datetime"

        # Date (e.g. "what is the date", "today's date", "what day is today", "what is the date today")
        date_patterns = [
            r"^(?:what(?:['’]s|\s+is)?\s+)?(?:the\s+)?(?:current\s+)?date(?:\s+today)?\??$",
            r"^(?:what(?:['’]s|\s+is)?\s+)?today['’]?s\s+date\??$",
            r"^what\s+(?:day|date)\s+is\s+(?:it|today)(?:\s+today)?\??$",
            r"^(?:the\s+)?date\s+today\??$",
            r"^current\s+date\??$",
        ]
        if any(re.search(pat, cleaned) for pat in date_patterns):
            return "date"

        # Time (e.g. "what time is it", "current time", "what is the time")
        time_patterns = [
            r"^(?:what(?:['’]s|\s+is)?\s+)?(?:the\s+)?(?:current\s+)?time\??$",
            r"^what\s+time\s+is\s+it(?:\s+now|\s+right\s+now)?\??$",
            r"^(?:the\s+)?time\s+(?:now|right\s+now)\??$",
            r"^current\s+time\??$",
        ]
        if any(re.search(pat, cleaned) for pat in time_patterns):
            return "time"

        # Nova Identity
        identity_patterns = [
            r"^(?:who\s+are\s+you|what\s+is\s+your\s+name|what\s+are\s+you)\??$",
        ]
        if any(re.search(pat, cleaned) for pat in identity_patterns):
            return "identity"

        return None

    # ========================================================
    # EXECUTE UTILITY ACTION
    # ========================================================

    def execute_utility_action(self, utility_action):
        now = datetime.now()
        date_str = now.strftime("%A, %B %d, %Y")
        time_str = now.strftime("%I:%M %p")
        year_str = str(now.year)

        if utility_action in ("date_year", "datetime"):
            return (
                True,
                f"📅 **Current Date**: {date_str}\n\n"
                f"🗓️ **Current Year**: {year_str}\n\n"
                f"🕒 **System Time**: {time_str}"
            )

        if utility_action == "year":
            return (
                True,
                f"🗓️ The current year is **{year_str}**.\n\n"
                f"📅 Today is **{date_str}**."
            )

        if utility_action == "date":
            return (
                True,
                f"📅 Today is **{date_str}** (Year **{year_str}**)."
            )

        if utility_action == "time":
            return (
                True,
                f"🕒 The current system time is **{time_str}**.\n\n"
                f"📅 Today is **{date_str}**."
            )

        if utility_action == "identity":
            return (
                True,
                "I am **Nova**, your personalized, privacy-first AI desktop assistant.\n\n"
                "I can execute local system actions (lock computer, control volume and media), "
                "find and open your files and documents, remember your personal coding preferences, "
                "and assist you with technical problem solving."
            )

        return (False, "Unknown utility action.")