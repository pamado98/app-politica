# Bússola Política – Legislativas 2025

Esta aplicação interativa foi criada com o objetivo de ajudar os cidadãos a refletirem sobre as suas posições políticas antes das eleições legislativas de 2025 em Portugal.

## 🧭 Como funciona?

Através de 30 perguntas simples, organizadas por tema (como Educação, Habitação, Justiça, etc.), a aplicação calcula a tua posição numa bússola política com dois eixos:

- **Económico**: Esquerda ↔ Direita
- **Liberdades Individuais**: Autoritário ↕ Libertário

No final, é gerado um gráfico com a tua posição e a dos principais partidos portugueses. Também é possível consultar os programas eleitorais dos partidos diretamente a partir da aplicação.

## 📌 Importante

Este projeto **não pretende indicar o “voto certo”** nem substituir a análise crítica. Os resultados são meramente indicativos e baseiam-se nas posições expressas nos programas eleitorais dos partidos.

Recomenda-se a leitura direta dos programas e o acompanhamento do debate político.

## 📂 Estrutura dos ficheiros

- `app.py` – Aplicação principal Streamlit
- `partidos.csv` – Coordenadas ideológicas e links para os programas
- `perguntas.csv` – Perguntas por tema e respetiva orientação política
- `.streamlit/config.toml` – Personalização de cores da interface

## 💡 Tecnologias utilizadas

- [Streamlit](https://streamlit.io/)
- Python 3.12
- Pandas, Matplotlib, Numpy

## 🗳️ Dados utilizados

Todos os programas eleitorais de 2025 dos seguintes partidos foram lidos para construir a lógica desta aplicação:

- PS – Partido Socialista  
- AD (PSD+CDS) – Aliança Democrática  
- IL – Iniciativa Liberal  
- Chega  
- BE – Bloco de Esquerda  
- CDU (PCP-PEV) – Coligação Democrática Unitária  
- Livre  
- PAN – Pessoas-Animais-Natureza  

---

Criado por [Pedro](https://github.com/pamado98)  
Projeto independente, sem afiliação a qualquer força política.
