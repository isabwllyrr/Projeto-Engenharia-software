"""FinTrack Insights — dashboard de inteligência de campanhas bancárias."""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from app_core import load_data, segment_summary, summarize


st.set_page_config(
    page_title="FinTrack Insights",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#1F5C4F"
SECONDARY = "#2E7D6B"
ACCENT = "#F2A65A"
BLUE = "#4C6EF5"
TEXT = "#17211E"
MUTED = "#66736F"
GRID = "#E8ECEA"
PALETTE = [PRIMARY, ACCENT, BLUE, "#E4572E", "#8E5572", "#3AAFA9"]
px.defaults.color_discrete_sequence = PALETTE

st.markdown(
    f"""
    <style>
      .stApp {{ background: #F5F7F6; }}
      .block-container {{ max-width: 1260px; padding-top: 1.4rem; padding-bottom: 3rem; }}
      #MainMenu, footer {{ visibility: hidden; }}
      .hero {{
        padding: 28px 32px; border-radius: 20px; color: white;
        background: linear-gradient(120deg, {PRIMARY}, #143E35);
        box-shadow: 0 12px 30px rgba(31,92,79,.20); margin-bottom: 20px;
      }}
      .hero h1 {{ margin: 0; font-size: 2rem; }}
      .hero p {{ margin: 7px 0 0; opacity: .9; }}
      .definition {{ color: {MUTED}; font-size: .82rem; line-height: 1.45; }}
      section[data-testid="stSidebar"] {{ background: white; }}
      div[data-testid="stMetric"] {{
        background: white; border: 1px solid #E5EAE8; border-radius: 15px;
        padding: 16px 18px; box-shadow: 0 4px 14px rgba(20,62,53,.05);
      }}
    </style>
    """,
    unsafe_allow_html=True,
)


def style_figure(fig: go.Figure, height: int = 360) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=34, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color=TEXT, size=13),
        xaxis=dict(gridcolor=GRID, zeroline=False),
        yaxis=dict(gridcolor=GRID, zeroline=False),
        legend=dict(orientation="h", y=1.12, x=0),
        hoverlabel=dict(bgcolor="white"),
    )
    return fig


@st.cache_data
def get_data():
    return load_data()


df = get_data()

