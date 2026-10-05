import streamlit as st
import folium
from streamlit_folium import st_folium
import zipfile
import xml.etree.ElementTree as ET
import os

def extrair_elementos_kmz(arquivo):
    """Abre o ficheiro KMZ, extrai Linhas, Pontos e os Limites exatos da obra"""
    elementos = {'linhas': [], 'pontos': []}
    bounds = [[float('inf'), float('inf')], [float('-inf'), float('-inf')]] # [min_lat, min_lon], [max_lat, max_lon]
    tem_coordenadas = False

    try:
        with zipfile.ZipFile(arquivo, 'r') as z:
            kml_name = [f for f in z.namelist() if f.endswith('.kml')][0]
            kml_data = z.read(kml_name)
            
        root = ET.fromstring(kml_data)
        
        # Varre cada Placemark (Pasta de marcação do Google Earth)
        for placemark in root.iter():
            if placemark.tag.endswith('Placemark'):
                
                # Tenta capturar o nome do ponto/linha para mostrar no mapa
                nome_elemento = "Pino/Traçado"
                for name_tag in placemark.iter():
                    if name_tag.tag.endswith('name') and name_tag.text:
                        nome_elemento = name_tag.text
                        break

                # 1. Procura por Pontos (Pinos)
                for point in placemark.iter():
                    if point.tag.endswith('Point'):
                        for coords in point.iter():
                            if coords.tag.endswith('coordinates') and coords.text:
                                c = coords.text.strip().split(',')
                                if len(c) >= 2:
                                    lon, lat = float(c[0].strip()), float(c[1].strip())
                                    elementos['pontos'].append({'nome': nome_elemento, 'coord': [lat, lon]})
                                    
                                    bounds[0][0], bounds[0][1] = min(bounds[0][0], lat), min(bounds[0][1], lon)
                                    bounds[1][0], bounds[1][1] = max(bounds[1][0], lat), max(bounds[1][1], lon)
                                    tem_coordenadas = True

                # 2. Procura por Linhas (Traçados)
                for linestring in placemark.iter():
                    if linestring.tag.endswith('LineString'):
                        for coords in linestring.iter():
                            if coords.tag.endswith('coordinates') and coords.text:
                                coords_limpas = coords.text.replace('\n', ' ').strip()
                                pares = coords_limpas.split()
                                linha = []
                                for p in pares:
                                    c = p.split(',')
                                    if len(c) >= 2:
                                        lon, lat = float(c[0].strip()), float(c[1].strip())
                                        linha.append([lat, lon])
                                        
                                        bounds[0][0], bounds[0][1] = min(bounds[0][0], lat), min(bounds[0][1], lon)
                                        bounds[1][0], bounds[1][1] = max(bounds[1][0], lat), max(bounds[1][1], lon)
                                        tem_coordenadas = True
                                        
                                if linha:
                                    elementos['linhas'].append({'nome': nome_elemento, 'coords': linha})

    except Exception as e:
        st.error(f"Erro ao ler o ficheiro KMZ: {e}")
        
    return elementos, (bounds if tem_coordenadas else None)

def renderizar_painel_mapa():
    """Constrói o quadro do mapa de satélite e o menu lateral"""
    st.subheader("MAPA DE OBRAS (VISUALIZAÇÃO SATÉLITE)")
    
    col_mapa, col_menu = st.columns([3, 1])
    kmz_para_exibir = None

    # --- MENU LATERAL DIREITO ---
    with col_menu:
        st.markdown("#### 📂 Biblioteca de KMZs")
        st.caption("Projetos vinculados a esta secção.")
        
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
        
        # Mapa base de Satélite (Esri World Imagery - Alta Resolução)
        mapa = folium.Map(
            location=[-17.0, -49.0], 
            zoom_start=6, 
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri World Imagery'
        )
        
        if kmz_para_exibir:
            elementos, bounds = extrair_elementos_kmz(kmz_para_exibir)
            
            if elementos['linhas'] or elementos['pontos']:
                
                # Renderiza as linhas em Amarelo para destacar sobre o fundo de satélite
                for linha in elementos['linhas']:
                    folium.PolyLine(
                        linha['coords'], 
                        color="#FFD700", # Amarelo Ouro
                        weight=5, 
                        opacity=0.9,
                        tooltip=f"Traçado: {linha['nome']}"
                    ).add_to(mapa)
                
                # Renderiza os Pinos com popups clicáveis
                for ponto in elementos['pontos']:
                    folium.Marker(
                        location=ponto['coord'],
                        popup=ponto['nome'],
                        tooltip="Clique para ver o pino",
                        icon=folium.Icon(color='red', icon='info-sign')
                    ).add_to(mapa)
                
                # Foca o mapa na obra
                if bounds:
                    mapa.fit_bounds(bounds)
            else:
                st.warning("O KMZ selecionado não contém traçados ou pinos legíveis.")
        else:
            st.info("👈 Selecione ou faça o upload de um projeto KMZ no painel ao lado.")
            
        st_folium(mapa, width="100%", height=500)
        st.markdown('</div>', unsafe_allow_html=True)
