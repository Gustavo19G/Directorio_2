
import streamlit as st
import pandas as pd

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
