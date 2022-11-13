import streamlit as st

st.set_page_config(
    page_title="Calçados Semelhantes",
    page_icon="👞"
)

with open('files/css/styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("""<h1 style="text-align:center">IA para Obtenção de Calçados Semelhantes</h1>""", unsafe_allow_html=True)
st.markdown("***")

def check_password():

    def password_entered():
        if (st.session_state["db_username"] in st.secrets["db_username"] and st.session_state["db_password"] == st.secrets["db_password"][st.session_state["db_username"]]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["db_username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Usuário", key="db_username")
        st.text_input("Senha", type="password", key="password")
        if st.button("Entrar"):
            password_entered()
            return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Usuário", key="db_username")
        st.text_input("Senha", type="password", key="password")
        if st.button("Entrar"):
            password_entered()
            st.error("😕 Usuário ou senha incorreta")
            return False
    else:
        # Password correct.
        st.markdown("""<p style="text-align:center">Você entrou!</p>""", unsafe_allow_html=True)
        return True

check_password()