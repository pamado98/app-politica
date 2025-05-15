import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os

# Estilo personalizado
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    h1, h2, h3 {
        color: #007a33;
    }
    .stButton>button {
        background-color: #007a33 !important;
        color: white !important;
        border: none;
        padding: 0.5em 1.2em;
        font-size: 16px;
        border-radius: 6px;
    }
    .stButton>button:hover {
        background-color: #005924 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'started' not in st.session_state:
    st.title("Bússola Política")
    st.write("""
    Esta aplicação é uma ferramenta representativa. Serve como ponto de partida para refletires sobre as tuas posições políticas antes das eleições legislativas de 18 de março. 
    Com base nas tuas respostas, será apresentada uma aproximação à ideologia dos partidos.
    """)
    if st.button("Vamos a isso!"):
        st.session_state.started = True
    st.stop()

MAPA_RESPOSTA = {"Sim": 1, "Não": -1, "Depende": 0.5, "Não sei": 0}

PERGUNTAS = {
    "Economia e Estado Social": [
        ("O Estado deve ser o principal responsável pelos serviços essenciais como saúde e educação?", "econ", -1),
        ("O salário mínimo deve continuar a subir por decisão política?", "econ", -1),
        ("Deve haver impostos mais altos para quem ganha mais?", "econ", -1),
        ("O setor privado deve ter mais liberdade para negociar contratos de trabalho?", "econ", 1),
        ("Devem existir benefícios fiscais para empresas que criem emprego em Portugal?", "econ", 1)
    ]
}

respostas = []
st.title("Questionário")
for tema, perguntas in PERGUNTAS.items():
    st.subheader(tema)
    for texto, eixo, peso in perguntas:
        r = st.radio(texto, ["Sim", "Não", "Depende", "Não sei"], key=texto)
        respostas.append((r, eixo, peso))

if st.button("Ver resultado"):
    eixo_econ = sum(MAPA_RESPOSTA[r] * peso for r, eixo, peso in respostas if eixo == "econ")
    eixo_soc = sum(MAPA_RESPOSTA[r] * peso for r, eixo, peso in respostas if eixo == "soc")

    df = pd.read_csv("partidos.csv")
    df['dist'] = np.sqrt((df['econ'] - eixo_econ)**2 + (df['soc'] - eixo_soc)**2)
    partido_mais_proximo = df.loc[df['dist'].idxmin(), 'partido_completo']

    st.subheader("Resultado")
    st.write(f"Posição política: {'Esquerda' if eixo_econ < -2 else 'Direita' if eixo_econ > 2 else 'Centro'}")
    st.write(f"Partido mais próximo: {partido_mais_proximo}")

    # Carregar logótipos
    logo_cache = {}
    for _, row in df.iterrows():
        logo_path = os.path.join("logos", row['logo'])
        if os.path.exists(logo_path):
            logo_cache[row['partido']] = plt.imread(logo_path)

    fig, ax = plt.subplots(figsize=(6,6))
    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(0, color='gray', linestyle='--')
    ax.set_xlabel("Economia (Esquerda <-> Direita)")
    ax.set_ylabel("Liberdades Individuais (Autoritário <-> Libertário)")
    ax.set_title("Bússola Política – Legislativas 2025")

    # Utilizador
    ax.scatter(eixo_econ, eixo_soc, color="black", s=120)
    ax.text(eixo_econ + 0.2, eixo_soc, "Estás aqui!", fontsize=9)

    for _, row in df.iterrows():
        econ, soc = row['econ'], row['soc']
        partido = row['partido']
        if partido in logo_cache:
            img = logo_cache[partido]
            imagebox = OffsetImage(img, zoom=0.12)
            ab = AnnotationBbox(imagebox, (econ, soc), frameon=False)
            ax.add_artist(ab)
        else:
            ax.scatter(econ, soc, s=80)
            ax.text(econ + 0.2, soc, partido, fontsize=8)

    st.pyplot(fig)

    st.subheader("Consulta os programas dos partidos")
    for _, row in df.iterrows():
        st.markdown(f"[{row['partido_completo']}]({row['link']})")