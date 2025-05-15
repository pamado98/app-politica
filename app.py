
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

if 'started' not in st.session_state:
    st.title("Bússola Política")
    st.write("""
    Esta aplicação é uma ferramenta representativa. Serve como ponto de partida para refletires sobre as tuas posições políticas antes das eleições legislativas de 18 de março. 
    Com base nas tuas respostas, será apresentada uma aproximação à ideologia dos partidos.
    """)
    if st.button("Começar"):
        st.session_state.started = True
    st.stop()

MAPA_RESPOSTA = {"Sim": 1, "Não": -1, "Depende": 0.5, "Não sei": 0}

PERGUNTAS = {
    "Economia e Estado Social": [
        ("O Estado deve ser o principal responsável pelos serviços essenciais como saúde e educação?", "econ", -1),
        ("O salário mínimo deve continuar a subir por decisão política?", "econ", -1),
        ("Deve haver impostos mais altos para quem ganha mais?", "econ", -1)
    ],
    "Habitação": [
        ("O Estado deve construir mais habitação pública para arrendamento acessível?", "econ", -1),
        ("Devem existir limites máximos às rendas em zonas de pressão?", "econ", -1),
        ("O alojamento local deve ser restringido em zonas residenciais?", "soc", 1)
    ],
    "Educação e Saúde": [
        ("O ensino superior público deve ser gratuito para todos?", "econ", -1),
        ("O SNS deve colaborar com privados para reduzir listas de espera?", "econ", 1),
        ("A disciplina de cidadania deve ser obrigatória nas escolas públicas?", "soc", -1)
    ],
    "Sociedade e Justiça": [
        ("A canábis deve ser legalizada para uso recreativo?", "soc", 1),
        ("A eutanásia deve ser legalizada?", "soc", 1),
        ("Devem existir penas mais duras para crimes de corrupção?", "soc", -1)
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

    st.subheader("Resultado")
    pos = "Centro"
    if eixo_econ < -4: pos = "Esquerda"
    elif eixo_econ > 4: pos = "Direita"
    elif eixo_econ <= -2: pos = "Centro-Esquerda"
    elif eixo_econ >= 2: pos = "Centro-Direita"

    df = pd.read_csv("partidos.csv")
    df['dist'] = np.sqrt((df['econ'] - eixo_econ)**2 + (df['soc'] - eixo_soc)**2)
    partido_mais_proximo = df.loc[df['dist'].idxmin(), 'partido']

    st.write(f"Posição política: {pos}")
    st.write(f"Partido mais próximo: {partido_mais_proximo}")

    fig, ax = plt.subplots(figsize=(6,6))
    ax.scatter(eixo_econ, eixo_soc, color="black", s=120)
    ax.text(eixo_econ + 0.2, eixo_soc, "Estás aqui!", fontsize=9)
    for _, row in df.iterrows():
        ax.scatter(row['econ'], row['soc'], s=80)
        ax.text(row['econ'] + 0.2, row['soc'], row['partido'], fontsize=8)
    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(0, color='gray', linestyle='--')
    ax.set_xlabel("Economia (↔)")
    ax.set_ylabel("Liberdades Individuais (↕)")
    ax.set_title("Bússola Política")
    st.pyplot(fig)

    st.subheader("Consulta os programas dos partidos")
    for _, row in df.iterrows():
        st.markdown(f"[{row['partido']}]({row['link']})")
