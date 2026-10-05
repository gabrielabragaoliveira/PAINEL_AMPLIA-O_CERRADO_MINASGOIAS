import streamlit as st
import pandas as pd
import os
import base64
import maps  # Importa o ficheiro maps.py que criámos para processar o KMZ

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Obras Ampliação",
    page_icon="🚧",
    layout="wide"
)

# 2. Funções de Carregamento (CSS e Imagens)
def carregar_css(arquivo_css):
    try:
        with open(arquivo_css) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

carregar_css("style.css")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Tenta carregar as imagens das logos
img_minas_goias = ""
img_cerrado = ""
if os.path.exists("Ecovias Minas Goias_Logo (1).png"):
    img_minas_goias = f"data:image/png;base64,{get_base64_of_bin_file('Ecovias Minas Goias_Logo (1).png')}"
if os.path.exists("Ecovias_Cerrado_Logo_Vertical_RGB_Preferencial_20241212_Keenwork_AF.png"):
    img_cerrado = f"data:image/png;base64,{get_base64_of_bin_file('Ecovias_Cerrado_Logo_Vertical_RGB_Preferencial_20241212_Keenwork_AF.png')}"

# 3. Cabeçalho Superior
st.markdown(f"""
    <div class="cabecalho">
        <h1>OBRAS AMPLIAÇÃO</h1>
        <div class="logos">
            {'<img src="' + img_cerrado + '" class="logo-img">' if img_cerrado else ''}
            {'<img src="' + img_minas_goias + '" class="logo-img">' if img_minas_goias else ''}
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. Barra Lateral (PAINEL DE CONTROLE)
st.sidebar.markdown("### PAINEL DE CONTROLE")

concessao = st.sidebar.selectbox("CONCESSÃO", ["Cerrado", "Minas Goiás"])

# Lógica dinâmica: Contorno Uberlândia aparece APENAS na concessão Minas Goiás
if concessao == "Minas Goiás":
    opcoes_estado = ["Minas", "Goiás", "Contorno Uberlândia"]
else:
    opcoes_estado = ["Minas", "Goiás"]

estado = st.sidebar.selectbox("ESTADO / REGIÃO", opcoes_estado)

# Tooltip dinâmico para os limites do KM
dica_km = "Digite o KM desejado."
if concessao == "Minas Goiás":
    if estado == "Minas":
        dica_km = "Limites: KM 207+300 ao 77+400 e KM 65+473 ao 00+000"
    elif estado == "Goiás":
        dica_km = "Limites: KM 314+000 ao 95+700"
    elif estado == "Contorno Uberlândia":
        dica_km = "Limites: KM 00+000 ao 21+000"

km = st.sidebar.text_input("KM", placeholder="Ex: 120+500", help=dica_km)
obra = st.sidebar.text_input("OBRA", placeholder="Digite a obra...")

# Upload da Base de Dados
st.sidebar.markdown("---")
st.sidebar.markdown("**BASE DE DADOS:**")
arquivo_upado = st.sidebar.file_uploader("Upload do BI - AMPLIAÇÃO", type=["xlsx", "xls", "csv"])

# Processamento dos dados na memória
@st.cache_data
def processar_arquivo(upload):
    if upload is not None:
        try:
            if upload.name.endswith('.csv'):
                df = pd.read_csv(upload)
            else:
                df = pd.read_excel(upload)
            return df
        except Exception as e:
            st.sidebar.error(f"Erro ao processar a planilha: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

df = processar_arquivo(arquivo_upado)

# 5. Navegação Principal (Abas Horizontais)
aba_resumo, aba_cerrado, aba_minas = st.tabs(["QUADRO DE RESUMO", "CERRADO (ECC)", "MINAS GOIÁS (EMG)"])

# --- ABA 1: QUADRO DE RESUMO ---
with aba_resumo:
    st.subheader("RESUMO")
    col_esquerda, col_direita = st.columns([2, 1])
    
    with col_esquerda:
        st.markdown('<div class="caixa-verde-clara" style="height: 400px; display:flex; align-items:center; justify-content:center;"><i>[INSERIR GRÁFICOS DE RESUMO AQUI]</i></div>', unsafe_allow_html=True)

    with col_direita:
        st.markdown('<div class="titulo-verde">EM ANDAMENTO</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.markdown('<div class="caixa-indicador">[CERRADO]</div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="caixa-indicador">[MINAS GOIÁS]</div>', unsafe_allow_html=True)
        
        st.write("") # Espaçamento
        
        st.markdown('<div class="titulo-verde">PREVISTO A INICIAR</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3: st.markdown('<div class="caixa-indicador">[CERRADO]</div>', unsafe_allow_html=True)
        with c4: st.markdown('<div class="caixa-indicador">[MINAS GOIÁS]</div>', unsafe_allow_html=True)

    st.divider()

    # --- SEÇÃO DO MAPA ---
    st.subheader("MAPA DE OBRAS")
    col_mapa, col_menu_mapa = st.columns([3, 1])
    
    with col_mapa:
        # Chama a lógica de mapa que foi isolada no arquivo maps.py
        maps.renderizar_secao_mapa()

    with col_menu_mapa:
        st.markdown("""
            <div class="menu-lateral-mapa">
                <div style="text-align: right; color: white;">☰</div>
                <br><br>
                <i>[CONSTRUIR PAINEL DE NAVEGAÇÃO DESSA ABA - ABA RETRÁTIL]</i>
            </div>
        """, unsafe_allow_html=True)

# --- ABA 2: CERRADO (ECC) ---
with aba_cerrado:
    st.write("### Conteúdo Específico: Cerrado (ECC)")
    if not df.empty:
        # Aqui pode futuramente filtrar o dataframe apenas para a concessão Cerrado
        st.dataframe(df, use_container_width=True)
    else:
        st.info("👈 Por favor, faça o upload do ficheiro BI - AMPLIAÇÃO na barra lateral para visualizar os dados.")

# --- ABA 3: MINAS GOIÁS (EMG) ---
with aba_minas:
    st.write("### Conteúdo Específico: Minas Goiás (EMG)")
    if not df.empty:
         # Aqui pode futuramente filtrar o dataframe apenas para a concessão Minas Goiás
        st.dataframe(df, use_container_width=True)
    else:
        st.info("👈 Por favor, faça o upload do ficheiro BI - AMPLIAÇÃO na barra lateral para visualizar os dados.")
