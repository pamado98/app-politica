import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bússola Política – Legislativas 2025", layout="centered")

# Estilo visual
st.markdown("""
<style>
.stApp {
    background-color: #ffffff;
}
.stButton>button {
    background-color: #007a33;
    color: white;
    padding: 0.5em 1em;
    border: none;
    border-radius: 6px;
    font-size: 16px;
}
.stButton>button:hover {
    background-color: #005924;
}
</style>
""", unsafe_allow_html=True)

# Carregar perguntas e partidos
perguntas_df = pd.read_csv("perguntas.csv")
temas = perguntas_df["tema"].unique().tolist()
partidos_df = pd.read_csv("partidos.csv")

# Inicializar estados
if "tema_index" not in st.session_state:
    st.session_state.tema_index = 0
if "respostas" not in st.session_state:
    st.session_state.respostas = []

MAPA_RESPOSTA = {"Sim": 1, "Não": -1, "Depende": 0.5, "Não sei": 0}

# Página inicial
if st.session_state.tema_index == 0 and not st.session_state.respostas:
    st.title("Bússola Política – Legislativas 2025")
    st.markdown("""
Esta aplicação foi desenvolvida com base nos programas eleitorais das principais forças políticas candidatas às Legislativas de 2025.  
Através de um conjunto de perguntas divididas por temas, poderás avaliar a tua tendência política de forma simples e visual.

No final, um gráfico do tipo *bússola política* vai mostrar-te a tua posição ideológica, com base nas tuas respostas.
""")
    if st.button("Vamos começar!"):
        st.experimental_rerun()
    st.stop()

# Mostrar perguntas do tema atual
tema_atual = temas[st.session_state.tema_index]
st.title(f"Tema: {tema_atual}")

perguntas_tema = perguntas_df[perguntas_df["tema"] == tema_atual]
for _, row in perguntas_tema.iterrows():
    resposta = st.radio(row["pergunta"], ["Sim", "Não", "Depende", "Não sei"], key=row["pergunta"])
    st.session_state.respostas.append((resposta, row["eixo"], row["peso"]))

# Botão para avançar
if st.session_state.tema_index < len(temas) - 1:
    if st.button(f"Avançar para {temas[st.session_state.tema_index + 1]}"):
        st.session_state.tema_index += 1
        st.experimental_rerun()
else:
    if st.button("Ver Resultados"):
        st.session_state.tema_index += 1
        st.experimental_rerun()

# Página final com gráfico
if st.session_state.tema_index >= len(temas):
    eixo_econ = sum(MAPA_RESPOSTA[r] * float(peso) for r, eixo, peso in st.session_state.respostas if eixo == "econ")
    eixo_soc = sum(MAPA_RESPOSTA[r] * float(peso) for r, eixo, peso in st.session_state.respostas if eixo == "soc")

    st.title("O teu resultado")
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(0, color='gray', linestyle='--')
    ax.set_xlabel("Economia (Esquerda <-> Direita)")
    ax.set_ylabel("Liberdades Individuais (Autoritário <-> Libertário)")
    ax.set_title("Bússola Política – Legislativas 2025")

    # Adicionar partidos
    for _, row in partidos_df.iterrows():
        ax.scatter(row["econ"], row["soc"], label=row["sigla"])
        ax.text(row["econ"] + 0.2, row["soc"], row["sigla"], fontsize=8)

    # Adicionar utilizador
    ax.scatter(eixo_econ, eixo_soc, color="black", s=120)
    ax.text(eixo_econ + 0.2, eixo_soc, "Estás aqui!", fontsize=9, color="black")

    st.pyplot(fig)

    st.markdown("### Mantém-te a par! Vê os Programas Eleitorais de cada partido abaixo.")
    for _, row in partidos_df.iterrows():
        st.markdown(f"[{row['sigla']} - {row['partido_completo']}]({row['link']})")

    if st.button("Vê aqui a tua tendência política em cada um dos temas!"):
        st.info("Funcionalidade em desenvolvimento: comparação por tema.")