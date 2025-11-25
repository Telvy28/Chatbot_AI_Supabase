"""
Script de Diagnóstico - Chatbot Importaciones v5.0
Ejecuta esto para verificar tu entorno antes de correr la app
"""

import sys

def check_python_version():
    print("\n🐍 PYTHON VERSION")
    print(f"   Versión: {sys.version}")
    if sys.version_info >= (3, 9) and sys.version_info < (3, 12):
        print("   ✅ Compatible")
    else:
        print("   ⚠️  Recomendado: Python 3.9-3.11")

def check_packages():
    print("\n📦 PACKAGES")
    packages = {
        'streamlit': '1.31.0',
        'langchain': '0.1.4',
        'langchain_openai': '0.0.5',
        'langchain_community': '0.0.16',
        'openai': '1.10.0',
        'supabase': '2.3.4',
        'pandas': '2.1.4'
    }
    
    for package, expected_version in packages.items():
        try:
            if package == 'langchain_openai':
                import langchain_openai
                version = langchain_openai.__version__
            elif package == 'langchain_community':
                import langchain_community
                version = langchain_community.__version__
            else:
                pkg = __import__(package)
                version = pkg.__version__
            
            status = "✅" if version == expected_version else "⚠️"
            print(f"   {status} {package}: {version} (esperado: {expected_version})")
        except ImportError:
            print(f"   ❌ {package}: NO INSTALADO")
        except AttributeError:
            print(f"   ⚠️  {package}: Instalado (versión no detectable)")

def check_env_file():
    print("\n🔑 VARIABLES DE ENTORNO")
    try:
        from dotenv import load_dotenv
        import os
        load_dotenv()
        
        vars_to_check = [
            ('SUPABASE_URL', False),
            ('SUPABASE_KEY', False),
            ('TABLE_NAME', False),
            ('SUPABASE_CONNECTION_STRING', True),  # Opcional para v5.0
            ('OPENAI_API_KEY', False)
        ]
        
        for var, optional in vars_to_check:
            value = os.getenv(var)
            if value:
                masked = value[:10] + "..." if len(value) > 10 else value
                print(f"   ✅ {var}: {masked}")
            else:
                status = "⚠️" if optional else "❌"
                note = " (Opcional para v5.0)" if optional else " (REQUERIDO)"
                print(f"   {status} {var}: NO CONFIGURADO{note}")
    except Exception as e:
        print(f"   ❌ Error al cargar .env: {e}")

def check_files():
    print("\n📂 ESTRUCTURA DE ARCHIVOS")
    import os
    
    required_files = [
        'app.py',
        'requirements.txt',
        '.env',
        'utils/__init__.py',
        'utils/supabase_client.py',
        'utils/langchain_chatbot.py',
        'utils/chatbot.py'  # Crítico para v4.0
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            critical = " ⚠️  CRÍTICO!" if file == 'utils/chatbot.py' else ""
            print(f"   ❌ {file}{critical}")

def test_imports():
    print("\n🧪 TEST DE IMPORTS CRÍTICOS")
    
    tests = [
        ("Streamlit", "import streamlit as st"),
        ("LangChain", "from langchain_community.utilities import SQLDatabase"),
        ("LangChain OpenAI", "from langchain_openai import ChatOpenAI"),
        ("OpenAI", "import openai"),
        ("Supabase", "from supabase import create_client"),
        ("Pandas", "import pandas as pd")
    ]
    
    for name, import_stmt in tests:
        try:
            exec(import_stmt)
            print(f"   ✅ {name}")
        except Exception as e:
            print(f"   ❌ {name}: {str(e)[:50]}")

def main():
    print("="*60)
    print("🔍 DIAGNÓSTICO DEL ENTORNO - Chatbot Importaciones v5.0")
    print("="*60)
    
    check_python_version()
    check_packages()
    check_env_file()
    check_files()
    test_imports()
    
    print("\n" + "="*60)
    print("📊 RESUMEN")
    print("="*60)
    print("""
Si ves:
✅ Todo verde → Ejecuta: streamlit run app.py
⚠️  Amarillo → Revisa versiones pero debería funcionar
❌ Rojo → Instala faltantes: pip install -r requirements.txt

Si falta utils/chatbot.py:
- Chat v4.0 NO funcionará
- Chat v5.0 (LangChain) SÍ funcionará
    """)

if __name__ == "__main__":
    main()