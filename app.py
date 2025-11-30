import streamlit as st
import os
from dotenv import load_dotenv
from utils.supabase_client import SupabaseClient
from utils.chatbot import ImportacionesChatbot

# Cargar variables
load_dotenv()

# Función helper para leer variables
def get_env(key, default=None):
    """Lee de st.secrets en producción, .env en local"""
    if hasattr(st, 'secrets') and key in st.secrets:
        return st.secrets[key]
    return os.getenv(key, default)

# Usa esta función en lugar de os.getenv
SUPABASE_URL = get_env("SUPABASE_URL")
SUPABASE_KEY = get_env("SUPABASE_KEY")
GROQ_API_KEY = get_env("GROQ_API_KEY")

# Configuración de página
st.set_page_config(
    page_title="Chatbot Importaciones IA", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)
# CSS personalizado
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem !important;
    }
    .main > div {
        padding-left: 1rem !important;
    }
    [data-testid="stSidebar"] {
        padding-top: 2rem !important;
    }
    [data-testid="stSidebar"] h1 {
        margin-bottom: 0.5rem !important;
    }
    .firma {
        font-size: 0.85rem;
        color: #666;
        margin-top: -0.5rem;
        margin-bottom: 1rem;
        font-style: italic;
    }
    iframe {
        display: block;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# CSS personalizado
st.markdown("""
<style>
    /* Reducir padding superior */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 100% !important;
    }
    
    /* Eliminar espacio lateral del main */
    .main > div {
        padding-left: 0.5rem !important;
        padding-right: 0.5rem !important;
        max-width: 100% !important;
    }
    
    /* Contenedor del dashboard más ancho */
    [data-testid="column"] {
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    /* Power BI iframe responsive y centrado */
    iframe {
        display: block;
        margin: 0 auto;
        max-width: 98% !important;
        width: 100% !important;
    }
    
    /* Sidebar más compacta */
    [data-testid="stSidebar"] {
        padding-top: 2rem !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0rem !important;
    }
    
    [data-testid="stSidebar"] h1 {
        margin-top: 0rem !important;
        margin-bottom: 0.5rem !important;
        padding-top: 0rem !important;
    }
    
    .firma {
        font-size: 0.85rem;
        color: #666;
        margin-top: -0.5rem;
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    /* Eliminar scroll horizontal */
    .main {
        overflow-x: hidden !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== INICIALIZACIÓN ==========
@st.cache_resource
def init_db():
    return SupabaseClient()

db = init_db()

# ========== SIDEBAR: CHATBOT ==========
with st.sidebar:
    # Título y firma (sin espacio extra)
    st.markdown("# 🤖 Asistente IA")
    st.markdown('<p class="firma">by Telvy Pizarro</p>', unsafe_allow_html=True)
    
    # Selectores compactos (sin dividers innecesarios)
    chat_mode = st.radio(
        "Versión:",
        ["💬 Chat v4.0 (Rápido)", "🚀 Chat v5.0 (SQL Agent)"],
        label_visibility="visible"
    )
    
    model_option = st.selectbox(
        "🧠 Modelo IA:",
        ["🆓 Groq (Llama 3.3 - Potente)", "💰 DeepSeek (Chat)", "🌟 OpenAI (GPT-4o)"],
        label_visibility="visible"
    )
    
    # Mapeo de providers
    if "Groq" in model_option: provider = "groq"
    elif "DeepSeek" in model_option: provider = "deepseek"
    else: provider = "openai"
    
    st.markdown("---")
    
    # ====== INPUT DE CHAT (siempre visible) ======
    prompt = st.chat_input("💬 Pregunta sobre importaciones...")
    
    # Botón limpiar compacto
    if st.button("🗑️ Limpiar conversación", use_container_width=True, type="secondary"):
        st.session_state.chat_v4 = []
        st.session_state.chat_v5 = []
        st.rerun()
    
    st.markdown("---")
    
    # ====== ÁREA DE RESPUESTAS CON SCROLL ======
    # Determinar chat activo
    current_chat = []
    if chat_mode == "💬 Chat v4.0 (Rápido)":
        if "chat_v4" not in st.session_state: 
            st.session_state.chat_v4 = []
        current_chat = st.session_state.chat_v4
    else:
        if "chat_v5" not in st.session_state: 
            st.session_state.chat_v5 = []
        current_chat = st.session_state.chat_v5
    
    # Contenedor de mensajes (ajusta height según necesites)
    chat_container = st.container(height=400, border=True)
    
    with chat_container:
        if len(current_chat) == 0:
            st.info("👋 Haz una pregunta sobre importaciones para comenzar")
        else:
            for msg in current_chat:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])
    
    # ====== PROCESAMIENTO DEL PROMPT ======
    if prompt:
        # Añadir mensaje del usuario
        current_chat.append({"role": "user", "content": prompt})
        
        # Procesar respuesta
        try:
            response = ""
            if chat_mode == "💬 Chat v4.0 (Rápido)":
                bot = ImportacionesChatbot(db, provider=provider)
                with st.spinner("🔍 Analizando..."):
                    response = bot.chat(prompt)
            else:
                # Chat v5.0 - SQL Agent
                try:
                    from utils.langchain_chatbot import LangChainChatbot
                except ImportError:
                    from langchain_chatbot import LangChainChatbot
                
                with st.spinner("🧠 Ejecutando consulta SQL..."):
                    agent = LangChainChatbot(provider=provider)
                    response = agent.chat(prompt)
                    
                    # Limpiar respuesta verbose
                    if "Thought:" in response:
                        if "Final Answer:" in response:
                            response = response.split("Final Answer:")[-1].strip()
            
            # Añadir respuesta del asistente
            current_chat.append({"role": "assistant", "content": response})
            
            # Rerun para actualizar
            st.rerun()
                    
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ========== ÁREA PRINCIPAL: POWER BI ==========
powerbi_url = os.getenv("POWERBI_URL", "")

if powerbi_url:
    # Usamos un div contenedor con padding-top inline para bajarlo visualmente
    st.markdown(f"""
        <div style="padding-top: 30px; height: 90vh;">
            <iframe 
                title="Dashboard Importaciones" 
                width="100%" 
                height="100%" 
                src="{powerbi_url}" 
                frameborder="0" 
                allowFullScreen="true">
            </iframe>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("👈 Configura POWERBI_URL en tu archivo .env")
