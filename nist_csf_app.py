import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Calculadora de Maturidade NIST CSF 2.0", layout="wide")

st.title("🛡️ Calculadora de Maturidade em Segurança Cibernética - NIST CSF 2.0")
st.markdown("Avalie o nível de maturidade da sua organização com base nas funções do NIST.")

# --------- EXPLICAÇÃO DOS NÍVEIS ---------
st.sidebar.header("📘 Níveis de Maturidade")

st.sidebar.markdown("""
**0 — Inexistente**  
Não há processo ou controle implementado.

**1 — Inicial / Ad hoc**  
Existe alguma prática, mas não é padronizada.

**2 — Gerenciado**  
Processo documentado, aplicado e monitorado.

**3 — Otimizado**  
Processo medido, melhorado continuamente e estratégico.
""")

# --------- PERGUNTAS ---------
questions = {
    "GOVERN": [
        "A organização possui uma estratégia formal de gestão de risco cibernético?",
        "Papéis e responsabilidades de segurança estão definidos?",
        "A liderança acompanha indicadores de segurança?",
        "Existem políticas de segurança aprovadas e revisadas?"
    ],
    "IDENTIFY": [
        "Os ativos de TI são inventariados?",
        "Os riscos de segurança são avaliados periodicamente?",
        "Existem classificações de dados?"
    ],
    "PROTECT": [
        "Controles de acesso são aplicados aos sistemas?",
        "Há uso de antivírus e firewall?",
        "Funcionários recebem treinamentos de segurança?"
    ],
    "DETECT": [
        "Eventos de segurança são monitorados?",
        "Existe detecção de intrusão ou SIEM?"
    ],
    "RESPOND": [
        "Existe plano de resposta a incidentes?",
        "A equipe sabe como agir em caso de ataque?"
    ],
    "RECOVER": [
        "Há backups regulares e testados?",
        "Existe plano de continuidade de negócios?"
    ]
}

scores = {}

st.header("📋 Questionário de Avaliação")

options = {
    "Inexistente": 0,
    "Inicial / Ad hoc": 1,
    "Gerenciado": 2,
    "Otimizado": 3
}

for function, qs in questions.items():
    st.subheader(f"Função: {function}")
    total = 0

    for q in qs:
        resposta = st.radio(q, options.keys(), key=q, horizontal=True)
        total += options[resposta]

    scores[function] = total / len(qs)

# --------- RESULTADO ---------

if st.button("📊 Gerar Relatório de Maturidade"):

    st.header("📈 Resultado da Avaliação")

    labels = list(scores.keys())
    values = list(scores.values())

    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])
    ax.set_title("Maturidade por Função NIST CSF 2.0", size=12)

    st.pyplot(fig)

    media_geral = sum(scores.values()) / len(scores)

    st.subheader("📝 Nível Geral de Maturidade")

    if media_geral < 1:
        nivel = "🔴 Baixo"
        desc = "A segurança é reativa e pouco estruturada."
    elif media_geral < 2:
        nivel = "🟠 Intermediário"
        desc = "Existem controles, mas ainda não padronizados."
    else:
        nivel = "🟢 Avançado"
        desc = "A segurança é gerenciada e integrada ao negócio."

    st.markdown(f"### **Nível Geral:** {nivel}")
    st.write(desc)

    st.subheader("📌 Pontos de Atenção")
    for func, val in scores.items():
        if val < 2:
            st.write(f"⚠️ A função **{func}** precisa de melhorias.")
