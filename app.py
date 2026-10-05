import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
import base64
import json

st.set_page_config(page_title="Obras Ampliação", page_icon="🚧", layout="wide")

# 1. Funções de Carregamento (CSS e Imagens)
def carregar_css(arquivo_css):
    try:
        with open(arquivo_css) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

carregar_css("style.css")

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

img_minas_goias = ""
img_cerrado = ""
if os.path.exists("Ecovias Minas Goias_Logo (1).png"):
    img_minas_goias = f"data:image/png;base64,{get_base64_of_bin_file('Ecovias Minas Goias_Logo (1).png')}"
if os.path.exists("Ecovias_Cerrado_Logo_Vertical_RGB_Preferencial_20241212_Keenwork_AF.png"):
    img_cerrado = f"data:image/png;base64,{get_base64_of_bin_file('Ecovias_Cerrado_Logo_Vertical_RGB_Preferencial_20241212_Keenwork_AF.png')}"

# 2. Cabeçalho Superior
st.markdown(f"""
    <div class="cabecalho">
        <h1>OBRAS AMPLIAÇÃO</h1>
        <div class="logos">
            {'<img src="' + img_cerrado + '" class="logo-img">' if img_cerrado else ''}
            {'<img src="' + img_minas_goias + '" class="logo-img">' if img_minas_goias else ''}
        </div>
    </div>
""", unsafe_allow_html=True)

# 3. Navegação Principal (Abas Horizontais)
aba_resumo, aba_cerrado, aba_minas = st.tabs(["QUADRO DE RESUMO", "CERRADO (ECC)", "MINAS GOIÁS (EMG)"])

# --- ABA 1: QUADRO DE RESUMO ---
with aba_resumo:
    st.subheader("RESUMO")
    
    col_esquerda, col_direita = st.columns([2, 1])
    
    with col_esquerda:
        st.markdown('<div class="caixa-verde-clara" style="height: 400px; display:flex; align-items:center; justify-content:center;"><i>[INSERIR GRÁFICOS DE RESUMO AQUI]</i></div>', unsafe_allow_html=True)

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

    st.divider()

    # --- SEÇÃO DO MAPA ---
    st.subheader("MAPA DE OBRAS")
    
    col_mapa, col_menu_mapa = st.columns([3, 1])
    
    with col_mapa:
        st.markdown('<div class="caixa-verde-clara" style="height: 500px; display:flex; align-items:center; justify-content:center;">', unsafe_allow_html=True)
        
        # Alterado para receber GeoJSON
        arquivo_geo = st.file_uploader("Upload Traçado (GeoJSON)", type=["geojson", "json"], key="geo_resumo")
        
        mapa = folium.Map(location=[-17.0, -49.0], zoom_start=6)
        
        if arquivo_geo:
            try:
                # Carrega nativamente pelo JSON do Python (sem Geopandas)
                geo_data = json.load(arquivo_geo)
                folium.GeoJson(
                    geo_data,
                    style_function=lambda feature: {
                        'color': '#179C33',
                        'weight': 3,
                    }
                ).add_to(mapa)
                st.success("Mapa renderizado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao processar o arquivo: {e}")
        
        st_folium(mapa, width="100%", height=400)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_menu_mapa:
        st.markdown("""
            <div class="menu-lateral-mapa">
                <div style="text-align: right; color: white;">☰</div>
                <br><br>
                <i>[CONSTRUIR PAINEL DE NAVEGAÇÃO DESSA ABA - ABA RETRÁTIL]</i>
            </div>
        """, unsafe_allow_html=True)


# --- ABA 2: CERRADO (ECC) ---
with aba_cerrado:
    st.write("### Conteúdo Específico: Cerrado (ECC)")
    st.info("Aqui entrarão os dados filtrados apenas para a concessão Cerrado da planilha BI - AMPLIAÇÃO.")

# --- ABA 3: MINAS GOIÁS (EMG) ---
with aba_minas:
    st.write("### Conteúdo Específico: Minas Goiás (EMG)")
    st.info("Aqui entrarão os dados filtrados apenas para a concessão Minas Goiás da planilha BI - AMPLIAÇÃO.")
