import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

def cargar_datos_a_supabase(ruta_excel):
    """
    Carga datos desde un archivo Excel a Supabase
    """
    print("=" * 60)
    print("🚀 CARGANDO DATOS A SUPABASE")
    print("=" * 60)
    
    # Conectar a Supabase
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    table_name = os.getenv("TABLE_NAME", "importaciones")
    
    if not url or not key:
        print("❌ Error: Configura SUPABASE_URL y SUPABASE_KEY en .env")
        return
    
    client = create_client(url, key)
    print(f"✅ Conectado a Supabase")
    print(f"📋 Tabla destino: {table_name}")
    
    # Leer Excel
    try:
        # Primero ver las hojas disponibles
        excel_file = pd.ExcelFile(ruta_excel)
        hojas = excel_file.sheet_names
        
        print(f"\n📂 Archivo: {ruta_excel}")
        print(f"📋 Hojas disponibles: {hojas}")
        
        # Seleccionar hoja
        if len(hojas) > 1:
            print(f"\n¿Qué hoja deseas cargar?")
            for i, hoja in enumerate(hojas, 1):
                print(f"  {i}. {hoja}")
            hoja_num = input(f"\nIngresa el número (1-{len(hojas)}) o presiona Enter para usar la hoja 1: ").strip()
            hoja_index = int(hoja_num) - 1 if hoja_num else 0
            hoja_seleccionada = hojas[hoja_index]
        else:
            hoja_seleccionada = hojas[0]
        
        print(f"\n📄 Cargando hoja: {hoja_seleccionada}")
        df = pd.read_excel(ruta_excel, sheet_name=hoja_seleccionada)
        
        print(f"📊 Total de registros: {len(df)}")
        print(f"📋 Columnas: {len(df.columns)}")
        print(f"\nColumnas encontradas:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        # Mostrar preview de primeras filas
        print("\n📋 Preview de primeros 3 registros:")
        print(df.head(3).to_string())
        
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return
    
    # Convertir fechas a string ISO
    if 'Fecha' in df.columns:
        df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    # Limpiar datos: Reemplazar NaN, inf, -inf con None
    print("\n🧹 Limpiando datos (NaN, inf, -inf → NULL)...")
    
    # Reemplazar infinitos con NaN primero
    df = df.replace([float('inf'), float('-inf')], pd.NA)
    
    # Convertir NaN a None de forma más robusta
    df = df.astype(object).where(pd.notnull(df), None)
    
    # Verificar columnas numéricas y limpiar
    for col in df.columns:
        if df[col].dtype == 'float64' or df[col].dtype == 'int64':
            df[col] = df[col].apply(lambda x: None if pd.isna(x) or x == float('inf') or x == float('-inf') else x)
    
    print("✅ Datos limpiados")
    
    # Validar datos antes de continuar
    print("\n" + "=" * 60)
    print("🔍 VALIDACIÓN DE DATOS")
    print("=" * 60)
    
    # Contar valores nulos por columna
    nulos_por_columna = df.isnull().sum()
    if nulos_por_columna.sum() > 0:
        print(f"⚠️  Se encontraron {nulos_por_columna.sum()} valores nulos en total:")
        for col, count in nulos_por_columna[nulos_por_columna > 0].items():
            print(f"   - {col}: {count} nulos")
    else:
        print("✅ No hay valores nulos")
    
    # Preguntar si desea continuar
    print("\n" + "=" * 60)
    continuar = input("¿Deseas continuar con la carga? (S/N): ").strip().upper()
    if continuar != 'S':
        print("❌ Carga cancelada por el usuario")
        return
    
    # Preguntar si desea limpiar la tabla primero
    print("\n" + "=" * 60)
    respuesta = input("¿Deseas ELIMINAR los datos existentes antes de cargar? (S/N): ").strip().upper()
    
    if respuesta == 'S':
        try:
            # Eliminar todos los registros
            client.table(table_name).delete().neq('ID', -999999).execute()
            print("🗑️  Datos existentes eliminados")
        except Exception as e:
            print(f"⚠️  Advertencia al limpiar: {e}")
    
    # Cargar datos en lotes
    batch_size = 500
    total_registros = len(df)
    registros_cargados = 0
    errores = 0
    registros_con_error = []
    
    print(f"\n🔄 Iniciando carga en lotes de {batch_size}...")
    print("=" * 60)
    
    for i in range(0, total_registros, batch_size):
        batch = df.iloc[i:i+batch_size]
        batch_data = batch.to_dict('records')
        
        try:
            response = client.table(table_name).insert(batch_data).execute()
            registros_cargados += len(batch_data)
            progreso = (registros_cargados / total_registros) * 100
            print(f"✅ Lote {i//batch_size + 1}: {len(batch_data)} registros | Progreso: {progreso:.1f}%")
        except Exception as e:
            errores += len(batch_data)
            print(f"❌ Error en lote {i//batch_size + 1}: {e}")
            
            # Guardar registros con error para análisis
            for registro in batch_data:
                registros_con_error.append(registro)
    
    # Si hay errores, guardar archivo para revisión
    if registros_con_error:
        error_file = "registros_con_error.csv"
        df_errores = pd.DataFrame(registros_con_error)
        df_errores.to_csv(error_file, index=False, encoding='utf-8-sig')
        print(f"\n💾 Registros con error guardados en: {error_file}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE CARGA")
    print("=" * 60)
    print(f"✅ Registros cargados exitosamente: {registros_cargados}")
    if errores > 0:
        print(f"❌ Registros con error: {errores}")
    print(f"📈 Total procesados: {total_registros}")
    print(f"✅ Carga completada!")
    print("=" * 60)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("📦 SCRIPT DE CARGA DE IMPORTACIONES")
    print("=" * 60)
    
    # Solicitar ruta del archivo
    print("\n📁 Ingresa la ruta completa del archivo Excel:")
    print("   Ejemplo: D:\\Datos\\importaciones_2024.xlsx")
    print("   O presiona Enter para usar: datos_importaciones.xlsx\n")
    
    ruta = input("Ruta del archivo: ").strip()
    
    if not ruta:
        ruta = "datos_importaciones.xlsx"
    
    # Verificar que el archivo existe
    if not os.path.exists(ruta):
        print(f"\n❌ Error: No se encontró el archivo en {ruta}")
        print("   Verifica la ruta y vuelve a intentar")
    else:
        cargar_datos_a_supabase(ruta)
    
    input("\n\nPresiona Enter para salir...")
