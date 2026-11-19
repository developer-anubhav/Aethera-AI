import os
import sys
import time
from dotenv import load_dotenv

# Resolve paths
backend_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(backend_dir)
env_path = os.path.join(backend_dir, ".env")
root_env = os.path.join(root_dir, ".env")

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path, override=True)
elif os.path.exists(root_env):
    load_dotenv(dotenv_path=root_env, override=True)

api_key = os.environ.get("GROQ_API_KEY")
if not api_key or api_key.strip("'\" \t\r\n") == "" or "YOUR_" in api_key.upper():
    print("\n[-] Notice: No GROQ_API_KEY found in backend/.env.")
    print("    1. Go to https://console.groq.com/keys and create your free key (starts with 'gsk_').")
    print("    2. Open backend/.env and paste it on line 8:")
    print("       GROQ_API_KEY=gsk_...")
    print("    3. Then re-run this script: python backend/test_groq.py\n")
    sys.exit(0)

api_key = api_key.strip("'\" \t\r\n")
configured_model = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b").strip("'\" \t\r\n")
print(f"[*] Loaded Groq API Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 8 else ''}")
print(f"[*] Configured Model: {configured_model}")

try:
    from groq import Groq
except ImportError:
    print("[-] Error: groq library not installed. Run: pip install groq")
    sys.exit(1)

def test_groq_model(model_name: str) -> bool:
    print(f"\n[*] Testing Groq connection with model: '{model_name}'...")
    try:
        client = Groq(api_key=api_key)
        start = time.time()
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a scientific test assistant."},
                {"role": "user", "content": "Respond with only the single word: SUCCESS"}
            ],
            temperature=0.2,
            max_tokens=20
        )
        elapsed_ms = int((time.time() - start) * 1000)
        output = (completion.choices[0].message.content or "").strip()
        print(f"[+] Model '{model_name}' Success in {elapsed_ms}ms! Response: {output}")
        return True
    except Exception as e:
        print(f"[-] Model '{model_name}' Failed: {e}")
        return False

# Test configured model and modern fallback models
success = False
models_to_test = [configured_model]
for fallback in ["openai/gpt-oss-120b", "qwen/qwen3.8-27b", "openai/gpt-oss-20b"]:
    if fallback not in models_to_test:
        models_to_test.append(fallback)

for m in models_to_test:
    if test_groq_model(m):
        success = True
        break

print("\n========================================================")
print("DIAGNOSTIC ANALYSIS")
print("========================================================")

if success:
    print("[+] Status: Your Groq API key is VALID and working!")
    print("[+] Action: Aera AI will stream at lightning speed without 503 errors.")
else:
    print("[-] Status: Groq validation failed.")
    print("\nTroubleshooting tips:")
    print("1. Did you copy the key from https://console.groq.com/keys?")
    print("2. Ensure the key begins with 'gsk_' without quotes or whitespace.")

print("========================================================\n")
