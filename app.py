import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração inicial da página
st.set_page_config(
    page_title="Painel Ampliação Cerrado",
    page_icon="🚧",
    layout="wide"
)

st.title("🚧 Painel de Controle - Ampliação Cerrado (Minas/Goiás)")
st.markdown("Visualização de dados do projeto ECO-GO050.")

# 2. Carregamento dos dados
# O @st.cache_data garante que a planilha pesada não seja recarregada toda vez que você clicar em algo
@st.cache_data
def carregar_dados():
    caminho_arquivo = "7.ECO-GO050-000278-PL-X2-01-R05_COC-Completo.xlsx"
    try:
        # Caso a planilha tenha várias abas, você pode especificar com sheet_name='Nome_da_Aba'
        df = pd.read_excel(caminho_arquivo)
        return df
    except FileNotFoundError:
        st.error(f"Arquivo '{caminho_arquivo}' não encontrado na pasta.")
        return pd.DataFrame()

df = carregar_dados()

if not df.empty:
    # 3. Barra Lateral (Sidebar) para Filtros
    st.sidebar.header("🔍 Filtros do Projeto")
    
    # Exemplo: Pegue uma coluna de "Status", "Trecho" ou "Disciplina" da sua planilha
    # Substitua 'Status_da_Obra' pelo nome exato da coluna na sua planilha Excel
    coluna_filtro_1 = "Status" # <-- Altere aqui
    
    if coluna_filtro_1 in df.columns:
        opcoes = df[coluna_filtro_1].dropna().unique()
        selecao = st.sidebar.multiselect(f"Filtrar por {coluna_filtro_1}:", opcoes, default=opcoes)
        df_filtrado = df[df[coluna_filtro_1].isin(selecao)]
    else:
        df_filtrado = df
        st.sidebar.warning(f"Coluna '{coluna_filtro_1}' não encontrada. Filtro desativado.")

    # 4. Cartões de Indicadores (KPIs)
    st.subheader("Resumo Executivo")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total de Linhas/Itens", len(df_filtrado))
    
    # Exemplo de outras métricas que você pode querer calcular:
    # Se houver uma coluna de "Avanço" ou "Volume":
    # avanco_medio = df_filtrado['Avanco_Fisico'].mean()
    # col2.metric("Avanço Físico Médio", f"{avanco_medio:.2f}%")
    
    st.divider()

    # 5. Gráficos Interativos (Plotly)
    st.subheader("Análise Gráfica")
    colA, colB = st.columns(2)
    
    with colA:
        # Substitua 'Disciplina' ou 'Trecho' por colunas reais do seu arquivo
        coluna_grafico_barras = "Trecho" # <-- Altere aqui
        if coluna_grafico_barras in df_filtrado.columns:
            contagem = df_filtrado[coluna_grafico_barras].value_counts().reset_index()
            contagem.columns = [coluna_grafico_barras, 'Quantidade']
            fig_bar = px.bar(contagem, x=coluna_grafico_barras, y='Quantidade', 
                             title=f"Itens por {coluna_grafico_barras}",
                             color='Quantidade', color_continuous_scale="Blues")
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("Ajuste a variável `coluna_grafico_barras` para visualizar o gráfico.")

    with colB:
        coluna_grafico_pizza = "Status" # <-- Altere aqui
        if coluna_grafico_pizza in df_filtrado.columns:
            fig_pie = px.pie(df_filtrado, names=coluna_grafico_pizza, 
                             title=f"Distribuição de {coluna_grafico_pizza}", hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("Ajuste a variável `coluna_grafico_pizza` para visualizar o gráfico.")

    # 6. Tabela Completa
    st.subheader("Tabela de Dados Filtrada")
    st.dataframe(df_filtrado, use_container_width=True)

else:
    # Caso o arquivo fixo não esteja presente, exibe um uploader de fallback
    st.warning("Envie a planilha manualmente para testar o painel:")
    arquivo_upado = st.file_uploader("Faça o upload do .xlsx", type=["xlsx", "xls"])
    if arquivo_upado:
        df_upado = pd.read_excel(arquivo_upado)
        st.success("Arquivo carregado! Altere o código para usar os nomes de colunas exibidos abaixo:")
        st.write(df_upado.columns.tolist())
        st.dataframe(df_upado)
