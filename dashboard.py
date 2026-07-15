"""
FinTrack — Dashboard de Análise de Dados (AV2)
Rode com: streamlit run dashboard.py
Abre automaticamente em http://localhost:8501
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------
st.set_page_config(
    page_title="FinTrack — Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#2E7D6B"
PRIMARY_DARK = "#1F5C4F"
ACCENT = "#F2A65A"
ACCENT_2 = "#4C6EF5"
MUTED = "#8A9A97"
CARD_BG = "#FFFFFF"
PAGE_BG = "#F4F6F5"
TEXT = "#1F2A28"

PALETTE = ["#2E7D6B", "#F2A65A", "#4C6EF5", "#E4572E", "#8E5572", "#3AAFA9"]
px.defaults.color_discrete_sequence = PALETTE

# ---------------------------------------------------------------
# CSS customizado
# ---------------------------------------------------------------
st.markdown(
    f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background-color: {PAGE_BG};
        }}

        #MainMenu, footer, header {{visibility: hidden;}}

        .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }}

        /* ---- Cabeçalho ---- */
        .fintrack-header {{
            background: linear-gradient(120deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
            padding: 28px 34px;
            border-radius: 18px;
            color: white;
            margin-bottom: 26px;
            box-shadow: 0 10px 30px rgba(46, 125, 107, 0.25);
        }}
        .fintrack-header h1 {{
            margin: 0;
            font-size: 30px;
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        .fintrack-header p {{
            margin: 6px 0 0 0;
            opacity: 0.9;
            font-size: 14.5px;
            font-weight: 400;
        }}

        /* ---- Cards de KPI ---- */
        .kpi-card {{
            background: {CARD_BG};
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: 0 4px 18px rgba(31, 42, 40, 0.06);
            border: 1px solid rgba(31, 42, 40, 0.05);
            height: 100%;
        }}
        .kpi-label {{
            font-size: 13px;
            font-weight: 600;
            color: {MUTED};
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-bottom: 6px;
        }}
        .kpi-value {{
            font-size: 28px;
            font-weight: 800;
            color: {TEXT};
        }}
        .kpi-sub {{
            font-size: 12.5px;
            color: {MUTED};
            margin-top: 4px;
        }}

        /* ---- Cards de gráfico ---- */
        .chart-card {{
            background: {CARD_BG};
            border-radius: 16px;
            padding: 20px 20px 6px 20px;
            box-shadow: 0 4px 18px rgba(31, 42, 40, 0.06);
            border: 1px solid rgba(31, 42, 40, 0.05);
            margin-bottom: 22px;
        }}
        .chart-title {{
            font-size: 15.5px;
            font-weight: 700;
            color: {TEXT};
            margin-bottom: 4px;
        }}
        .chart-subtitle {{
            font-size: 12.5px;
            color: {MUTED};
            margin-bottom: 10px;
        }}

        /* ---- Sidebar ---- */
        section[data-testid="stSidebar"] {{
            background-color: #FFFFFF;
            border-right: 1px solid rgba(31,42,40,0.06);
        }}
        section[data-testid="stSidebar"] .stMultiSelect label,
        section[data-testid="stSidebar"] .stSlider label {{
            font-weight: 600;
            color: {TEXT};
        }}

        div[data-testid="stExpander"] {{
            background: {CARD_BG};
            border-radius: 14px;
            border: 1px solid rgba(31, 42, 40, 0.06);
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


def chart_layout(fig, height=380):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=10, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(family="Inter, sans-serif", color=TEXT, size=13),
        xaxis=dict(showgrid=True, gridcolor="#EEF1F0", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#EEF1F0", zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    return fig


# ---------------------------------------------------------------
# Carregamento dos dados
# ---------------------------------------------------------------
@st.cache_data
def carregar_dados():
    df = pd.read_csv("dados_tratados.csv")
    mapa_meses = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }
    df["mes_num"] = df["mes_contato"].map(mapa_meses)
    df["aderiu_label"] = df["aderiu_produto"].map({1: "Sim", 0: "Não"})
    df["emprestimo_label"] = df["possui_emprestimo_pessoal"].map({1: "Sim", 0: "Não"})
    df["financiamento_label"] = df["possui_financiamento_imovel"].map({1: "Sim", 0: "Não"})
    return df


df = carregar_dados()

# ---------------------------------------------------------------
# Cabeçalho
# ---------------------------------------------------------------
st.markdown(
    """
    <div class="fintrack-header">
        <h1>💰 FinTrack — Painel de Análise de Dados</h1>
        <p>APS · Engenharia de Software para Negócios (DADM00270) · UFPB · Base tratada de clientes</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# Filtros (sidebar)
# ---------------------------------------------------------------
st.sidebar.markdown("### 🔎 Filtros")

profissoes = st.sidebar.multiselect(
    "Profissão", sorted(df["profissao"].unique()), default=[]
)
escolaridades = st.sidebar.multiselect(
    "Escolaridade", sorted(df["escolaridade"].unique()), default=[]
)
faixa_idade = st.sidebar.slider(
    "Faixa etária",
    int(df["idade"].min()), int(df["idade"].max()),
    (int(df["idade"].min()), int(df["idade"].max())),
)

df_f = df.copy()
if profissoes:
    df_f = df_f[df_f["profissao"].isin(profissoes)]
if escolaridades:
    df_f = df_f[df_f["escolaridade"].isin(escolaridades)]
df_f = df_f[(df_f["idade"] >= faixa_idade[0]) & (df_f["idade"] <= faixa_idade[1])]

