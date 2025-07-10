import streamlit as st
import pandas as pd

# Cambiar el ícono de la pestaña
st.set_page_config(page_title="Directorio Telefónico Tamex", page_icon="📞")

# Cargar el archivo Excel
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_excel("Directorio2.xlsx", sheet_name="Base de datos", engine="openpyxl")
    except Exception as e:
        st.error(f"No se pudo cargar el archivo Excel: {e}")
        df = pd.DataFrame(columns=["Nombre", "Correo Electrónico", "Sucursal", "Extensión"])
    return df

df = cargar_datos()

# Título
st.title("Directorio Telefónico Tamex")

# Buscador
query = st.text_input("Buscar por nombre o sucursal:")

# Filtrado
if query:
    filtro = df[
        df["Nombre"].str.lower().str.contains(query.lower()) |
        df["Sucursal"].str.lower().str.contains(query.lower())
    ]
    if filtro.empty:
        st.warning("No se encontraron coincidencias.")
    else:
        st.dataframe(filtro)
else:
    st.dataframe(df)

# Sección para actualizar el archivo Excel en una barra desplegable
with st.expander("Actualizar Archivo Excel"):
    # Cargar nuevo archivo
    uploaded_file = st.file_uploader("Cargar nuevo archivo Excel", type=["xlsx"])

    # Solicitar contraseña
    password = st.text_input("Ingrese la contraseña para actualizar el archivo:", type="password")

    # Verificar la contraseña y actualizar el archivo
    if st.button("Actualizar"):
        if password == "tu_contraseña_secreta":  # Cambia esto por la contraseña que desees
            if uploaded_file is not None:
                try:
                    # Leer el nuevo archivo
                    new_data = pd.read_excel(uploaded_file, engine="openpyxl")
                    # Guardar el nuevo archivo
                    new_data.to_excel("Directorio2.xlsx", index=False, sheet_name="Base de datos", engine="openpyxl")
                    st.success("El archivo se ha actualizado correctamente.")
                except Exception as e:
                    st.error(f"No se pudo actualizar el archivo: {e}")
            else:
                st.warning("Por favor, carga un archivo Excel.")
        else:
            st.error("Contraseña incorrecta.")
