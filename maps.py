import streamlit as st
import folium
from streamlit_folium import st_folium
import zipfile
import xml.etree.ElementTree as ET
import os

def extrair_linhas_kmz(arquivo):
    """Abre o ficheiro KMZ, extrai o KML e calcula os limites exatos (bounds) da obra"""
    linhas = []
    bounds = None
    try:
        with zipfile.ZipFile(arquivo, 'r') as z:
            # Encontra o ficheiro KML escondido dentro do KMZ
            kml_name = [f for f in z.namelist() if f.endswith('.kml')][0]
            kml_data = z.read(kml_name)
            
        root = ET.fromstring(kml_data)
        
        # Variáveis para calcular a "caixa" (bounding box) que envolve toda a obra
        min_lat, max_lat = float('inf'), float('-inf')
        min_lon, max_lon = float('inf'), float('-inf')
        
        # Varre o XML em busca de tags de coordenadas geográficas
        for elem in root.iter():
            if 'coordinates' in elem.tag and elem.text:
                # Remove quebras de linha que costumam corromper ficheiros exportados de CAD/Civil 3D
                coords_limpas = elem.text.replace('\n', ' ').strip()
                coords = coords_limpas.split()
                
                linha = []
                for c in coords:
                    partes = c.split(',')
                    if len(partes) >= 2:
                        lon = float(partes[0].strip())
                        lat = float(partes[1].strip())
                        linha.append([lat, lon]) # Folium requer a ordem [Latitude, Longitude]
                        
                        # Atualiza os limites extremos da obra para o zoom automático
                        if lat < min_lat: min_lat = lat
                        if lat > max_lat: max_lat = lat
                        if lon < min_lon: min_lon = lon
                        if lon > max_lon: max_lon = lon
                        
                if linha:
                    linhas.append(linha)
        
        # Se encontrou coordenadas válidas, cria a caixa de limites
        if linhas:
            bounds = [[min_lat, min_lon], [max_lat, max_lon]]
            
    except Exception as e:
        st.error(f"Erro ao ler o ficheiro KMZ: {e}")
        
    return linhas, bounds

def renderizar_painel_mapa():
    """Constrói o quadro do mapa e o menu lateral de projetos"""
    st.subheader("MAPA DE OBRAS")
    
    col_mapa, col_menu = st.columns([3, 1])
    kmz_para_exibir = None

    # --- MENU LATERAL DIREITO ---
    with col_menu:
        st.markdown("#### 📂 Biblioteca de KMZs")
        st.caption("Projetos vinculados a esta secção.")
        
        # Procura ficheiros KMZ locais
        kmzs_locais = [f for f in os.listdir('.') if f.endswith('.kmz')]
        projeto_selecionado = st.selectbox("Projetos na Pasta:", ["Nenhum"] + kmzs_locais)
        
        st.divider()
        st.markdown("**Testar outro ficheiro?**")
        arquivo_upado = st.file_uploader("Upload de novo KMZ", type=["kmz"], label_visibility="collapsed")
        
        if arquivo_upado:
            kmz_para_exibir = arquivo_upado
            st.success(f"A ler: {arquivo_upado.name}")
        elif projeto_selecionado != "Nenhum":
            kmz_para_exibir = projeto_selecionado

    # --- QUADRO DO MAPA ---
    with col_mapa:
        st.markdown('<div class="caixa-verde-clara">', unsafe_allow_html=True)
        
        # Mapa base (sem as marcas d'água de API Key)
        mapa = folium.Map(location=[-17.0, -49.0], zoom_start=6, tiles="OpenStreetMap")
        
        if kmz_para_exibir:
            # Chama a função que agora devolve tanto as linhas como os limites
            linhas, bounds = extrair_linhas_kmz(kmz_para_exibir)
            
            if linhas:
                # Desenha o traçado da rodovia no mapa
                for linha in linhas:
                    folium.PolyLine(linha, color="#179C33", weight=5, opacity=0.9).add_to(mapa)
                
                # CÂMARA AUTOMÁTICA: Obriga o mapa a fazer zoom exatamente no retângulo da obra
                if bounds:
                    mapa.fit_bounds(bounds)
            else:
                st.warning("O KMZ selecionado não contém traçados legíveis (apenas pontos ou ficheiro vazio).")
        else:
            st.info("👈 Selecione ou faça o upload de um projeto KMZ no painel ao lado para visualizar o traçado.")
            
        st_folium(mapa, width="100%", height=500)
        st.markdown('</div>', unsafe_allow_html=True)