st.markdown(
    """
    <div class="hero">
      <h1>FinTrack Insights</h1>
      <p>Inteligência de dados para segmentar clientes e apoiar campanhas de depósito a prazo.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("Filtros globais")
st.sidebar.caption("Todos os indicadores e gráficos respondem a estes filtros.")

jobs = st.sidebar.multiselect("Profissão", sorted(df["profissao"].astype(str).unique()))
education = st.sidebar.multiselect("Escolaridade", sorted(df["escolaridade"].astype(str).unique()))
contact_types = st.sidebar.multiselect("Tipo de contato", sorted(df["tipo_contato"].astype(str).unique()))
age = st.sidebar.slider(
    "Faixa etária",
    int(df["idade"].min()),
    int(df["idade"].max()),
    (int(df["idade"].min()), int(df["idade"].max())),
)

filtered = df[df["idade"].between(*age)].copy()
if jobs:
    filtered = filtered[filtered["profissao"].isin(jobs)]
if education:
    filtered = filtered[filtered["escolaridade"].isin(education)]
if contact_types:
    filtered = filtered[filtered["tipo_contato"].isin(contact_types)]

st.sidebar.metric("Clientes no recorte", f"{len(filtered):,.0f}".replace(",", "."))
if st.sidebar.button("Limpar filtros", width="stretch"):
    st.rerun()

if filtered.empty:
    st.warning("Nenhum cliente corresponde aos filtros escolhidos. Ajuste o recorte na barra lateral.")
    st.stop()

metrics = summarize(filtered)
overall = summarize(df)
delta_conversion = metrics["taxa_adesao"] - overall["taxa_adesao"]

st.subheader("Visão executiva")
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Clientes", f"{metrics['clientes']:,.0f}".replace(",", "."))
k2.metric("Adesões", f"{metrics['adesoes']:,.0f}".replace(",", "."))
k3.metric("Taxa de adesão", f"{metrics['taxa_adesao']:.1f}%", f"{delta_conversion:+.1f} p.p. vs. base")
k4.metric("Saldo médio anual", f"€ {metrics['saldo_medio']:,.0f}".replace(",", "."))
k5.metric("Com empréstimo", f"{metrics['taxa_emprestimo']:.1f}%")
st.markdown(
    '<p class="definition">Taxa de adesão = clientes que contrataram o depósito a prazo ÷ clientes contatados. '
    'Os valores descrevem a amostra histórica e não constituem previsão individual.</p>',
    unsafe_allow_html=True,
)

st.subheader("Onde a adesão é maior?")
left, right = st.columns(2)

job = segment_summary(filtered, "profissao").sort_values("taxa_adesao")
fig = px.bar(
    job,
    x="taxa_adesao",
    y="profissao",
    orientation="h",
    text=job["taxa_adesao"].map(lambda x: f"{x:.1f}%"),
    hover_data={"clientes": ":,", "adesoes": ":,", "saldo_medio": ":.0f"},
    labels={"taxa_adesao": "Taxa de adesão (%)", "profissao": "Profissão"},
    title="Taxa de adesão por profissão",
)
fig.update_traces(marker_color=SECONDARY, textposition="outside")
left.plotly_chart(style_figure(fig, 420), width="stretch", config={"displayModeBar": False})

education_chart = segment_summary(filtered, "escolaridade").sort_values("taxa_adesao")
fig = px.bar(
    education_chart,
    x="taxa_adesao",
    y="escolaridade",
    orientation="h",
    text=education_chart["taxa_adesao"].map(lambda x: f"{x:.1f}%"),
    hover_data={"clientes": ":,", "adesoes": ":,"},
    labels={"taxa_adesao": "Taxa de adesão (%)", "escolaridade": "Escolaridade"},
    title="Taxa de adesão por escolaridade",
)
fig.update_traces(marker_color=ACCENT, textposition="outside")
right.plotly_chart(style_figure(fig, 420), width="stretch", config={"displayModeBar": False})

st.subheader("Contexto da campanha")
c1, c2 = st.columns(2)

monthly = segment_summary(filtered, "mes_contato").sort_values("mes_contato")
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=monthly["mes_contato"].astype(str),
        y=monthly["taxa_adesao"],
        mode="lines+markers+text",
        text=monthly["clientes"].map(lambda n: f"n={n}"),
        textposition="top center",
        line=dict(color=PRIMARY, width=3),
        marker=dict(size=8),
        name="Adesão",
    )
)
fig.update_layout(title="Taxa mensal e tamanho da amostra")
fig.update_yaxes(title="Taxa de adesão (%)")
c1.plotly_chart(style_figure(fig, 380), width="stretch", config={"displayModeBar": False})

previous = segment_summary(filtered, "resultado_campanha_anterior").sort_values("taxa_adesao")
fig = px.bar(
    previous,
    x="taxa_adesao",
    y="resultado_campanha_anterior",
    orientation="h",
    text=previous["taxa_adesao"].map(lambda x: f"{x:.1f}%"),
    hover_data={"clientes": ":,", "adesoes": ":,"},
    labels={"taxa_adesao": "Taxa de adesão (%)", "resultado_campanha_anterior": "Resultado anterior"},
    title="Resultado da campanha anterior",
)
fig.update_traces(marker_color=BLUE, textposition="outside")
c2.plotly_chart(style_figure(fig, 380), width="stretch", config={"displayModeBar": False})

st.info(
    "Leitura recomendada: compare taxa e volume antes de priorizar um segmento. "
    "Meses ou grupos pequenos podem apresentar taxas altas com maior incerteza."
)

st.subheader("Tabela operacional de segmentos")
dimension = st.selectbox(
    "Agrupar clientes por",
    options=["profissao", "escolaridade", "tipo_contato", "mes_contato", "resultado_campanha_anterior"],
    format_func=lambda x: {
        "profissao": "Profissão",
        "escolaridade": "Escolaridade",
        "tipo_contato": "Tipo de contato",
        "mes_contato": "Mês de contato",
        "resultado_campanha_anterior": "Resultado anterior",
    }[x],
)
table = segment_summary(filtered, dimension).sort_values(["taxa_adesao", "clientes"], ascending=False)
table = table.rename(
    columns={
        dimension: "Segmento",
        "clientes": "Clientes",
        "adesoes": "Adesões",
        "taxa_adesao": "Taxa de adesão (%)",
        "saldo_medio": "Saldo médio anual (€)",
    }
)
st.dataframe(
    table.style.format({"Taxa de adesão (%)": "{:.1f}", "Saldo médio anual (€)": "{:,.0f}"}),
    width="stretch",
    hide_index=True,
)

with st.expander("Metodologia, fonte e limitações"):
    st.markdown(
        """
        - **Fonte:** Bank Marketing, UCI Machine Learning Repository, amostra `bank.csv` com 4.521 registros.
        - **Unidade de análise:** um cliente contatado em uma campanha de marketing direto.
        - **Desfecho:** adesão ou não a um depósito a prazo.
        - **Limitação:** a base é histórica, amostral e não contém custos de campanha nem datas completas.
        - **Cuidado analítico:** duração da ligação só é conhecida após o contato; por isso não deve ser usada para selecionar previamente clientes.
        - **Uso responsável:** o painel apoia análise agregada. Não recomenda decisões individuais automatizadas.
        """
    )

st.caption(
    "Fonte: Moro, Rita & Cortez (2014), UCI Bank Marketing, DOI 10.24432/C5K306 · "
    "Snapshot acadêmico tratado para a AV2."
)
