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
