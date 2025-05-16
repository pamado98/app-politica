# Bússola Política – Legislativas 2025

Esta aplicação interativa foi criada com o objetivo de ajudar os cidadãos a refletirem sobre as suas posições políticas antes das eleições legislativas de 2025 em Portugal.

## 🧭 Como funciona?

A aplicação apresenta 30 perguntas (3 por tema), com 4 opções de resposta: Sim, Não, Depende e Não sei.
Cada resposta tem um peso associado que permite calcular a tua orientação política.

No final, em vez de uma bússola política, é apresentada uma linha ideológica horizontal, onde:

Os principais partidos portugueses estão dispostos de forma equidistante, da Esquerda para a Direita.

A tua posição aparece assinalada com um marcador personalizado “Estás aqui!”.

Esta visualização simples permite perceber rapidamente com que espectro político te identificas mais, com base nas tuas respostas.

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
