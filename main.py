import base64
import requests
import streamlit as st
import streamlit.components.v1 as st_components
from utils.jwt_utils import *
from utils.user import *
from utils.components import component_hide_sidebar

def initialize_session_state():
    if 'jwt_token' not in st.session_state:
        st.session_state['jwt_token'] = None
        st.session_state['loggedIn'] = False
        st.session_state['user_data'] = None
        st.session_state['page'] = 'login'

def authenticate(userName: str, userPassword: str):
    login_data = {
        "username": userName,
        "password": userPassword,
        "loginSource": 1,
    }
    
    try :
        response = requests.post('https://api.eshows.com.br/v1/Security/Login', json=login_data).json()
        if "error" in response:
            return None
        elif response["data"]["success"]:
            return response
        else:
            return None
    except Exception as e:
            st.error("Não foi possível acessar seu login")
            
def add_bg(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/png;base64,{encoded});
            background-repeat: no-repeat;
            background-position-x: 90%;
            background-position-y: 30%;
            background-size: 800px auto;  
            background-color: #0e1117; /* cor de fundo visível pelas partes transparentes */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    initialize_session_state()
    if st.session_state['jwt_token']:
        user_data = decode_jwt(st.session_state['jwt_token'])
        if user_data:
            st.session_state['user_data'] = user_data
            st.session_state['loggedIn'] = True
        else:
            st.session_state['jwt_token'] = None
            st.session_state['loggedIn'] = False

    if not st.session_state['loggedIn']:
        show_login_page()
        st.stop()
    else:
        st.switch_page("pages/home.py")


def show_login_page():
    add_bg("./assets/imgs/background.png")
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        image_center = st.columns([1.1, 1, 1])
        with image_center[1]:
            st.image("./assets/imgs/eshows-logo.png", width=100)

        st.markdown("""<div style='width: fit-content; margin-left: 85px'><h3>Oportunidades</h3></div>""", unsafe_allow_html=True)
        
        input_col1, input_col2, input_col3 = st.columns([1, 100, 1])
        with input_col2:
            userName = st.text_input(label="-", value="", placeholder="login", label_visibility="hidden", key="userName_input")
            userPassword = st.text_input(label="-", value="", placeholder="Senha", type="password", label_visibility="hidden", key="userPassword_input")

            if st.button("login"):
                user_data = authenticate(userName, userPassword)
                if user_data:
                    st.session_state['jwt_token'] = encode_jwt(user_data)
                    st.session_state['user_data'] = user_data
                    st.session_state['loggedIn'] = True
                    st.switch_page("pages/home.py")
                    st.experimental_rerun()
                else:
                    st.error("Email ou senha inválidos!")

if __name__ == "__main__":
    initialize_session_state()
    st.set_page_config(
    page_title="login | Apresentação Login",
    page_icon="./assets/imgs/eshows-logo100x100.png",
    layout="centered",
    )

    component_hide_sidebar()
    main()