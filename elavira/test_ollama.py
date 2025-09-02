import os
import subprocess

# --- Ajouter le chemin vers Ollama au PATH (Apple Silicon) ---
ollama_path = "/opt/homebrew/bin"
if ollama_path not in os.environ["PATH"]:
    os.environ["PATH"] += os.pathsep + ollama_path

OLLAMA_BIN = os.path.join(ollama_path, "ollama")

# --- Test de l'accessibilité d'Ollama ---
try:
    result = subprocess.run([OLLAMA_BIN, "list"], capture_output=True, text=True, check=True)
    print("✅ Ollama accessible depuis Python :\n", result.stdout)
except FileNotFoundError:
    print("❌ Ollama introuvable : vérifie le chemin.")
except subprocess.CalledProcessError as e:
    print("❌ Erreur lors de l'appel à Ollama :", e.stderr)
except Exception as e:
    print("❌ Erreur inattendue :", e)
