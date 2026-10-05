import streamlit as st
import folium
from streamlit_folium import st_folium
import zipfile
import xml.etree.ElementTree as ET
import requests
import os

def tentar_baixar_sharepoint(url):
    """Tenta baixar o KMZ do SharePoint forçando o parâmetro de download"""
    url_download = url.split("?")[0] + "?download=1"
    try:
        # Timeout curto para não travar a aplicação se pedir login corporativo
        response = requests.get(url_download, timeout=5)
        # Se for um ficheiro real (e não a página HTML de login da Microsoft)
        if response.status_code == 200 and not b"<html" in response.content[:100].lower():
            caminho_temp = "temp_sharepoint.kmz"
            with open(caminho_temp, "wb") as f:
                f.write(response.content)
            return caminho_temp
    except:
        pass
    return None

def extrair_linhas_kmz(caminho_arquivo):
    """Lê o KMZ como um ZIP, extrai o KML e varre as tags <coordinates>"""
    linhas = []
    try:
        with zipfile.ZipFile(caminho_arquivo, 'r') as z:
            kml_name = [f for f in z.namelist() if f.endswith('.kml')][0]
            kml_data = z.read(kml_name)
            
        root = ET.fromstring(kml_data)
        
        # Varre a árvore XML em busca de coordenadas ignorando namespaces
        for elem in root.iter():
            if 'coordinates' in elem.tag and elem.text:
                coords = elem.text.strip().split()
                linha = []
                for c in coords:
                    partes = c.split(',')
                    if len(partes) >= 2:
                        # O Folium renderiza mapas no padrão [Latitude, Longitude]
                        linha.append([float(partes[1]), float(partes[0])])
                if linha:
                    linhas.append(linha)
    except Exception as e:
        st.error(f"Erro ao extrair geometrias do KMZ: {e}")
    return linhas

def renderizar_secao_mapa():
    """Função principal que será chamada pelo app.py"""
    st.markdown('<div class="caixa-verde-clara" style="height: 500px; display:flex; align-items:center; justify-content:center;">', unsafe_allow_html=True)
    
    url_sharepoint = "https://grupoecorodovias-my.sharepoint.com/:u:/g/personal/vitor_r_silva_ecovias_com_br/IQBaIUMlc9GIRry8sGWW4mXJAXfSOIW8N2n_7g2POHDOs9o?e=3QttES"
    arquivo_local = "KMZ-TH15-149+000_150+600.kmz"
    caminho_kmz = None
    
    # 1. Tentativa de conexão com a Nuvem
    kmz_baixado = tentar_baixar_sharepoint(url_sharepoint)
    
    # 2. Definição da origem dos dados
    if kmz_baixado:
        caminho_kmz = kmz_baixado
        st.success("Traçado lido via SharePoint com sucesso!")
    elif os.path.exists(arquivo_local):
        caminho_kmz = arquivo_local
        st.success(f"Lido a partir do ficheiro local: {arquivo_local}")
    else:
        st.warning(f"O SharePoint bloqueou o acesso sem credenciais e o ficheiro {arquivo_local} não foi encontrado na pasta do GitHub.")
        
    # 3. Criação do Mapa Folium Base
    mapa = folium.Map(location=[-17.0, -49.0], zoom_start=6)
    
    # 4. Injeção do Traçado
    if caminho_kmz:
        linhas_tracado = extrair_linhas_kmz(caminho_kmz)
        
        for linha in linhas_tracado:
            folium.PolyLine(linha, color="#179C33", weight=5, opacity=0.8).add_to(mapa)
        
        # Foca a câmara automaticamente na primeira coordenada encontrada
        if linhas_tracado and linhas_tracado[0]:
            mapa.location = linhas_tracado[0][0]
            mapa.zoom_start = 14
            
    st_folium(mapa, width="100%", height=400)
    st.markdown('</div>', unsafe_allow_html=True)
