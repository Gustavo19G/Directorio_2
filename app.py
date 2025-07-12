import streamlit as st
import pandas as pd
import os
import hashlib
from io import BytesIO


st.set_page_config(
    page_title="Directorio Telefónico Tamex",
    page_icon="📞",
    layout="wide"
)


USUARIOS = {
    "admin": {"password": "admin123", "role": "administrador"},
    "usuario": {"password": "user123", "role": "usuario"},
    "tamex_admin": {"password": "tamex2024", "role": "administrador"},
    "empleado": {"password": "empleado123", "role": "usuario"}
}


def verificar_credenciales(username, password):
    if username in USUARIOS:
        if USUARIOS[username]["password"] == password:
            return USUARIOS[username]["role"]
    return None


def inicializar_sesion():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'username' not in st.session_state:
        st.session_state.username = None


def mostrar_login():
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 20px auto;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .login-title {
        text-align: center;
        color: #2c3e50;
        margin-bottom: 2rem;
    }
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .responsive-logo {
        max-width: 100%;
        height: auto;
        max-height: 150px;
        display: block;
        margin: 0 auto;
    }
    .credentials-info {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
        font-size: 0.9rem;
    }
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .login-container {
            max-width: 90%;
            margin: 10px auto;
            padding: 1rem;
        }
        .responsive-logo {
            max-height: 100px;
        }
    }
    @media (max-width: 480px) {
        .responsive-logo {
            max-height: 80px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            
            # Logo en la pantalla de login - Centrado y Responsive
            st.markdown('<div class="logo-container">', unsafe_allow_html=True)
            try:
                if os.path.exists("tamex.png"):
                    # Usar contenedor centrado para el logo
                    logo_col1, logo_col2, logo_col3 = st.columns([1, 2, 1])
                    with logo_col2:
                        st.image("tamex.png", use_column_width=True)
                else:
                    st.info("Logo tamex.png no encontrado")
            except Exception as e:
                st.warning(f"Error al cargar el logo: {str(e)}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<h2 class="login-title">🔐 Acceso al Directorio Tamex</h2>', unsafe_allow_html=True)
            
            with st.form("login_form"):
                username = st.text_input("Usuario:", key="login_username")
                password = st.text_input("Contraseña:", type="password", key="login_password")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    submit_usuario = st.form_submit_button("Ingresar como Usuario", use_container_width=True)
                with col_btn2:
                    submit_admin = st.form_submit_button("Ingresar como Admin", use_container_width=True)
                
                if submit_usuario or submit_admin:
                    if username and password:
                        role = verificar_credenciales(username, password)
                        if role:
                            if (submit_usuario and role == "usuario") or (submit_admin and role == "administrador"):
                                st.session_state.authenticated = True
                                st.session_state.user_role = role
                                st.session_state.username = username
                                st.rerun()
                            else:
                                st.error("❌ No tiene permisos para acceder con este rol")
                        else:
                            st.error("❌ Usuario o contraseña incorrectos")
                    else:
                        st.error("❌ Por favor ingrese usuario y contraseña")
            
            st.markdown("""
            <div class="credentials-info">
                <strong>📋 Credenciales de prueba:</strong><br>
                <strong>Usuarios normales:</strong><br>
                • usuario / user123<br>
                • empleado / empleado123<br><br>
                <strong>Administradores:</strong><br>
                • admin / admin123<br>
                • tamex_admin / tamex2024
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)


@st.cache_data
def cargar_datos():
    try:
        if not os.path.exists("Directorio2.xlsx"):
            st.warning("Archivo 'Directorio2.xlsx' no encontrado. Usando datos de ejemplo.")
            return pd.DataFrame({
                "Nombre": ["Juan Pérez", "María González", "Carlos Rodríguez", "Ana López", "Pedro Martínez"],
                "Correo Electrónico": ["juan.perez@tamex.com", "maria.gonzalez@tamex.com", "carlos.rodriguez@tamex.com", "ana.lopez@tamex.com", "pedro.martinez@tamex.com"],
                "Puesto": ["Gerente de Ventas", "Contadora", "Desarrollador", "Recursos Humanos", "Analista"],
                "Sucursal": ["México DF", "Guadalajara", "Monterrey", "Puebla", "Tijuana"],
                "Extensión": ["101", "102", "103", "104", "105"]
            })
        
        df = pd.read_excel(
            "Directorio2.xlsx",
            sheet_name="Base de datos",
            engine="openpyxl",
            dtype=str
        )

        required_columns = ["Nombre", "Correo Electrónico", "Sucursal", "Extensión"]
        
        if "Puesto" not in df.columns:
            df["Puesto"] = ""
            st.info("ℹ️ Se agregó la columna 'Puesto' al directorio")
        
        column_order = ["Nombre", "Correo Electrónico", "Puesto", "Sucursal", "Extensión"]
        df = df.reindex(columns=column_order, fill_value="")
        
        if not all(col in df.columns for col in required_columns):
            st.error(f"El archivo debe contener estas columnas: {', '.join(required_columns)}")
            return pd.DataFrame(columns=column_order)
        
        df = df.dropna(how='all')
        
        if df.empty:
            st.warning("El archivo está vacío o no contiene datos válidos")
            
        return df.fillna("")
    
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")
        return pd.DataFrame(columns=["Nombre", "Correo Electrónico", "Puesto", "Sucursal", "Extensión"])


def guardar_datos(df):
    try:
        df.to_excel(
            "Directorio2.xlsx",
            index=False,
            sheet_name="Base de datos",
            engine="openpyxl"
        )
        st.success("✅ Archivo actualizado correctamente")
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"❌ Error al guardar el archivo: {str(e)}")
        return False


def mostrar_header():
    st.markdown("""
    <style>
    .user-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .user-info {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .user-role {
        background: rgba(255,255,255,0.2);
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
    }
    .header-logo {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .header-responsive {
        display: flex;
        align-items: center;
        gap: 1rem;
        flex-wrap: wrap;
    }
    .header-title {
        color: #2c3e50;
        margin: 0;
        flex-grow: 1;
    }
    .user-section {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 10px;
    }
    .user-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .header-responsive {
            flex-direction: column;
            text-align: center;
            gap: 0.5rem;
        }
        .header-title {
            font-size: 1.2rem;
        }
        .user-content {
            flex-direction: column;
            gap: 0.5rem;
        }
    }
    @media (max-width: 480px) {
        .header-title {
            font-size: 1rem;
        }
        .user-section {
            padding: 0.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header responsive con logo
    st.markdown('<div class="header-responsive">', unsafe_allow_html=True)
    
    col_logo, col_header = st.columns([1, 4])
    
    with col_logo:
        try:
            if os.path.exists("tamex.png"):
                st.image("tamex.png", use_column_width=True)
            else:
                st.info("Logo tamex.png no encontrado")
        except Exception as e:
            st.warning(f"Error al cargar el logo: {str(e)}")
    
    with col_header:
        st.markdown('<h2 class="header-title">📞 Directorio Telefónico Tamex</h2>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sección de usuario responsive
    col_user, col_btn = st.columns([3, 1])
    
    with col_user:
        role_display = "👤 Usuario" if st.session_state.user_role == "usuario" else "🔧 Administrador"
        st.markdown(f"""
        <div class="user-section">
            <div class="user-content">
                <span>Bienvenido: <strong>{st.session_state.username}</strong></span>
                <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">{role_display}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_btn:
        if st.button("🚪 Cerrar Sesión", type="secondary", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.username = None
            st.rerun()


def interfaz_usuario(df):
    st.markdown("### 📋 Consulta de Directorio")
    
    col1, col2 = st.columns(2)
    with col1:
        busqueda_nombre = st.text_input("🔍 Buscar por nombre:", key="search_name")
    with col2:
        busqueda_sucursal = st.text_input("🏢 Buscar por sucursal:", key="search_branch")
    
    if not df.empty:
        mask = (
            df["Nombre"].str.contains(busqueda_nombre, case=False, na=False) &
            df["Sucursal"].str.contains(busqueda_sucursal, case=False, na=False)
        )
        df_filtrado = df[mask].copy()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("👥 Total de Contactos", len(df))
        with col2:
            st.metric("📊 Resultados Filtrados", len(df_filtrado))
        with col3:
            st.metric("🏢 Sucursales", df["Sucursal"].nunique())
        
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Nombre": st.column_config.TextColumn("👤 Nombre", width="medium"),
                "Correo Electrónico": st.column_config.TextColumn("📧 Email", width="medium"),
                "Puesto": st.column_config.TextColumn("💼 Puesto", width="medium"),
                "Sucursal": st.column_config.TextColumn("🏢 Sucursal", width="medium"),
                "Extensión": st.column_config.TextColumn("📞 Extensión", width="small")
            }
        )
    else:
        st.info("ℹ️ No hay datos para mostrar")


def interfaz_administrador(df):
    tab1, tab2, tab3 = st.tabs(["📋 Consulta", "📝 Gestión de Datos", "📁 Administración de Archivos"])
    
    with tab1:
        interfaz_usuario(df)
    
    with tab2:
        st.markdown("### 📝 Gestión de Contactos")
        
        with st.expander("➕ Agregar Nuevo Contacto", expanded=False):
            with st.form("add_contact_form"):
                col1, col2 = st.columns(2)
                with col1:
                    nombre = st.text_input("Nombre completo:")
                    correo = st.text_input("Correo electrónico:")
                    puesto = st.text_input("Puesto:")
                with col2:
                    sucursal = st.text_input("Sucursal:")
                    extension = st.text_input("Extensión:")
                
                if st.form_submit_button("➕ Agregar Contacto", type="primary"):
                    if nombre and correo and sucursal and extension:
                        nuevo_contacto = pd.DataFrame({
                            "Nombre": [nombre],
                            "Correo Electrónico": [correo],
                            "Puesto": [puesto],
                            "Sucursal": [sucursal],
                            "Extensión": [extension]
                        })
                        df_actualizado = pd.concat([df, nuevo_contacto], ignore_index=True)
                        if guardar_datos(df_actualizado):
                            st.balloons()
                            st.info("🔄 Recargue la página para ver los cambios")
                    else:
                        st.error("❌ Por favor complete al menos los campos obligatorios: Nombre, Correo, Sucursal y Extensión")
        
        if not df.empty:
            st.markdown("### 📊 Datos Actuales")
            
            if len(df) > 0:
                with st.expander("✏️ Editar Contacto Existente"):
                    selected_index = st.selectbox(
                        "Seleccionar contacto para editar:",
                        range(len(df)),
                        format_func=lambda x: f"{df.iloc[x]['Nombre']} - {df.iloc[x]['Puesto']} - {df.iloc[x]['Sucursal']}"
                    )
                    
                    if selected_index is not None:
                        selected_contact = df.iloc[selected_index]
                        
                        with st.form("edit_contact_form"):
                            col1, col2 = st.columns(2)
                            with col1:
                                nombre_edit = st.text_input("Nombre completo:", value=selected_contact["Nombre"])
                                correo_edit = st.text_input("Correo electrónico:", value=selected_contact["Correo Electrónico"])
                                puesto_edit = st.text_input("Puesto:", value=selected_contact["Puesto"])
                            with col2:
                                sucursal_edit = st.text_input("Sucursal:", value=selected_contact["Sucursal"])
                                extension_edit = st.text_input("Extensión:", value=selected_contact["Extensión"])
                            
                            col_btn1, col_btn2 = st.columns(2)
                            with col_btn1:
                                if st.form_submit_button("💾 Guardar Cambios", type="primary"):
                                    df.loc[selected_index, "Nombre"] = nombre_edit
                                    df.loc[selected_index, "Correo Electrónico"] = correo_edit
                                    df.loc[selected_index, "Puesto"] = puesto_edit
                                    df.loc[selected_index, "Sucursal"] = sucursal_edit
                                    df.loc[selected_index, "Extensión"] = extension_edit
                                    if guardar_datos(df):
                                        st.balloons()
                                        st.info("🔄 Recargue la página para ver los cambios")
                            
                            with col_btn2:
                                if st.form_submit_button("🗑️ Eliminar Contacto", type="secondary"):
                                    df_actualizado = df.drop(selected_index).reset_index(drop=True)
                                    if guardar_datos(df_actualizado):
                                        st.info("🔄 Recargue la página para ver los cambios")
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Nombre": st.column_config.TextColumn("👤 Nombre", width="medium"),
                    "Correo Electrónico": st.column_config.TextColumn("📧 Email", width="medium"),
                    "Puesto": st.column_config.TextColumn("💼 Puesto", width="medium"),
                    "Sucursal": st.column_config.TextColumn("🏢 Sucursal", width="medium"),
                    "Extensión": st.column_config.TextColumn("📞 Extensión", width="small")
                }
            )
    
    with tab3:
        st.markdown("### 📁 Administración de Archivos")
        
        with st.expander("📤 Subir Archivo de Reemplazo"):
            uploaded_file = st.file_uploader(
                "Seleccione archivo Excel",
                type=["xlsx"],
                help="El archivo debe contener las columnas: Nombre, Correo Electrónico, Puesto, Sucursal, Extensión"
            )
            
            if uploaded_file is not None:
                if st.button("📥 Reemplazar Directorio", type="primary"):
                    try:
                        new_df = pd.read_excel(uploaded_file, engine="openpyxl", dtype=str)
                        required_columns = ["Nombre", "Correo Electrónico", "Sucursal", "Extensión"]
                        
                        if "Puesto" not in new_df.columns:
                            new_df["Puesto"] = ""
                            st.info("ℹ️ Se agregó la columna 'Puesto' al archivo importado")
                        
                        column_order = ["Nombre", "Correo Electrónico", "Puesto", "Sucursal", "Extensión"]
                        new_df = new_df.reindex(columns=column_order, fill_value="")
                        
                        if all(col in new_df.columns for col in required_columns):
                            if guardar_datos(new_df):
                                st.balloons()
                                st.info("🔄 Recargue la página para ver los cambios")
                        else:
                            st.error(f"❌ El archivo debe contener las columnas: {', '.join(required_columns)}")
                    except Exception as e:
                        st.error(f"❌ Error al procesar archivo: {str(e)}")
        
        with st.expander("📤 Exportar Datos"):
            if not df.empty:
                from io import BytesIO
                excel_buffer = BytesIO()
                df.to_excel(excel_buffer, index=False, engine='openpyxl')
                excel_data = excel_buffer.getvalue()
                
                st.download_button(
                    label="📥 Descargar Directorio Actual",
                    data=excel_data,
                    file_name="directorio_backup.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.info("ℹ️ No hay datos para exportar")


def main():
    inicializar_sesion()
    
    if not st.session_state.authenticated:
        mostrar_login()
    else:
        mostrar_header()
        df = cargar_datos()
        
        if st.session_state.user_role == "usuario":
            interfaz_usuario(df)
        elif st.session_state.user_role == "administrador":
            interfaz_administrador(df)

if __name__ == "__main__":
    main()
