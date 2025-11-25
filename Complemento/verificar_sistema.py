#!/usr/bin/env python3
"""
Script de Verificación Rápida - Chatbot Importaciones IA
=========================================================
Ejecuta este script para verificar que todo funciona correctamente.
"""
import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def check_env_vars():
    """Verifica variables de entorno"""
    print("\n🔍 VERIFICANDO VARIABLES DE ENTORNO")
    print("="*50)
    
    required_vars = {
        "SUPABASE_URL": "URL de Supabase",
        "SUPABASE_KEY": "API Key de Supabase", 
        "SUPABASE_CONNECTION_STRING": "String de conexión PostgreSQL",
        "GROQ_API_KEY": "API Key de Groq (opcional)",
        "DEEPSEEK_API_KEY": "API Key de DeepSeek (opcional)",
        "OPENAI_API_KEY": "API Key de OpenAI (opcional)",
        "POWERBI_URL": "URL del Dashboard Power BI (opcional)"
    }
    
    missing = []
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: Configurado")
        else:
            print(f"❌ {var}: NO configurado - {desc}")
            if "opcional" not in desc:
                missing.append(var)
    
    return len(missing) == 0

def check_imports():
    """Verifica que todos los módulos se importen correctamente"""
    print("\n📦 VERIFICANDO IMPORTACIONES")
    print("="*50)
    
    modules = [
        ("streamlit", "Framework web"),
        ("pandas", "Procesamiento de datos"),
        ("supabase", "Cliente Supabase"),
        ("openai", "OpenAI/DeepSeek"),
        ("groq", "Groq API"),
        ("langchain", "LangChain framework"),
        ("psycopg2", "PostgreSQL driver")
    ]
    
    failed = []
    for module, desc in modules:
        try:
            __import__(module)
            print(f"✅ {module}: {desc}")
        except ImportError as e:
            print(f"❌ {module}: {desc} - {e}")
            failed.append(module)
    
    return len(failed) == 0

def test_supabase_connection():
    """Prueba la conexión a Supabase"""
    print("\n🗄️ PROBANDO CONEXIÓN A SUPABASE")
    print("="*50)
    
    try:
        from utils.supabase_client import SupabaseClient
        db = SupabaseClient()
        
        # Probar una consulta simple
        result = db.get_summary_stats()
        if result:
            print(f"✅ Conexión exitosa")
            print(f"   Total registros: {result.get('total_records', 'N/A')}")
            print(f"   Años disponibles: {result.get('years_available', 'N/A')}")
            return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    return False

def test_chatbots():
    """Prueba rápida de los chatbots"""
    print("\n🤖 PROBANDO CHATBOTS")
    print("="*50)
    
    # Test v4.0
    try:
        from utils.chatbot import ImportacionesChatbot
        from utils.supabase_client import SupabaseClient
        
        db = SupabaseClient()
        
        # Probar con Groq primero (gratis)
        if os.getenv("GROQ_API_KEY"):
            bot = ImportacionesChatbot(db, provider="groq")
            response = bot.chat("¿Cuántos registros hay en total?")
            print(f"✅ Chat v4.0 (Groq): Funciona")
        elif os.getenv("OPENAI_API_KEY"):
            bot = ImportacionesChatbot(db, provider="openai")
            print(f"✅ Chat v4.0 (OpenAI): Configurado")
        else:
            print(f"⚠️ Chat v4.0: Sin API keys configuradas")
            
    except Exception as e:
        print(f"❌ Chat v4.0: {e}")
    
    # Test v5.0
    try:
        from utils.langchain_chatbot import LangChainChatbot
        
        if os.getenv("DEEPSEEK_API_KEY"):
            agent = LangChainChatbot(provider="deepseek")
            print(f"✅ Chat v5.0 (DeepSeek): Configurado")
        elif os.getenv("OPENAI_API_KEY"):
            agent = LangChainChatbot(provider="openai")
            print(f"✅ Chat v5.0 (OpenAI): Configurado")
        else:
            print(f"⚠️ Chat v5.0: Sin API keys configuradas")
            
    except Exception as e:
        print(f"❌ Chat v5.0: {e}")

def main():
    """Ejecuta todas las verificaciones"""
    print("\n" + "="*60)
    print("🚀 VERIFICACIÓN DEL SISTEMA - CHATBOT IMPORTACIONES IA")
    print("="*60)
    
    # Verificar todo
    env_ok = check_env_vars()
    imports_ok = check_imports()
    
    if env_ok and imports_ok:
        db_ok = test_supabase_connection()
        if db_ok:
            test_chatbots()
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN FINAL")
    print("="*60)
    
    if env_ok and imports_ok:
        print("✅ Sistema listo para ejecutar")
        print("\n🎯 Para iniciar la aplicación:")
        print("   streamlit run app.py")
    else:
        print("❌ Hay problemas que resolver")
        print("\n📝 Pasos siguientes:")
        print("1. Verifica tu archivo .env")
        print("2. Instala dependencias: pip install -r requirements.txt")
        print("3. Ejecuta este script nuevamente")

if __name__ == "__main__":
    main()
