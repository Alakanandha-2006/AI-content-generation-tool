from google import genai
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Read API key
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("❌ GEMINI_API_KEY not found in .env file")
    exit()

print("✅ API Key Loaded Successfully\n")

# Create Gemini client
client = genai.Client(api_key=API_KEY)

print("=" * 80)
print("AVAILABLE GEMINI MODELS")
print("=" * 80)

try:
    for model in client.models.list():

        print(f"Model Name : {model.name}")

        # Display supported actions if available
        if hasattr(model, "supported_actions"):
            print("Supported Actions:")
            for action in model.supported_actions:
                print(f"   - {action}")

        # Print complete model information
        print("\nFull Model Details:")
        print(model)

        print("-" * 80)

except Exception as e:
    print("\n❌ Error while fetching models")
    print(e)