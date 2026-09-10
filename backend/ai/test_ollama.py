from ollama_engine import OllamaEngine


engine = OllamaEngine()

response = engine.chat("Say hello to me in one short sentence.")

print("\nNova AI:")
print(response)