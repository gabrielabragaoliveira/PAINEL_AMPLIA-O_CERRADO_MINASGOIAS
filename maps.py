import streamlit as st
import folium
from streamlit_folium import st_folium
import zipfile
import xml.etree.ElementTree as ET
import os

def extrair_linhas_kmz(arquivo):
    """Abre o ficheiro KMZ, extrai o KML de dentro do ZIP e lê as coordenadas"""
    linhas = []
    try:
        with zipfile.ZipFile(arquivo, 'r') as z:
            # Encontra o ficheiro KML escondido dentro do KMZ
            kml_name = [f for f in z.namelist() if f.endswith('.kml')][0]
            kml_data = z.read(kml_name)
            
        root = ET.fromstring(kml_data)
        
        # Varre o XML em busca de tags de coordenadas geográficas
        for elem in root.iter():
            if 'coordinates' in elem.tag and elem.text:
                coords = elem.text.strip().split()
                linha = []
                for c in coords:
                    partes = c.split(',')
                    if len(partes) >= 2:
                        # Folium requer a ordem [Latitude, Longitude]
                        linha.append([float(partes[1]), float(partes[0])])
                if linha:
                    linhas.append(linha)
    except Exception as e:
        st.error(f"Erro ao ler o ficheiro KMZ: {e}")
    return linhas

def renderizar_painel_mapa():
    """Constrói o quadro do mapa e o menu lateral de projetos"""
    st.subheader("MAPA DE OBRAS")
    
    # Divide a tela: Quadro do mapa (largo) e Menu (estreito)
    col_mapa, col_menu = st.columns([3, 1])
    
    kmz_para_exibir = None

    # --- MENU LATERAL DIREITO ---
    with col_menu:
        st.markdown("#### 📂 Biblioteca de KMZs")
        st.caption("Projetos vinculados a esta secção.")
        
        # 1. Procura ficheiros KMZ que você já deixou na pasta do GitHub
        kmzs_locais = [f for f in os.listdir('.') if f.endswith('.kmz')]
        
        # 2. Caixa suspensa para escolher qual ficheiro visualizar
        projeto_selecionado = st.selectbox(
            "Projetos na Pasta:", 
            ["Nenhum"] + kmzs_locais
        )
        
        st.divider()
        
        # 3. Opção de carregar um projeto novo na hora (Upload)
        st.markdown("**Testar outro ficheiro?**")
        arquivo_upado = st.file_uploader("Upload de novo KMZ", type=["kmz"], label_visibility="collapsed")
        
        # Lógica de prioridade: O ficheiro carregado na hora sobrepõe a seleção da lista
        if arquivo_upado:
            kmz_para_exibir = arquivo_upado
            st.success(f"A ler: {arquivo_upado.name}")
        elif projeto_selecionado != "Nenhum":
            kmz_para_exibir = projeto_selecionado

    # --- QUADRO DO MAPA ---
    with col_mapa:
        st.markdown('<div class="caixa-verde-clara">', unsafe_allow_html=True)
        
        # Configuração do mapa focado na região central
        mapa = folium.Map(location=[-17.0, -49.0], zoom_start=6, tiles="CartoDB positron")
        
        if kmz_para_exibir:
            linhas = extrair_linhas_kmz(kmz_para_exibir)
            
            if linhas:
                for linha in linhas:
                    folium.PolyLine(linha, color="#179C33", weight=5, opacity=0.9).add_to(mapa)
                
                # Foca o mapa automaticamente nas coordenadas do projeto escolhido
                mapa.location = linhas[0][0]
                mapa.zoom_start = 14
            else:
                st.warning("O KMZ selecionado não contém linhas/traçados legíveis.")
        else:
            st.info("👈 Selecione ou faça o upload de um projeto KMZ no painel ao lado para visualizar o traçado.")
            
        st_folium(mapa, width="100%", height=500)
        st.markdown('</div>', unsafe_allow_html=True)
