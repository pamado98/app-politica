
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

st.set_page_config(page_title="Bússola Política – Legislativas 2025", layout="wide")

st.title("Bússola Política – Legislativas 2025")
st.markdown("Esta é a tua posição ideológica com base nas tuas respostas.")

# Limites e posição do utilizador (exemplo entre PAN e PS)
pos_utilizador = 3.4  # Pode ser qualquer valor entre 0 e 7

# Limitar a posição aos extremos
pos_utilizador = max(0, min(7, pos_utilizador))

# Lista dos partidos na ordem ideológica
partidos = ["cdu", "be", "livre", "pan", "ps", "ad", "il", "chega"]
nomes = ["CDU", "BE", "LIVRE", "PAN", "PS", "AD", "IL", "CHEGA"]
caminho_logos = "logos"

# Gráfico
fig, ax = plt.subplots(figsize=(10, 2))
ax.set_xlim(-0.5, 7.5)
ax.set_ylim(-1, 1)
ax.axis("off")

# Plotar os logótipos
for i, partido in enumerate(partidos):
    logo_path = os.path.join(caminho_logos, f"{partido}.png")
    if os.path.exists(logo_path):
        img = mpimg.imread(logo_path)
        ax.imshow(img, extent=(i-0.4, i+0.4, -0.4, 0.4), aspect="auto", zorder=2)
    ax.text(i, -0.8, nomes[i], ha="center", fontsize=10)

# Adicionar posição do utilizador
ax.plot(pos_utilizador, 0.6, "o", color="black", markersize=12, zorder=3)
ax.text(pos_utilizador, 0.85, "Estás aqui!", ha="center", fontsize=10)

st.pyplot(fig)
