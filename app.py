import streamlit as st
import os
import base64
import maps
import planilhas # Importa o novo módulo de dados

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

if concessao == "Minas Goiás":
    opcoes_estado = ["Minas", "Goiás", "Contorno Uberlândia"]
else:
    opcoes_estado = ["Minas", "Goiás"]

estado = st.sidebar.selectbox("ESTADO / REGIÃO", opcoes_estado)

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


# 5. Navegação Principal (Abas Horizontais)
aba_resumo, aba_cerrado, aba_minas = st.tabs(["QUADRO DE RESUMO", "CERRADO (ECC)", "MINAS GOIÁS (EMG)"])

# --- ABA 1: QUADRO DE RESUMO ---
with aba_resumo:
    
    # Chama o layout de gráficos do planilhas.py e passa o ficheiro para ele
    planilhas.renderizar_resumo(arquivo_upado)

    st.divider()

    # --- SEÇÃO DO MAPA ---
    # Chama a estrutura visual do mapa e do menu lateral gerida pelo maps.py
    maps.renderizar_painel_mapa()

# --- ABA 2: CERRADO (ECC) ---
with aba_cerrado:
    # Chama a função que criamos no planilhas.py, injetando o ficheiro carregado
    planilhas.renderizar_cerrado(arquivo_upado)

# --- ABA 3: MINAS GOIÁS (EMG) ---
with aba_minas:
    st.write("### Conteúdo Específico: Minas Goiás (EMG)")
    st.info("👈 Faça o upload do ficheiro BI - AMPLIAÇÃO na barra lateral.")
