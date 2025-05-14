import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Perguntas + eixo associado + peso
QUESTOES = [
    ("O Estado deve ser o principal responsável pela saúde?", "econ", -1),
    ("O salário mínimo deve continuar a subir por decisão política?", "econ", -1),
    ("O alojamento local deve ser limitado em zonas residenciais?", "soc", 1),
    ("Devem existir limites máximos às rendas em zonas de pressão?", "econ", -1),
    ("O Estado deve construir mais habitação pública?", "econ", -1),
    ("A transição energética deve ser rápida, mesmo que aumente os custos?", "econ", -1),
    ("O SNS deve colaborar com privados para reduzir listas de espera?", "econ", 1),
    ("O ensino superior público deve ser gratuito para todos?", "econ", -1),
    ("Disciplina de cidadania deve ser obrigatória?", "soc", -1),
    ("A canábis deve ser legalizada para uso recreativo?", "soc", 1)
]

MAPA_RESPOSTA = {"Sim": 1, "Não": -1, "Depende": 0.5, "Não sei": 0}

st.set_page_config(page_title="Descobre a tua posição política", layout="wide")
st.title("🧭 Descobre a tua posição política")

respostas = []
for texto, _, _ in QUESTOES:
    r = st.radio(texto, ["Sim", "Não", "Depende", "Não sei"], key=texto)
    respostas.append(r)

if st.button("Ver resultado"):
    eixo_econ = 0
    eixo_soc = 0

    for i, (texto, eixo, peso) in enumerate(QUESTOES):
        val = MAPA_RESPOSTA[respostas[i]] * peso
        if eixo == "econ":
            eixo_econ += val
        elif eixo == "soc":
            eixo_soc += val

    st.subheader("📍 A tua posição")
    st.write(f"Económico: {eixo_econ:.2f} | Social: {eixo_soc:.2f}")

    df = pd.read_csv("partidos.csv")

    fig, ax = plt.subplots()
    ax.scatter(eixo_econ, eixo_soc, color="black", s=120, label="Tu")

    for _, row in df.iterrows():
        ax.scatter(row['econ'], row['soc'], s=80)
        ax.text(row['econ'] + 0.2, row['soc'], row['partido'], fontsize=9)

    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(0, color='gray', linestyle='--')
    ax.set_xlabel("Economia (Esquerda ↔ Direita)")
    ax.set_ylabel("Liberdades Individuais (Autoritário ↔ Libertário)")
    ax.set_title("Bússola Política")
    st.pyplot(fig)

    st.subheader("📊 Comparação por tema")
    st.dataframe(df.drop(columns=["econ", "soc"]).set_index("partido"))
