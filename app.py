import streamlit as st
import pandas as pd
import os

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

# Executa o CSS
try:
    carregar_css("style.css")
except FileNotFoundError:
    st.warning("Ficheiro style.css não encontrado. Verifique se ele está na mesma pasta.")

# 3. Renderizando o Cabeçalho Superior
st.markdown("""
    <div class="cabecalho">
        <h1>OBRAS AMPLIAÇÃO</h1>
        <div class="logos">
            <div class="logo-badge">ecovias Cerrado</div>
            <div class="logo-badge">ecovias Minas Goiás</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 4. Barra Lateral (PAINEL DE CONTROLE)
st.sidebar.markdown("### PAINEL DE CONTROLE")

concessao = st.sidebar.selectbox("CONCESSÃO", ["Cerrado", "Minas Goiás"])

# Lógica inteligente com a ordem atualizada
if concessao == "Minas Goiás":
    estado = st.sidebar.selectbox("ESTADO / REGIÃO", ["Minas", "Goiás", "Contorno Uberlândia"])
    
    # OBRA logo após o Estado
    obra = st.sidebar.text_input("OBRA", placeholder="Digite a obra...")
    
    # Lógica de KM dinâmica no final
    if estado == "Minas":
        opcoes_km = [
            "Todos",
            "Trecho 1: KM 207+300 ao 77+400", 
            "Trecho 2: KM 65+473 ao 00+000",
            "KM Específico (Digitar)"
        ]
    elif estado == "Goiás":
        opcoes_km = [
            "Todos",
            "Trecho Único: KM 314+000 ao 95+700",
            "KM Específico (Digitar)"
        ]
    elif estado == "Contorno Uberlândia":
        opcoes_km = [
            "Todos",
            "Trecho Único: KM 00+000 ao 21+000",
            "KM Específico (Digitar)"
        ]
    
    selecao_trecho = st.sidebar.selectbox("TRECHO (KM)", opcoes_km)
    
    if selecao_trecho == "KM Específico (Digitar)":
        km = st.sidebar.text_input("Digite o KM exato", placeholder="Ex: 120+500")
    else:
        km = selecao_trecho

else:
    # Ordem padrão para concessão "Cerrado"
    estado = st.sidebar.selectbox("ESTADO", ["Minas", "Goiás"])
    obra = st.sidebar.text_input("OBRA", placeholder="Digite a obra...")
    km = st.sidebar.text_input("KM", placeholder="Ex: 120+500")

# 5. Integração com os dados do BI - AMPLIAÇÃO
@st.cache_data
def carregar_dados():
    # O script busca automaticamente o ficheiro "BI - AMPLIAÇÃO"
    arquivos = [f for f in os.listdir('.') if "BI - AMPLIAÇÃO" in f]
    
    if arquivos:
        caminho_arquivo = arquivos[0]
        try:
            # Caso seja Excel (.xlsx ou .xls)
            if caminho_arquivo.endswith('.xlsx') or caminho_arquivo.endswith('.xls'):
                df = pd.read_excel(caminho_arquivo)
            else:
                # Caso seja CSV
                df = pd.read_csv(caminho_arquivo)
            return df
        except Exception as e:
            st.error(f"Erro ao ler o ficheiro: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

df = carregar_dados()

# 6. Área Central (Exibição)
st.write("### Resumo do Filtro Atual")
st.success(f"**Concessão:** {concessao} | **Estado:** {estado} | **Obra:** {obra if obra else 'Todas'} | **KM:** {km if km else 'Todos'}")

st.divider()

if not df.empty:
    st.write("✅ **Dados carregados com sucesso a partir do ficheiro BI - AMPLIAÇÃO!**")
    
    # Exibindo a tabela na tela
    st.dataframe(df, use_container_width=True)
else:
    st.info("O ficheiro **BI - AMPLIAÇÃO** não foi encontrado na pasta ou está vazio. Certifique-se de que fez o upload no seu repositório.")
