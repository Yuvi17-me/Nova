import shutil
import subprocess
import time
import re

import ollama
from backend.memory.memory_manager import MemoryManager


class OllamaEngine:

    def __init__(self, model="qwen3:1.7b", host=None):
        self.model = model
        self.host = host or "http://127.0.0.1:11434"
        self.client = ollama.Client(host=self.host)
        self.memory = MemoryManager()

    def _ensure_service(self):
        try:
            self.client.list()
            return
        except Exception as initial_error:
            executable = shutil.which("ollama")
            if not executable:
                raise RuntimeError(
                    "Ollama is not installed. Install it from https://ollama.com/download."
                ) from initial_error

            subprocess.Popen(
                [executable, "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )

            last_error = initial_error
            for _ in range(20):
                time.sleep(0.25)
                try:
                    self.client.list()
                    return
                except Exception as error:
                    last_error = error

            raise RuntimeError(
                "Ollama is installed but could not be started. "
                "Please open Ollama and try again."
            ) from last_error

    def _ensure_model(self):
        models = self.client.list().get("models", [])
        installed = {
            model.get("name") if isinstance(model, dict) else getattr(model, "model", None)
            for model in models
        }
        if self.model not in installed:
            raise RuntimeError(
                f"The model '{self.model}' is not installed. "
                f"Run `ollama pull {self.model}` and try again."
            )

    @staticmethod
    def _is_follow_up(message, history):
        if not history:
            return False
        msg_lower = message.lower().strip()

        # 1. Explicit follow-up markers (references to prior content/turns)
        follow_up_markers = [
            r"\b(?:convert|rewrite|translate|modify|fix|update|optimize|refactor)\b",
            r"\b(?:now\s+in|now\s+with|how\s+about|what\s+about)\b",
            r"^(?:why|how|explain\s+(?:that|it|this|the\s+above|the\s+code))\b",
            r"\b(?:make\s+it|change\s+it|do\s+it|add\s+to\s+it)\b",
            r"\b(?:the\s+above|the\s+previous|the\s+former)\b",
            r"\b(?:instead\s+of)\b",
        ]
        for marker in follow_up_markers:
            if re.search(marker, msg_lower):
                return True

        # Strip conversational prefixes (e.g., "can you please", "could you", "i want to")
        cleaned = re.sub(
            r"^(?:can\s+you\s+|could\s+you\s+|please\s+|i\s+want\s+(?:you\s+)?to\s+|help\s+me\s+)+",
            "",
            msg_lower
        ).strip()

        # 2. Standalone intents that should NOT inherit prior code/tasks
        standalone_starters = [
            # Writing / Letters / Leave applications / Correspondence
            r"^(?:write|draft|compose|prepare|generate)\s+(?:an?\s+)?(?:application|leave\s+application|letter|email|mail|essay|note|resume|cover\s+letter|memo|notice|speech|article|poem|story)\b",
            r"^(?:leave\s+application|sick\s+leave|application\s+for|letter\s+to)\b",
            # Conceptual / Definitions / Explanations (excluding "explain that/it/the code")
            r"^(?:explain|what\s+is|what\s+are|tell\s+me\s+about|overview\s+of|introduce|define)\s+(?!that\b|it\b|this\b|the\s+above|the\s+code)([a-zA-Z0-9_+ -]+)\??$",
            r"^(?:who\s+is|who\s+was|history\s+of)\s+([a-zA-Z0-9_+ -]+)\??$",
            r"^(?:difference\s+between|compare|contrast)\s+([a-zA-Z0-9_+ -]+)\??$",
            r"^how\s+(?:does|do|can)\s+([a-zA-Z0-9_+ -]+)\s+(?:work|function|operate)\??$",
            # Fresh code / implementation starters
            r"^(?:write|create|implement|give\s+me|generate|build|code)\s+(?:a|an)?\s*(?:new\s+)?(?:\w+\s+)?(?:program|code|function|script|class|algorithm|solution)\b",
            r"^(?:implement|code)\s+([a-zA-Z0-9_+ -]+)",
        ]
        for starter in standalone_starters:
            if re.search(starter, cleaned):
                return False

        # Standalone pronouns referring back
        if re.search(r"\b(?:it|above|previous)\b", msg_lower):
            return True

        return True

    # ========================================================
    # PERSONALIZED CHAT WITH CONTEXT & MEMORY
    # ========================================================

    def chat(self, message, history=None):
        try:
            self._ensure_service()
            self._ensure_model()

            # ------------------------------------------------
            # Auto-learn user facts & preferences
            # ------------------------------------------------
            try:
                self.memory.extract_and_learn(message)
            except Exception:
                pass

            # ------------------------------------------------
            # Build personalized system prompt
            # ------------------------------------------------
            system_prompt = self.memory.build_system_prompt()

            # ------------------------------------------------
            # Assemble multi-turn conversation payload
            # ------------------------------------------------
            messages = [{"role": "system", "content": system_prompt}]

            # Only inject history if this query is a follow-up to prior turns
            is_follow_up = self._is_follow_up(message, history)
            if is_follow_up and history:
                for h in history[-8:]:
                    if isinstance(h, dict) and "role" in h and "content" in h:
                        messages.append({
                            "role": h["role"],
                            "content": h["content"]
                        })

            # Add current user prompt
            messages.append({
                "role": "user",
                "content": message
            })

            response = self.client.chat(
                model=self.model,
                messages=messages,
                think=False,
                stream=False,
                options={
                    "num_predict": 2048,  # Ample token limit for complete code
                    "num_ctx": 4096,      # Expanded context window
                    "temperature": 0.2,   # Focused, deterministic, intent-aligned
                },
                keep_alive="30m"
            )

            raw_content = response["message"]["content"]
            # Strip any internal thinking tags if emitted by reasoning models
            cleaned = re.sub(r"<think>.*?</think>", "", raw_content, flags=re.DOTALL).strip()
            return cleaned if cleaned else raw_content

        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"Ollama error: {e}")

    def chat_stream(self, message, history=None):
        response = self.chat(message, history=history)
        if response:
            yield response