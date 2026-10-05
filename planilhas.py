import streamlit as st
import pandas as pd
import plotly.express as px

# 1. FUNÇÃO BASE: LÊ E LIMPA O EXCEL
@st.cache_data
def carregar_dados_resumo(upload):
    """Lê a aba QUADRO RESUMO ignorando as quebras de linha e totais"""
    if upload is not None:
        try:
            # header=[1, 2] indica que as linhas 2 e 3 do Excel formam o cabeçalho
            df = pd.read_excel(upload, sheet_name="QUADRO RESUMO", header=[1, 2])
            
            # Captura a primeira coluna que contém os nomes dos trechos
            coluna_trechos = df.columns[0]
            
            # Limpeza
            df = df.dropna(subset=[coluna_trechos])
            df = df[~df[coluna_trechos].astype(str).str.upper().str.contains("TOTAL")]
            
            return df, coluna_trechos
        except Exception as e:
            st.error(f"Erro ao ler a aba QUADRO RESUMO da planilha: {e}")
            return pd.DataFrame(), None
    return pd.DataFrame(), None


# 2. FUNÇÃO DA ABA 1: QUADRO DE RESUMO (Geral)
def renderizar_resumo(arquivo_upado):
    """Constrói os gráficos gerais e os indicadores da aba de resumo"""
    st.subheader("RESUMO")
    col_esquerda, col_direita = st.columns([3, 1])
    
    df_resumo, col_trechos = carregar_dados_resumo(arquivo_upado)
    
    with col_esquerda:
        if not df_resumo.empty:
            abas_servicos = st.tabs([
                "Serviços Preliminares", "Terraplenagem", "Regularização", 
                "Sub-base", "Base", "Revestimento", "Drenagem", "Paisagismo"
            ])
            
            servicos = [
                "Serviços preliminares", "Terraplenagem", "Regularização do subleito",
                "Sub-base", "Base", "Revestimento", "Drenagem", "Paisagismo"
            ]
            
            for aba, nome_servico in zip(abas_servicos, servicos):
                with aba:
                    try:
                        df_grafico = pd.DataFrame({
                            'Trecho': df_resumo[col_trechos],
                            'Extensão (m)': df_resumo[(nome_servico, 'Extensão (m)')],
                            'Executado': df_resumo[(nome_servico, 'Executado')]
                        })
                        
                        df_grafico['Extensão (m)'] = pd.to_numeric(df_grafico['Extensão (m)'], errors='coerce').fillna(0)
                        df_grafico['Executado'] = pd.to_numeric(df_grafico['Executado'], errors='coerce').fillna(0)
                        
                        fig = px.bar(
                            df_grafico, x='Trecho', y=['Extensão (m)', 'Executado'],
                            barmode='group', title=nome_servico.upper(),
                            color_discrete_map={'Extensão (m)': '#D3D3D3', 'Executado': '#179C33'}
                        )
                        fig.update_layout(xaxis_title="", yaxis_title="Metros", legend_title="")
                        st.plotly_chart(fig, use_container_width=True)
                        
                    except KeyError:
                        st.warning(f"A coluna '{nome_servico}' não foi encontrada.")
        else:
            st.markdown('<div class="caixa-verde-clara" style="height: 400px; display:flex; align-items:center; justify-content:center;"><i>Faça o upload do BI - AMPLIAÇÃO para ver os gráficos.</i></div>', unsafe_allow_html=True)

    with col_direita:
        st.markdown('<div class="titulo-verde">EM ANDAMENTO</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: st.markdown('<div class="caixa-indicador">[CERRADO]</div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="caixa-indicador">[MINAS GOIÁS]</div>', unsafe_allow_html=True)
        
        st.write("") 
        
        st.markdown('<div class="titulo-verde">PREVISTO A INICIAR</div>', unsafe_allow_html=True)
        c3, c4 = st.columns(2)
        with c3: st.markdown('<div class="caixa-indicador">[CERRADO]</div>', unsafe_allow_html=True)
        with c4: st.markdown('<div class="caixa-indicador">[MINAS GOIÁS]</div>', unsafe_allow_html=True)


# 3. FUNÇÃO DA ABA 2: CERRADO (Por Disciplina e Projeto)
def renderizar_cerrado(arquivo_upado):
    """Constrói os gráficos individuais por disciplina específicos para a aba Cerrado"""
    st.subheader("📊 Análise de Projetos - CERRADO (ECC)")
    
    if arquivo_upado is not None:
        df, col_trechos = carregar_dados_resumo(arquivo_upado)
        
        if not df.empty:
            st.markdown('<div class="caixa-verde-clara">', unsafe_allow_html=True)
            
            # Filtro Interativo por Projeto
            projetos = df[col_trechos].dropna().unique()
            projeto_selecionado = st.selectbox("📌 Selecione o Projeto / Trecho:", projetos)
            
            df_projeto = df[df[col_trechos] == projeto_selecionado]
            
            disciplinas = [
                "Serviços preliminares", "Terraplenagem", "Regularização do subleito",
                "Sub-base", "Base", "Revestimento", "Drenagem", "Paisagismo"
            ]
            
            st.divider()
            st.markdown(f"<h4 style='text-align: center; color: #179C33;'>Avanço Físico por Disciplina: {projeto_selecionado}</h4>", unsafe_allow_html=True)
            st.write("")
            
            # Grelha de 4 colunas
            colunas_grid = st.columns(4)
            
            for i, disc in enumerate(disciplinas):
                try:
                    extensao = pd.to_numeric(df_projeto[(disc, 'Extensão (m)')].values[0], errors='coerce')
                    executado = pd.to_numeric(df_projeto[(disc, 'Executado')].values[0], errors='coerce')
                    
                    df_grafico = pd.DataFrame({
                        'Métrica': ['Extensão (m)', 'Executado'],
                        'Metros': [extensao, executado]
                    })
                    
                    fig = px.bar(
                        df_grafico, x='Métrica', y='Metros', color='Métrica',
                        color_discrete_map={'Extensão (m)': '#D3D3D3', 'Executado': '#179C33'},
                        title=disc.upper()
                    )
                    
                    fig.update_layout(
                        showlegend=False, xaxis_title="", yaxis_title="",
                        title_x=0.5, margin=dict(l=20, r=20, t=40, b=20), height=300
                    )
                    
                    colunas_grid[i % 4].plotly_chart(fig, use_container_width=True)
                    
                except (KeyError, IndexError):
                    pass 
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Não foi possível carregar os dados. O ficheiro pode estar vazio.")
    else:
        st.info("👈 Faça o upload do ficheiro base na barra lateral para visualizar o avanço do Cerrado.")
