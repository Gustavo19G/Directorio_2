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
        if not os.path.exists("Directorio2.xlsx"):
            st.error("Archivo 'Directorio2.xlsx' no encontrado")
            return pd.DataFrame(columns=["Nombre", "Correo Electrónico", "Sucursal", "Extensión"])
        
        df = pd.read_excel(
            "Directorio2.xlsx",
            sheet_name="Base de datos",
            engine="openpyxl",
            dtype=str
        )
        
        required_columns = ["Nombre", "Correo Electrónico", "Sucursal", "Extensión"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"El archivo debe contener estas columnas: {', '.join(required_columns)}")
            return pd.DataFrame(columns=required_columns)
        
        df = df.dropna(how='all')
        
        if df.empty:
            st.warning("El archivo está vacío o no contiene datos válidos")
            
        return df.fillna("")
    
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")
        return pd.DataFrame(columns=required_columns)

def guardar_datos(df):
    try:
        df.to_excel(
            "Directorio2.xlsx",
            index=False,
            sheet_name="Base de datos",
            engine="openpyxl"
        )
        st.success("Archivo actualizado correctamente")
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error al guardar el archivo: {str(e)}")
        return False

def main():
    st.title("📞 Directorio Telefónico Tamex")
    st.markdown("---")
    
    df = cargar_datos()
    
    # Barra lateral para actualización (ahora colapsada por defecto)
    with st.sidebar:
        st.header("Actualización de Datos")
        
        # Expandable container que inicia colapsado
        with st.expander("Subir nuevo archivo", expanded=False):
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
                if password == "admin123":
                    if uploaded_file is not None:
                        try:
                            new_df = pd.read_excel(uploaded_file, engine="openpyxl")
                            if guardar_datos(new_df):
                                df = cargar_datos()
                        except Exception as e:
                            st.error(f"Error al procesar archivo: {str(e)}")
                    else:
                        st.warning("Por favor seleccione un archivo")
                else:
                    st.error("Contraseña incorrecta")
    
    # Sección de búsqueda (sin cambios)
    col1, col2 = st.columns(2)
    with col1:
        busqueda_nombre = st.text_input("Buscar por nombre:", key="busqueda_nombre")
    
    with col2:
        busqueda_sucursal = st.text_input("Buscar por sucursal:", key="busqueda_sucursal")
    
    # Filtrado de datos (sin cambios)
    if "Nombre" in df.columns and "Sucursal" in df.columns:
        mask_nombre = pd.Series(False, index=df.index)
        mask_sucursal = pd.Series(False, index=df.index)
        
        if busqueda_nombre.strip() != "":
            mask_nombre = df["Nombre"].str.contains(busqueda_nombre, case=False, na=False)
        
        if busqueda_sucursal.strip() != "":
            mask_sucursal = df["Sucursal"].str.contains(busqueda_sucursal, case=False, na=False)
        
        mask = mask_nombre | mask_sucursal
        
        if busqueda_nombre.strip() == "" and busqueda_sucursal.strip() == "":
            df_filtrado = df.copy()
        else:
            df_filtrado = df[mask].copy()
    else:
        st.error("Las columnas 'Nombre' y 'Sucursal' no están disponibles en los datos.")
        df_filtrado = pd.DataFrame(columns=df.columns)
    
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
