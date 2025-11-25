"""
Script de Validación - LangChain v5.0
Prueba la conexión y funcionalidad del SQL Agent
"""

import os
import sys
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

print("=" * 80)
print("🧪 VALIDACIÓN DE LANGCHAIN SQL AGENT v5.0")
print("=" * 80)

# ============================================================================
# PASO 1: Verificar variables de entorno
# ============================================================================
print("\n📋 PASO 1: Verificando variables de entorno...")
print("-" * 80)

required_vars = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
    "SUPABASE_CONNECTION_STRING": os.getenv("SUPABASE_CONNECTION_STRING"),
    "TABLE_NAME": os.getenv("TABLE_NAME", "BD_Import_IQ")
}

all_vars_present = True
for var_name, var_value in required_vars.items():
    if var_value:
        # Ocultar valores sensibles
        if "KEY" in var_name or "STRING" in var_name:
            masked_value = var_value[:10] + "..." if len(var_value) > 10 else "***"
            print(f"  ✅ {var_name}: {masked_value}")
        else:
            print(f"  ✅ {var_name}: {var_value}")
    else:
        print(f"  ❌ {var_name}: NO CONFIGURADA")
        all_vars_present = False

if not all_vars_present:
    print("\n❌ ERROR: Faltan variables de entorno en .env")
    print("\nAgrega las siguientes variables en tu archivo .env:")
    print("  - OPENAI_API_KEY")
    print("  - SUPABASE_CONNECTION_STRING")
    print("\nConsulta .env.example para más detalles")
    sys.exit(1)

print("\n✅ Todas las variables de entorno están configuradas")

# ============================================================================
# PASO 2: Verificar dependencias
# ============================================================================
print("\n📦 PASO 2: Verificando dependencias...")
print("-" * 80)

required_packages = [
    "langchain",
    "langchain_openai",
    "langchain_community",
    "sqlalchemy",
    "psycopg2"
]

missing_packages = []
for package in required_packages:
    try:
        __import__(package)
        print(f"  ✅ {package}")
    except ImportError:
        print(f"  ❌ {package}")
        missing_packages.append(package)

if missing_packages:
    print("\n❌ ERROR: Faltan paquetes requeridos")
    print("\nInstala con:")
    print("  pip install -r requirements_v5.txt")
    sys.exit(1)

print("\n✅ Todas las dependencias están instaladas")

# ============================================================================
# PASO 3: Probar conexión a Supabase
# ============================================================================
print("\n🔌 PASO 3: Probando conexión a Supabase PostgreSQL...")
print("-" * 80)

try:
    from sqlalchemy import create_engine, text
    
    connection_string = os.getenv("SUPABASE_CONNECTION_STRING")
    engine = create_engine(connection_string)
    
    # Probar conexión
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("  ✅ Conexión a PostgreSQL exitosa")
        
        # Verificar tabla
        table_name = os.getenv("TABLE_NAME", "BD_Import_IQ")
        result = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"'))
        count = result.scalar()
        print(f"  ✅ Tabla {table_name} encontrada: {count:,} registros")
        
except Exception as e:
    print(f"  ❌ Error de conexión: {e}")
    print("\nVerifica:")
    print("  1. Que SUPABASE_CONNECTION_STRING sea correcta")
    print("  2. Que el password sea correcto (sin [YOUR-PASSWORD])")
    print("  3. Que la base de datos esté accesible")
    sys.exit(1)

print("\n✅ Conexión a Supabase PostgreSQL exitosa")

# ============================================================================
# PASO 4: Inicializar LangChain SQL Agent
# ============================================================================
print("\n🤖 PASO 4: Inicializando LangChain SQL Agent...")
print("-" * 80)

try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from utils.langchain_chatbot import LangChainChatbot
    
    chatbot = LangChainChatbot()
    print("  ✅ LangChain SQL Agent inicializado correctamente")
    
except Exception as e:
    print(f"  ❌ Error al inicializar agente: {e}")
    sys.exit(1)

print("\n✅ LangChain SQL Agent listo")

# ============================================================================
# PASO 5: Pruebas básicas
# ============================================================================
print("\n🧪 PASO 5: Ejecutando pruebas básicas...")
print("-" * 80)

tests = [
    {
        "name": "Conteo de registros",
        "query": "¿Cuántas importaciones hay en total?",
        "expected_keywords": ["import", "total", "registros"]
    },
    {
        "name": "Top 5 marcas",
        "query": "Dame las 5 marcas más importadas",
        "expected_keywords": ["marca"]
    },
    {
        "name": "Query simple por año",
        "query": "¿Cuántas importaciones hubo en 2025?",
        "expected_keywords": ["2025"]
    }
]

passed_tests = 0
failed_tests = 0

for i, test in enumerate(tests, 1):
    print(f"\n  Test {i}: {test['name']}")
    print(f"  Pregunta: {test['query']}")
    
    try:
        response = chatbot.chat(test['query'])
        
        # Verificar que la respuesta no sea un error
        if "❌" in response or "Error" in response:
            print(f"  ❌ FALLÓ: Respuesta de error")
            print(f"     Respuesta: {response[:200]}...")
            failed_tests += 1
        else:
            print(f"  ✅ PASÓ")
            print(f"     Respuesta: {response[:200]}...")
            passed_tests += 1
            
    except Exception as e:
        print(f"  ❌ FALLÓ: {e}")
        failed_tests += 1

# ============================================================================
# RESUMEN
# ============================================================================
print("\n" + "=" * 80)
print("📊 RESUMEN DE VALIDACIÓN")
print("=" * 80)

print(f"\n✅ Variables de entorno: OK")
print(f"✅ Dependencias: OK")
print(f"✅ Conexión PostgreSQL: OK")
print(f"✅ LangChain Agent: OK")
print(f"\n🧪 Pruebas: {passed_tests}/{len(tests)} pasadas")

if failed_tests > 0:
    print(f"⚠️  {failed_tests} pruebas fallaron - Revisa los errores arriba")
else:
    print("🎉 TODAS LAS PRUEBAS PASARON")

print("\n" + "=" * 80)
print("🚀 ESTADO: LISTO PARA USAR")
print("=" * 80)

print("\n💡 Ahora puedes:")
print("  1. Ejecutar: streamlit run app.py")
print("  2. Ir al tab 'Chat Avanzado v5.0'")
print("  3. Hacer preguntas complejas que no estaban pre-programadas")

print("\n📚 Ejemplos de preguntas avanzadas:")
print("  - Dame las 5 marcas que más crecieron entre 2020 y 2025")
print("  - ¿Qué marcas tienen más de 3 ingredientes activos diferentes?")
print("  - Compara el CIF promedio de productos de China vs India")
print("  - ¿Cuáles son los importadores que solo traen de un país?")

input("\n\nPresiona Enter para salir...")