st.sidebar.markdown(
    f"<div style='margin-top:14px; font-size:13px; color:{MUTED};'>"
    f"<b>{len(df_f)}</b> de {len(df)} clientes selecionados</div>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------
taxa_adesao = 100 * df_f["aderiu_produto"].mean() if len(df_f) else 0
taxa_emprestimo = 100 * df_f["possui_emprestimo_pessoal"].mean() if len(df_f) else 0
saldo_medio = df_f["saldo_conta"].mean() if len(df_f) else 0

kpis = [
    ("Clientes", f"{len(df_f):,}".replace(",", "."), "no filtro atual"),
    ("Saldo médio em conta", f"€ {saldo_medio:,.0f}".replace(",", "."), "média anual"),
    ("Taxa de adesão à campanha", f"{taxa_adesao:.1f}%", "clientes que aderiram"),
    ("Com empréstimo pessoal", f"{taxa_emprestimo:.1f}%", "do total filtrado"),
]

cols = st.columns(4)
for c, (label, value, sub) in zip(cols, kpis):
    c.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")

# ---------------------------------------------------------------
# Linha 1 de gráficos
# ---------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.markdown(
        '<div class="chart-card"><div class="chart-title">Saldo médio por profissão</div>'
        '<div class="chart-subtitle">Saldo médio anual em conta (€)</div>',
        unsafe_allow_html=True,
    )
    saldo_prof = (
        df_f.groupby("profissao", as_index=False)["saldo_conta"]
        .mean()
        .sort_values("saldo_conta", ascending=True)
    )
    fig = px.bar(
        saldo_prof, x="saldo_conta", y="profissao", orientation="h",
        labels={"saldo_conta": "", "profissao": ""},
        color_discrete_sequence=[PRIMARY],
    )
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(chart_layout(fig, 400), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown(
        '<div class="chart-card"><div class="chart-title">Taxa de adesão por escolaridade</div>'
        '<div class="chart-subtitle">% de clientes que aderiram à campanha</div>',
        unsafe_allow_html=True,
    )
    adesao_esc = df_f.groupby("escolaridade", as_index=False)["aderiu_produto"].mean()
    adesao_esc["taxa_pct"] = adesao_esc["aderiu_produto"] * 100
    fig = px.bar(
        adesao_esc.sort_values("taxa_pct"), x="taxa_pct", y="escolaridade",
        orientation="h", labels={"taxa_pct": "", "escolaridade": ""},
        color_discrete_sequence=[ACCENT],
    )
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(chart_layout(fig, 400), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------
# Linha 2 de gráficos
# ---------------------------------------------------------------
c3, c4 = st.columns(2)

with c3:
    st.markdown(
        '<div class="chart-card"><div class="chart-title">Distribuição de saldo em conta</div>'
        '<div class="chart-subtitle">Frequência de clientes por faixa de saldo (€)</div>',
        unsafe_allow_html=True,
    )
    fig = px.histogram(
        df_f, x="saldo_conta", nbins=40,
        labels={"saldo_conta": ""},
        color_discrete_sequence=[ACCENT_2],
    )
    fig.update_traces(marker_line_width=0)
    fig = chart_layout(fig, 340)
    fig.update_layout(bargap=0.08)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown(
        '<div class="chart-card"><div class="chart-title">Empréstimo pessoal ativo</div>'
        '<div class="chart-subtitle">Proporção de clientes no filtro atual</div>',
        unsafe_allow_html=True,
    )
    contagem = df_f["emprestimo_label"].value_counts()
    fig = go.Figure(
        data=[go.Pie(
            labels=contagem.index,
            values=contagem.values,
            hole=0.62,
            marker=dict(colors=[PRIMARY, "#DCE3E1"]),
            textinfo="percent",
            textfont=dict(size=13, color="white"),
        )]
    )
    st.plotly_chart(chart_layout(fig, 340), use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------
# Linha 3 — tendência mensal
# ---------------------------------------------------------------
st.markdown(
    '<div class="chart-card"><div class="chart-title">Adesão à campanha ao longo dos meses de contato</div>'
    '<div class="chart-subtitle">Taxa de adesão (%) por mês em que o contato foi feito</div>',
    unsafe_allow_html=True,
)
ordem_meses = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
adesao_mes = df_f.groupby("mes_contato", as_index=False)["aderiu_produto"].mean()
adesao_mes["mes_contato"] = pd.Categorical(adesao_mes["mes_contato"], categories=ordem_meses, ordered=True)
adesao_mes = adesao_mes.sort_values("mes_contato")
adesao_mes["taxa_pct"] = adesao_mes["aderiu_produto"] * 100

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=adesao_mes["mes_contato"], y=adesao_mes["taxa_pct"],
    mode="lines+markers",
    line=dict(color=PRIMARY, width=3, shape="spline"),
    marker=dict(size=8, color=PRIMARY),
    fill="tozeroy",
    fillcolor="rgba(46, 125, 107, 0.10)",
))
st.plotly_chart(chart_layout(fig, 340), use_container_width=True, config={"displayModeBar": False})
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------
# Tabela de dados filtrados
# ---------------------------------------------------------------
with st.expander("🔍 Ver dados filtrados (tabela)"):
    st.dataframe(df_f, use_container_width=True)

st.markdown(
    f"<p style='color:{MUTED}; font-size:12.5px; margin-top:10px;'>"
    "Fonte dos dados: Bank Marketing Dataset (tratado) — dados_tratados.csv</p>",
    unsafe_allow_html=True,
)
