import os
import sys
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

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key or api_key.strip("'\" \t\r\n") == "" or "YOUR_" in api_key.upper():
    print("\n[-] Notice: No GEMINI_API_KEY found in backend/.env.")
    print("    Paste your key on line 4 of backend/.env:")
    print("    GEMINI_API_KEY=AIzaSy...")
    print("    Then re-run this script: python test_gemini.py\n")
    sys.exit(0)

api_key = api_key.strip("'\" \t\r\n")
configured_model = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash").strip("'\" \t\r\n")
if any(legacy in configured_model for legacy in ["1.5", "2.0", "2.5", "3.1"]):
    configured_model = "gemini-3.8-flash"
print(f"[*] Loaded API Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 8 else ''}")
print(f"[*] Configured Model: {configured_model}")

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("[-] Error: google-genai library not installed. Run: pip install google-genai")
    sys.exit(1)

def test_model(model_name: str) -> bool:
    print(f"\n[*] Testing Gemini connection with model: '{model_name}'...")
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents="Respond with only the single word: SUCCESS"
        )
        output = (response.text or "").strip()
        print(f"[+] Model '{model_name}' Success! Response: {output}")
        return True
    except Exception as e:
        print(f"[-] Model '{model_name}' Failed: {e}")
        return False

# Test configured model and modern fallback models
success = False
models_to_test = [configured_model]
for fallback in ["gemini-3.8-flash", "gemini-flash-latest", "gemini-4-hydrogen"]:
    if fallback not in models_to_test:
        models_to_test.append(fallback)

for m in models_to_test:
    if test_model(m):
        success = True
        break

print("\n========================================================")
print("DIAGNOSTIC ANALYSIS")
print("========================================================")

if success:
    print("[+] Status: Your Gemini API key is VALID and working!")
    print("[+] Action: Aera will now dynamically use this key to generate real responses.")
else:
    print("[-] Status: API key validation failed.")
    print("\nTroubleshooting tips:")
    print("1. Did you copy the key from https://aistudio.google.com/?")
    print("   -> In Google AI Studio, click 'Get API key', create/select a project, and copy the key.")
    print("2. Ensure there are no surrounding quotes, spaces, or placeholder strings.")
    print("3. Check that the 'Generative Language API' is enabled and unrestricted.")

print("========================================================\n")
