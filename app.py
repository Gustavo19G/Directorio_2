import streamlit as st
import pandas as pd
import os

# Configuración de la página
st.set_page_config(
    page_title="Directorio Telefónico Tamex",
    page_icon="📞",
    layout="wide"
)

# Función para cargar datos con validación robusta
@st.cache_data
def cargar_datos():
    try:
        # Verificar si el archivo existe
        if not os.path.exists("Directorio2.xlsx"):
            st.error("Archivo 'Directorio2.xlsx' no encontrado")
            return pd.DataFrame(columns=["Nombre", "Correo Electrónico", "Sucursal", "Extensión"])
        
        # Leer el archivo con múltiples validaciones
        df = pd.read_excel(
            "Directorio2.xlsx",
            sheet_name="Base de datos",
            engine="openpyxl",
            dtype=str
        )
        
        # Validar columnas requeridas
        required_columns = ["Nombre", "Correo Electrónico", "Sucursal", "Extensión"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"El archivo debe contener estas columnas: {', '.join(required_columns)}")
            return pd.DataFrame(columns=required_columns)
        
        # Eliminar filas completamente vacías
        df = df.dropna(how='all')
        
        if df.empty:
            st.warning("El archivo está vacío o no contiene datos válidos")
            
        return df.fillna("")
    
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")
        return pd.DataFrame(columns=required_columns)

# Función para guardar datos
def guardar_datos(df):
    try:
        df.to_excel(
            "Directorio2.xlsx",
            index=False,
            sheet_name="Base de datos",
            engine="openpyxl"
        )
        st.success("Archivo actualizado correctamente")
        st.cache_data.clear()  # Limpiar caché para recargar datos
        return True
    except Exception as e:
        st.error(f"Error al guardar el archivo: {str(e)}")
        return False

# Interfaz principal
def main():
    st.title("📞 Directorio Telefónico Tamex")
    st.markdown("---")
    
    # Cargar datos
    df = cargar_datos()
    
    # Barra lateral para actualización
    with st.sidebar:
        st.header("Actualización de Datos")
        with st.expander("Subir nuevo archivo"):
            uploaded_file = st.file_uploader(
                "Seleccione archivo Excel",
                type=["xlsx"],
                help="El archivo debe contener las columnas requeridas"
            )
            
            password = st.text_input(
                "Contraseña de administrador:",
                type="password",
                help="Ingrese la contraseña para realizar cambios"
            )
            
            if st.button("Actualizar Directorio"):
                if password == "admin123":  # Cambiar por tu contraseña segura
                    if uploaded_file is not None:
                        try:
                            new_df = pd.read_excel(uploaded_file, engine="openpyxl")
                            if guardar_datos(new_df):
                                df = cargar_datos()  # Recargar datos
                        except Exception as e:
                            st.error(f"Error al procesar archivo: {str(e)}")
                    else:
                        st.warning("Por favor seleccione un archivo")
                else:
                    st.error("Contraseña incorrecta")
    
    # Sección de búsqueda
    col1, col2 = st.columns([3, 1])
    with col1:
        busqueda = st.text_input("Buscar por nombre o sucursal:", key="busqueda")
    
    with col2:
        mostrar_todos = st.checkbox("Mostrar todos los registros", True)
    
    # Filtrado de datos
    if not mostrar_todos and busqueda:
        mask = (
            df["Nombre"].str.contains(busqueda, case=False) |
            df["Sucursal"].str.contains(busqueda, case=False)
        )
        df_filtrado = df[mask].copy()
    else:
        df_filtrado = df.copy()
    
    # Mostrar resultados
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nombre": "Nombre",
            "Correo Electrónico": "Email",
            "Sucursal": "Sucursal",
            "Extensión": st.column_config.NumberColumn(
                "Extensión",
                format="%d"
            )
        }
    )

if __name__ == "__main__":
    main()
