import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def carregar_dados_resumo(upload):
    """Lê a aba QUADRO RESUMO ignorando as quebras de linha e totais"""
    if upload is not None:
        try:
            # header=[1, 2] indica que as linhas 2 e 3 do Excel formam o cabeçalho
            df = pd.read_excel(upload, sheet_name="QUADRO RESUMO", header=[1, 2])
            
            # A Coluna A geralmente fica sem nome no nível 0, vamos capturá-la
            coluna_trechos = df.columns[0]
            
            # 1. Limpeza: Remove linhas vazias
            df = df.dropna(subset=[coluna_trechos])
            
            # 2. Limpeza: Remove a linha "TOTAL" e os seus erros
            df = df[~df[coluna_trechos].astype(str).str.upper().str.contains("TOTAL")]
            
            return df, coluna_trechos
        except Exception as e:
            st.error(f"Erro ao ler a aba QUADRO RESUMO da planilha: {e}")
            return pd.DataFrame(), None
    return pd.DataFrame(), None

def renderizar_resumo(arquivo_upado):
    """Constrói os gráficos e os indicadores da aba de resumo"""
    st.subheader("RESUMO")
    col_esquerda, col_direita = st.columns([3, 1])
    
    # Processa os dados
    df_resumo, col_trechos = carregar_dados_resumo(arquivo_upado)
    
    with col_esquerda:
        if not df_resumo.empty:
            # Cria abas internas para navegar entre os diferentes serviços sem poluir a tela
            abas_servicos = st.tabs([
                "Serviços Preliminares", "Terraplenagem", "Regularização", 
                "Sub-base", "Base", "Revestimento", "Drenagem", "Paisagismo"
            ])
            
            # Dicionário mapeando o nome da aba para o nome exato no Excel
            servicos = [
                "Serviços preliminares", "Terraplenagem", "Regularização do subleito",
                "Sub-base", "Base", "Revestimento", "Drenagem", "Paisagismo"
            ]
            
            for aba, nome_servico in zip(abas_servicos, servicos):
                with aba:
                    try:
                        # Prepara os dados matemáticos para o Plotly
                        df_grafico = pd.DataFrame({
                            'Trecho': df_resumo[col_trechos],
                            'Extensão (m)': df_resumo[(nome_servico, 'Extensão (m)')],
                            'Executado': df_resumo[(nome_servico, 'Executado')]
                        })
                        
                        # Converte para numérico (força erros como '-' a virarem 0)
                        df_grafico['Extensão (m)'] = pd.to_numeric(df_grafico['Extensão (m)'], errors='coerce').fillna(0)
                        df_grafico['Executado'] = pd.to_numeric(df_grafico['Executado'], errors='coerce').fillna(0)
                        
                        # Cria o gráfico de barras dinâmico
                        fig = px.bar(
                            df_grafico, 
                            x='Trecho', 
                            y=['Extensão (m)', 'Executado'],
                            barmode='group',
                            title=nome_servico.upper(),
                            color_discrete_map={'Extensão (m)': '#D3D3D3', 'Executado': '#179C33'}
                        )
                        fig.update_layout(xaxis_title="", yaxis_title="Metros", legend_title="")
                        st.plotly_chart(fig, use_container_width=True)
                        
                    except KeyError:
                        st.warning(f"A coluna '{nome_servico}' não foi encontrada. Verifique a ortografia do ficheiro.")
        else:
            st.markdown('<div class="caixa-verde-clara" style="height: 400px; display:flex; align-items:center; justify-content:center;"><i>Faça o upload do BI - AMPLIAÇÃO para ver os gráficos.</i></div>', unsafe_allow_html=True)

    # --- PAINEL DIREITO (INDICADORES) ---
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
