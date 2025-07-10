import streamlit as st
import pandas as pd
import os
from PIL import Image

# Configuración de la página
st.set_page_config(
    page_title="Directorio Telefónico Tamex",
    page_icon="📞",
    layout="wide"
)

# Función mejorada para cargar logo desde archivo local
def load_local_image(image_path):
    """Carga imagen desde la ruta especificada con manejo de errores robusto"""
    try:
        # Verificar si el archivo existe
        if not os.path.exists(image_path):
            st.error(f"Archivo de imagen no encontrado: {image_path}")
            return None
        
        # Cargar imagen con PIL
        image = Image.open(image_path)
        return image
        
    except Exception as e:
        st.error(f"Error al cargar la imagen: {str(e)}")
        return None

def main():
    # Encabezado con título e imagen
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.title("📞 Directorio Telefónico Tamex")
    
    with col2:
        # Especificar ruta relativa o absoluta a tu imagen
        logo_path = "tamex.png"  # O "./tamex.png" o "assets/tamex.png" dependiendo de tu estructura
        
        # Cargar logo
        logo = load_local_image(logo_path)
        
        if logo:
            # Mostrar logo con tamaño adecuado
            st.image(
                logo,
                width=200,  # Ancho en pixels
                caption="",  # Sin texto debajo
                use_column_width=False
            )
        else:
            # Mensaje más descriptivo si falla la carga
            st.warning("Logo corporativo no disponible")

    st.markdown("---")
    
    # Resto de tu código de la aplicación
    df = cargar_datos()
    
    with st.sidebar:
        st.header("Actualización de Datos")
        with st.expander("Subir nuevo archivo"):
            uploaded_file = st.file_uploader("Seleccione archivo Excel", type=["xlsx"])
            password = st.text_input("Contraseña de administrador:", type="password")
            
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
    
    busqueda_nombre = st.text_input("Buscar por nombre:")
    busqueda_sucursal = st.text_input("Buscar por sucursal:")
    
    mask = (
        df["Nombre"].str.contains(busqueda_nombre, case=False) &
        df["Sucursal"].str.contains(busqueda_sucursal, case=False)
    )
    df_filtrado = df[mask].copy()
    
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Nombre": "Nombre",
            "Correo Electrónico": "Email",
            "Sucursal": "Sucursal",
            "Extensión": st.column_config.NumberColumn("Extensión", format="%d")
        }
    )

if __name__ == "__main__":
    main()
