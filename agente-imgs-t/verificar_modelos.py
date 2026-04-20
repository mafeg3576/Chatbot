# verificar_modelos.py
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

try:
    # Listar modelos disponibles
    models = client.models.list()
    print("✅ Modelos disponibles en TU cuenta:")
    print("-" * 40)
    for model in models.data:
        print(f"  • {model.id}")
except Exception as e:
    print(f"❌ Error: {e}")