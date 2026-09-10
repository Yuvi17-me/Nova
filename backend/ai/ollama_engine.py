import ollama


class OllamaEngine:

    def __init__(self, model="qwen3:1.7b"):

        self.model = model

    # ========================================================
    # NORMAL CHAT
    # Used for simple tests and non-streaming requests
    # ========================================================

    def chat(self, message):

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            think=False,
            options={
                "num_predict": 128,
                "num_ctx": 2048,
            },
            keep_alive="30m"
        )

        return response["message"]["content"]

    # ========================================================
    # STREAMING CHAT
    # Used by the ChatPage for live responses
    # ========================================================

    def chat_stream(self, message):

        stream = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            stream=True,
            think=False,
            options={
                "num_predict": 128,
                "num_ctx": 2048,
            },
            keep_alive="30m"
        )

        for chunk in stream:

            content = chunk["message"].get(
                "content",
                ""
            )

            if content:
                yield content