import streamlit as st
import pandas as pd
import os
from PIL import Image  # Importar para manejo de imágenes

# Configuración de la página
st.set_page_config(
    page_title="Directorio Telefónico Tamex",
    page_icon="📞",
    layout="wide"
)

# Ruta del logo
LOGO_PATH = "tamex.png"  # Asegúrate de que el archivo esté en la misma carpeta

# Función para cargar el logo con manejo de errores
def load_logo(path):
    try:
        return Image.open(path)
    except Exception as e:
        st.error(f"No se pudo cargar el logo: {str(e)}")
        return None

def main():
    # Encabezado con título e imagen
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("📞 Directorio Telefónico Tamex")
    
    with col2:
        logo = load_logo(LOGO_PATH)
        if logo:
            st.image(
                logo,
                width=200,  # Ajusta según necesidad
                caption="",
                use_column_width=False
            )
        else:
            # Placeholder alternativo si no se carga el logo
            st.image(
                "https://placehold.co/200x100/3a86ff/FFFFFF?text=Logo+Tamex",
                width=200,
                caption="Logo no encontrado",
                use_column_width=False
            )
    
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
    
    # Sección de búsqueda
    busqueda_nombre = st.text_input("Buscar por nombre:")
    busqueda_sucursal = st.text_input("Buscar por sucursal:")
    
    # Filtrado de datos
    mask = (
        df["Nombre"].str.contains(busqueda_nombre, case=False) &
        df["Sucursal"].str.contains(busqueda_sucursal, case=False)
    )
    df_filtrado = df[mask].copy()
    
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
