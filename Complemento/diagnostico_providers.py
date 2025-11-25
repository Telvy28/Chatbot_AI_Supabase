import os
from dotenv import load_dotenv

load_dotenv()

def test_providers_detallado():
    print("🧪 DIAGNÓSTICO DETALLADO DE PROVIDERS")
    print("=" * 60)
    
    # Test Groq - MUY DETALLADO
    print("\n🔍 ANALIZANDO GROQ...")
    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        models = client.models.list()
        groq_models = [model.id for model in models.data]
        print(f"✅ Groq: Conectado. Total modelos: {len(groq_models)}")
        
        # Mostrar TODOS los modelos disponibles
        print("   Todos los modelos disponibles:")
        for model in sorted(groq_models):
            print(f"     - {model}")
        
        # Probar modelos específicos conocidos
        test_models = [
            "llama3-8b-8192",
            "llama3-70b-8192", 
            "mixtral-8x7b-32768",
            "gemma-7b-it"
        ]
        
        print("\n   Probando modelos específicos:")
        for model in test_models:
            if model in groq_models:
                try:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": "Responde 'OK'"}],
                        max_tokens=5,
                        temperature=0
                    )
                    print(f"     ✅ {model}: FUNCIONA - {response.choices[0].message.content}")
                except Exception as e:
                    error_msg = str(e)
                    if "decommissioned" in error_msg:
                        print(f"     ❌ {model}: DESCONTINUADO")
                    else:
                        print(f"     ⚠️ {model}: Error - {error_msg[:100]}")
            else:
                print(f"     ❌ {model}: NO DISPONIBLE")
                
    except Exception as e:
        print(f"❌ Groq: Error general - {e}")
    
    # Test DeepSeek
    print("\n🔍 ANALIZANDO DEEPSEEK...")
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com"
        )
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "Responde 'OK'"}],
            max_tokens=5
        )
        print(f"✅ DeepSeek: Conectado - {response.choices[0].message.content}")
        
        # Probar function calling
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": "Hola"}],
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "test_function",
                        "description": "Función de prueba",
                        "parameters": {"type": "object", "properties": {}}
                    }
                }],
                max_tokens=50
            )
            print("✅ DeepSeek: Function calling disponible")
        except Exception as e:
            print(f"⚠️ DeepSeek: Function calling error - {e}")
            
    except Exception as e:
        print(f"❌ DeepSeek: Error - {e}")
    
    # Test OpenAI
    print("\n🔍 ANALIZANDO OPENAI...")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        models = client.models.list()
        openai_models = [model.id for model in models.data if 'gpt' in model.id]
        print(f"✅ OpenAI: Conectado. Modelos GPT: {len(openai_models)}")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Responde 'OK'"}],
            max_tokens=5
        )
        print(f"   Test chat: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ OpenAI: Error - {e}")

    print("\n" + "=" * 60)
    print("🎯 MODELOS RECOMENDADOS:")
    print("1. Groq: 'llama3-8b-8192' o 'mixtral-8x7b-32768'")
    print("2. DeepSeek: 'deepseek-chat'")
    print("3. OpenAI: 'gpt-4o-mini'")
    print("=" * 60)

if __name__ == "__main__":
    test_providers_detallado()