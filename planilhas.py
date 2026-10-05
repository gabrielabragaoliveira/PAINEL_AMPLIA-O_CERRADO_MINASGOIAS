def renderizar_cerrado(arquivo_upado):
    """Constrói os gráficos por disciplina específicos para a aba Cerrado"""
    st.subheader("📊 Análise de Projetos - CERRADO (ECC)")
    
    if arquivo_upado is not None:
        # Reutilizamos a inteligência de leitura do MultiIndex do Excel
        df, col_trechos = carregar_dados_resumo(arquivo_upado)
        
        if not df.empty:
            st.markdown('<div class="caixa-verde-clara">', unsafe_allow_html=True)
            
            # 1. Filtro Interativo por Projeto
            projetos = df[col_trechos].dropna().unique()
            projeto_selecionado = st.selectbox("📌 Selecione o Projeto / Trecho:", projetos)
            
            df_projeto = df[df[col_trechos] == projeto_selecionado]
            
            # Lista das disciplinas presentes no nível superior do seu Excel
            disciplinas = [
                "Serviços preliminares", "Terraplenagem", "Regularização do subleito",
                "Sub-base", "Base", "Revestimento", "Drenagem", "Paisagismo"
            ]
            
            st.divider()
            st.markdown(f"<h4 style='text-align: center; color: #179C33;'>Avanço Físico por Disciplina: {projeto_selecionado}</h4>", unsafe_allow_html=True)
            st.write("")
            
            # 2. Criação de uma Grelha Dinâmica (4 colunas para distribuir os gráficos de forma limpa)
            colunas_grid = st.columns(4)
            
            for i, disc in enumerate(disciplinas):
                try:
                    # Extrai os valores exatos daquele projeto e daquela disciplina
                    extensao = pd.to_numeric(df_projeto[(disc, 'Extensão (m)')].values[0], errors='coerce')
                    executado = pd.to_numeric(df_projeto[(disc, 'Executado')].values[0], errors='coerce')
                    
                    df_grafico = pd.DataFrame({
                        'Métrica': ['Extensão (m)', 'Executado'],
                        'Metros': [extensao, executado]
                    })
                    
                    # Cria um mini-gráfico de barras para a disciplina
                    fig = px.bar(
                        df_grafico, 
                        x='Métrica', 
                        y='Metros',
                        color='Métrica',
                        color_discrete_map={'Extensão (m)': '#D3D3D3', 'Executado': '#179C33'},
                        title=disc.upper()
                    )
                    
                    # Limpa o layout para não poluir a tela com excesso de eixos e legendas
                    fig.update_layout(
                        showlegend=False, 
                        xaxis_title="", 
                        yaxis_title="",
                        title_x=0.5, # Centraliza o título do gráfico
                        margin=dict(l=20, r=20, t=40, b=20),
                        height=300
                    )
                    
                    # Distribui o gráfico ciclicamente pelas 4 colunas (0, 1, 2, 3)
                    colunas_grid[i % 4].plotly_chart(fig, use_container_width=True)
                    
                except (KeyError, IndexError):
                    # Se o gestor não preencheu essa disciplina no Excel para este projeto, o Python ignora silenciosamente
                    pass 
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("Não foi possível carregar os dados. O ficheiro pode estar vazio ou com o cabeçalho alterado.")
    else:
        st.info("👈 Faça o upload do ficheiro base na barra lateral para visualizar o avanço do Cerrado.")
