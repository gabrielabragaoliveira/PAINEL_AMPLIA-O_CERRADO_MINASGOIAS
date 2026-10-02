import streamlit as st
import pandas as pd
import os
import base64

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Obras Ampliação",
    page_icon="🚧",
    layout="wide"
)

# 2. Função para carregar o ficheiro CSS externo
def carregar_css(arquivo_css):
    with open(arquivo_css) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    carregar_css("style.css")
except FileNotFoundError:
    st.warning("Ficheiro style.css não encontrado.")

# 3. Função para carregar imagens locais para o HTML
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Tenta carregar as imagens. Se não encontrar, fica em branco para não quebrar a aplicação
img_minas_goias = ""
img_cerrado = ""

if os.path.exists("Ecovias Minas Goias_Logo (1).png"):
    img_minas_goias = f"data:image/png;base64,{get_base64_of_bin_file('Ecovias Minas Goias_Logo (1).png')}"
    
if os.path.exists("Ecovias_Cerrado_Logo_Vertical_RGB_Preferencial_20241212_Keenwork_AF.png"):
    img_cerrado = f"data:image/png;base64,{get_base64_of_bin_file('Ecovias_Cerrado_Logo_Vertical_RGB_Preferencial_20241212_Keenwork_AF.png')}"

# Renderizando o Cabeçalho Superior com as imagens
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
estado = st.sidebar.selectbox("ESTADO / REGIÃO", ["Minas", "Goiás", "Contorno Uberlândia"])

# Exibição INFORMATIVA dos limites do trecho (apenas texto, não é um input)
st.sidebar.markdown("---")
st.sidebar.markdown("**LIMITES DO TRECHO:**")

if concessao == "Minas Goiás":
    if estado == "Minas":
        st.sidebar.info("KM 207+300 ao 77+400\n\nKM 65+473 ao 00+000")
    elif estado == "Goiás":
        st.sidebar.info("KM 314+000 ao 95+700")
    elif estado == "Contorno Uberlândia":
        st.sidebar.info("KM 00+000 ao 21+000")
elif concessao == "Cerrado":
    st.sidebar.info("Limites não especificados.")
    
st.sidebar.markdown("---")

# Inputs de OBRA e KM
obra = st.sidebar.text_input("OBRA", placeholder="Digite a obra...")
km = st.sidebar.text_input("KM", placeholder="Ex: 120+500")

# 5. Integração com os dados do BI - AMPLIAÇÃO
@st.cache_data
def carregar_dados():
    arquivos = [f for f in os.listdir('.') if "BI - AMPLIAÇÃO" in f]
    if arquivos:
        caminho_arquivo = arquivos[0]
        try:
            if caminho_arquivo.endswith('.xlsx') or caminho_arquivo.endswith('.xls'):
                df = pd.read_excel(caminho_arquivo)
            else:
                df = pd.read_csv(caminho_arquivo)
            return df
        except Exception as e:
            st.error(f"Erro ao ler o ficheiro: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

df = carregar_dados()

# 6. Área Central (Exibição)
st.write("### Resumo do Filtro Atual")
st.success(f"**Concessão:** {concessao} | **Estado:** {estado} | **Obra:** {obra if obra else 'Não informada'} | **KM:** {km if km else 'Não informado'}")

st.divider()

if not df.empty:
    st.write("✅ **Dados carregados com sucesso a partir do ficheiro BI - AMPLIAÇÃO!**")
    st.dataframe(df, use_container_width=True)
else:
    st.info("O ficheiro **BI - AMPLIAÇÃO** não foi encontrado na pasta ou está vazio.")
