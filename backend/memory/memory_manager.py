import os
import sqlite3
import re
from datetime import datetime
from pathlib import Path


class MemoryManager:
    """
    Nova Long-Term Personal Memory & Learning Manager.
    Stores and retrieves persistent user facts, preferences, project context,
    and automatic learnings in an SQLite database.
    """

    def __init__(self, db_path=None):
        if db_path is None:
            # Project data/memory path
            project_root = Path(__file__).resolve().parent.parent.parent
            memory_dir = project_root / "data" / "memory"
            memory_dir.mkdir(parents=True, exist_ok=True)
            self.db_path = str(memory_dir / "nova_memory.db")
        else:
            self.db_path = str(db_path)

        self._init_db()
        self._init_default_profile()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Table for personal memories / learned facts
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL UNIQUE,
                    importance INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Table for key-value user profile
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profile (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def _init_default_profile(self):
        defaults = {
            "user_name": "Yuvraj",
            "assistant_name": "Nova",
            "primary_os": "Windows 11",
            "developer_role": "Software Engineer & Creator of Nova",
            "preferred_languages": "C++, Python",
            "tone_preference": "Concise, highly technical, intelligent, and proactive",
        }
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for key, val in defaults.items():
                cursor.execute("""
                    INSERT OR IGNORE INTO user_profile (key, value)
                    VALUES (?, ?)
                """, (key, val))
            conn.commit()

    # ========================================================
    # PROFILE MANAGEMENT
    # ========================================================

    def get_profile(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT key, value FROM user_profile")
            return {row[0]: row[1] for row in cursor.fetchall()}

    def set_profile_value(self, key, value):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_profile (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = CURRENT_TIMESTAMP
            """, (key, value))
            conn.commit()

    # ========================================================
    # MEMORY CRUD
    # ========================================================

    def add_memory(self, content, category="general", importance=1):
        content = content.strip()
        if not content:
            return None

        with self._get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO memories (category, content, importance)
                    VALUES (?, ?, ?)
                """, (category, content, importance))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # Already remembered
                cursor.execute("SELECT id FROM memories WHERE content = ?", (content,))
                row = cursor.fetchone()
                return row[0] if row else None

    def get_memories(self, limit=50):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, category, content, importance, created_at
                FROM memories
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [
                {
                    "id": r[0],
                    "category": r[1],
                    "content": r[2],
                    "importance": r[3],
                    "created_at": r[4],
                }
                for r in rows
            ]

    def delete_memory(self, memory_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_memory_count(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM memories")
            return cursor.fetchone()[0]

    # ========================================================
    # AUTO-LEARNING EXTRACTION
    # Automatically extracts facts, preferences, and details
    # from natural user conversation
    # ========================================================

    def extract_and_learn(self, text):
        """
        Analyzes user input and automatically registers facts into long-term memory.
        """
        cleaned = text.strip()
        learned = []

        patterns = [
            # "remember that X" or "note that X"
            (r"\b(?:remember\s+that|note\s+that|remember)\s+(.+)", "instruction"),
            # "I prefer X" or "I like X"
            (r"\b(?:i\s+prefer|i\s+like|i\s+love|my\s+favorite\s+\w+\s+is)\s+(.+)", "preference"),
            # "I am working on X"
            (r"\b(?:i\s+am\s+working\s+on|i'm\s+working\s+on|my\s+project\s+is)\s+(.+)", "project"),
            # "My name is X" or "Call me X"
            (r"\b(?:my\s+name\s+is|call\s+me)\s+([A-Za-z]+)", "identity"),
        ]

        for pat, cat in patterns:
            match = re.search(pat, cleaned, re.IGNORECASE)
            if match:
                fact = match.group(1).strip()
                # Clean trailing punctuation
                fact = re.sub(r"[.?!]+$", "", fact).strip()
                if len(fact) > 3 and not fact.lower().startswith("what"):
                    if cat == "identity":
                        self.set_profile_value("user_name", fact.capitalize())
                        mem_content = f"User's name is {fact.capitalize()}."
                    elif cat == "preference":
                        mem_content = f"User preference: prefers {fact}."
                    elif cat == "project":
                        mem_content = f"Active project: {fact}."
                    else:
                        mem_content = fact

                    mem_id = self.add_memory(mem_content, category=cat, importance=2)
                    if mem_id:
                        learned.append(mem_content)

        return learned

    # ========================================================
    # SYSTEM PROMPT BUILDER
    # Injects user profile & memories into the LLM context
    # ========================================================

    def build_system_prompt(self):
        profile = self.get_profile()
        memories = self.get_memories(limit=15)

        user_name = profile.get("user_name", "Yuvraj")
        role = profile.get("developer_role", "Developer")
        pref_langs = profile.get("preferred_languages", "C++, Python")

        now = datetime.now()
        current_date_str = now.strftime("%A, %B %d, %Y")
        current_year = str(now.year)
        current_time_str = now.strftime("%I:%M %p")

        memory_lines = ""
        if memories:
            memory_lines = "\n".join(f"- {m['content']}" for m in memories)
        else:
            memory_lines = "- User is working on desktop AI automation with Nova."

        system_prompt = f"""You are Nova, an elite, highly intelligent, personalized AI engineer and personal assistant created for {user_name}.
You operate as a native desktop AI running completely locally on {user_name}'s PC.

## USER PROFILE & PERSONAL CONTEXT:
- User Name: {user_name} ({role})
- Preferred Languages: {pref_langs}
- Operating System: Windows 11

## SYSTEM ENVIRONMENT & REAL-TIME CLOCK:
- Current Date: {current_date_str}
- Current Year: {current_year}
- Current Time: {current_time_str}

## WHAT YOU REMEMBER ABOUT {user_name.upper()}:
{memory_lines}

## CORE CAPABILITIES & RESPONSE GUIDELINES:
1. **Accurately Respect User Intent**:
   - **Real-Time Temporal Grounding**:
     The current year is {current_year}, and today's date is {current_date_str}.
     When asked for the date, year, or time, always state the real-time system values ({current_date_str}, Year {current_year}).
     NEVER state that the year is 2023 or any outdated training cutoff year.
   - **Writing, Letters & Formal Applications** (e.g., "write an application for leave", "leave application for school/work", "draft an email", "write a letter", "job application"):
     CRITICAL: In requests like "application for leave", "sick leave application", or "school application", the word "application" refers to a FORMAL WRITTEN LETTER or petition, NOT a software program!
     Provide a polished, properly formatted formal letter or application with Date, Subject, Salutation, Body, and Sign-off.
     NEVER output C++, Python, or any programming code for letters, leave requests, essays, or emails.
   - **Explanations & Conceptual Questions** (e.g., "Explain Python", "What is multithreading?", "How does memory management work in C++?"):
     Provide a clear, well-structured, insightful explanation in text covering what the technology is, its core philosophy, key characteristics, syntax highlights, and pros/cons. Do NOT generate an unsolicited programming task or replace an explanation with random code.
   - **Code Requests** (e.g., "Write code for...", "Implement...", "Give me code..."):
     Provide complete, production-grade, working code in standard markdown code blocks (```cpp, ```python, etc.) with clean explanations.
   - **Conversational Queries**:
     Answer concisely, directly, and intelligently.

2. **Topic Independence & No Context Leakage**:
   - Each prompt is evaluated on its own merits. Never carry over or repeat exercises, tasks, or code examples from previous turns into new conceptual questions unless the user explicitly asks to continue or convert that exact task.
   - "Explain Python" means explain the Python programming language itself.
   - "write an application for leave" means write a formal leave application letter.

## EXAMPLES OF INTENT:
[Example 1 - Coding Request]
User: Write a C++ function to check if a number is prime
Assistant: Here is the C++ function:
```cpp
bool is_prime(int n) {{
    if (n <= 1) return false;
    for (int i = 2; i * i <= n; ++i) {{
        if (n % i == 0) return false;
    }}
    return true;
}}
```

[Example 2 - Conceptual Request]
User: Explain Python
Assistant: Python is a high-level, general-purpose programming language renowned for its clear syntax and developer productivity.

### Core Philosophy:
Python prioritizes human readability, famously summarized in *The Zen of Python* ("Readability counts", "Simple is better than complex").

### Key Characteristics:
- **Clean Syntax**: Employs whitespace indentation to define code blocks instead of curly braces.
- **Dynamically Typed & Interpreted**: Variables do not require explicit type declarations, and code is executed line-by-line via the Python Virtual Machine.
- **Rich Standard Library**: Ships "batteries included" with built-in support for OS operations, networking, mathematics, and data structures.
- **Ecosystem**: Dominant in machine learning, data engineering, web backends, and scripting.

[Example 3 - Formal Letter / Application Request]
User: write a application for leave for 5 days from my school
Assistant: Here is a formal leave application letter for your school:

**To:**  
The Principal,  
[School Name],  
[City]  

**Date:** {current_date_str}  

**Subject: Application for 5 Days Leave of Absence**  

Respected Principal,  

I am writing to respectfully request leave of absence for five days, from [Start Date] to [End Date], due to [Reason, e.g., an urgent family matter / illness].  

I will ensure that I complete all missed classroom assignments and notes upon my return. I kindly request you to grant me leave for these days.  

Thanking you.  

Yours obediently,  
**{user_name}**  
Class: [Class / Grade]  
Roll No: [Roll Number]

3. **Tone & Style**:
   - Address {user_name} warmly, directly, and professionally.
   - Be concise, clear, and technically sharp. Avoid unnecessary fluff or robotic disclaimers.

4. **Desktop Agent Awareness**:
   - You are integrated into the Nova desktop application, which can find files, open downloads, and control media playback.
   - You are synchronized with {user_name}'s live PC system clock: today is {current_date_str}, Year {current_year}.
"""
        return system_prompt
