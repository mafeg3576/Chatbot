from db.supabase_client import supabase

try:
    # Buscar empresa con ID 2
    result = supabase.table('empresas').select('id, nombre_empresa').eq('id', 2).execute()
    if result.data:
        print(f"Conectado. Empresa ID 2: {result.data[0]['nombre_empresa']}")
    else:
        print("No se encontró empresa con ID 2")
except Exception as e:
    print(f"Error de conexión: {e}")