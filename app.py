
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
    .stButton > button {
        background-color: #007a33 !important;
        color: white !important;
        border: none;
        padding: 0.5em 1.2em;
        font-size: 16px;
        border-radius: 6px;
    }
    .stButton > button:hover {
        background-color: #005924 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Mensagem inicial
if 'started' not in st.session_state:
    st.title("Bússola Política")
    st.write("""
    Esta aplicação é uma ferramenta representativa. Serve como ponto de partida para refletires sobre as tuas posições políticas antes das eleições legislativas de 18 de março. 
    Com base nas tuas respostas, será apresentada uma aproximação à ideologia dos partidos.
    """)
    if st.button("Vamos a isso!"):
        st.session_state.started = True
    st.stop()

# Mapeamento de respostas
MAPA_RESPOSTA = {"Sim": 1, "Não": -1, "Depende": 0.5, "Não sei": 0}

# Perguntas organizadas por tema
PERGUNTAS = {
    "Economia e Estado Social": [
        ("O Estado deve ser o principal responsável pelos serviços essenciais como saúde e educação?", "econ", -1),
        ("O salário mínimo deve continuar a subir por decisão política?", "econ", -1),
        ("Deve haver impostos mais altos para quem ganha mais?", "econ", -1),
        ("O setor privado deve ter mais liberdade para negociar contratos de trabalho?", "econ", 1),
        ("Devem existir benefícios fiscais para empresas que criem emprego em Portugal?", "econ", 1)
    ],
    "Habitação": [
        ("O Estado deve construir mais habitação pública para arrendamento acessível?", "econ", -1),
        ("Devem existir limites máximos às rendas em zonas de pressão?", "econ", -1),
        ("O alojamento local deve ser restringido em zonas residenciais?", "soc", 1),
        ("Devem ser atribuídos apoios diretos aos jovens para compra de casa?", "econ", -1)
    ],
    "Educação e Saúde": [
        ("O ensino superior público deve ser gratuito para todos?", "econ", -1),
        ("O SNS deve colaborar com privados para reduzir listas de espera?", "econ", 1),
        ("A disciplina de cidadania deve ser obrigatória nas escolas públicas?", "soc", -1),
        ("Os médicos estrangeiros devem poder exercer mais facilmente em Portugal?", "soc", 1)
    ],
    "Sociedade e Justiça": [
        ("A canábis deve ser legalizada para uso recreativo?", "soc", 1),
        ("A eutanásia deve ser legalizada?", "soc", 1),
        ("Devem existir penas mais duras para crimes de corrupção?", "soc", -1),
        ("A polícia deve ter mais meios para atuar em zonas problemáticas?", "soc", -1)
    ],
    "Ambiente e Transportes": [
        ("Devem ser implementadas medidas ambientais mesmo que aumentem os custos para os cidadãos?", "econ", -1),
        ("O investimento em transportes públicos deve ser prioritário?", "econ", -1),
        ("As empresas poluentes devem pagar impostos mais altos?", "econ", -1)
    ],
    "Imigração e Europa": [
        ("Portugal deve aceitar mais imigrantes para combater a escassez de mão de obra?", "soc", 1),
        ("A União Europeia deve ter mais influência nas decisões políticas nacionais?", "econ", 1)
    ],
    "Sistema Político": [
        ("Deve haver menos deputados na Assembleia da República?", "soc", 1),
        ("O voto obrigatório deve ser implementado?", "soc", -1)
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

    # Carregar logótipos
    logo_cache = {}
    for partido in df['partido']:
        partido_id = partido.lower().replace(" ", "_").replace("(", "").replace(")", "").replace("+", "").replace("!", "").replace(".", "").replace("-", "").replace("/", "")
        logo_path = os.path.join("logos", f"{partido_id}.png")
        if os.path.exists(logo_path):
            logo_cache[partido] = plt.imread(logo_path)

    # Gráfico
    fig, ax = plt.subplots(figsize=(6,6))
    ax.scatter(eixo_econ, eixo_soc, color="black", s=120)
    ax.text(eixo_econ + 0.2, eixo_soc, "Estás aqui!", fontsize=9)

    for _, row in df.iterrows():
        if row['partido'] in logo_cache:
            img = logo_cache[row['partido']]
            imagebox = OffsetImage(img, zoom=0.12)
            ab = AnnotationBbox(imagebox, (row['econ'], row['soc']), frameon=False)
            ax.add_artist(ab)
        else:
            ax.scatter(row['econ'], row['soc'], s=80)
            ax.text(row['econ'] + 0.2, row['soc'], row['partido'], fontsize=8)

    ax.axhline(0, color='gray', linestyle='--')
    ax.axvline(0, color='gray', linestyle='--')
    ax.set_xlabel("Economia (↔)")
    ax.set_ylabel("Liberdades Individuais (↕)")
    ax.set_title("Bússola Política")
    st.pyplot(fig)

    st.write(f"Posição política: {pos}")
    st.write(f"Partido mais próximo: {partido_mais_proximo}")

    st.subheader("Consulta os programas dos partidos")
    for _, row in df.iterrows():
        st.markdown(f"[{row['partido']}]({row['link']})")
