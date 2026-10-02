import streamlit as st
import pandas as pd
import os

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Obras Ampliação",
    page_icon="🚧",
    layout="wide"
)

# 2. Função para carregar o arquivo CSS externo
def carregar_css(arquivo_css):
    with open(arquivo_css) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Executa o CSS
try:
    carregar_css("style.css")
except FileNotFoundError:
    st.warning("Arquivo style.css não encontrado. Verifique se ele está na mesma pasta.")

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
estado = st.sidebar.selectbox("ESTADO", ["Minas", "Goiás"])
obra = st.sidebar.text_input("OBRA", placeholder="Digite a obra...")
km = st.sidebar.text_input("KM", placeholder="Ex: 120+500")

# 5. Integração com os dados do BI - AMPLIAÇÃO
@st.cache_data
def carregar_dados():
    # O script busca automaticamente o arquivo "BI - AMPLIAÇÃO"
    # Adicione a extensão correta (.xlsx, .xls ou .csv) caso necessário.
    arquivos = [f for f in os.listdir('.') if "BI - AMPLIAÇÃO" in f]
    
    if arquivos:
        caminho_arquivo = arquivos[0]
        try:
            # Caso seja Excel (.xlsx)
            if caminho_arquivo.endswith('.xlsx') or caminho_arquivo.endswith('.xls'):
                df = pd.read_excel(caminho_arquivo)
            else:
                # Caso seja CSV
                df = pd.read_csv(caminho_arquivo)
            return df
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

df = carregar_dados()

# 6. Área Central (Exibição)
st.write("### Resumo do Filtro Atual")
st.success(f"**Concessão:** {concessao} | **Estado:** {estado} | **Obra:** {obra if obra else 'Todas'} | **KM:** {km if km else 'Todos'}")

st.divider()

if not df.empty:
    st.write("✅ **Dados carregados com sucesso a partir do arquivo BI - AMPLIAÇÃO!**")
    
    # Aqui você pode aplicar os filtros da barra lateral no seu dataframe
    # Exemplo: df_filtrado = df[df['Estado'] == estado] (depende dos nomes das colunas)
    
    # Exibindo uma amostra da tabela na tela
    st.dataframe(df, use_container_width=True)
else:
    st.info("O arquivo **BI - AMPLIAÇÃO** não foi encontrado na pasta ou está vazio. Certifique-se de que ele foi feito o upload no seu repositório.")
