import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Directorio Telefónico Tamex",
    page_icon="📞",
    layout="wide"
)

# Contraseña para cargar nuevos archivos (cambiar por una segura)
PASSWORD = "S1s7em4s"

# Función para cargar datos iniciales
@st.cache_data
def cargar_datos(archivo="Directorio2.xlsx"):
    try:
        df = pd.read_excel(archivo, sheet_name="Base de datos", engine="openpyxl")
        # Validar estructura del archivo
        columnas_requeridas = ["Nombre", "Correo Electrónico", "Sucursal", "Extensión"]
        if not all(col in df.columns for col in columnas_requeridas):
            st.error("El archivo no tiene la estructura requerida")
            return pd.DataFrame(columns=columnas_requeridas)
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return pd.DataFrame(columns=["Nombre", "Correo Electrónico", "Sucursal", "Extensión"])

# Función para cargar nuevo archivo
def cargar_nuevo_archivo():
    st.warning("⚠️ Al cargar un nuevo archivo se reemplazará la base de datos actual")
    uploaded_file = st.file_uploader(
        "Seleccione el nuevo archivo Excel", 
        type=["xlsx"],
        help="El archivo debe contener una hoja llamada 'Base de datos' con las columnas requeridas"
    )
    
    if uploaded_file is not None:
        try:
            df_nuevo = pd.read_excel(uploaded_file, sheet_name="Base de datos", engine="openpyxl")
            # Validar estructura
            if all(col in df_nuevo.columns for col in ["Nombre", "Correo Electrónico", "Sucursal", "Extensión"]):
                st.success("✅ Archivo validado correctamente")
                return df_nuevo
            else:
                st.error("El archivo no contiene todas las columnas requeridas")
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
    return None

# Interfaz principal
st.title("📞 Directorio Telefónico Tamex")
st.markdown("---")

# Sidebar para funciones administrativas
with st.sidebar:
    st.header("Administración")
    if st.button("🔒 Cambiar base de datos"):
        # Solicitar contraseña
        password = st.text_input("Ingrese la contraseña:", type="password", key="password_input")
        
        if password:
            if password == PASSWORD:
                st.success("Contraseña correcta")
                nuevo_df = cargar_nuevo_archivo()
                if nuevo_df is not None:
                    # Actualizar los datos en caché
                    st.cache_data.clear()
                    df = cargar_datos()  # Esto ahora usará el nuevo archivo
                    st.rerun()
            else:
                st.error("Contraseña incorrecta")

# Cargar datos iniciales
df = cargar_datos()

# Buscadores separados
st.header("Buscar Contactos")
col1, col2 = st.columns(2)

with col1:
    nombre_query = st.text_input("Buscar por Nombre:", placeholder="Nombre...")

with col2:
    sucursal_query = st.text_input("Buscar por Sucursal:", placeholder="Sucursal...")

# Mostrar resultados
st.markdown("---")

# Filtrar por nombre
if nombre_query:
    nombre_query = nombre_query.lower()
    filtro_nombre = df[df["Nombre"].str.lower().str.contains(nombre_query)]
else:
    filtro_nombre = pd.DataFrame(columns=df.columns)

# Filtrar por sucursal
if sucursal_query:
    sucursal_query = sucursal_query.lower()
    filtro_sucursal = df[df["Sucursal"].str.lower().str.contains(sucursal_query)]
else:
    filtro_sucursal = pd.DataFrame(columns=df.columns)

# Combinar resultados
filtro_combined = pd.concat([filtro_nombre, filtro_sucursal]).drop_duplicates()

if filtro_combined.empty:
    st.warning("No se encontraron coincidencias")
else:
    st.dataframe(
        filtro_combined,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nombre": "Nombre",
            "Correo Electrónico": "Correo",
            "Sucursal": "Sucursal",
            "Extensión": "Extensión"
        }
    )

# Información de la base de datos actual
st.markdown("---")
st.caption(f"Base de datos actual: {len(df)} contactos registrados")
