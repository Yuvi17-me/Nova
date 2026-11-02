# ✨ NOVA AI – Local AI Desktop Assistant

### Your Desktop. Your Data. Your AI.

A privacy-focused AI desktop assistant that combines local AI conversations, desktop automation, file management, and personalized memory in one application.

---

## 🚀 About NOVA AI

**NOVA AI** is a Python-based desktop AI assistant designed to make everyday computer interactions easier through natural language commands.

It integrates a locally running Large Language Model (LLM) with desktop automation tools, allowing users to interact with AI, search and open files, launch applications, access websites, and perform supported system operations.

Unlike cloud-dependent AI assistants, NOVA AI uses **Ollama** to run AI models locally, reducing the need to send conversational data to external AI services.

The project is built using Python and PySide6 with a modular architecture that separates the user interface, AI engine, automation, and memory management.

## 🌟 Features

| Feature | Description |
|---|---|
| 🤖 Local AI Chat | Interact with a locally running AI model. |
| ⚙️ Desktop Automation | Open applications, websites, and perform supported system operations. |
| 📁 File Management | Search for and open files from supported directories. |
| 🧠 Personalized Memory | Store and use user preferences and context locally. |
| 🖥️ Desktop Interface | Modern interface with dedicated application pages. |
| 🔒 Privacy Focus | Run core AI inference locally using Ollama. |

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| PySide6 | Desktop application interface |
| Ollama | Local AI model runtime |
| Qwen3:1.7B | Language model |
| SQLite | Local memory storage |
| Git & GitHub | Version control |

## 🏗️ System Architecture

NOVA AI follows a modular architecture where different components work together to understand commands and perform tasks.

```text
                 USER
                   |
                   v
          PySide6 Desktop UI
                   |
                   v
               Agent Core
                   |
          +--------+--------+
          |        |        |
          v        v        v
        AI Chat  FileTools SystemTools
          |        |        |
          +--------+--------+
                   |
                   v
              Ollama Engine
                   |
                   v
               Qwen3:1.7B
                   |
                   v
             AI Response
```

### Core Modules

- **Frontend:** Handles the graphical interface and user interaction.
- **Agent Core:** Processes commands and coordinates operations.
- **Ollama Engine:** Connects the application with the local AI model.
- **FileTools:** Handles supported file search and opening operations.
- **Memory Manager:** Stores and manages user context and preferences.
- **System Tools:** Handles supported desktop automation tasks.

## 💻 Installation & Setup

Follow these steps to run NOVA AI on your Windows machine.

### 1. Prerequisites

Make sure you have installed:

- Python 3.11 or a compatible version
- Git
- Ollama

### 2. Clone the Repository

```bash
git clone https://github.com/Yuvi17-me/Nova.git
```

```bash
cd Nova
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Environment

For Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Download the AI Model

Make sure Ollama is installed and run:

```bash
ollama pull qwen3:1.7b
```

### 7. Launch NOVA AI

```bash
python launcher.py
```

The desktop application should now start.

## 📂 Project Structure

```text
Nova/
│
├── backend/
│   ├── agent/
│   │   ├── agent_core.py
│   │   ├── file_tools.py
│   │   └── test_agent.py
│   │
│   ├── ai/
│   │   └── ollama_engine.py
│   │
│   └── memory/
│       └── memory_manager.py
│
├── frontend/
│   ├── components/
│   ├── chat_page.py
│   ├── documents_page.py
│   ├── home_page.py
│   ├── main_window.py
│   ├── memory_page.py
│   ├── settings_page.py
│   ├── sidebar.py
│   └── styles.py
│
├── configs/
├── data/
├── folders/
│
├── launcher.py
├── requirements.txt
├── .gitignore
└── Readme.md
```

## 🎯 Project Objectives

- Develop a privacy-focused local AI desktop assistant.
- Integrate a locally hosted language model with a desktop application.
- Enable natural language-based desktop interaction.
- Simplify file searching and application access.
- Explore practical applications of AI and desktop automation.

## 🔮 Future Scope

Some planned improvements include:

- Improved natural language understanding.
- More advanced desktop automation.
- Enhanced document reading and analysis.
- Better long-term memory and personalization.
- Voice-based interaction.
- Improved response speed and performance.
- Support for additional local AI models.

## 🔐 Privacy & Security

NOVA AI follows a local-first approach for its core AI processing.

- AI inference is performed through Ollama on the local machine.
- Local memory information is stored on the user's system.
- Cloud AI services are not required for core model inference.
- Sensitive configuration files and local runtime databases should remain excluded from public repositories.

## 👨‍💻 Project Information

**Project:** NOVA AI – Local AI Desktop Assistant

**Category:** Artificial Intelligence / Desktop Automation

**Language:** Python

**Repository:** [GitHub – NOVA AI](https://github.com/Yuvi17-me/Nova)

---

### Built with Python, Ollama & AI ❤️

*Your Desktop. Your Data. Your AI.*