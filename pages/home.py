import streamlit as st
from menu.net_costs import NetCost
from menu.opportunity_audience import OpportunityAudience
from menu.opportunity_creation import OpportunityCreation
from utils.components import *
from utils.user import logout
from streamlit_theme import st_theme

def render():
    # pegando dados da sessão como ID e NOME
    user_id = st.session_state['user_data']["data"]["user_id"]
    user_name = st.session_state['user_data']["data"]['full_name']
    theme = st_theme(key=f"theme_")
    base_theme = theme.get("base") if theme else "default"
    st.session_state["base_theme"] = base_theme
    
    col1, col2, col3 = st.columns([3.5,0.4,0.3])
    
    col1.write(f"## Olá, "+user_name)
    col2.image("./assets/imgs/eshows100x100.png")
    col3.markdown("<p style='padding-top:0.0em'></p>", unsafe_allow_html=True)
    col3.button(label="Logout", on_click=logout)
    
    component_effect_underline()
    st.write('## Assinatura de Artistas')
    st.markdown('<div class="full-width-line-white"></div>', unsafe_allow_html=True)
    st.markdown('<div class="full-width-line-black"></div>', unsafe_allow_html=True)

    col6, col7, col8, = st.columns([3.4,0.2,0.4])
    col8.button(label="Atualizar", on_click = st.cache_data.clear)
    
    tbs = st.tabs(["Publico de Oportunidades", "Criação de Oportunidades", "Valores Liquidos"])
    
    with tbs[0]:
        page = OpportunityAudience()

    with tbs[1]:
        page = OpportunityCreation()
    
    with tbs[2]:
        page = NetCost()

if __name__ == "__main__":
    if 'jwt_token' not in st.session_state:
        st.switch_page("main.py")
    
    st.set_page_config(page_title="Home | Assinatura de Artistas",page_icon="./assets/imgs/eshows-logo100x100.png", layout="wide")

    component_hide_sidebar()
    component_fix_tab_echarts()

    if 'user_data' in st.session_state:
        render()
    else:
        st.switch_page("main.py")